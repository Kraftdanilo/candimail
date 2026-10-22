# Architecture technique

> © 2026 Dane hk \Manifest — Licence MIT

---

## 1. Vue d'ensemble

Architecture en couches, du business vers le rendu :

```
┌─────────────────────────────────────────────────────────┐
│  PRÉSENTATION                                           │
│  templates/*.html  +  static/brutalist.css               │
├─────────────────────────────────────────────────────────┤
│  WEB ( FastAPI + uvicorn )           web/api.py          │
│  app FastAPI unique : 79 routes (~68 endpoints API)      │
│  Auth : vide (mono-utilisateur local)                    │
├─────────────────────────────────────────────────────────┤
│  SERVICES                                  services/      │
│  smtp.py  — envoi, retries, rotation, pièces jointes     │
│  imap.py  — réponses, bounces, filtres Gmail             │
│  ia_agent.py — agent IA (Groq/Google/Mistral)            │
├─────────────────────────────────────────────────────────┤
│  BUSINESS ( STATE )                        core/noyau.py │
│  verrous · config · quotas · validation · anti-fuite     │
├─────────────────────────────────────────────────────────┤
│  DONNÉES                       core/db.py · core/crypto.py│
│  SQLite (WAL)  ·  Fernet  ·  scrypt                      │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Modules

### `core/config.py` (273 l.)
Constantes : chemins, configuration par défaut, CV par défaut, 3 modèles
prédéfinis.

| Symbole | Rôle |
|---|---|
| `BASE_DIR` | Données modifiables (racine projet) |
| `RESS_DIR` | Ressources en lecture seule (templates, static) |
| `DEFAULT_CONFIG` | Structure de config de base + modèle « Candidature stage » |
| `DEFAULT_CV` | CV de démonstration |
| `TEMPLATES` | 3 modèles prédéfinis : standard, direct, formel |

### `core/crypto.py` (95 l.)
- `chiffrer()` / `dechiffrer()` — Fernet, marqueur `enc$`, idempotent
- `hash_mdp()` / `verifier_mdp()` — scrypt (n=16384, r=8, p=1)
- Clé dans `secret.key` (**hors base** : copier `app.db` seul est inutile)

> Repli gracieux si `cryptography` est absent : les secrets restent en clair
> et l'application affiche un avertissement au démarrage.

### `core/db.py` (414 l.)
SQLite en mode WAL, un `RLock` global, **une nouvelle connexion par opération**
(évite les problèmes de partage entre threads).

| Table | Clé | Contenu |
|---|---|---|
| `config` | `main` ou `u<uid>` | blob JSON |
| `log` | (entreprise, uid) | journal d'envois |
| `companies` | (name, uid) | entreprises |
| `cv` | `main` ou `u<uid>` | blob JSON |
| `meta` | cle | flags de migration |
| `users` | id | legacy multi-utilisateur |

Migrations automatiques : lecture de `config.json` et `envois.json` au premier
lancement (versionnés une fois via la table `meta`).

### `core/noyau.py` (369 l.)
Le cœur applicatif — état partagé en mémoire + logique métier.

**Verrous**

| Verrou | Protège |
|---|---|
| `_config_lock` (RLock) | cache de configuration globale |
| `_log_lock` | lecture/écriture du journal |
| `_send_lock` (RLock) | quotas, délais, rotation de comptes |
| `_log_send_lock` | `_send_timestamps` (anti-quota) |
| `_bulk_lock` | état du worker d'envoi de masse |
| `_NONCE` (dict) | nonces anti-CSRF |

**Fonctions clés**

| Fonction | Rôle |
|---|---|
| `charger_config()` / `sauver_config()` | config par utilisateur |
| `check_rate_limit()` | quota horaire glissant |
| `get_delai()` | délai fixe ou aléatoire |
| `compte_suivant()` | rotation round-robin des comptes |
| `_email_valide()` | validation stricte d'adresse |
| `erreur_publique()` / `log_erreur()` | **anti-fuite** : message générique + log serveur |
| `creer_nonce()` / `_nonce_valide()` | nonce anti-CSRF (HMAC + session) |
| `recharger_pieces()` | isolation des pièces jointes par utilisateur |

### `services/smtp.py` (136 l.)
`_envoyer_un_email()` construit un `MIMEMultipart`, attache les PDF, se
connecte en `SMTP_SSL(465)`. Retries avec backoff exponentiel (`2^n`) sur
erreur réseau uniquement. Modes : individuel (1 email par destinataire) ou
groupe (tous en Cci, `To` = expéditeur).

### `services/imap.py` (375 l.)
- `check_imap_compte()` — recherche `SINCE`, corrélation avec le journal,
  détection bounces via en-tête `X-Failed-Recipients`
- `verifier_toutes_boites()` — agrège et met à jour le journal
- `appliquer_filtres_compte()` — règles par **priorité**, un mail = une règle
- `_utf7()` — encodage IMAP UTF-7 modifié pour les libellés accentués

### `web/api.py` (~1 640 l.)
App FastAPI unique : templates Jinja2, fichiers statiques, en-têtes de
sécurité, boucle IMAP automatique (daemon, boucle 60 s), endpoints API
(companies, config, comptes, pièces, templates, filtres, IA, historique…).
Aucun serveur autonome : le lancement est assuré par `candimail.py`
(racine), seul point d'entrée — uvicorn sur `127.0.0.1` (ou `0.0.0.0` avec `--lan`).

**Total : 79 routes FastAPI** (application de bureau, aucune route web publique).

---

## 3. Flux — envoi d'un e-mail

```
POST /api/send
  │
  ├─ 1. Validation : champs, compte actif, destinataires (_email_valide)
  ├─ 2. Quota : check_rate_limit() + délai depuis _last_send_time
  ├─ 3. compte_suivant()          → rotation round-robin
  ├─ 4. Template du compte ?      → construit sujet + corps
  ├─ 5. envoyer_email()
  │      ├─ parse_emails(dest)
  │      ├─ get_pieces_actives()
  │      ├─ mode groupe ? 1 email Cci : N emails individuels
  │      └─ _envoyer_un_email() × N
  │            ├─ MIMEMultipart + PDF
  │            ├─ SMTP_SSL(465) + login
  │            ├─ send_message()
  │            └─ retry backoff si réseau
  │      └─ (erreur → log_erreur() + message public)
  ├─ 6. _send_timestamps.append()  → quota
  ├─ 7. Journal : log[company] = {envoye, date, compte…}
  └─ 8. JSON {ok, message, sans_pj, nb_destinataires}
