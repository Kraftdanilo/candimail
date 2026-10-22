# Documentation complète — Candimail r0.0.1

> **Copyright © 2026 — Dane hk \Manifest. Tous droits réservés.**
> Créateur de l'application. Voir [`LICENSE`](../LICENSE) (licence propriétaire)
> et les [CGU](http://127.0.0.1:9999/cgu).

---

## Sommaire

| Document | Contenu |
|---|---|
| **README.md** (ce fichier) | Vue d'ensemble, architecture, guide de démarrage |
| [INSTALLATION.md](INSTALLATION.md) | Prérequis, installation pas à pas, build `.exe` |
| [GUIDE-UTILISATEUR.md](GUIDE-UTILISATEUR.md) | Guide fonctionnel complet, pas à pas |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique, modules, flux de données |
| [API.md](API.md) | Référence des 68 endpoints HTTP |
| [SECURITE.md](SECURITE.md) | Modèle de sécurité, chiffrement, mesures anti-fuite |
| [DEVELOPPEMENT.md](DEVELOPPEMENT.md) | Conventions, build, dépannage, contribution |

---

## 1. Présentation

**Candimail** est une application web locale qui automatise l'usage de sa
messagerie Gmail, **librement et sans abonnement coûteux**. Elle gère des
cibles (entreprises, groupes, contacts), génère des messages personnalisés
à partir de modèles, envoie en séquence avec respect des quotas, et suit
les réponses reçues par IMAP. Un agent IA (Groq/Google/Mistral) peut
rédiger, classer ou résumer les messages.

C'est aussi un **projet de compétences et d'entraînement** : il n'est
**pas limité aux candidatures** — messages, groupes, notifications, tout
ce qui s'envoie par e-mail peut être automatisé.

- **Version** : r0.0.1
- **Auteur** : Dane hk \Manifest
- **Stack** : Python 3.11 · FastAPI + uvicorn · SQLite · serveur web local · navigateur
- **Plateforme** : Windows 10/11 (le code est portable macOS/Linux)
- **Usage** : **personnel, privé, mono-utilisateur**

---

## 2. Fonctionnalités

| Domaine | Fonctionnalités |
|---|---|
| **Comptes Gmail** | Multi-comptes, rotation automatique, test de connexion, mot de passe d'application (chiffré) |
| **Entreprises** | CRUD, catégories (grands groupes / PME / porte-à-porte), import en masse, contexte par entreprise |
| **Modèles de lettres** | 3 modèles prédéfinis + modèles personnalisés, variables (`{entreprise}`, `{contexte}`, `{nom}`, `{ville}`…) |
| **Envois** | Envoi unitaire, envoi de masse, groupes, mode Cci, pièces jointes PDF |
| **Quotas** | Délai entre envois (fixe ou aléatoire), plafond horaire, protection anti-spam |
| **Suivi** | Journal des envois, détection de réponses et bounces (IMAP), statistiques, export |
| **Filtres Gmail** | Règles automatiques de classement (libellés, archivage, suppression), apprentissage |
| **CV** | Éditeur CV complet, export et impression |
| **Données** | Sauvegarde/restauration JSON, exports CSV et Excel |

---

## 3. Architecture

```
autogmail/
├── candimail.py              Point d'entrée UNIQUE (uvicorn + FastAPI en thread)
├── LICENSE                   Licence propriétaire — usage personnel
│
├── candimail/                Package applicatif
│   ├── core/
│   │   ├── config.py         Chemins, config par défaut, CV, modèles
│   │   ├── crypto.py         Chiffrement Fernet, hash scrypt
│   │   ├── db.py             Persistance SQLite (schéma, migrations)
│   │   └── noyau.py          État partagé, verrous, anti-fuite, nonces
│   ├── services/
│   │   ├── smtp.py           Envoi d'e-mails, retries, pièces jointes
│   │   └── imap.py           Réponses, bounces, filtres Gmail
│   └── web/
│       └── api.py            App FastAPI unique (79 routes)
│
├── templates/                5 pages HTML + 404
├── static/                   CSS partagé, favicon
├── scripts/                  admin_comptes.py
├── docs/                     Documentation (7 documents)
├── uploads/                  Pièces jointes PDF (non versionné)
└── app.db                    Base SQLite (non versionnée)
```

**Candimail est une application de bureau, pas un site web.** Aucun
déploiement, aucun reverse proxy, aucune vitrine publique, aucun SEO. Le
serveur FastAPI/uvicorn est un support **interne** (`127.0.0.1` par défaut ;
option `--lan` pour l'ouvrir au réseau local).

**Principes de conception**
- **Mono-utilisateur personnel** : aucune authentification, aucune gestion de comptes
- **Usage strictement local** : écoute sur `127.0.0.1` uniquement
- **Données locales** : SQLite en fichier, aucun serveur externe
- **Secrets chiffrés** : Fernet avec clé hors base (`secret.key`)
- **Anti-fuite** : le front ne reçoit jamais de traceback ni de message technique

---

## 4. Démarrage rapide

```powershell
# 1. Dépendances
pip install -r requirements.txt

# 2. Lancement (fenêtre de bureau, port 9999)
python candimail.py

# Variantes
python candimail.py --port 9000     # port imposé
python candimail.py --debug         # logs détaillés + console navigateur
```

**Variables d'environnement**

| Variable | Défaut | Rôle |
|---|---|---|
| `CANDIMAIL_PORT` | `9999` | Port du serveur **local interne** |
| `CANDIMAIL_DEBUG` | — | `1` active les logs détaillés et `/api/debug/info` |


➡️ Voir [INSTALLATION.md](INSTALLATION.md) pour le détail.

---

## 5. Pages (locales)

| URL | Rôle |
|---|---|
| `/` | Redirige vers `/app` |
| `/app` | Application principale |
| `/cv` | Éditeur de CV |
| `/suivi` | Tableau de suivi des envois |
| `/cgu` | Conditions générales d'utilisation |
| `/rgpd` | Politique de confidentialité |

---

## 6. Licence

Candimail est un logiciel **propriétaire** sous licence « Tous droits
réservés ». La redistribution, la modification et l'usage commercial sont
interdits sans autorisation écrite du titulaire.

Voir [`LICENSE`](../LICENSE) pour le texte intégral (13 articles + 2 annexes).

---

**© 2026 Dane hk \Manifest — Tous droits réservés.**