# Sécurité

> © 2026 Dane hk \Manifest — Tous droits réservés.

---

## 1. Modèle de menace

Candimail est une application **de bureau à usage personnel**, mono-utilisateur.
Elle n'a pas d'authentification et son serveur interne écoute sur
`127.0.0.1` (option `--lan` = ouverture explicite au réseau local).

| Attaquant | Capacité | Impact |
|---|---|---|
| Site web tiers | HTTP vers `127.0.0.1` (CSRF / DNS-rebinding) | ⚠️ **Bloqué** par les protections ci-dessous |
| Autre utilisateur du poste | Accès au système de fichiers | Lecture de `secret.key` + `app.db` |
| Réseau local | Impossible (écoute restreinte à la boucle locale) | Aucun |
| Logs / sauvegardes | Divulgation par l'utilisateur | ⚠️ Responsabilité utilisateur |

> **Usage personnel, jamais sur un réseau.** L'application ne doit jamais être
> exposée sur Internet ou un réseau local : elle stocke des mots de passe
> Gmail chiffrés et ne dispose d'aucune protection d'accès.

---

## 2. Chiffrement des secrets

### Mots de passe Gmail
- Chiffrés en **Fernet (AES-128-CBC + HMAC-SHA256)**
- **Clé hors base** : `secret.key`, jamais dans `app.db`
  → copier `app.db` seul ne permet pas de récupérer les mots de passe
- Marqueur `enc$` : la fonction `chiffrer()` est **idempotente**
- Migration automatique au premier lancement si un secret est en clair

### Mots de passe d'accès (héritage multi-utilisateur)
- Hash **scrypt** : `n=16384, r=8, p=1, dklen=32`, sel de 16 octets
- Stockage : `salt_hex$hash_hex`, jamais réversible
- Comparaison à temps constant (`hmac.compare_digest`)

### Fichiers sensibles

| Fichier | Contenu | Protection |
|---|---|---|
| `secret.key` | Clé Fernet | `.gitignore`, hors base |
| `admin.key` | Hash du mot de passe admin | `.gitignore` |
| `app.db` | Config, journal, entreprises | `.gitignore`, secrets chiffrés |
| `config.json` | **Legacy** — peut contenir des secrets en clair | ⚠️ À supprimer après migration |

---

## 3. Anti-fuite vers le front

**Règle : le front ne reçoit jamais le détail technique d'une erreur.**

Deux helpers dans `core/noyau.py` :

```python
log_erreur(where, exc, contexte)   # journalise le traceback serveur
erreur_publique(type_erreur=…)      # renvoie un message générique
```

### Messages publics par famille

| Type | Message renvoyé |
|---|---|
| `smtp` | Échec de l'envoi — vérifie le compte Gmail et la connexion |
| `imap` | Échec de la connexion à la boîte Gmail |
| `fichier` | Erreur lors de l'accès au fichier |
| `db` | Erreur interne de base de données |
| `crypto` | Erreur interne de chiffrement |
| `generique` | Erreur interne — consulte le journal |

### Ce qui a été neutralisé

| Avant (fuite) | Après |
|---|---|
| `{"trace": "Traceback…", "error": "InvalidToken: …"}` | `{"error": "Erreur interne — consulte le journal"}` |
| `{"error": "AuthSMTPServer: 535 (Bad credentials)"}` | `{"error": "Échec de l'envoi — vérifie le compte Gmail…"}` |
| `{"error": "WinError 5: C:\\…\\secret.key"}` | `{"error": "Erreur lors de l'accès au fichier"}` |
| `{"erreur": "IMAP4.error: NO … [UID 1234]"}` | `{"erreur": "Échec de la connexion à la boîte Gmail"}` |
| `{"error": "JSON invalide : Expecting value: line 1"}` | `{"error": "Fichier JSON invalide ou illisible"}` |

> **`CANDIMAIL_DEBUG=1` ne change rien à la réponse HTTP.** Le debug ne
> contrôle que le niveau de détail du journal fichier.

### Surface d'information fermée

