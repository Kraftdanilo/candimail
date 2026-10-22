#!/usr/bin/env python3
"""Candimail — application FastAPI.

Routes HTTP de l'application web locale (FastAPI + uvicorn).
Le serveur écoute sur 127.0.0.1 par défaut (option --lan = réseau local).

Dépendances legacy retirées : noyau.py utilise désormais un stockage de session
propre (thread-local) au lieu d'une session framework.
"""
import json, io, csv, time, uuid, threading, logging, socket, base64, os
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from candimail.core import crypto, db
from candimail.core.config import RESS_DIR, RACINE, UPLOADS_DIR, DATA_DIR, TEMPLATES, DEFAULT_CV
from candimail.core.noyau import (
    charger_config, sauver_config, _config_globale, get_comptes_actifs,
    get_pieces_actives, get_delai, recharger_pieces, erreur_publique,
    log_erreur, current_uid, session_set, session_get, _bulk_lock,
    _bulk_running, _bulk_state, _send_lock, _log_send_lock, _send_timestamps,
    _last_send_time, _email_valide, _MESSAGES_PUBLICS, parse_emails,
    compte_suivant, build_letter, build_subject, check_rate_limit,
    maintenant_str, charger_log, sauver_log, modifier_log, _pieces,
    _NONCE_TTL, _NONCE, creer_nonce, _nonce_valide, app_secret_bytes,
    _txt, get_selected_compte_index, set_selected_compte_index,
)
from candimail.services.smtp import envoyer_email, _envoyer_un_email
from candimail.services.imap import (
    verifier_toutes_boites, appliquer_filtres_compte, _gimap_ouvre,
)
from candimail.core.regles import (
    REGLES_DEFAUT, seed_regles, normaliser_regle, reindexer_priorites,
    appliquer_apprentissage, calculer_suggestions, export_sans_secrets,
)
from candimail.web import hist_helpers as hh
from candimail.core.purge import purger_orphelins
from candimail.services.ia_agent import (
    GROQ_MODELS, GOOGLE_MODELS, MISTRAL_MODELS, IA_TASKS,
    openrouter_models as _openrouter_models, agent_par_defaut as _ia_agent,
)

# ============================================================
# CONFIG GLOBALE (port, debug, chemins logs)
# ============================================================
PORT_DEFAUT = 9999
DEBUG_ACTIF = os.environ.get("CANDIMAIL_DEBUG") == "1"

LOG_DIR = RACINE / ".webview"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE_APP = LOG_DIR / "candimail.log"

from logging.handlers import RotatingFileHandler
_file_handler = RotatingFileHandler(LOG_FILE_APP, maxBytes=1_000_000,
                                    backupCount=3, encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[_file_handler, logging.StreamHandler()],
)
log = logging.getLogger("candimail")

# ============================================================
# APP FASTAPI
# ============================================================
app = FastAPI(title="Candimail", docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory=str(RESS_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(RESS_DIR / "templates"))

_AUTEUR = "Dane hk \\Manifest"
_COPYRIGHT = ("Copyright © 2026 — Dane hk \\Manifest. "
              "Licence MIT — créateur de l'app.")

app.state.MAX_CONTENT_LENGTH = 20 * 1024 * 1024

# Anti-mojibake
try:
    app.json.ensure_ascii = False
except Exception:
    pass


@app.middleware("http")
async def _set_uid_middleware(request: Request, call_next):
    """Définit l'uid du profil actif dans le stockage thread-local
    à partir du header X-UID, pour que current_uid() dans noyau fonctionne."""
    try:
        uid_header = request.headers.get("x-uid")
        if uid_header:
            session_set("uid", int(uid_header))
        else:
            # Pas de header : on garde 0 (profil par défaut) ou on ne touche rien
            if session_get("uid") is None:
                session_set("uid", 0)
    except (TypeError, ValueError):
        session_set("uid", 0)
    response = await call_next(request)
    return response


@app.middleware("http")
async def _force_utf8(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        log.error("Middleware error on %s %s: %s", request.method, request.url.path, e, exc_info=True)
        return JSONResponse({"ok": False, "error": "Erreur interne"}, status_code=500)
    ctype = response.headers.get("content-type", "")
    if ctype.startswith(("text/", "application/json", "application/xml")):
        if "charset=" not in ctype:
            response.headers["content-type"] = ctype + "; charset=utf-8"
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


# ============================================================
# SESSION UID (multi-profils : uid lu depuis le header X-UID,
# fallback sur le stockage thread-local, puis 0)
# ============================================================
def _get_uid(request: Request) -> int:
    # 1. Priorité : header X-UID envoyé par le front (profil sélectionné)
    try:
        uid_header = request.headers.get("x-uid")
        if uid_header:
            return int(uid_header)
    except (TypeError, ValueError):
        pass
    # 2. Fallback : stockage thread-local (defini par le middleware)
    return int(session_get("uid", 0) or 0)


def _profil_verrouille(uid: int) -> bool:
    """Le profil 0 est le profil SYSTÈME (données de démonstration) :
    on ne peut pas y saisir d'informations personnelles. Pour utiliser
    l'application pour de vrai, crée un profil (uid >= 1)."""
    return int(uid or 0) == 0


def _templates_context() -> dict:
    return {
        "AUTEUR": _AUTEUR,
        "COPYRIGHT": _COPYRIGHT,
        "annee": datetime.now().year,
    }


def _render(template_name: str, **kwargs) -> HTMLResponse:
    ctx = _templates_context()
    ctx.update(kwargs)
    html = templates.get_template(template_name).render(**ctx)
    return HTMLResponse(content=html)


# ============================================================
# ROUTES DE BASE
# ============================================================
@app.get("/")
async def racine():
    return RedirectResponse(url="/app")


@app.get("/app")
async def index(request: Request):
    return _render("index.html", templates=TEMPLATES)


@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse(url="/static/favicon.svg", status_code=302)


@app.get("/rgpd")
async def page_rgpd(request: Request):
    return _render("rgpd.html")


@app.get("/cgu")
async def page_cgu(request: Request):
    return _render("cgu.html")


@app.get("/cv")
async def cv_page(request: Request):
    data = db.cv_get(current_uid())
    if not isinstance(data, dict):
        data = json.loads(json.dumps(DEFAULT_CV))
    base = json.loads(json.dumps(DEFAULT_CV))
    base.update(data)
    return _render("cv.html", cv=base)


# ------------------------------------------------------------
# CV (GET /api/cv, POST /api/cv)
# ------------------------------------------------------------
@app.get("/api/cv")
async def api_cv_get():
    """Renvoie le CV du profil actif (fusionné avec les valeurs par défaut)."""
    data = db.cv_get(current_uid())
    if not isinstance(data, dict):
        data = json.loads(json.dumps(DEFAULT_CV))
    base = json.loads(json.dumps(DEFAULT_CV))
    base.update(data)
    return {"ok": True, "cv": base}


@app.post("/api/cv")
async def api_cv_set(request: Request):
    """Enregistre le CV du profil actif."""
    uid = current_uid()
    if _profil_verrouille(uid):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour enregistrer ton CV."}, status_code=403)
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "error": "JSON invalide"}, status_code=400)
    cv = data.get("cv")
    if not isinstance(cv, dict):
        return JSONResponse({"ok": False, "error": "CV invalide"}, status_code=400)
    try:
        db.cv_set(cv, current_uid())
    except Exception as e:
        log_erreur("api_cv_set", e, "sauvegarde CV")
        return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="db")[0]}, status_code=500)
    return {"ok": True}


@app.get("/api/health")
async def api_health():
    return {"ok": True, "service": "candimail"}


@app.get("/api/debug/info")
async def api_debug_info(request: Request):
    if not DEBUG_ACTIF:
        return JSONResponse({"ok": False, "error": "Ressource introuvable"}, status_code=404)
    import platform
    try:
        import fastapi as _fastapi
        v_fastapi = _fastapi.__version__
    except Exception:
        v_fastapi = "?"
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
        log.error("api_debug_info: %s", e, exc_info=True)
        comptes, info_cfg = [], {"erreur": "informations indisponibles"}
    try:
        taille_db = db.DB_FILE.stat().st_size if db.DB_FILE.exists() else 0
    except Exception:
        taille_db = -1
    queue_log = []
    try:
        if LOG_FILE_APP.exists():
            lignes = LOG_FILE_APP.read_text(encoding="utf-8", errors="replace").splitlines()
            queue_log = lignes[-30:]
    except Exception:
        pass
    return {
        "ok": True,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "fastapi": v_fastapi,
        "version": "r0.0.1",
        "port": "",
        "heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "debug": DEBUG_ACTIF,
        "db_octets": taille_db,
        "comptes": comptes,
        "config": info_cfg,
        "pieces_actives": len(get_pieces_actives()),
        "log_tail": queue_log,
    }


# ============================================================
# PROFILS UTILISATEURS (multi-profils isolés)
# ============================================================
@app.get("/api/profils")
async def api_profils_lister():
    """Liste tous les profils existants avec leur uid et nom."""
    return {"ok": True, "profils": db.profils_lister()}


