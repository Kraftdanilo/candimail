# Candimail v7 — automatisation Gmail (desktop pywebview + Flask)

> **Copyright © 2026 — Dane hk \Manifest. Tous droits réservés.**
> Créateur de l'application. Logiciel propriétaire : redistribution,
> modification et usage commercial interdits sans autorisation écrite.
> Voir [`LICENSE`](LICENSE).

## Documentation

Documentation complète dans [`docs/`](docs/) :

| Document | Contenu |
|---|---|
| [docs/README.md](docs/README.md) | Vue d'ensemble et architecture |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Prérequis, installation |
| [docs/GUIDE-UTILISATEUR.md](docs/GUIDE-UTILISATEUR.md) | Guide fonctionnel complet |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture technique, flux, données |
| [docs/API.md](docs/API.md) | Référence des 68 endpoints |
| [docs/SECURITE.md](docs/SECURITE.md) | Chiffrement, anti-fuite, mesures |
| [docs/DEVELOPPEMENT.md](docs/DEVELOPPEMENT.md) | Conventions, build, dépannage |

## Arborescence

```text
autogmail/
  candimail.py            Point d'entrée UNIQUE (fenêtre pywebview + Flask en thread)
  LICENSE                 Licence propriétaire — usage personnel (14 articles)
  candimail/              Package applicatif (v7.1.0)
    core/                 config.py, crypto.py, db.py, noyau.py
    services/             smtp.py (envoi), imap.py (reponses/bounces)
    web/                  app.py (fabrique Flask) + routes/*.py (4 blueprints)
  docs/                   Documentation complete (7 documents)
  static/  templates/     Assets Flask (servis via RESS_DIR)
  scripts/                admin_comptes
  uploads/  app.db        Donnees locales (jamais versionnees)
  .webview/               Logs + profil WebView2
```

> **Application de bureau** : Candimail n'est **pas** un site web. Il n'y a
> ni déploiement, ni reverse proxy, ni vitrine publique, ni SEO. Le serveur
> Flask est un support **interne** à la fenêtre pywebview, sur `127.0.0.1`.

Blueprints de `candimail/web/routes/` :

| Fichier | Responsabilite |
| --- | --- |
| `pages.py` | Pages HTML (racine, app, suivi, CV, CGU, RGPD, 404) |
| `donnees.py` | CV, entreprises, config, comptes, pieces jointes |
| `envoi.py` | Envoi unitaire, envoi de masse, groupes |
| `divers.py` | Templates, IMAP/filtres, exports/imports |

> **Données non versionnées** : `app.db`, `config.json`, `envois.json`,
> `uploads/`, `secret.key`, `admin.key`, `.webview/` et les logs sont
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
> est considéré comme connecté sur chaque requête. L'application n'est jamais
> exposée sur un réseau : son serveur Flask reste sur `127.0.0.1`, au sein de
> la fenêtre de bureau.

## Lancement

```powershell
pip install -r requirements.txt
python candimail.py              # fenêtre desktop, port 9999
python candimail.py --debug      # + badge debug + console WebView2
python candimail.py --port 9000  # port imposé
python candimail.py --plein-ecran
```

Env : `CANDIMAIL_PORT=9999`, `CANDIMAIL_DEBUG=1`.

## Debug

- `GET /api/health` : sonde (port, version, taille DB)
- `GET /api/debug/info` : état interne — **fermé par défaut**,
  disponible uniquement si `CANDIMAIL_DEBUG=1`.
- Logs : `.webview/candimail.log`, `.webview/desktop.log`

## Sécurité — aucune fuite vers le front

Règle appliquée : **le front ne reçoit jamais le détail technique d'une
erreur ni un secret en clair.** Le détail part uniquement dans
`.webview/candimail.log`.

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