```

---

## 4. Modèle de données

```
config (cle, valeur)              log (entreprise, uid, data)
  cle = "main" | "u<uid>"           │
                                    └── {email, emails[], envoyé, date,
  companies (name, uid, cat,        repondu, bounce, sans_pj, compte,
  email, context, custom)           sujet_reponse, erreur, groupe}
  cv (cle, valeur)                meta (cle, valeur)
  users (id, email, pass_hash)     ← legacy multi-utilisateur
```

Le journal est **écrit en entier** à chaque sauvegarde
(`DELETE` + `INSERT`) : simple et sûr pour le volume visé.

---

## 5. Concurrence

| Mécanisme | Détail |
|---|---|
| uvicorn (ASGI) | event-loop async + threads pour les blocants |
| SQLite WAL | lectures concurrentes, 1 écrivain |
| Verrous Python | sérialisent envois, config, journal |
| Thread daemon | boucle IMAP auto + serveur desktop |
| Thread d'envoi | `_bulk_worker` avec arrêt coopératif |

L'envoi de masse est **mono-thread** : un seul envoi à la fois, respect du
délai, ce qui garantit la conformité des quotas Gmail.

---

## 6. Performance

- **Cache de config** en mémoire (`_config_cache`) — invalidé par
  `invalider_cache_config()`
- **Index SQLite** sur les clés primaires
- **Rate limit** en liste Python, purgée à chaque appel
- **uvicorn** en serveur ASGI (FastAPI)
- **Statique** : un seul CSS partagé, aucune dépendance CDN

Limite : le rendu de l'interface est dominé par la taille de
`templates/index.html` (~3 000 lignes, HTML/CSS/JS inline).

---

## 7. Dépendances

| Bibliothèque | Version | Rôle |
|---|---|---|
| fastapi | 0.115.0 | Framework web (ASGI) |
| uvicorn | 0.30.6 | Serveur ASGI |
| cryptography | 46.0.7 | Fernet |
| openpyxl | 3.1.2 | Export Excel |
| httpx | 0.27.0 | Agent IA (appels Groq/Google/Mistral) |
| python-multipart | 0.0.9 | Uploads (pièces jointes) |

Python **3.11+** testé. SQLite inclus dans la bibliothèque standard.

---

**© 2026 Dane hk \Manifest — Licence MIT**