@app.post("/api/profils")
async def api_profils_creer(request: Request):
    """Crée un nouveau profil avec un uid unique."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "error": "JSON invalide"}, status_code=400)

    nom = (data.get("nom") or "").strip()
    if not nom:
        return JSONResponse({"ok": False, "error": "Nom requis"}, status_code=400)

    # Générer un uid unique : max(uid existants) + 1, ou 1 si vide
    profils = db.profils_lister()
    if profils:
        nouvel_uid = max(p["uid"] for p in profils) + 1
    else:
        nouvel_uid = 1

    if not db.profil_creer(nouvel_uid, nom):
        return JSONResponse({"ok": False, "error": "Profil déjà existant"}, status_code=409)

    return {"ok": True, "uid": nouvel_uid, "nom": nom}


# ============================================================
# INIT (point d'entrée utilisé par candimail.py)
# ============================================================
_imap_thread_lance = [False]


def purge_orphelins_au_demarrage():
    try:
        supprimes, octets = purger_orphelins()
        if supprimes:
            print(f"  🧹 uploads/ : {len(supprimes)} fichier(s) orphelin(s) "
                  f"supprimé(s) ({octets // 1024} Ko libérés)")
    except Exception as e:
        log.warning("purge uploads ignorée: %s", e)


def initialiser():
    """Prépare DB, pièces jointes, migration crypto. Retourne la config."""
    db.init_db(with_migration=True)
    recharger_pieces()
    cfg = charger_config()
    purge_orphelins_au_demarrage()
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
    # Stocke le secret de session pour le nonce
    _sec0 = _config_globale().setdefault("securite", {})
    if not _sec0.get("secret_key"):
        _sec0["secret_key"] = crypto.generer_secret()
        sauver_config(_config_globale(), 0)
    return cfg


def trouver_port(debut=None, fin=None):
    """Port libre : CANDIMAIL_PORT prioritaire, sinon défaut → +100.
    En dernier recours, demande un port éphémère à l'OS (port=0) : l'app
    démarre TOUJOURS, quel que soit l'état de la machine."""
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
    # Dernier recours : l'OS choisit un port libre garanti
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def demarrer_imap():
    """Lance la boucle IMAP auto une seule fois (idempotent)."""
    from candimail.services.imap import verifier_toutes_boites
    if _imap_thread_lance[0]:
        return
    _imap_thread_lance[0] = True

    def _loop():
        while True:
            try:
                for uid in db.uids_actifs():
                    cfg = charger_config(uid)
                    if cfg["imap"].get("auto_verif"):
                        intervalle = cfg["imap"].get("intervalle_min", 30) * 60
                        derniere = cfg["imap"].get("derniere_verif", 0)
                        if time.time() - derniere > intervalle and get_comptes_actifs():
                            print(f"[IMAP] Vérification auto (uid {uid})...")
                            verifier_toutes_boites(jours=30, uid=uid)
                time.sleep(60)
            except Exception as e:
                print(f"[IMAP AUTO] {e}")
                time.sleep(300)

    t = threading.Thread(target=_loop, daemon=True, name="imap-auto")
    t.start()


def afficher_banniere(cfg, port):
    print()
    print("=" * 64)
    print("  📧 CANDIMAIL — r0.0.1 — automatisation Gmail libre (licence MIT)")
    print(f"  Créateur : {_AUTEUR}   |   © 2026 — Licence MIT")
    print("=" * 64)
    comptes = get_comptes_actifs()
    print(f"  Comptes Gmail : {len(comptes)} actif(s)")
    print(f"  Pièces jointes: {len(get_pieces_actives())} active(s)")
    print(f"  Groupes       : {len(cfg.get('groupes', []))}")
    print(f"  Templates     : {len(cfg.get('templates_perso', []))} perso + 3 prédéfinis")
    print(f"  Délai         : {get_delai()}s"
          + (" (aléatoire)" if cfg['parametres'].get('delai_aleatoire') else ""))
    print(f"  Serveur local : http://127.0.0.1:{port}")
    print("=" * 64)
    print()


# ============================================================
# SUIVI DES ENVOIS
# ============================================================
def _calculer_suivi():
    log = charger_log()
    items = sorted(log.items(), key=lambda x: x[1].get("date", ""), reverse=True)
    total = len(items)
    envoyes = len([x for x in items if x[1].get("envoye")])
    repondus = len([x for x in items if x[1].get("repondu")])
    bounces = len([x for x in items if x[1].get("bounce")])
    echecs = total - envoyes
    sans_pj = len([x for x in items if x[1].get("sans_pj")])

    from collections import Counter
    par_jour = Counter()
    for _, info in items:
        d = info.get("date", "")
        if d and len(d) >= 10:
            par_jour[d[:10]] += 1

    jours = []
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        jours.append({"date": d, "total": par_jour.get(d, 0)})

    lignes = []
    for company, info in items:
        if info.get("repondu"):
            statut = "replied"
        elif info.get("bounce"):
            statut = "bounce"
        elif info.get("envoye"):
            statut = "ok"
        else:
            statut = "err"
        lignes.append({
            "company": company, "email": info.get("email") or "", "date": info.get("date") or "",
            "statut": statut, "envoye": bool(info.get("envoye")), "repondu": bool(info.get("repondu")),
            "bounce": bool(info.get("bounce")), "sans_pj": bool(info.get("sans_pj")),
            "groupe_nom": info.get("groupe_nom") or "", "sujet_reponse": info.get("sujet_reponse") or "",
            "bounce_raison": info.get("bounce_raison") or "", "erreur": info.get("erreur") or "",
        })
    return {
        "items": lignes, "total": total, "envoyes": envoyes, "repondus": repondus,
        "bounces": bounces, "echecs": echecs, "sans_pj": sans_pj, "jours": jours,
    }


@app.get("/api/suivi")
async def api_suivi():
    return {"ok": True, **_calculer_suivi()}


@app.get("/api/suivi/recherche")
async def api_suivi_recherche(q: str = "", statut: str = "", limite: int = 50):
    """Recherche rapide et paginée dans le log des envois.
    Query : q (texte libre, sur entreprise+email+erreur), statut
    (ok|err|replied|bounce), limite. Optimisé pour l'autocomplétion.
    """
    q = (q or "").strip().lower()
    items = _calculer_suivi()["items"]
    if q:
        items = [l for l in items
                 if q in l["company"].lower()
                 or q in (l["email"] or "").lower()
                 or q in (l["erreur"] or "").lower()]
    if statut in ("ok", "err", "replied", "bounce"):
        items = [l for l in items if l["statut"] == statut]
    try:
        limite = max(1, min(int(limite), 200))
    except (TypeError, ValueError):
        limite = 50
    return {"ok": True, "total": len(items), "items": items[:limite]}


@app.get("/suivi")
async def suivi(request: Request):
    d = _calculer_suivi()
    return _render("suivi.html",
                   items=[(l["company"], l) for l in d["items"]],
                   total=d["total"], envoyes=d["envoyes"], repondus=d["repondus"],
                   bounces=d["bounces"], echecs=d["echecs"],
                   chart_data=json.dumps({
                       "envoyes": d["envoyes"], "echecs": d["echecs"],
                       "repondus": d["repondus"], "bounces": d["bounces"],
                       "jours": d["jours"],
                   }, ensure_ascii=False))


@app.get("/historique")
async def page_historique(request: Request):
    return _render("historique.html")


# ============================================================
# HISTORIQUE (API)
# ============================================================
@app.get("/api/historique")
async def api_historique():
    return {"ok": True, "actions": db.hist_lister(current_uid(), limite=60)}


@app.delete("/api/historique")
async def api_historique_vider():
    db.hist_purger(current_uid())
    return {"ok": True}


@app.post("/api/historique/{hid}/undo")
async def api_historique_undo(hid: int):
    uid = current_uid()
    h = db.hist_get(hid, uid)
    if not h:
        return JSONResponse({"ok": False, "error": "Action introuvable"}, status_code=404)
    a_jouer = h["undo"] if not h["undone"] else h["redo"]
    if a_jouer is None:
        return JSONResponse({"ok": False, "error": "Cette action ne peut pas être annulée"}, status_code=400)
    try:
        ok, message = hh.appliquer(a_jouer, uid)
    except Exception as e:
        log_erreur("api_historique_undo", e, f"action {hid}")
        return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="db")[0]}, status_code=500)
    if not ok:
        return JSONResponse({"ok": False, "error": message}, status_code=400)
    etait_annulee = bool(h["undone"])
    db.hist_marquer(hid, not etait_annulee, uid)
    return {"ok": True, "message": ("Action rétablie" if etait_annulee else "Action annulée"),
            "undone": not etait_annulee, "type": h["type"]}


@app.post("/api/historique/{hid}/redo")
async def api_historique_redo(hid: int):
    uid = current_uid()
    h = db.hist_get(hid, uid)
    if not h:
        return JSONResponse({"ok": False, "error": "Action introuvable"}, status_code=404)
    if not h["undone"]:
        return JSONResponse({"ok": False, "error": "Cette action est déjà appliquée"}, status_code=400)
    if h["redo"] is None:
        return JSONResponse({"ok": False, "error": "Rétablissement impossible"}, status_code=400)
    try:
        ok, message = hh.appliquer(h["redo"], uid)
    except Exception as e:
        log_erreur("api_historique_redo", e, f"action {hid}")
        return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="db")[0]}, status_code=500)
    if not ok:
        return JSONResponse({"ok": False, "error": message}, status_code=400)
    db.hist_marquer(hid, False, uid)
    return {"ok": True, "message": "Action rétablie", "type": h["type"]}


