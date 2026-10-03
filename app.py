#!/usr/bin/env python3
"""Point d'entree serveur classique (compat : delegue au package).

Lancement :  python app.py   ou   python -m candimail.web.app
"""
from candimail.web.app import (  # noqa: F401
    app, PORT_DEFAUT, DEBUG_ACTIF, initialiser, trouver_port,
    demarrer_imap, afficher_banniere, log,
)

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
    log.info("Demarrage serveur port=%s debug=%s", port, DEBUG_ACTIF)
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)


