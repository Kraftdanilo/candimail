# Candimail v7 — automatisation Gmail (desktop pywebview + Flask)

## Arborescence

```text
autogmail/
  app.py                  Entree serveur classique (-> candimail.web.app)
  desktop.py              Entree desktop pywebview (serveur + fenetre)
  candimail/              Package applicatif (v7.1.0)
    core/                 config.py, crypto.py, db.py, noyau.py
    services/             smtp.py (envoi), imap.py (reponses/bounces)
    web/                  app.py (fabrique Flask) + routes/*.py (5 blueprints)
  static/  templates/     Assets Flask (servis via RESS_DIR)
  scripts/                admin_comptes, build_exe, QA, verifs
  tests/                  test_smoke.py (+ QA historiques)
  deploy/                 Caddy / Nginx / systemd (serveur web classique)
  uploads/  app.db        Donnees locales (jamais versionnees)
  .webview/               Logs + profil WebView2
```

> Compat : les anciens `constantes.py`, `db.py`, `noyau.py`,
> `smtp_service.py`, `imap_service.py`, `routes_*.py`, `admin_comptes.py`,
> `build_exe.py` a la racine sont des **calques** qui re-exportent le
> package. Tout l'existant (`import db`, `python app.py`, QA...) continue
> de marcher sans modification.

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

## Build .exe

```powershell
pip install pyinstaller
python scripts/build_exe.py
```