@app.post("/api/historique")
async def api_historique_ajouter(request: Request):
    data = await request.json()
    typ = _txt(data.get("type"))[:40]
    if not typ:
        return JSONResponse({"ok": False, "error": "Type requis"}, status_code=400)
    hid = db.hist_ajouter(
        typ, _txt(data.get("label"))[:200] or typ,
        data.get("undo"), data.get("redo"), current_uid(),
    )
    return {"ok": True, "id": hid}


# ============================================================
# ENTREPRISES
# ============================================================
@app.get("/api/companies")
async def api_companies_get():
    return {"ok": True, "companies": db.companies_get(current_uid())}


@app.post("/api/companies")
async def api_companies_add(request: Request):
    if _profil_verrouille(current_uid()):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour ajouter des entreprises."}, status_code=403)
    data = await request.json()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    cat = (data.get("cat") or "pme").strip()
    context = (data.get("context") or "").strip()
    if not name or not email or "@" not in email:
        return JSONResponse({"ok": False, "error": "Nom et email valides requis"}, status_code=400)
    if cat not in ("grands", "pme", "port"):
        cat = "pme"
    db.companies_add({"name": name, "cat": cat, "email": email, "context": context, "custom": True}, current_uid())
    return {"ok": True}


@app.delete("/api/companies/{name:path}")
async def api_companies_delete(name: str):
    uid = current_uid()
    companies = db.companies_get(uid)
    cible = next((c for c in companies if c["name"] == name), None)
    if cible is None:
        return JSONResponse({"ok": False, "error": "Entreprise introuvable"}, status_code=404)
    db.companies_delete(name, uid)
    _hist_suppr(uid, [cible], "Supprimer")
    return {"ok": True, "nom": name}


@app.delete("/api/companies")
async def api_companies_delete_bulk(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    noms = data.get("names")
    if not isinstance(noms, list) or not noms:
        return JSONResponse({"ok": False, "error": "Aucune entreprise indiquée"}, status_code=400)
    noms = {_txt(n) for n in noms[:500] if _txt(n)}
    uid = current_uid()
    companies = db.companies_get(uid)
    cibles = [c for c in companies if c["name"] in noms]
    if not cibles:
        return JSONResponse({"ok": False, "error": "Aucune entreprise trouvée"}, status_code=404)
    db.companies_replace([c for c in companies if c["name"] not in noms], uid)
    _hist_suppr(uid, cibles, "Supprimer")
    return {"ok": True, "supprimees": len(cibles)}


@app.put("/api/companies/{name:path}")
async def api_companies_update(name: str, request: Request):
    data = await request.json()
    new_name = (data.get("name") or name).strip()
    email = (data.get("email") or "").strip()
    cat = (data.get("cat") or "pme").strip()
    context = (data.get("context") or "").strip()
    if not new_name or not email or "@" not in email:
        return JSONResponse({"ok": False, "error": "Nom et email valides requis"}, status_code=400)
    if cat not in ("grands", "pme", "port"):
        cat = "pme"
    companies = db.companies_get(current_uid())
    idx = next((i for i, c in enumerate(companies) if c["name"] == name), -1)
    if idx < 0:
        return JSONResponse({"ok": False, "error": "Entreprise introuvable"}, status_code=404)
    if new_name != name and any(c["name"] == new_name for c in companies):
        return JSONResponse({"ok": False, "error": "Une autre entreprise porte déjà ce nom"}, status_code=400)
    companies[idx] = {"name": new_name, "cat": cat, "email": email, "context": context, "custom": companies[idx].get("custom", True)}
    db.companies_replace(companies, current_uid())
    if new_name != name:
        def _renommer(l):
            if name in l:
                l[new_name] = l.pop(name)
        modifier_log(_renommer)
    return {"ok": True}


@app.post("/api/companies/seed")
async def api_companies_seed(request: Request):
    data = await request.json()
    companies = data.get("companies") or []
    if not isinstance(companies, list) or not companies:
        return JSONResponse({"ok": False, "error": "Liste invalide"}, status_code=400)
    existing = {c["name"] for c in db.companies_get(current_uid())}
    added = 0
    for c in companies:
        name = (c.get("name") or "").strip()
        if not name or name in existing:
            continue
        db.companies_add({
            "name": name,
            "cat": c.get("cat") if c.get("cat") in ("grands", "pme", "port") else "pme",
            "email": c.get("email") or "", "context": c.get("context") or "", "custom": bool(c.get("custom")),
        }, current_uid())
        existing.add(name)
        added += 1
    return {"ok": True, "added": added}


def _hist_suppr(uid, cibles, verbe):
    try:
        db.hist_ajouter(
            "supprimer_entreprise",
            f"{verbe} « {cibles[0]['name']} »" + (f" +{len(cibles) - 1} autre(s)" if len(cibles) > 1 else ""),
            {"op": "ajouter_entreprises", "data": cibles},
            {"op": "supprimer_entreprises", "noms": [c["name"] for c in cibles]}, uid,
        )
    except Exception as e:
        log_erreur("api_companies_delete", e, "historique")


# ============================================================
# CONFIG
# ============================================================
@app.get("/api/config")
async def api_config_get():
    cfg = charger_config()
    safe = {"candidat": {k: _txt(cfg.get("candidat", {}).get(k)) for k in ("nom", "tel", "email", "ville", "pays", "diplome", "spec")}}
    p = cfg.get("parametres", {})
    safe["parametres"] = {k: p.get(k) for k in ("delai_secondes", "delai_aleatoire", "delai_min", "delai_max", "max_par_heure", "smtp_timeout", "smtp_retries", "template")}
    im = cfg.get("imap", {})
    safe["imap"] = {k: im.get(k) for k in ("auto_verif", "intervalle_min", "derniere_verif")}
    safe["groupes"] = cfg.get("groupes", [])
    safe["templates_perso"] = cfg.get("templates_perso", [])
    safe["pieces_jointes"] = cfg.get("pieces_jointes", {})
    safe["filtres_gmail"] = cfg.get("filtres_gmail", [])
    safe["filtres_init"] = cfg.get("filtres_init", 0)
    # Comptes sans mot de passe (démo) masqués dans les vrais profils
    tous_comptes = [{"index": i, "email": c.get("email", ""), "actif": bool(c.get("actif", True)), "has_password": bool(c.get("password")), "devoiler": bool(c.get("devoiler", False)), "template": c.get("template", "") or ""} for i, c in enumerate(_config_globale().get("comptes", []))]
    if not _profil_verrouille(current_uid()):
        tous_comptes = [c for c in tous_comptes if c["has_password"]]
    safe["comptes"] = tous_comptes
    tous = {k: {"nom": v["nom"], "predefini": True, "categorie": "predefini"} for k, v in TEMPLATES.items()}
    for t in cfg.get("templates_perso", []):
        tid = t.get("id")
        if not tid:
            continue
        tous[tid] = {"nom": t.get("nom", "Sans nom"), "categorie": t.get("categorie", "autre"), "predefini": False}
    safe["templates_dispo"] = tous
    return safe


@app.post("/api/config")
async def api_config_update(request: Request):
    data = await request.json()
    uid = current_uid()
    if _profil_verrouille(uid):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système de démonstration — crée un vrai profil pour saisir tes informations."}, status_code=403)
    cfg = charger_config()
    profil_avant = None
    if isinstance(data.get("candidat"), dict):
        profil_avant = dict(cfg.get("candidat", {}))
        for k, v in data["candidat"].items():
            if k in cfg["candidat"]:
                cfg["candidat"][k] = _txt(v)
        if not cfg["candidat"].get("nom", "").strip():
            return JSONResponse({"ok": False, "error": "Le nom du profil est obligatoire"}, status_code=400)
        cfg["candidat"]["pays"] = cfg["candidat"].get("pays") or "Côte d'Ivoire"
    if "parametres" in data:
        for k, v in data["parametres"].items():
            if k not in cfg["parametres"]:
                continue
            if k in ("delai_secondes", "max_par_heure", "smtp_timeout", "smtp_retries", "delai_min", "delai_max"):
                try: cfg["parametres"][k] = int(v)
                except (TypeError, ValueError): pass
            elif k == "delai_aleatoire":
                cfg["parametres"][k] = bool(v)
            else:
                cfg["parametres"][k] = str(v)
    sauver_config(cfg)
    if profil_avant is not None:
        profil_apres = dict(cfg["candidat"])
        if profil_avant != profil_apres:
            try:
                db.hist_ajouter("profil", f"Modifier le profil ({profil_apres.get('nom', '')})", {"op": "profil", "avant": profil_avant}, {"op": "profil", "avant": profil_apres}, current_uid())
            except Exception:
                log_erreur("api_config_update", None, "historique profil")
    return {"ok": True}


# ============================================================
# COMPTES
# ============================================================
@app.post("/api/comptes/nonce")
async def api_comptes_nonce():
    return {"ok": True, "nonce": creer_nonce()}


@app.get("/api/comptes")
async def api_comptes_list():
    cfg = _config_globale()
    # Les comptes SANS mot de passe (comme le compte de démo) ne sont pas
    # utilisables : on ne les montre pas dans les vrais profils (uid >= 1).
    masquer_demo = not _profil_verrouille(current_uid())
    safe = [{"index": i, "email": c.get("email", ""), "actif": bool(c.get("actif", True)), "has_password": bool(c.get("password")), "template": c.get("template", "") or "", "devoiler": bool(c.get("devoiler", False))}
            for i, c in enumerate(cfg.get("comptes", []))]
    if masquer_demo:
        safe = [c for c in safe if c["has_password"]]
    return {"comptes": safe}


@app.post("/api/comptes")
async def api_comptes_add(request: Request):
    uid = current_uid()
    if _profil_verrouille(uid):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour ajouter ton compte Gmail."}, status_code=403)
    data = await request.json()
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    template = (data.get("template") or "").strip()
    if not email or not password or "@" not in email:
        return JSONResponse({"ok": False, "error": "Email ou mot de passe invalide"}, status_code=400)
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    for c in comptes:
        if str(c.get("email", "")).lower() == email.lower():
            c["password"] = crypto.chiffrer(password)
            c["actif"] = True
            c["template"] = template
            sauver_config(cfg, 0)
            return {"ok": True, "updated": True}
    comptes.append({"email": email, "password": crypto.chiffrer(password), "actif": True, "template": template})
    cfg["comptes"] = comptes
    sauver_config(cfg, 0)
    return {"ok": True, "created": True}


@app.delete("/api/comptes/{idx}")
async def api_comptes_delete(idx: int):
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return JSONResponse({"ok": False, "error": "Index invalide"}, status_code=404)
    comptes.pop(idx)
    cfg["comptes"] = comptes
    sauver_config(cfg, 0)
    return {"ok": True}


@app.post("/api/comptes/{idx}/template")
async def api_comptes_template(idx: int, request: Request):
    data = await request.json()
    template = (data.get("template") or "").strip()
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return JSONResponse({"ok": False, "error": "Index invalide"}, status_code=404)
    comptes[idx]["template"] = template
    sauver_config(cfg, 0)
    return {"ok": True, "template": template}


@app.get("/api/comptes/selected")
async def api_comptes_selected():
    return {"index": get_selected_compte_index()}


@app.post("/api/comptes/selected")
async def api_comptes_selected_set(request: Request):
    data = await request.json()
    idx = data.get("index")
    if idx is not None and (idx < 0 or idx >= len(get_comptes_actifs())):
        return JSONResponse({"ok": False, "error": "Index invalide"}, status_code=400)
    set_selected_compte_index(idx)
    return {"ok": True, "index": idx}


@app.post("/api/comptes/{idx}/toggle")
async def api_comptes_toggle(idx: int):
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return JSONResponse({"ok": False, "error": "Index invalide"}, status_code=404)
    comptes[idx]["actif"] = not comptes[idx].get("actif", True)
    sauver_config(cfg, 0)
    return {"ok": True, "actif": comptes[idx]["actif"]}


@app.post("/api/comptes/{idx}/reveal")
async def api_comptes_reveal(idx: int, request: Request):
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return JSONResponse({"ok": False, "error": "Index invalide"}, status_code=404)
    if not comptes[idx].get("devoiler", False):
        return JSONResponse({"ok": False, "error": "Révélation désactivée — active-la volontairement dans la config du compte"}, status_code=403)
    try:
        data = await request.json()
    except Exception:
        data = {}
    if not _nonce_valide(data.get("nonce")):
        return JSONResponse({"ok": False, "error": "Requête non autorisée (nonce invalide)"}, status_code=403)
    c = comptes[idx]
    if not c.get("password"):
        return JSONResponse({"ok": False, "error": "Aucun mot de passe enregistré"}, status_code=400)
    try:
        mdp = crypto.dechiffrer(c["password"])
    except Exception as e:
        log_erreur("api_comptes_reveal", e, f"compte idx={idx}")
        msg, _ = erreur_publique(type_erreur="crypto", where="api_comptes_reveal")
        return JSONResponse({"ok": False, "error": msg}, status_code=500)
    if not mdp:
        return JSONResponse({"ok": False, "error": "Mot de passe illisible (clé de chiffrement absente)"}, status_code=500)
    return {"ok": True, "email": c.get("email", ""), "password": mdp, "longueur": len(mdp), "actif": bool(c.get("actif", True))}


@app.post("/api/comptes/test")
async def api_comptes_test(request: Request):
    import smtplib, ssl
    data = await request.json()
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    if not password:
        cfg = _config_globale()
        for c in cfg.get("comptes", []):
            if str(c.get("email", "")).lower() == email.lower():
                password = crypto.dechiffrer(c["password"])
                break
        if not password:
            return JSONResponse({"ok": False, "error": "Compte introuvable"}, status_code=404)
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=15) as srv:
            srv.login(email, password)
        return {"ok": True, "message": f"✅ SMTP OK pour {email}"}
    except smtplib.SMTPAuthenticationError:
        return JSONResponse({"ok": False, "error": "❌ Auth refusée — vérifie le mot de passe"}, status_code=400)
    except Exception as e:
        log_erreur("api_comptes_test", e, f"test SMTP {email}")
        return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="smtp")[0]}, status_code=502)


