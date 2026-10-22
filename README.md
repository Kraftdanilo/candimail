# Candimail r0.0.1 — automatisation Gmail libre (serveur web local + FastAPI)

> **Copyright © 2026 — Dane hk \Manifest. Tous droits réservés.**
> Créateur de l'application. Logiciel propriétaire, usage personnel :
> exécution libre sur tes propres postes (Windows/Linux/mac), modification
> privée autorisée (projet d'entraînement), mais pas de revente, d'usage
> commercial, ni de redistribution publique sous un autre nom.
> Voir [`LICENSE`](LICENSE).

**Candimail** est un projet de compétences et d'entraînement : il facilite
l'automatisation de sa messagerie Gmail **librement et sans abonnement coûteux** —
envois personnalisés à grande échelle, suivi des réponses, filtres, agent IA,
sur son propre compte, sans plateforme tierce ni quota payant.
Il n'est **pas limité aux candidatures** : messages, groupes, parents d'élèves,
collègues, notifications… tout ce qui s'envoie par e-mail peut être automatisé.

## Portabilité (autre PC, autre utilisateur, autre OS)

L'application fonctionne sur **Windows, Linux et macOS** (Python 3.11+) :

```bash
# Sur la nouvelle machine (Win/Linux/mac — mêmes commandes)
git clone https://github.com/Kraftdanilo/candimail.git
cd candimail
python -m venv .venv
# Windows : .\.venv\Scripts\pip install -r requirements.txt
# Linux/mac : .venv/bin/pip install -r requirements.txt
.venv/Scripts/pip install -r requirements.txt   # (Windows) ; .venv/bin/… sinon
.venv/Scripts/python candimail.py               # (Windows) ; .venv/bin/… sinon
```

- **Port** : jamais un problème — `9999` par défaut, sinon le 1er port libre,
sinon un port éphémère garanti par l'OS.
- **Données** : tout est dans `data/`, `uploads/`, `.webview/` (créés au
premier démarrage, jamais versionnés). Copier ces dossiers d'un PC à un
autre transfère la configuration complète.
- **Réseau** : `127.0.0.1` par défaut ; `--lan` pour y accéder depuis un
téléphone ou un autre appareil du même réseau.
- **Routeur / changement d'IP** : aucun impact. Le serveur écoute en local,
l'IP réseau affichée au démarrage (`ip_locale()`) se recalcule à chaque
lancement. IP dynamique (DHCP) = relancer l'app, ou réserver une IP fixe
dans le routeur pour une adresse stable.

## Documentation

Documentation complète dans [`docs/`](docs/) :

| Document | Contenu |
|---|---|
| [docs/README.md](docs/README.md) | Vue d'ensemble et architecture |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Prérequis, installation |
| [docs/GUIDE-UTILISATEUR.md](docs/GUIDE-UTILISATEUR.md) | Guide fonctionnel complet |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture technique, flux, données |
| [docs/API.md](docs/API.md) | Référence des endpoints |
| [docs/SECURITE.md](docs/SECURITE.md) | Chiffrement, anti-fuite, mesures |
| [docs/DEVELOPPEMENT.md](docs/DEVELOPPEMENT.md) | Conventions, build, dépannage |

## Arborescence

```text
autogmail/
  candimail.py            Point d'entrée UNIQUE (uvicorn + FastAPI en thread, --lan pour le réseau local)
  LICENSE                 Licence propriétaire — usage personnel (14 articles)
  candimail/              Package applicatif (r0.0.1)
    core/                 config.py, crypto.py, db.py, noyau.py, purge.py, regles.py
    services/             smtp.py (envoi), imap.py (reponses/bounces), ia_agent.py (agent IA)
    web/                  api.py (app FastAPI, 79 routes)
  docs/                   Documentation complete (7 documents)
  static/  templates/     Assets statiques + templates Jinja2 (servis via RESS_DIR)
  scripts/                admin_comptes
  uploads/  app.db        Donnees locales (jamais versionnees)
  .serveur web local/               Logs + profil navigateur
```

> **Application de bureau** : Candimail n'est **pas** un site web. Il n'y a
> ni déploiement, ni reverse proxy, ni vitrine publique, ni SEO. Le serveur
> FastAPI/uvicorn est un support **interne** (`127.0.0.1` par défaut ;
> option `--lan` pour l'ouvrir au réseau local).

Routes définies dans `candimail/web/api.py` (app FastAPI unique, 79 routes) :

| Fichier | Responsabilite |
| --- | --- |
| `pages.py` | Pages HTML (racine, app, suivi, CV, CGU, RGPD, 404) |
| `donnees.py` | CV, entreprises, config, comptes, pieces jointes |
| `envoi.py` | Envoi unitaire, envoi de masse, groupes |
| `divers.py` | Templates, IMAP/filtres, exports/imports |

> **Données non versionnées** : `app.db`, `config.json`, `envois.json`,
> `uploads/`, `secret.key`, `admin.key`, `.serveur web local/` et les logs sont
> exclus via `.gitignore` (ils contiennent des données personnelles
> et/ou des secrets). Ne jamais les commiter.

> **⚠️ `config.json` et `envois.json` sont des RELIQUES** : migrés une
> seule fois vers `app.db`, puis automatiquement archivés (`.legacy-save`)
> et supprimés au démarrage. Ne les recréez pas — la base `app.db` est
> désormais la **source de vérité unique**.

> **Compat** : historiquement, la racine contenait des calques
> (`constantes.py`, `db.py`, `routes_*.py`…) qui ré-exportaient le package.
> Ils ont été **supprimés** : plus aucun module ne les importe.
> Importez toujours directement `candimail.*`.

## Pages (locales, dans la fenêtre)

| URL | Rôle |
| --- | --- |
| `/` | Redirige vers `/app` |
| `/app` | Application principale (footer : CV, suivi, CGU, RGPD) |
| `/cv` `/suivi` `/cgu` `/rgpd` | Pages secondaires |

> **Usage personnel, mono-utilisateur, sans authentification.** L'utilisateur
> est considéré comme connecté sur chaque requête. Le serveur reste sur
> `127.0.0.1` par défaut (option `--lan` = ouverture explicite au réseau local).

## Lancement

```powershell
pip install -r requirements.txt
python candimail.py              # serveur local, port 9999 (ou 1er libre)
python candimail.py --port 9000  # port imposé
python candimail.py --lan        # accessible depuis le réseau local (0.0.0.0)
python candimail.py --debug      # + logs détaillés
```

Env : `CANDIMAIL_PORT=9999`, `CANDIMAIL_DEBUG=1`.

## Debug

- `GET /api/health` : sonde (port, version, taille DB)
- `GET /api/debug/info` : état interne — **fermé par défaut**,
  disponible uniquement si `CANDIMAIL_DEBUG=1`.
- Logs : `.serveur web local/candimail.log`, `.serveur web local/desktop.log`

## Sécurité — aucune fuite vers le front

Règle appliquée : **le front ne reçoit jamais le détail technique d'une
erreur ni un secret en clair.** Le détail part uniquement dans
`.serveur web local/candimail.log`.

| Protection | Où |
| --- | --- |
| `erreur_publique()` / `log_erreur()` — messages génériques par famille (smtp, imap, fichier, db, crypto) | `core/noyau.py` |
| Plus aucun `traceback` ni `type(e).__name__` renvoyé, **même avec `CANDIMAIL_DEBUG=1`** | `web/app.py` |
| Erreurs SMTP/IMAP brutes (hôte, port, code d'auth) → journal serveur uniquement | `services/smtp.py`, `services/imap.py` |
| Révélation des mots de passe : **double contrôle** — opt-in `devoiler` par compte + nonce anti-CSRF lié à la session (15 min, usage unique) | `web/routes/donnees.py`, route `POST /api/comptes/nonce` |
| Chemins de fichiers absolus jamais renvoyés | `web/routes/donnees.py` |
| Traversée de répertoire refusée (`..`, séparateurs, absolu) | `_resoudre_piece()` |

### Activer la révélation d'un mot de passe

Désactivée par défaut (le bouton 👁️ est masqué). Pour un compte donné,
dans la config du compte (clé `comptes`) :

```json
{ "email": "xxx@gmail.com", "password": "enc$...", "actif": true,
  "devoiler": true }
```

