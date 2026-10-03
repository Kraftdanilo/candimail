#!/usr/bin/env python3
"""
Candimail v7 — Fabrique Flask (package candimail.web.app).

Structure (après refactor) :
  - constantes.py     : chemins, config par défaut, CV, templates
  - noyau.py          : état partagé, verrous, gestion config/log/envois
  - smtp_service.py   : envoi SMTP (rotation, retries, pièces jointes)
  - imap_service.py   : réponses/bounces + filtres Gmail
  - routes_pages.py   : pages HTML (vitrine, app, suivi, cv, SEO, 404)
  - routes_auth.py    : inscription / connexion / sécurité
  - routes_donnees.py : CV, entreprises, config, comptes, pièces jointes
  - routes_envoi.py   : envoi unitaire, envoi de masse, groupes
  - routes_divers.py  : templates, IMAP/filtres, exports/imports
  - app.py            : ce fichier — assemble tout et lance le serveur
"""
import os, socket, time, threading, logging, traceback
from datetime import datetime
from pathlib import Path

from flask import Flask, request, jsonify

from candimail.core import crypto, db
from candimail.core.config import RESS_DIR, RACINE
from candimail.core.noyau import (charger_config, sauver_config, _config_globale,
                   get_comptes_actifs, get_pieces_actives, get_delai,
                   recharger_pieces, _auth_attempts)  # (compat. scripts QA)
from candimail.services.imap import verifier_toutes_boites, appliquer_filtres_compte


# ============================================================
# CONFIG GLOBALE (port, debug, chemins logs)
# ============================================================
# Nouveau port par défaut : 8765 (le 5000 est pris par WinNAT / Docker /
# services système sur beaucoup de PC Windows → EACCES / conflits).
PORT_DEFAUT = int(os.environ.get("CANDIMAIL_PORT", "8765"))
DEBUG_ACTIF = os.environ.get("CANDIMAIL_DEBUG") == "1"

LOG_DIR = RACINE / ".webview"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE_APP = LOG_DIR / "candimail.log"

# ---- Logger fichier (debug avancé : .webview/candimail.log) ----
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("CANDIMAIL_DEBUG") == "1" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "candimail.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("candimail")

app = Flask(__name__,
            template_folder=str(RESS_DIR / "templates"),
            static_folder=str(RESS_DIR / "static"))
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
# ------------------------------------------------------------
# REVERSE PROXY / HTTPS
# ------------------------------------------------------------
# Candimail tourne en HTTP en local. Quand il est exposé derrière un reverse
# proxy (Caddy, Nginx, Traefik…) qui termine le TLS, la variable d'environnement
# CANDIMAIL_BEHIND_PROXY=1 active ProxyFix : Flask lit alors correctement
# X-Forwarded-Proto (https), X-Forwarded-For et Host.
if os.environ.get("CANDIMAIL_BEHIND_PROXY") == "1":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Cookie de session : marqué « Secure » uniquement quand on sert en HTTPS,
# sinon le login local en http serait cassé.
_session_secure = (
    os.environ.get("CANDIMAIL_HTTPS") == "1"
    or os.environ.get("CANDIMAIL_BEHIND_PROXY") == "1"
)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=_session_secure,
)

# Secret de session : généré une fois, persisté en base
_sec0 = _config_globale().setdefault("securite", {})
if not _sec0.get("secret_key"):
    _sec0["secret_key"] = crypto.generer_secret()
    sauver_config(_config_globale(), 0)
app.secret_key = _sec0["secret_key"].encode()

# Anti-mojibake
try:
    app.json.ensure_ascii = False
except Exception:
    app.config["JSON_AS_ASCII"] = False
app.config["JSON_AS_ASCII"] = False

@app.after_request
def _force_utf8(resp):
    ctype = resp.headers.get("Content-Type", "")
    if ctype.startswith(("text/", "application/json", "application/xml")):
        if "charset=" not in ctype:
            resp.headers["Content-Type"] = ctype + "; charset=utf-8"
    # En-têtes de sécurité (HSTS seulement si on est bien en HTTPS)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    if request.is_secure:
        resp.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains")
    return resp


# ============================================================
# ENREGISTREMENT DES BLUEPRINTS
# ============================================================
from candimail.web.routes.pages import bp as bp_pages
from candimail.web.routes.auth import bp as bp_auth
from candimail.web.routes.donnees import bp as bp_donnees
from candimail.web.routes.envoi import bp as bp_envoi
from candimail.web.routes.divers import bp as bp_divers

app.register_blueprint(bp_pages)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_donnees)
app.register_blueprint(bp_envoi)
app.register_blueprint(bp_divers)


@app.route("/api/health")
def api_health():
    """Sonde locale : port, version, heure, taille DB (debug + pywebview)."""
    try:
        taille_db = db.DB_FILE.stat().st_size if db.DB_FILE.exists() else 0
    except Exception:
        taille_db = -1
    try:
        port = request.host.split(":")[-1] if ":" in request.host else ""
    except Exception:
        port = ""
    return jsonify({
        "ok": True,
        "service": "candimail",
        "version": "v7-desktop",
        "port": port,
        "heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "debug": DEBUG_ACTIF,
        "db_octets": taille_db,
    })