| Endpoint | État |
|---|---|
| `/api/debug/info` | **404** sauf si `CANDIMAIL_DEBUG=1` (var d'env serveur, pas activable depuis le front) |
| `/api/config` | Mot de passe toujours remplacé par `••••••••` |
| `/api/comptes` | Ne renvoie **jamais** de `password` — seulement `has_password` et `devoiler` |

---

## 4. Révélation des mots de passe — double contrôle

`POST /api/comptes/<idx>/reveal` est la seule route qui retourne un secret en
clair. Elle est protégée par **deux barrières indépendantes** :

### Barrière 1 — Opt-in explicite

Le compte doit porter `"devoiler": true` dans la configuration.
**Par défaut `false`** → le bouton 👁️ est masqué dans l'interface.

```json
{"email": "xxx@gmail.com", "password": "enc$…", "actif": true,
 "devoiler": true}
```

### Barrière 2 — Nonce anti-CSRF

1. Le front appelle `POST /api/comptes/nonce` → reçoit un jeton
2. Le serveur le stocke en mémoire (15 min) **et** sa signature HMAC dans la session
3. `reveal` exige `{nonce}` dans le corps de la requête
4. Vérification : existence + âge + signature HMAC + **usage unique**

```
POST /api/comptes/0/reveal                → 403 Révélation désactivée
POST /api/comptes/0/reveal {nonce:"faux"} → 403 nonce invalide
POST /api/comptes/0/reveal {nonce:valide}  → 200 (puis 403 si réutilisé)
```

Un site tiers ne peut **ni lire** la réponse (cross-origin) **ni construire**
un jeton valide (signature HMAC liée au secret de session).

---

## 5. Robustesse des entrées

| Vecteur | Protection |
|---|---|
| **Path traversal** | `_resoudre_piece()` refuse `..`, `/`, `\`, `\x00`, `:` et vérifie que le chemin résolu est un enfant direct de `uploads/` |
| **Upload** | PDF uniquement, nom assaini, 20 Mo max (`MAX_CONTENT_LENGTH`) |
| **XSS stored** | `escapeHtml()` sur toutes les interpolations `innerHTML` du front |
| **Email** | `_email_valide()` : longueur ≤ 254, pas d'espace, domaine avec point, pas de `..` |
| **Filtres Gmail** | `_normaliser_regle()` : champs et actions strictement allowlistés |
| **Import JSON** | Structure validée, clés filtrées, secrets exclus de l'export |

---

## 6. En-têtes HTTP

Tous appliqués via `after_request` :

| En-tête | Effet |
|---|---|
| `X-Content-Type-Options: nosniff` | Empêche l'interprétation MIME abusive |
| `X-Frame-Options: SAMEORIGIN` | Anti-clickjacking |
| `Referrer-Policy: strict-origin-when-cross-origin` | Réduit les fuites d'URL |
| `Strict-Transport-Security` | **Uniquement si HTTPS** (`request.is_secure`) |
| `Content-Type: …; charset=utf-8` | Anti-mojibake sur toutes les réponses texte |

**Cookies de session** : `HttpOnly` + `SameSite=Lax`. Application de bureau
servie en HTTP local : le cookie `Secure` n'est jamais positionné (il serait
rejeté par WebView2 sur `http://127.0.0.1`).

---

## 7. Quotas et anti-spam

| Protection | Valeur par défaut |
|---|---|
| Délai minimum entre envois | 40 s (aléatoire 35-55 s) |
| Plafond horaire | 100 envois |
| Retries SMTP | 3 avec backoff exponentiel |
| Fenêtre glissante | 1 heure |
| Limite d'envoi | 20 Mo, 1 envoi à la fois (`_send_lock`) |

Ces mécanismes protègent **la réputation de la boîte Gmail** autant que
l'utilisateur : un envoi massif non maîtrisé serait un signal de spam.

---

## 8. Recommandations

1. **Ne jamais exposer le port** sur Internet ou le réseau local
2. **Supprimer `config.json`** une fois la migration vérifiée (il peut contenir
   un mot de passe en clair)
3. **Sauvegarder `secret.key` séparément** (sans lui, les mots de passe sont
   irrécupérables)
4. **Utiliser un mot de passe d'application Gmail** dédié, jamais le mot de
   passe du compte
5. **Laisser `devoiler` à `false`** sauf besoin ponctuel
6. **Protéger l'accès au poste** : les données sont en clair côté fichiers
   (mots de passe chiffrés, mais CV et journal lisibles)

---

**© 2026 Dane hk \Manifest — Tous droits réservés.**