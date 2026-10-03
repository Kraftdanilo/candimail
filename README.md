# Candimail v7 — automatisation Gmail (desktop pywebview + Flask)

## Arborescence

```text
autogmail/
  app.py                  Entree serveur classique (-> candimail.web.app)
  desktop.py              Entree desktop pywebview (serveur + fenetre)
  candimail/              Package applicatif (v7.1.0)
    core/                 config.py, crypto.py, db.py, noyau.py
    services/             smtp.py (envoi), imap.py (reponses/bounces)
    web/                  app.py (fabrique Flask) + routes/*.py (4 blueprints)
  static/  templates/     Assets Flask (servis via RESS_DIR)
  scripts/                admin_comptes, build_exe
  tests/                  test_smoke.py
  deploy/                 Caddy / Nginx / systemd (serveur web classique)
  uploads/  app.db        Donnees locales (jamais versionnees)
  .webview/               Logs + profil WebView2
```

Blueprints de `candimail/web/routes/` :

| Fichier | Responsabilite |
| --- | --- |
| `pages.py` | Pages HTML (racine, vitrine, app, suivi, CV, SEO, 404) |
| `donnees.py` | CV, entreprises, config, comptes, pieces jointes |
| `envoi.py` | Envoi unitaire, envoi de masse, groupes |
| `divers.py` | Templates, IMAP/filtres, exports/imports |

> **Donnees non versionnees** : `app.db`, `config.json`, `envois.json`,
> `uploads/`, `secret.key`, `admin.key`, `.webview/` et les logs sont
> exclus via `.gitignore` (ils contiennent des donnees personnelles
> et/ou des secrets). Ne jamais les commiter.

> **Compat** : historiquement, la racine contenait des calques
> (`constantes.py`, `db.py`, `routes_*.py`…) qui ré-exportaient le package.
> Ils ont été **supprimés** : plus aucun module ne les importe.
> Importez toujours directement `candimail.*`.

## Pages

| URL | Rôle |
| --- | --- |
| `/` | Redirige vers `/app` |
| `/app` | Application principale (footer : vitrine, CV, suivi, CGU, RGPD) |
| `/vitrine` | Vitrine publique (déplacée depuis `/`) |
| `/cv` `/suivi` `/cgu` `/rgpd` | Pages secondaire |

> **Pas d'authentification** : usage local mono-utilisateur. L'utilisateur 1
> est considéré comme connecté sur chaque requête. Les routes `/login` et
> `/api/auth/*` ont été supprimées. **Ne pas exposer cette app sur Internet**
> (elle stocke des mots de passe Gmail) sans rétablir une protection d'accès.

## Lancement

```powershell
pip install -r requirements.txt
python desktop.py            # fenetre desktop, port 8765
python desktop.py --debug    # + badge debug + console WebView2
python desktop.py --port 9000 --browser
python app.py                # serveur seul (navigateur manuel)
```

Env : `CANDIMAIL_PORT=9000`, `CANDIMAIL_DEBUG=1`.

## Debug

- `GET /api/health` : sonde (port, version, taille DB)
- `GET /api/debug/info` : etat interne SANS secrets + queue des logs
- Logs : `.webview/candimail.log`, `.webview/desktop.log`

## Tests

```powershell
python -m pytest tests -q
```

## Build .exe

```powershell
pip install pyinstaller
python scripts/build_exe.py
```