# ============================================================
# PIÈCES JOINTES
# ============================================================
def _resoudre_piece(piece_id):
    nom = str(piece_id or "").strip()
    if not nom or len(nom) > 255:
        return None
    if nom != Path(nom).name:
        return None
    if nom in (".", "..") or nom.startswith("."):
        return None
    if any(c in nom for c in ('/', '\\', '\x00')) or ":" in nom:
        return None
    path = (UPLOADS_DIR / nom).resolve()
    try:
        racine = UPLOADS_DIR.resolve()
    except OSError:
        return None
    if racine != path.parent:
        return None
    return path


@app.get("/api/pieces")
async def api_pieces_list():
    u = current_uid()
    recharger_pieces(u)
    pieces = []
    for k, p in _pieces.get(int(u or 0), {}).items():
        pieces.append({"id": k, "nom_original": p.get("nom_original", k), "actif": p.get("actif", True), "taille_kb": Path(p["chemin"]).stat().st_size // 1024 if Path(p["chemin"]).exists() else 0})
    return {"pieces": pieces}


@app.post("/api/pieces")
async def api_pieces_add(request: Request):
    if _profil_verrouille(current_uid()):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour ajouter des pièces jointes."}, status_code=403)
    form = await request.form()
    if "fichier" not in form:
        return JSONResponse({"ok": False, "error": "Aucun fichier"}, status_code=400)
    f = form["fichier"]
    if not f.filename or not f.filename.lower().endswith(".pdf"):
        return JSONResponse({"ok": False, "error": "PDF requis"}, status_code=400)
    uid = current_uid()
    safe_name = f"u{uid}_{int(time.time()*1000)}_{f.filename}"
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._-")
    path = UPLOADS_DIR / safe_name
    content = await f.read()
    path.write_bytes(content)
    cfg = charger_config()
    cfg.setdefault("pieces_jointes", {})[safe_name] = {"nom_original": f.filename, "actif": True}
    sauver_config(cfg)
    recharger_pieces()
    return {"ok": True, "id": safe_name}


@app.delete("/api/pieces/{piece_id:path}")
async def api_pieces_delete(piece_id: str):
    try:
        path = _resoudre_piece(piece_id)
        if path is None:
            return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
        if path.exists():
            path.unlink()
        cfg = charger_config()
        cfg.get("pieces_jointes", {}).pop(piece_id, None)
        sauver_config(cfg)
        recharger_pieces()
        try:
            purger_orphelins()
        except Exception:
            pass
        return {"ok": True}
    except Exception as e:
        log_erreur("api_pieces_delete", e, "suppression piece")
        return JSONResponse({"ok": False, "error": erreur_publique(type_erreur="fichier")[0]}, status_code=500)


@app.post("/api/pieces/{piece_id:path}/toggle")
async def api_pieces_toggle(piece_id: str):
    cfg = charger_config()
    pj = cfg.get("pieces_jointes", {})
    if piece_id not in pj:
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    pj[piece_id]["actif"] = not pj[piece_id].get("actif", True)
    sauver_config(cfg)
    recharger_pieces()
    return {"ok": True, "actif": pj[piece_id]["actif"]}


# ============================================================
# TEMPLATES PERSONNALISÉS
# ============================================================
def _seed_templates_defauts(cfg):
    templates = cfg.get("templates_perso", [])
    ids = {t.get("id") for t in templates}
    ajoutes = False
    for key, t in TEMPLATES.items():
        tid = f"tpl_predef_{key}"
        if tid in ids:
            continue
        templates.append({"id": tid, "nom": t["nom"], "objet": t["objet"], "corps": t["corps"], "categorie": "candidature", "cree_le": maintenant_str()})
        ajoutes = True
    if ajoutes:
        cfg["templates_perso"] = templates
        sauver_config(cfg)


@app.get("/api/templates")
async def api_templates_list():
    cfg = charger_config()
    _seed_templates_defauts(cfg)
    return {"templates": cfg.get("templates_perso", [])}


@app.post("/api/templates")
async def api_templates_save(request: Request):
    data = await request.json()
    nom = (data.get("nom") or "").strip()
    objet = (data.get("objet") or "").strip()
    corps = (data.get("corps") or "").strip()
    categorie = (data.get("categorie") or "autre").strip()
    tpl_id = (data.get("id") or "").strip()
    if not nom or not objet or not corps:
        return JSONResponse({"ok": False, "error": "Nom, objet et corps requis"}, status_code=400)
    cfg = charger_config()
    templates = cfg.get("templates_perso", [])
    if tpl_id:
        found = False
        for t in templates:
            if t.get("id") == tpl_id:
                t["nom"] = nom; t["objet"] = objet; t["corps"] = corps; t["categorie"] = categorie; t["maj_le"] = maintenant_str()
                found = True; break
        if not found:
            return JSONResponse({"ok": False, "error": "Template introuvable"}, status_code=404)
    else:
        new_id = f"tpl_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        templates.append({"id": new_id, "nom": nom, "objet": objet, "corps": corps, "categorie": categorie, "cree_le": maintenant_str()})
        tpl_id = new_id
    cfg["templates_perso"] = templates
    sauver_config(cfg)
    return {"ok": True, "id": tpl_id}


@app.delete("/api/templates/{tpl_id}")
async def api_templates_delete(tpl_id: str):
    cfg = charger_config()
    templates = cfg.get("templates_perso", [])
    avant = len(templates)
    templates = [t for t in templates if t.get("id") != tpl_id]
    if len(templates) == avant:
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    cfg["templates_perso"] = templates
    sauver_config(cfg)
    return {"ok": True}


@app.post("/api/templates/{tpl_id}/duplicate")
async def api_templates_duplicate(tpl_id: str):
    cfg = charger_config()
    templates = cfg.get("templates_perso", [])
    src = next((t for t in templates if t.get("id") == tpl_id), None)
    if not src:
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    new_id = f"tpl_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    copie = {"id": new_id, "nom": f"{src['nom']} (copie)", "objet": src["objet"], "corps": src["corps"], "categorie": src.get("categorie", "autre"), "cree_le": maintenant_str()}
    templates.append(copie)
    cfg["templates_perso"] = templates
    sauver_config(cfg)
    return {"ok": True, "id": new_id}


# ============================================================
# IMAP / FILTRES
# ============================================================
from candimail.services.imap import _filtre_valide


def _seed_regles(cfg):
    seed_regles(cfg)


@app.post("/api/imap/check")
async def api_imap_check(request: Request):
    data = await request.json()
    try:
        jours = min(max(int(data.get("jours", 30)), 1), 365)
    except (TypeError, ValueError):
        jours = 30
    res = verifier_toutes_boites(jours=jours, uid=current_uid())
    return res


@app.get("/api/imap/status")
async def api_imap_status():
    cfg = charger_config()
    return {"derniere_verif": cfg["imap"].get("derniere_verif", 0), "auto_verif": cfg["imap"].get("auto_verif", True), "intervalle_min": cfg["imap"].get("intervalle_min", 30)}


@app.get("/api/filtres")
async def api_filtres_get():
    cfg = charger_config()
    _seed_regles(cfg)
    if "filtres_init" in cfg:
        sauver_config(cfg)
    return {"ok": True, "filtres": cfg.get("filtres_gmail", [])}


@app.post("/api/filtres")
async def api_filtres_add(request: Request):
    data = await request.json()
    cfg = charger_config()
    filtre = normaliser_regle(data)
    filtre["priority"] = len(cfg.get("filtres_gmail", [])) + 1
    if not _filtre_valide(filtre):
        return JSONResponse({"ok": False, "error": "Règle invalide (champ, valeur ou actions)"}, status_code=400)
    cfg.setdefault("filtres_gmail", []).append(filtre)
    sauver_config(cfg)
    return {"ok": True, "filtres": cfg["filtres_gmail"]}


@app.put("/api/filtres/{idx}")
@app.patch("/api/filtres/{idx}")
async def api_filtres_update(idx: int, request: Request):
    data = await request.json()
    cfg = charger_config()
    filtres = cfg.get("filtres_gmail", [])
    if not 0 <= idx < len(filtres):
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    data.pop("priority", None)
    data.pop("id", None)
    mise_a_jour = normaliser_regle(data, existante=filtres[idx])
    if not _filtre_valide(mise_a_jour):
        return JSONResponse({"ok": False, "error": "Règle invalide (champ, valeur ou actions)"}, status_code=400)
    filtres[idx] = mise_a_jour
    sauver_config(cfg)
    return {"ok": True, "filtres": filtres}


@app.post("/api/filtres/reorder")
async def api_filtres_reorder(request: Request):
    data = await request.json()
    ordre = data.get("ordre")
    if not isinstance(ordre, list):
        return JSONResponse({"ok": False, "error": "ordre requis"}, status_code=400)
    cfg = charger_config()
    filtres = cfg.get("filtres_gmail", [])
    par_id = {str(f.get("id")): f for f in filtres}
    if sorted(ordre) != sorted(par_id):
        return JSONResponse({"ok": False, "error": "Liste d'ids invalide"}, status_code=400)
    nouveaux = []
    for i, fid in enumerate(ordre, 1):
        f = par_id[str(fid)]
        f["priority"] = i
        nouveaux.append(f)
    cfg["filtres_gmail"] = nouveaux
    sauver_config(cfg)
    return {"ok": True, "filtres": nouveaux}


@app.post("/api/filtres/{idx}/toggle")
async def api_filtres_toggle(idx: int):
    cfg = charger_config()
    filtres = cfg.get("filtres_gmail", [])
    if not 0 <= idx < len(filtres):
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    filtres[idx]["enabled"] = not filtres[idx].get("enabled", True)
    sauver_config(cfg)
    return {"ok": True, "filtres": filtres}


@app.post("/api/filtres/corriger")
async def api_filtres_corriger(request: Request):
    data = await request.json()
    email = _txt(data.get("email")).strip().lower()
    label = _txt(data.get("label")).strip()
    if not email or "@" not in email or not label:
        return JSONResponse({"ok": False, "error": "Email et libellé requis"}, status_code=400)
    cfg = charger_config()
    apprentissage = appliquer_apprentissage(cfg, email, label, notifier=_txt(data.get("notify")).lower() in ("1", "true", "oui"))
    for e in cfg.get("apprentissage", {}).values():
        if e.get("derniere") is None:
            e["derniere"] = maintenant_str()
    sauver_config(cfg)
    suggestions = calculer_suggestions(cfg)
    return {"ok": True, "filtres": cfg["filtres_gmail"], "apprentissage": cfg["apprentissage"], "suggestions": suggestions}


@app.get("/api/filtres/suggestions")
async def api_filtres_suggestions():
    cfg = charger_config()
    return {"ok": True, "suggestions": calculer_suggestions(cfg), "apprentissage": cfg.get("apprentissage", {})}


@app.get("/api/notifications")
async def api_notifications_get(request: Request):
    cfg = charger_config()
    notifs = cfg.get("notifications", [])
    vues = session_get("notifs_vues", 0)
    return {"ok": True, "notifications": notifs[:20], "non_vues": max(0, len(notifs) - vues)}


@app.post("/api/notifications/vue")
async def api_notifications_vue(request: Request):
    cfg = charger_config()
    session_set("notifs_vues", len(cfg.get("notifications", [])))
    return {"ok": True}


@app.delete("/api/filtres/{idx}")
async def api_filtres_delete(idx: int):
    cfg = charger_config()
    filtres = cfg.get("filtres_gmail", [])
    if not 0 <= idx < len(filtres):
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    filtres.pop(idx)
    cfg["filtres_gmail"] = reindexer_priorites(filtres)
    sauver_config(cfg)
    return {"ok": True, "filtres": filtres}


@app.post("/api/filtres/creer-libelles")
async def api_filtres_creer_libelles():
    import imaplib
    cfg = charger_config()
    comptes = get_comptes_actifs()
    if not comptes:
        return JSONResponse({"ok": False, "error": "Aucun compte actif"}, status_code=400)
    libelles = sorted({(f.get("label") or "").strip() for f in cfg.get("filtres_gmail", []) if "label" in (f.get("actions") or []) and (f.get("label") or "").strip()})
    if not libelles:
        return JSONResponse({"ok": False, "error": "Aucune règle avec libellé"}, status_code=400)
    resultats = []
    for compte in comptes:
        mail = None
        crees = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=25)
            mail.login(compte["email"], crypto.dechiffrer(compte["password"]))
            for lbl in libelles:
                try:
                    status, _ = mail.select(_utf7(lbl))
                    if status == "OK":
                        continue
                except Exception:
                    pass
                if _creer_libelle(mail, lbl):
                    crees.append(lbl)
            resultats.append({"email": compte["email"], "ok": True, "crees": crees})
        except Exception as e:
            log_erreur("api_filtres_creer_libelles", e, str(compte.get("email", "")))
            resultats.append({"email": compte["email"], "ok": False, "erreur": erreur_publique(type_erreur="imap")[0]})
        finally:
            if mail:
                try: mail.logout()
                except Exception: pass
    return {"ok": True, "libelles": libelles, "resultats": resultats}


@app.post("/api/filtres/appliquer")
async def api_filtres_appliquer():
    cfg = charger_config()
    filtres = cfg.get("filtres_gmail", [])
    if not filtres:
        return JSONResponse({"ok": False, "error": "Aucune règle définie"}, status_code=400)
    comptes = get_comptes_actifs()
    if not comptes:
        return JSONResponse({"ok": False, "error": "Aucun compte actif"}, status_code=400)
    uid = current_uid()
    resultats = []
    for compte in comptes:
        resultats.extend(appliquer_filtres_compte(compte, filtres, uid=uid))
    return {"ok": True, "resultats": resultats}


def _utf7(s):
    out = bytearray()
    buf = []
    for ch in s:
        if 0x20 <= ord(ch) <= 0x7E:
            if buf:
                out += b"&" + base64.b64encode("".join(buf).encode("utf-16-be")).replace(b"/", b",").rstrip(b"=") + b"-"
                buf = []
            if ch == "&":
                out += b"&-"
            else:
                out += ch.encode("ascii")
        else:
            buf.append(ch)
    if buf:
        out += b"&" + base64.b64encode("".join(buf).encode("utf-16-be")).replace(b"/", b",").rstrip(b"=") + b"-"
    return out.decode("ascii")


def _creer_libelle(mail, lbl):
    try:
        typ, _ = mail._simple_command("CREATE", b'"' + _utf7(lbl).encode("ascii") + b'"')
        return typ == "OK"
    except Exception:
        return False


# ============================================================
# MARQUER RÉPONSE
# ============================================================
@app.post("/api/mark-response")
async def api_mark_response(request: Request):
    data = await request.json()
    company = (data.get("company") or "").strip()
    repondu = bool(data.get("repondu", True))

    def _maj(l):
        if company not in l:
            return False
        l[company]["repondu"] = repondu
        if repondu:
            l[company]["date_reponse"] = maintenant_str()
        else:
            l[company].pop("date_reponse", None)
        return True

    _, trouve = modifier_log(_maj)
    if not trouve:
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    return {"ok": True, "repondu": repondu}


# ============================================================
# ENVOI
# ============================================================
@app.get("/api/status")
async def api_status():
    log = charger_log()
    recharger_pieces()
    ok_rl, cnt, mx = check_rate_limit()
    return {"pieces_count": len(get_pieces_actives()), "sent_count": len([x for x in log.values() if x.get("envoye")]), "log": log, "rate_limit": {"utilises": cnt, "max": mx, "ok": ok_rl}, "comptes_actifs": len(get_comptes_actifs())}


@app.post("/api/preview")
async def api_preview(request: Request):
    data = await request.json()
    company = (data.get("company") or "").strip()
    context = (data.get("context") or "").strip()
    template = data.get("template") or charger_config()["parametres"]["template"]
    if not company:
        return JSONResponse({"ok": False, "error": "company requis"}, status_code=400)
    return {"ok": True, "subject": build_subject(template, company), "body": build_letter(template, company, context), "template": template}


@app.post("/api/send")
async def api_send(request: Request):
    if _profil_verrouille(current_uid()):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour envoyer des emails."}, status_code=403)
    data = await request.json()
    dest = (data.get("email") or "").strip()
    company = (data.get("company") or "").strip()
    subject = (data.get("subject") or "").strip()
    body = (data.get("body") or "").strip()
    pieces = data.get("pieces")
    mode_grp = bool(data.get("mode_groupe", False))
    if not dest or not company or not body:
        return JSONResponse({"ok": False, "error": "Champs manquants"}, status_code=400)
    if not get_comptes_actifs():
        return JSONResponse({"ok": False, "error": "Aucun compte Gmail actif"}, status_code=400)
    emails_dest = [e for e in parse_emails(dest) if _email_valide(e)]
    if not emails_dest:
        return JSONResponse({"ok": False, "error": "Aucun destinataire valide"}, status_code=400)
    ok_rl, cnt, mx = check_rate_limit()
    if not ok_rl:
        return JSONResponse({"ok": False, "error": f"Rate limit {cnt}/{mx}"}, status_code=429)
    with _send_lock:
        delay = get_delai()
        ecoule = time.time() - _last_send_time[0]
        if ecoule < delay:
            return JSONResponse({"ok": False, "error": f"Attends {int(delay-ecoule)+1}s", "attente": int(delay-ecoule)+1}, status_code=429)
        _last_send_time[0] = time.time()
    selected_idx = get_selected_compte_index()
    comptes_actifs = get_comptes_actifs()
    if selected_idx is not None and 0 <= selected_idx < len(comptes_actifs):
        compte = comptes_actifs[selected_idx]
    else:
        compte = compte_suivant()
    if compte and compte.get("template"):
        template_id = compte["template"]
        context = (data.get("context") or "").strip()
        subject = build_subject(template_id, company)
        body = build_letter(template_id, company, context)
    ok, msg = envoyer_email(dest, subject, body, pieces_selectionnees=pieces, mode_groupe=mode_grp, compte=compte)
    with _log_send_lock:
        _send_timestamps.append(time.time())
    if ok:
        emails_list = parse_emails(dest)
        log = charger_log()
        sans_pj = len(get_pieces_actives()) == 0 and not pieces
        log[company] = {"email": dest, "emails": emails_list, "envoye": True, "date": maintenant_str(), "compte": (compte or {}).get("email", ""), "repondu": False, "sans_pj": sans_pj, "groupe": mode_grp}
        sauver_log(log)
        return {"ok": True, "message": msg, "sans_pj": sans_pj, "nb_destinataires": len(emails_list)}
    log_erreur("api_send", Exception(msg), f"envoi vers {company} / compte={(compte or {}).get('email', '')}")
    return JSONResponse({"ok": False, "error": _MESSAGES_PUBLICS["smtp"]}, status_code=502)


def _bulk_worker(companies, template, owner_uid=0):
    log = charger_log(owner_uid)
    try:
        for i, c in enumerate(companies):
            if not _bulk_running[0]:
                break
            with _bulk_lock:
                _bulk_state[0]["index"] = i + 1
                _bulk_state[0]["derniere"] = c["name"]
            compte = compte_suivant()
            tpl = template
            if compte and compte.get("template"):
                tpl = compte["template"]
            delay = get_delai()
            with _send_lock:
                ecoule = time.time() - _last_send_time[0]
                if ecoule < delay:
                    time.sleep(delay - ecoule)
            ok_rl, cnt, mx = check_rate_limit()
            while not ok_rl and _bulk_running[0]:
                reste = 60
                if _send_timestamps:
                    reste = int(_send_timestamps[0] + 3600 - time.time()) + 5
                reste = max(5, min(reste, 300))
                with _bulk_lock:
                    _bulk_state[0]["derniere"] = f"{c['name']} — ⏳ attente rate limit {reste}s ({cnt}/{mx})"
                time.sleep(reste)
                ok_rl, cnt, mx = check_rate_limit()
            if not _bulk_running[0]:
                break
            try:
                sujet = build_subject(tpl, c["name"], owner_uid)
                corps = build_letter(tpl, c["name"], c.get("context", ""), owner_uid)
                ok, msg = envoyer_email(c["email"], sujet, corps, compte=compte, uid=owner_uid)
            except Exception as e:
                log_erreur("_bulk_worker", e, f"envoi vers {c['name']}")
                ok, msg = False, _MESSAGES_PUBLICS["smtp"]
            with _log_send_lock:
                _send_timestamps.append(time.time())
                _last_send_time[0] = time.time()
            sans_pj = len(get_pieces_actives(owner_uid)) == 0
            if ok:
                log[c["name"]] = {"email": c["email"], "envoye": True, "date": maintenant_str(), "repondu": False, "sans_pj": sans_pj, "compte": (compte or {}).get("email", ""), "template": tpl}
                with _bulk_lock: _bulk_state[0]["envoyes"] += 1
            else:
                log[c["name"]] = {"email": c["email"], "envoye": False, "date": maintenant_str(), "erreur": msg}
                with _bulk_lock: _bulk_state[0]["erreurs"] += 1
            sauver_log(log, owner_uid)
    except Exception as e:
        print(f"[BULK] {e}")
    finally:
        with _bulk_lock:
            _bulk_state[0]["en_cours"] = False
            _bulk_state[0]["arrete"] = not _bulk_running[0]
        _bulk_running[0] = False
        try: sauver_log(log, owner_uid)
        except Exception: pass


@app.post("/api/send-bulk")
async def api_send_bulk(request: Request):
    if _profil_verrouille(current_uid()):
        return JSONResponse({"ok": False, "error": "Le profil par défaut (#0) est un profil système — crée un vrai profil pour lancer des envois."}, status_code=403)
    with _bulk_lock:
        if _bulk_running[0]:
            return JSONResponse({"ok": False, "error": "Déjà en cours"}, status_code=409)
    data = await request.json()
    companies = data.get("companies") or []
    template = data.get("template") or charger_config()["parametres"]["template"]
    if not companies:
        return JSONResponse({"ok": False, "error": "Aucune entreprise"}, status_code=400)
    if not get_comptes_actifs():
        return JSONResponse({"ok": False, "error": "Aucun compte Gmail actif"}, status_code=400)
    cfg = charger_config()
    cfg["parametres"]["template"] = template
    sauver_config(cfg)
    _bulk_running[0] = True
    _bulk_state[0] = {"en_cours": True, "index": 0, "total": len(companies), "derniere": "", "envoyes": 0, "erreurs": 0, "arrete": False, "sans_pj": len(get_pieces_actives()) == 0}
    t = threading.Thread(target=_bulk_worker, args=(companies, template, current_uid()), daemon=True)
    t.start()
    return {"ok": True, "total": len(companies)}


@app.get("/api/send-bulk-status")
async def api_send_bulk_status():
    with _bulk_lock:
        return dict(_bulk_state[0])


@app.post("/api/send-bulk-stop")
async def api_send_bulk_stop():
    _bulk_running[0] = False
    with _bulk_lock:
        _bulk_state[0]["en_cours"] = False
        _bulk_state[0]["arrete"] = True
    return {"ok": True}


# ============================================================
# GROUPES
# ============================================================
@app.get("/api/groupes")
async def api_groupes_list():
    cfg = charger_config()
    return {"groupes": cfg.get("groupes", [])}


@app.post("/api/groupes")
async def api_groupes_add(request: Request):
    data = await request.json()
    nom = (data.get("nom") or "").strip()
    desc = (data.get("description") or "").strip()
    grp_id = (data.get("id") or "").strip()
    emails_raw = data.get("emails") or []
    if isinstance(emails_raw, str):
        emails = parse_emails(emails_raw)
    else:
        emails = [str(e).strip().lower() for e in emails_raw if str(e).strip()]
        emails = [e for e in emails if _email_valide(e)]
    if not nom:
        return JSONResponse({"ok": False, "error": "Nom requis"}, status_code=400)
    if not emails:
        return JSONResponse({"ok": False, "error": "Au moins un email valide requis"}, status_code=400)
    cfg = charger_config()
    groupes = cfg.get("groupes", [])
    if grp_id:
        for i, g in enumerate(groupes):
            if g["id"] == grp_id:
                groupes[i].update({"nom": nom, "emails": emails, "description": desc, "maj_le": maintenant_str()})
                cfg["groupes"] = groupes
                sauver_config(cfg)
                return {"ok": True, "updated": True, "id": grp_id}
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    new_id = f"grp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    groupes.append({"id": new_id, "nom": nom, "emails": emails, "description": desc, "cree_le": maintenant_str()})
    cfg["groupes"] = groupes
    sauver_config(cfg)
    return {"ok": True, "created": True, "id": new_id}


@app.delete("/api/groupes/{grp_id}")
async def api_groupes_delete(grp_id: str):
    cfg = charger_config()
    groupes = cfg.get("groupes", [])
    avant = len(groupes)
    groupes = [g for g in groupes if g["id"] != grp_id]
    if len(groupes) == avant:
        return JSONResponse({"ok": False, "error": "Introuvable"}, status_code=404)
    cfg["groupes"] = groupes
    sauver_config(cfg)
    return {"ok": True}


@app.post("/api/groupes/{grp_id}/send")
async def api_groupes_send(grp_id: str, request: Request):
    cfg = charger_config()
    groupes = cfg.get("groupes", [])
    grp = next((g for g in groupes if g["id"] == grp_id), None)
    if not grp:
        return JSONResponse({"ok": False, "error": "Groupe introuvable"}, status_code=404)
    data = await request.json()
    subject = (data.get("subject") or "").strip()
    body = (data.get("body") or "").strip()
    mode = (data.get("mode") or "individuel").lower()
    joindre = bool(data.get("joindre_pieces", False))
    if not subject or not body:
        return JSONResponse({"ok": False, "error": "Objet et corps requis"}, status_code=400)
    emails = grp.get("emails", [])
    if not emails:
        return JSONResponse({"ok": False, "error": "Groupe vide"}, status_code=400)
    if not get_comptes_actifs():
        return JSONResponse({"ok": False, "error": "Aucun compte Gmail actif"}, status_code=400)
    pieces = get_pieces_actives() if joindre else []
    nom_exp = cfg["candidat"]["nom"]
    params = cfg["parametres"]
    max_retries = params["smtp_retries"]
    with _send_lock:
        delay = get_delai()
        ecoule = time.time() - _last_send_time[0]
        if ecoule < delay:
            return JSONResponse({"ok": False, "error": f"Attends {int(delay-ecoule)+1}s", "attente": int(delay-ecoule)+1}, status_code=429)
        _last_send_time[0] = time.time()
    if mode == "groupe":
        ok, msg = _envoyer_un_email(", ".join(emails), subject, body, compte_suivant(), pieces, nom_exp, params, max_retries, groupe=emails, bcc_mode=True)
        nb_ok = len(emails) if ok else 0
    else:
        nb_ok = 0
        for idx_e, e in enumerate(emails):
            ok, msg = _envoyer_un_email(e, subject, body, compte_suivant(), pieces, nom_exp, params, max_retries)
            if ok: nb_ok += 1
            if idx_e < len(emails) - 1:
                time.sleep(delay)
    with _log_send_lock:
        _send_timestamps.append(time.time())
    log = charger_log()
    log[f"[GROUPE] {grp['nom']}"] = {"email": ", ".join(emails[:3]) + (f" +{len(emails)-3}" if len(emails) > 3 else ""), "emails": emails, "envoye": nb_ok > 0, "date": maintenant_str(), "repondu": False, "sans_pj": not joindre, "groupe_nom": grp["nom"], "nb_envoyes": nb_ok, "nb_total": len(emails), "mode": mode}
    sauver_log(log)
    return {"ok": nb_ok > 0, "envoyes": nb_ok, "total": len(emails), "message": f"{nb_ok}/{len(emails)} envoyé(s)"}


# ============================================================
# AGENT IA — configuration par tâche (fichier local)
# ============================================================
IA_CONFIG_FILE = DATA_DIR / "ia_config.json"


def _charger_config_ia_fichier() -> dict:
    try:
        if IA_CONFIG_FILE.exists():
            return json.loads(IA_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


@app.get("/api/ia/config")
async def api_ia_config():
    """Renvoie toutes les configs IA par tâche."""
    return _charger_config_ia_fichier()


@app.get("/api/ia/catalogue")
async def api_ia_catalogue():
    """Catalogue des fournisseurs/modèles IA supportés par le backend.
    Le front construit ses listes déroulantes à partir de ça — plus de
    divergence entre le front et le back."""
    return {
        "ok": True,
        "tasks": IA_TASKS,
        "providers": {
            "groq":       {"label": "Groq (gratuit)",       "models": list(GROQ_MODELS.keys())},
            "google":     {"label": "Google AI (gratuit)",  "models": list(GOOGLE_MODELS.keys())},
            "mistral":    {"label": "Mistral (gratuit)",    "models": list(MISTRAL_MODELS.keys())},
            "openrouter": {"label": "OpenRouter (tous les modèles gratuits)",
                           "models": list(_openrouter_models().keys())},
        },
    }


@app.post("/api/ia/config")
async def api_ia_config_save(request: Request):
    """Sauvegarde la config IA d'une tâche spécifique."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "error": "JSON invalide"}, status_code=400)
    try:
        IA_CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log_erreur("api_ia_config_save", e, "sauvegarde config IA")
        return JSONResponse({"ok": False, "error": "Impossible de sauvegarder"}, status_code=500)
    return {"ok": True}


# ============================================================
# EXPORTS / RESET / IMPORT
# ============================================================
@app.post("/api/reset-log")
async def api_reset_log():
    db.log_reset(backup_to=LOG_FILE_APP.with_suffix(".backup.json"), uid=current_uid())
    with _send_lock:
        _send_timestamps[:] = []
        _last_send_time[0] = 0.0
    return {"ok": True}


@app.get("/api/export-csv")
async def api_export_csv():
    log = charger_log()
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Entreprise", "Email", "Statut", "Réponse", "Bounce", "Sans PJ", "Date", "Erreur"])
    for company, info in sorted(log.items(), key=lambda x: x[1].get("date", ""), reverse=True):
        w.writerow([company, info.get("email", ""), "Envoyé" if info.get("envoye") else "Échec", "Oui" if info.get("repondu") else "Non", "Oui" if info.get("bounce") else "Non", "Oui" if info.get("sans_pj") else "Non", info.get("date", ""), info.get("erreur", "")])
    return Response(content=out.getvalue().encode("utf-8-sig"), media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="envois_%s.csv"' % datetime.now().strftime("%Y%m%d_%H%M")})


@app.get("/api/export-json")
async def api_export_json():
    INTERDITS = {"securite", "comptes", "admin", "mots_de_passe"}
    try:
        _, texte = export_sans_secrets(charger_config(), charger_log)
    except RuntimeError:
        log_erreur("export_json", RuntimeError("secret dans l'export"), "export contenait un secret chiffré")
        cfg = {k: v for k, v in charger_config().items() if k not in INTERDITS and k.lower() not in INTERDITS}
        texte = json.dumps({"export_le": datetime.now().isoformat(), "config": cfg, "log": charger_log()}, ensure_ascii=False, indent=2)
    return Response(content=texte.encode("utf-8"), media_type="application/json", headers={"Content-Disposition": 'attachment; filename="backup_%s.json"' % datetime.now().strftime("%Y%m%d_%H%M")})


@app.post("/api/import-json")
async def api_import_json(request: Request):
    form = await request.form()
    if "file" not in form:
        return JSONResponse({"ok": False, "error": "Aucun fichier"}, status_code=400)
    f = form["file"]
    try:
        data = json.loads(await f.read())
    except Exception:
        log_erreur("api_import_json", None, "import de la sauvegarde")
        return JSONResponse({"ok": False, "error": "Fichier JSON invalide ou illisible"}, status_code=400)
    imported = data.get("log") or data
    if not isinstance(imported, dict):
        return JSONResponse({"ok": False, "error": "Structure invalide"}, status_code=400)
    imported = {str(k): v for k, v in imported.items() if isinstance(v, dict)}
    avant = len(charger_log())
    log, _ = modifier_log(lambda l: l.update(imported))
    return {"ok": True, "importees": len(imported), "total_avant": avant, "total_apres": len(log)}


@app.get("/api/export-excel")
async def api_export_excel():
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
    except ImportError:
        return JSONResponse({"ok": False, "error": "openpyxl requis : pip install openpyxl"}, status_code=500)
    log = charger_log()
    cfg = charger_config()
    wb = Workbook()
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill("solid", fgColor="2563EB")
    center = Alignment(horizontal="center", vertical="center")
    ws1 = wb.active
    ws1.title = "Envois"
    headers = ["Entreprise", "Email", "Statut", "Réponse", "Bounce", "Sans PJ", "Date envoi", "Date réponse", "Erreur"]
    ws1.append(headers)
    for col in range(1, len(headers) + 1):
        c = ws1.cell(row=1, column=col)
        c.font = header_font; c.fill = header_fill; c.alignment = center
    for company, info in sorted(log.items(), key=lambda x: x[1].get("date", ""), reverse=True):
        ws1.append([company, info.get("email", ""), "Envoyé" if info.get("envoye") else "Échec", "Oui" if info.get("repondu") else "Non", "Oui" if info.get("bounce") else "Non", "Oui" if info.get("sans_pj") else "Non", info.get("date", ""), info.get("date_reponse", ""), info.get("erreur", "")])
    widths = [30, 35, 12, 12, 12, 12, 18, 18, 40]
    for i, w in enumerate(widths, 1):
        ws1.column_dimensions[get_column_letter(i)].width = w
    ws2 = wb.create_sheet("Statistiques")
    total = len(log)
    envoyes = len([x for x in log.values() if x.get("envoye")])
    repondus = len([x for x in log.values() if x.get("repondu")])
    bounces = len([x for x in log.values() if x.get("bounce")])
    echecs = total - envoyes
    ws2.append(["Statistique", "Valeur"])
    for col in (1, 2):
        c = ws2.cell(row=1, column=col)
        c.font = header_font; c.fill = header_fill; c.alignment = center
    ws2.append(["Total entreprises contactées", total])
    ws2.append(["Emails envoyés avec succès", envoyes])
    ws2.append(["Échecs d'envoi", echecs])
    ws2.append(["Réponses reçues", repondus])
    ws2.append(["Bounces (emails invalides)", bounces])
    ws2.append(["Taux de réponse (%)", round(100 * repondus / envoyes, 1) if envoyes else 0])
    ws2.column_dimensions["A"].width = 32
    ws2.column_dimensions["B"].width = 15
    ws3 = wb.create_sheet("Candidat")
    ws3.append(["Champ", "Valeur"])
    for col in (1, 2):
        c = ws3.cell(row=1, column=col)
        c.font = header_font; c.fill = header_fill; c.alignment = center
    for k, v in cfg["candidat"].items():
        ws3.append([k.capitalize(), v])
    ws3.append(["Template", cfg["parametres"]["template"]])
    ws3.append(["Délai", f"{get_delai()}s"])
    ws3.append(["Export", datetime.now().strftime("%Y-%m-%d %H:%M")])
    ws3.column_dimensions["A"].width = 22
    ws3.column_dimensions["B"].width = 45
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return Response(content=output.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": 'attachment; filename="candimail_%s.xlsx"' % datetime.now().strftime('%Y%m%d_%H%M')})


# ============================================================
# AGENT IA — CHAT (conversation en langage naturel)
# ============================================================
def _lire_emails_recents(uid: int, limite: int = 15) -> list[dict]:
    """Lit les emails récents des boîtes actives (sujets + expéditeurs).
    Utilisé par l'agent IA pour résumer / classer le courrier."""
    comptes = get_comptes_actifs()
    if not comptes:
        return []
    import email as _email_mod
    from email.header import decode_header as _dh
    from email.utils import parseaddr as _parseaddr

    def _dec(raw):
        try:
            parts = _dh(raw or "")
            return " ".join(
                c.decode(cs or "utf-8", errors="ignore") if isinstance(c, bytes) else c
                for c, cs in parts)
        except Exception:
            return str(raw)

    emails = []
    for compte in comptes:
        mail = None
        try:
            mail = _gimap_ouvre(compte)
            mail.select("INBOX")
            status, msgs = mail.search(None, "(ALL)")
            if status != "OK" or not msgs[0]:
                continue
            nums = msgs[0].split()[-limite:]
            for num in reversed(nums):
                st, data = mail.fetch(num, "(BODY.PEEK[HEADER])")
                if st != "OK" or not data or not data[0]:
                    continue
                msg = _email_mod.message_from_bytes(data[0][1])
                emails.append({
                    "compte": compte.get("email", ""),
                    "de": _parseaddr(msg.get("From", ""))[1],
                    "sujet": _dec(msg.get("Subject", ""))[:200],
                    "date": msg.get("Date", "")[:40],
                })
        except Exception as e:
            log_erreur("_lire_emails_recents", e, compte.get("email", ""))
        finally:
            if mail:
                try: mail.logout()
                except Exception: pass
    return emails[:limite]


async def _ia_chat_repondre(message: str, uid: int) -> str:
    """Cerveau du chat : détecte l'intention, exécute l'action réelle
    correspondante, puis formule la réponse avec le LLM."""
    from candimail.services.ia_agent import IAAgentError
    msg = (message or "").strip()
    bas = msg.lower()

    # ---- Actions réelles détectées par mots-clés -------------------------
    contexte = ""
    intention = "conversation"

    if any(k in bas for k in ("résume", "resume", "résumé", "dernier", "recu", "reçus",
                              "boîte", "inbox", "mails", "emails")) \
            and any(k in bas for k in ("email", "mail", "courrier", "boîte", "reçu")):
        intention = "resumer_emails"
        emails = _lire_emails_recents(uid)
        if not emails:
            return "Aucun compte Gmail actif ou boîte vide — ajoute un compte dans la page Comptes & pièces."
        liste = "\n".join(f"- [{e['date']}] {e['de']} : {e['sujet']}" for e in emails)
        contexte = f"Voici les derniers emails reçus ({len(emails)}) :\n{liste}\n\n"
        intention = "resumer_emails"

    elif "classe" in bas or "ranger" in bas or "classer" in bas or "courrier" in bas:
        intention = "classer"
        cfg = charger_config(uid)
        filtres = cfg.get("filtres_gmail", [])
        comptes = get_comptes_actifs()
        if not filtres:
            return ("Il n'y a encore aucune règle de classement. Crée des règles dans la page "
                    "« Réponses & filtres » puis je pourrai les appliquer sur ta boîte.")
        if not comptes:
            return "Aucun compte Gmail actif — ajoute un compte d'abord."
        resultats = []
        for c in comptes:
            resultats.extend(appliquer_filtres_compte(c, filtres, uid=uid))
        n = sum(r.get("trouves", 0) for r in resultats if r.get("ok"))
        regles_ok = [r.get("regle") for r in resultats if r.get("ok") and r.get("trouves")]
        return (f"Classement terminé : {n} email(s) traité(s).\n" +
                ("Règles actives : " + ", ".join(regles_ok) if regles_ok
                 else "Aucune règle n'a trouvé de mail à classer."))

    elif bas.startswith("écris") or bas.startswith("ecris") or "rédige" in bas or "redige" in bas \
            or ("mail" in bas and ("à " in bas or "a " in bas or "pour " in bas)):
        intention = "rediger"
        cfg = charger_config(uid)
        cand = cfg.get("candidat", {})
        contexte = (f"Profil du candidat : nom={cand.get('nom')}, email={cand.get('email')}, "
                    f"ville={cand.get('ville')}, diplome={cand.get('diplome')}, spécialité={cand.get('spec')}.\n")

    # ---- Appel du LLM avec le contexte collecté --------------------------
    cfg_ia = _ia_agent.get_config("rediger")
    if not cfg_ia.api_key:
        # Pas de clé : l'agent ne peut pas répondre par IA.
        # On donne quand même une réponse utile selon l'intention.
        if intention == "resumer_emails":
            return ("Clé API IA manquante (page Agent IA) — je ne peux pas rédiger un résumé "
                    "intelligent, mais voici les derniers emails bruts :\n" + contexte)
        return ("Pour me faire parler, configure une clé API dans la page 🤖 Agent IA "
                "(Groq, Google, Mistral ou OpenRouter — gratuits).")

    system = (
        "Tu es l'assistant intégré de Candimail, une application de suivi de candidatures "
        "par email. Tu réponds en français, de façon concise et actionnable. "
        "Tu peux : résumer des emails, aider à classer le courrier, rédiger des mails "
        "professionnels (candidatures, relances), conseiller sur la stratégie de candidature."
    )
    if contexte:
        system += "\n\n" + contexte
    try:
        resp = await _ia_agent.chat("rediger", [
            {"role": "system", "content": system},
            {"role": "user", "content": msg},
        ])
        return resp.text
    except IAAgentError as e:
        return f"Erreur IA : {e}"


@app.post("/api/ia/chat")
async def api_ia_chat(request: Request):
    """Panneau de conversation IA : l'utilisateur demande en langage naturel
    (résumer les derniers mails, classer, rédiger à X…), le backend détecte
    l'intention, exécute l'action réelle si nécessaire puis répond via le LLM."""
    uid = current_uid()
    if _profil_verrouille(uid):
        return JSONResponse({"ok": False, "error": "Le profil système (#0) n'a pas d'agent IA — crée un vrai profil."}, status_code=403)
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"ok": False, "error": "JSON invalide"}, status_code=400)
    message = (data.get("message") or "").strip()
    if not message:
        return JSONResponse({"ok": False, "error": "Message vide"}, status_code=400)
    reponse = await _ia_chat_repondre(message, uid)
    return {"ok": True, "reponse": reponse}


def lancer_serveur(app_instance, port, host=None):
    """Lance uvicorn.
    Host : CANDIMAIL_HOST (ex. 0.0.0.0 pour accès depuis tout le réseau local)
    sinon 127.0.0.1 (usage local uniquement)."""
    import uvicorn
    host = host or os.environ.get("CANDIMAIL_HOST", "127.0.0.1")
    uvicorn.run(app_instance, host=host, port=port, log_level="warning")
