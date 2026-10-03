#!/usr/bin/env python3
"""
Candimail Desktop — lance Flask en thread + fenêtre pywebview.

Usage :
    python desktop.py                 # fenêtre desktop (défaut, port 8765)
    python desktop.py --port 9000     # forcer le port
    python desktop.py --debug         # logs détaillés + console dev WebView2
    python desktop.py --browser       # retombe sur le navigateur
    python desktop.py --help          # aide

Env :
    CANDIMAIL_PORT=9000   force le port (prioritaire sur --port si les 2)
    CANDIMAIL_DEBUG=1     debug avancé (logs détaillés .webview/candimail.log)

Notes :
  - Le serveur Flask tourne en thread daemon sur 127.0.0.1:port_libre.
  - pywebview utilise Edge WebView2 sous Windows (déjà présent sur Win10/11).
  - Fermer la fenêtre arrête proprement le programme (daemon threads).
"""
import argparse
import logging
import os
import socket
import sys
import threading
import time
import traceback
import urllib.request
from pathlib import Path

ICI = Path(__file__).parent
LOG_DIR = ICI / ".webview"
LOG_DIR.mkdir(exist_ok=True)
LOG_DESKTOP = LOG_DIR / "desktop.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] desktop: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DESKTOP, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
dlog = logging.getLogger("desktop")

# Profil WebView2 persistant (cookies/session conservés, pas de warning Temp)
WEBVIEW_DIR = LOG_DIR


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Candimail Desktop (pywebview)")
    p.add_argument("--port", type=int, default=None,
                   help="Port local (défaut : 8765 ou CANDIMAIL_PORT)")
    p.add_argument("--debug", action="store_true",
                   help="Debug avancé : logs détaillés + console WebView2")
    p.add_argument("--browser", action="store_true",
                   help="Ouvrir dans le navigateur au lieu de pywebview")
    p.add_argument("--plein-ecran", action="store_true",
                   help="Démarrer en plein écran")
    return p.parse_args(argv)


def port_libre(debut, fin=None):
    fin = (debut + 100) if fin is None else fin
    for port in range(debut, fin):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return debut


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


def lancer_serveur(app, port):
    # En desktop on préfère waitress (stable en thread) si dispo,
    # sinon le serveur Flask (use_reloader=False OBLIGATOIRE en thread).
    try:
        from waitress import serve
        dlog.info("serveur waitress sur 127.0.0.1:%s", port)
        serve(app, host="127.0.0.1", port=port, threads=8)
    except ImportError:
        dlog.warning("waitress absent → serveur Flask dev")
        app.run(host="127.0.0.1", port=port, debug=False,
                threaded=True, use_reloader=False)
    except Exception:
        dlog.error("crash serveur:\n%s", traceback.format_exc())
        raise


class PontDebug:
    """API JS↔Python (debug avancé déclenchable depuis la page)."""

    def __init__(self, get_port):
        self._get_port = get_port

    def ping(self):
        return {"ok": True, "port": self._get_port()}

    def ouvrir_logs(self):
        os.startfile(str(LOG_DIR))  # Windows : ouvre l'explorateur
        return {"ok": True}

    def lire_logs(self, n=50):
        out = {}
        for nom in ("candimail.log", "desktop.log"):
            f = LOG_DIR / nom
            try:
                lignes = f.read_text(encoding="utf-8",
                                     errors="replace").splitlines()
                out[nom] = lignes[-n:]
            except Exception as e:
                out[nom] = [f"(illisible : {e})"]
        return {"ok": True, "logs": out}


def injecter_debug_js(fenetre, active_debug):
    """Petit badge de debug dans la page : port + accès aux logs."""
    if not active_debug:
        return
    js = ("(function(){if(document.getElementById('cdm-dbg'))return;"
          "var d=document.createElement('div');d.id='cdm-dbg';"
          "d.style.cssText='position:fixed;bottom:8px;right:10px;z-index:99999;"
          "background:#43161C;color:#F2E7CE;font:11px monospace;"
          "padding:4px 10px;border-radius:8px;opacity:.92;cursor:pointer;';"
          "d.title='Clique : infos debug';"
          "d.textContent='DEBUG : '+location.host;"
          "d.onclick=function(){fetch('/api/debug/info')"
          ".then(function(r){return r.json();})"
          ".then(function(j){alert(JSON.stringify(j,null,1).slice(0,1500));});};"
          "document.body.appendChild(d);})();")
    try:
        fenetre.evaluate_js(js)
    except Exception as e:
        dlog.warning("injection JS debug impossible : %s", e)


