#!/usr/bin/env python3
"""
Candimail — application web locale (FastAPI + uvicorn).

Serveur HTTP accessible depuis le navigateur : 127.0.0.1 par défaut,
ou tout le réseau local avec l'option --lan (CANDIMAIL_HOST=0.0.0.0).

Usage :
    python candimail.py                 # navigateur par défaut, port 9999
    python candimail.py --port 9000     # forcer le port
    python candimail.py --debug         # logs détaillés
    python candimail.py --help          # aide

Env :
    CANDIMAIL_PORT=9999   force le port (prioritaire sur --port si les 2)
    CANDIMAIL_DEBUG=1     debug avancé (logs détaillés .webview/candimail.log)

Notes :
  - Le navigateur s'ouvre automatiquement sur http://127.0.0.1:<port>/app
  - Option --lan : accessible depuis un téléphone ou un autre PC du réseau local.
  - Fermer le terminal arrête proprement le programme.
"""
import argparse
import logging
import os
import sys
import threading
import time
import traceback
import urllib.request
import webbrowser
from pathlib import Path

ICI = Path(__file__).parent
LOG_DIR = ICI / ".webview"
LOG_DIR.mkdir(exist_ok=True)
LOG_DESKTOP = LOG_DIR / "desktop.log"

from logging.handlers import RotatingFileHandler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] candimail: %(message)s",
    handlers=[
        RotatingFileHandler(LOG_DESKTOP, maxBytes=1_000_000,
                            backupCount=3, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
dlog = logging.getLogger("candimail")


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Candimail — application Web (FastAPI)",
        epilog="L'application tourne en local (127.0.0.1), jamais sur un réseau.",
    )
    p.add_argument("--port", type=int, default=None,
                   help="Port local (défaut : 9999 ou CANDIMAIL_PORT, sinon port libre auto)")
    p.add_argument("--lan", action="store_true",
                   help="Accessible depuis tout le réseau local (0.0.0.0) au lieu de 127.0.0.1")
    p.add_argument("--debug", action="store_true",
                   help="Debug avancé : logs détaillés")
    return p.parse_args(argv)


def serveur_pret(port, timeout=20.0):
    """Attend que /api/health réponde (sonde fiable, pas juste TCP)."""
    debut = time.time()
    url = f"http://127.0.0.1:{port}/api/health"
    dernier_err = ""
    while time.time() - debut < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    dlog.info("sonde /api/health OK sur port %s", port)
                    return True
        except Exception as e:
            dernier_err = f"{type(e).__name__}: {e}"
            time.sleep(0.3)
    dlog.error("serveur non prêt après %.0fs (port %s) : %s",
               timeout, port, dernier_err)
    return False


def ip_locale(port):
    """IP locale pour l'accès réseau, portable et robuste (Win/Linux/mac).
    Utilise une connexion UDP (sans envoi) vers une adresse publique : la
    carte réseau qui servirait le trafic sortant est identifiée fiablement,
    même si le hostname ne se résout pas (fréquent sur macOS)."""
    import socket as _s
    s = _s.socket(_s.AF_INET, _s.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))     # rien n'est envoyé
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"                     # fallback universel
    finally:
        s.close()
    return f"http://{ip}:{port}"


def main(argv=None):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

    args = parse_args(argv)
    if args.debug:
        os.environ["CANDIMAIL_DEBUG"] = "1"

    # Import tardif : permet --help même si FastAPI manque.
    try:
        from candimail.web import api as candimail
    except Exception:
        dlog.error("import candimail impossible:\n%s",
                   traceback.format_exc())
        print("  Impossible de charger candimail — voir .webview/desktop.log")
        sys.exit(2)

    dlog.info("démarrage candimail.py args=%s", args)

    cfg = candimail.initialiser()

    # Port : CLI --port > CANDIMAIL_PORT > défaut 9999, puis 1er libre.
    if args.port:
        os.environ["CANDIMAIL_PORT"] = str(args.port)
    port = candimail.trouver_port()
    dlog.info("port choisi : %s", port)

    # Écoute réseau : --lan (ou CANDIMAIL_HOST=0.0.0.0) pour accéder
    # depuis un téléphone/autre PC du réseau local.
    host = "0.0.0.0" if (args.lan or os.environ.get("CANDIMAIL_HOST") == "0.0.0.0") else "127.0.0.1"

    candimail.demarrer_imap()
    candimail.afficher_banniere(cfg, port)

    t = threading.Thread(target=candimail.lancer_serveur,
                         args=(candimail.app, port),
                         kwargs={"host": host},
                         daemon=True, name="serveur-fastapi")
    t.start()

    url = f"http://127.0.0.1:{port}/app"

    if not serveur_pret(port):
        print("  ❌ Le serveur local n'a pas démarré à temps.")
        print("  Voir .webview/desktop.log et .webview/candimail.log")
        sys.exit(1)

    print(f"\n  🌐 Ouverture du navigateur : {url}")
    if host == "0.0.0.0":
        print(f"  📱 Accès réseau local : {ip_locale(port)}/app")
    print("  ⏹️  Fermez ce terminal pour arrêter Candimail.\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        dlog.warning("ouverture navigateur impossible : %s", e)
        print(f"  ⚠️  Ouvrez manuellement : {url}")

    # Boucle principale : attendre l'interruption (Ctrl+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dlog.info("arrêt demandé par l'utilisateur.")
        print("\n  👋 Arrêt de Candimail.")


if __name__ == "__main__":
    main()
