# Référence API

> © 2026 Dane hk \Manifest — Tous droits réservés.
> **68 endpoints** — serveur local `http://127.0.0.1:9999`

## Conventions

| Aspect | Règle |
|---|---|
| Base | `http://127.0.0.1:<port>` (port libre ≥ 9999) |
| Auth | **Aucune** — usage local mono-utilisateur |
| Format | JSON en entrée et sortie (`Content-Type: application/json`) |
| Succès | `{"ok": true, …}` |
| Erreur | `{"ok": false, "error": "message public"}` |
| Erreurs | 400 validation · 403 interdit · 404 absent · 409 conflit · 429 quota · 502 SMTP · 500 interne |

> **Anti-fuite** : aucun traceback, aucun nom d'exception, aucun chemin
> absolu, aucun message SMTP/IMAP brut n'est renvoyé. Le détail technique
> est dans `.webview/candimail.log`.

---

## Pages — blueprint `pages` (7)

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/` | Redirige vers `/app` |
| GET | `/app` | Application principale |
| GET | `/cv` | Éditeur de CV |
| GET | `/suivi` | Tableau de suivi |
| GET | `/cgu` | Conditions générales |
| GET | `/rgpd` | Politique de confidentialité |
| GET | `/favicon.ico` | Redirige vers le SVG |

> Les routes web publiques (`/vitrine`, `/robots.txt`, `/sitemap.xml`) ont
> été **supprimées** : Candimail est une application de bureau, pas un site.

---

## Système (2)

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/health` | Sonde : version, port, taille DB, debug |
| GET | `/api/debug/info` | État interne — **404 sauf si `CANDIMAIL_DEBUG=1`** |

---

## Données — blueprint `donnees` (21)

### CV
| Méthode | Route | Corps / réponse |
|---|---|---|
| GET | `/api/cv` | `{cv: {...}}` |
| POST | `/api/cv` | `{cv: {titre, resume, nom, ville, experiences[], formations[], references[], competences[], langues[]}}` |

### Entreprises
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/companies` | Liste `{companies: [...]}` |
| POST | `/api/companies` | `{name, email, cat, context}` — `cat` ∈ `grands`/`pme`/`port` |
| PUT | `/api/companies/<name>` | Modification (renommage : déplace l'entrée du journal) |
| DELETE | `/api/companies/<name>` | Suppression |
| POST | `/api/companies/seed` | Import en masse `{companies: [...]}` |

### Configuration
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/config` | Config complète **sans secrets** (mots de passe masqués) |
| POST | `/api/config` | Mise à jour `candidat` / `parametres` |

### Comptes Gmail
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/comptes` | Liste `{comptes: [{index, email, actif, has_password, template, devoiler}]}` |
| POST | `/api/comptes` | `{email, password, template}` — chiffré automatiquement |
| DELETE | `/api/comptes/<idx>` | Suppression |
| POST | `/api/comptes/<idx>/toggle` | Activer / mettre en pause |
| POST | `/api/comptes/<idx>/template` | `{template}` — modèle propre au compte |
| POST | `/api/comptes/test` | Test de connexion SMTP `{email}` |
| POST | `/api/comptes/nonce` | Émet un nonce anti-CSRF (15 min, usage unique) |
| POST | `/api/comptes/<idx>/reveal` | **Double contrôle** : `devoiler: true` + `{nonce}` |

> `reveal` renvoie **403** si l'opt-in `devoiler` est absent ou si le nonce
> est invalide/expiré. Voir [SECURITE.md](SECURITE.md).

### Pièces jointes
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/pieces` | Liste avec taille en Ko |
| POST | `/api/pieces` | Upload **PDF uniquement** (20 Mo max) |
| DELETE | `/api/pieces/<id>` | Suppression (traversée de chemin refusée) |
| POST | `/api/pieces/<id>/toggle` | Activer / désactiver |

---

## Envoi — blueprint `envoi` (11)

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/status` | État : log, quotas, comptes actifs, délai |
| POST | `/api/preview` | `{company, context, template}` → `{subject, body}` sans envoi |
| POST | `/api/send` | Envoi unitaire — voir corps ci-dessous |
| POST | `/api/send-bulk` | Lance l'envoi de masse (thread) |
| GET | `/api/send-bulk-status` | Progression `{index, total, envoyes, erreurs, en_cours}` |
| POST | `/api/send-bulk-stop` | Arrêt coopératif |

### `POST /api/send`

```json
{
  "email": "contact@entreprise.com, autre@entreprise.com",
  "company": "Nom Entreprise",
  "subject": "Objet (généré si absent)",
  "body": "Corps (généré si absent)",
  "pieces": ["u0_1700000000_CV.pdf"],
  "mode_groupe": false
}
```

Réponse succès :
```json
{"ok": true, "message": "Envoyé via … (1 PJ)",
 "sans_pj": false, "nb_destinataires": 1}