@app.route("/api/debug/info")
def api_debug_info():
    """Debug avancé : état interne SANS secrets (mots de passe jamais exposés)."""
    import platform
    try:
        import flask as _flask
        v_flask = _flask.__version__
    except Exception:
        v_flask = "?"
    try:
        cfg = charger_config()
        comptes = [{"email": c.get("email", ""), "actif": bool(c.get("actif"))}
                   for c in cfg.get("comptes", [])]
        info_cfg = {
            "groupes": len(cfg.get("groupes", [])),
            "templates_perso": len(cfg.get("templates_perso", [])),
            "pieces_meta": len(cfg.get("pieces_jointes", {})),
            "imap_auto": cfg.get("imap", {}).get("auto_verif"),
            "imap_derniere": cfg.get("imap", {}).get("derniere_verif", 0),
            "delai": get_delai(),
        }
    except Exception as e:
        comptes, info_cfg = [], {"erreur": str(e)[:200]}
    try:
        taille_db = db.DB_FILE.stat().st_size if db.DB_FILE.exists() else 0
    except Exception:
        taille_db = -1
    # Queue du log applicatif (debug avancé côté UI)
    queue_log = []
    try:
        if LOG_FILE_APP.exists():
            lignes = LOG_FILE_APP.read_text(encoding="utf-8",
                                            errors="replace").splitlines()
            queue_log = lignes[-30:]
    except Exception:
        pass
    return jsonify({
        "ok": True,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "flask": v_flask,
        "version": "v7-desktop",
        "port": request.host.split(":")[-1] if ":" in request.host else "",
        "heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "debug": DEBUG_ACTIF,
        "db_octets": taille_db,
        "comptes": comptes,
        "config": info_cfg,
        "pieces_actives": len(get_pieces_actives()),
        "log_tail": queue_log,
    })


@app.errorhandler(Exception)
def _erreur_globale(e):
    """Debug avancé : toute exception non gérée → log fichier + JSON."""
    try:
        log.error("EXCEPTION %s %s\n%s",
                  request.method, request.path,
                  traceback.format_exc())
    except Exception:
        pass
    try:
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            return jsonify({"ok": False, "error": e.description}), e.code
    except Exception:
        pass
    if DEBUG_ACTIF:
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}",
                        "trace": traceback.format_exc(limit=8)}), 500
    return jsonify({"ok": False,
                    "error": "Erreur interne (voir .webview/candimail.log)"}), 500


# ============================================================
# INIT (factorisée : utilisée par app.py ET desktop.py/pywebview)
# ============================================================
_imap_thread_lance = [False]


def initialiser():
    """Prépare DB, pièces jointes, migration crypto. Retourne (cfg, migration)."""
    db.init_db(with_migration=True)
    recharger_pieces()
    cfg = charger_config()
    # Migration sécurité : chiffrer les mots de passe Gmail en clair
    _mig = False
    for c in cfg.get("comptes", []):
        if c.get("password") and not crypto.est_chiffre(c["password"]):
            c["password"] = crypto.chiffrer(c["password"])
            _mig = True
    if _mig:
        sauver_config(cfg)
        print("  🔒 Mots de passe Gmail chiffrés dans la base")
    if not crypto.DISPONIBLE:
        print("  ⚠️ cryptography absent → secrets NON chiffrés (pip install cryptography)")
    return cfg


# ============================================================
# MAIN
# ============================================================
def trouver_port(debut=None, fin=None):
    """Port libre : CANDIMAIL_PORT prioritaire, sinon défaut → +100."""
    if debut is None:
        try:
            debut = int(os.environ.get("CANDIMAIL_PORT", str(PORT_DEFAUT)))
        except ValueError:
            debut = PORT_DEFAUT
    if fin is None:
        fin = debut + 100
    for p in range(debut, fin):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    return debut

def _imap_auto_loop():
    while True:
        try:
            # Vérifier la boîte de CHAQUE utilisateur (uid 0 = global)
            for uid in db.uids_actifs():
                cfg = charger_config(uid)
                if cfg["imap"].get("auto_verif"):
                    intervalle = cfg["imap"].get("intervalle_min", 30) * 60
                    derniere = cfg["imap"].get("derniere_verif", 0)
                    if time.time() - derniere > intervalle and get_comptes_actifs():
                        print(f"[IMAP] Vérification auto (uid {uid})...")
                        verifier_toutes_boites(jours=30, uid=uid)
                        # Applique aussi les règles de classement automatique
                        filtres = cfg.get("filtres_gmail", [])
                        if filtres:
                            for cpt in get_comptes_actifs():
                                appliquer_filtres_compte(cpt, filtres, uid=uid)
            time.sleep(60)
        except Exception as e:
            print(f"[IMAP AUTO] {e}")
            time.sleep(300)

def demarrer_imap():
    """Lance la boucle IMAP auto une seule fois (idempotent)."""
    if _imap_thread_lance[0]:
        return
    _imap_thread_lance[0] = True
    t = threading.Thread(target=_imap_auto_loop, daemon=True)
    t.start()


def afficher_banniere(cfg, port):
    print()
    print("=" * 64)
    print("  📧 CANDIMAIL — v7 (automatisation Gmail)")
    print("=" * 64)
    comptes = get_comptes_actifs()
    print(f"  Comptes Gmail : {len(comptes)} actif(s)")
    print(f"  Pièces jointes: {len(get_pieces_actives())} active(s)")
    print(f"  Groupes       : {len(cfg.get('groupes', []))}")
    print(f"  Templates     : {len(cfg.get('templates_perso', []))} perso + 3 prédéfinis")
    print(f"  Délai         : {get_delai()}s"
          + (" (aléatoire)" if cfg['parametres'].get('delai_aleatoire') else ""))
    print(f"  URL           : http://127.0.0.1:{port}")
    print("=" * 64)
    print()

if __name__ == "__main__":
    try:
        import sys
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    cfg = initialiser()
    port = trouver_port()
    demarrer_imap()
    afficher_banniere(cfg, port)
    log.info("Démarrage serveur port=%s debug=%s", port, DEBUG_ACTIF)
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)