def main(argv=None):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = parse_args(argv)
    if args.debug:
        os.environ["CANDIMAIL_DEBUG"] = "1"

    # Import tardif : permet --help même si Flask manque.
    try:
        from candimail.web import app as candimail
    except Exception:
        dlog.error("import candimail impossible:\n%s",
                   traceback.format_exc())
        print("  Impossible de charger candimail — voir .webview/desktop.log")
        sys.exit(2)

    dlog.info("démarrage desktop.py args=%s", args)

    cfg = candimail.initialiser()

    # Port : CLI --port > CANDIMAIL_PORT > défaut 8765, puis 1er libre.
    if args.port:
        os.environ["CANDIMAIL_PORT"] = str(args.port)
    port = candimail.trouver_port()
    dlog.info("port choisi : %s", port)

    candimail.demarrer_imap()
    candimail.afficher_banniere(cfg, port)

    t = threading.Thread(target=lancer_serveur,
                         args=(candimail.app, port),
                         daemon=True, name="serveur-flask")
    t.start()

    url = f"http://127.0.0.1:{port}/app"
    url_health = f"http://127.0.0.1:{port}/api/health"

    if args.browser:
        import webbrowser
        if serveur_pret(port):
            print(f"  Navigateur : {url}")
            print(f"  Santé      : {url_health}")
            webbrowser.open(url)
        else:
            print("  ❌ Serveur non démarré — voir .webview/desktop.log")
            sys.exit(1)
        # Le thread serveur étant daemon, on garde le process en vie.
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("\n  👋 Arrêt demandé.")
        return

    if not serveur_pret(port):
        print("  ❌ Le serveur local n'a pas démarré à temps.")
        print("  Voir .webview/desktop.log et .webview/candimail.log")
        sys.exit(1)

    try:
        import webview
    except ImportError:
        print("  ❌ pywebview non installé → pip install pywebview")
        print(f"  Repli navigateur : {url}")
        import webbrowser
        webbrowser.open(url)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
        return

    pont = PontDebug(lambda: port)
    fenetre = webview.create_window(  # noqa: F841 — garde une réf à la fenêtre
        "Candimail",
        url,
        width=1220,
        height=820,
        min_size=(900, 600),
        text_select=True,
        js_api=pont,
        fullscreen=args.plein_ecran,
    )

    def _on_charge():
        dlog.info("page chargée : %s", url)
        injecter_debug_js(fenetre, args.debug)

    try:
        fenetre.events.loaded += _on_charge
    except Exception as e:
        dlog.warning("hook 'loaded' indisponible : %s", e)

    dlog.info("ouverture fenêtre (debug=%s, plein_ecran=%s)",
              args.debug, args.plein_ecran)
    # gui="edgechromium" force WebView2 sous Windows ; None = auto sinon.
    # webview.start() bloque jusqu'à fermeture de la fenêtre, puis le
    # process se termine (threads serveur/IMAP en daemon).
    # private_mode=False : cookies/session + profil persistant dans .webview/
    # (sinon dossier Temp + warning au exit sous Windows).
    try:
        webview.start(gui="edgechromium", debug=args.debug,
                      private_mode=False, storage_path=str(WEBVIEW_DIR))
    except Exception as e:
        dlog.warning("edgechromium indisponible (%s) → gui auto", e)
        print(f"  ⚠️ edgechromium indisponible ({e}) → gui auto")
        webview.start(debug=args.debug, private_mode=False,
                      storage_path=str(WEBVIEW_DIR))
    dlog.info("fenêtre fermée — arrêt.")


if __name__ == "__main__":
    main()