```

Codes : **400** champs manquants / aucun destinataire valide · **429** quota
horaire atteint ou délai non écoulé (renvoie `attente` en secondes) ·
**502** échec SMTP.

### Groupes
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/groupes` | Liste des groupes |
| POST | `/api/groupes` | `{nom, description, emails[]}` — **emails validés strictement** |
| DELETE | `/api/groupes/<id>` | Suppression |
| POST | `/api/groupes/<id>/send` | `{subject, body, mode, joindre_pieces}` |

`mode` ∈ `individuel` (1 email/contact) ou `groupe` (tous en Cci).

---

## Divers — blueprint `divers` (26)

### Modèles de lettres
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/templates` | Modèles personnalisés |
| POST | `/api/templates` | Création `{nom, objet, corps, categorie}` ou modification `{id, …}` |
| DELETE | `/api/templates/<id>` | Suppression |
| POST | `/api/templates/<id>/duplicate` | Duplication |

**Variables disponibles** : `{entreprise}`, `{contexte}`, `{nom}`, `{tel}`,
`{email}`, `{ville}`, `{diplome}`, `{spec}`

### IMAP
| Méthode | Route | Rôle |
|---|---|---|
| POST | `/api/imap/check` | `{jours}` (1-365) — détecte réponses et bounces |
| GET | `/api/imap/status` | État de la vérification automatique |

### Filtres Gmail
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/filtres` | Liste (6 règles par défaut créées au 1er lancement) |
| POST | `/api/filtres` | Création — `priority` auto-attribuée |
| PUT/PATCH | `/api/filtres/<idx>` | Modification (priorité non modifiable ici) |
| DELETE | `/api/filtres/<idx>` | Suppression + réindexation |
| POST | `/api/filtres/<idx>/toggle` | Activer / mettre en pause |
| POST | `/api/filtres/reorder` | `{ordre: [id1, id2, …]}` — drag & drop |
| POST | `/api/filtres/corriger` | Apprentissage `{email, label, notify}` |
| GET | `/api/filtres/suggestions` | Suggestions d'amélioration |
| POST | `/api/filtres/creer-libelles` | Crée les libellés dans Gmail |
| POST | `/api/filtres/appliquer` | Exécute toutes les règles maintenant |

**Structure d'une règle**
```json
{"id": "rule-001", "priority": 1, "enabled": true,
 "name": "Opportunité", "label": "Opportunite", "icon": "💼",
 "items": [{"champ": "sujet", "valeur": "stage"}],
 "actions": ["label", "notify"]}
```

`champ` ∈ `from` · `sujet` · `motcle` — `actions` ∈ `label` · `archive` ·
`marquer_lu` · `supprimer` · `notify`

> **Priorité** : le tri est croissant (`0` gagne). Chaque mail n'est classé
> que par la **première** règle qui correspond.

### Notifications & suivi
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/notifications` | 20 dernières + compteur non vues |
| POST | `/api/notifications/vue` | Marque comme vues |
| POST | `/api/mark-response` | `{company, repondu}` |

### Exports & sauvegardes
| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/export-csv` | Journal au format CSV |
| GET | `/api/export-json` | Sauvegarde `{config, log}` |
| GET | `/api/export-excel` | Classeur 3 feuilles (openpyxl) |
| POST | `/api/import-json` | Restauration `{log}` |
| POST | `/api/reset-log` | Vide le journal (sauvegarde `.backup.json` préalable) |

---

## Exemples

```powershell
# Sonde de santé
curl http://127.0.0.1:9999/api/health

# Aperçu d'une lettre
curl -X POST http://127.0.0.1:9999/api/preview `
  -H "Content-Type: application/json" `
  -d '{"company":"BTP Express","context":"Votre chantier au Plateau"}'

# Envoi
curl -X POST http://127.0.0.1:9999/api/send `
  -H "Content-Type: application/json" `
  -d '{"email":"rh@btp-express.ci","company":"BTP Express","body":"Bonjour"}'
```

---

**© 2026 Dane hk \Manifest — Tous droits réservés.**