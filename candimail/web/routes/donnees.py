#!/usr/bin/env python3
"""Routes Flask — CV, entreprises, configuration, comptes, pièces jointes (blueprint)."""
import json, smtplib, ssl, time
from pathlib import Path

from flask import Blueprint, jsonify, request

from candimail.core import db, crypto
from candimail.core.config import UPLOADS_DIR, DEFAULT_CV, TEMPLATES
from candimail.core.noyau import current_uid, charger_config, sauver_config, _config_globale, charger_log, sauver_log, recharger_pieces, _pieces

bp = Blueprint("donnees", __name__)


# ------------------------------------------------------------
# CV
# ------------------------------------------------------------
@bp.route("/api/cv", methods=["GET"])
def api_cv_get():
    return jsonify({"ok": True, "cv": charger_cv()})

@bp.route("/api/cv", methods=["POST"])
def api_cv_save():
    data = request.get_json() or {}
    cv = data.get("cv")
    if not isinstance(cv, dict):
        return jsonify({"ok": False, "error": "Données CV invalides"}), 400
    nettoye = _nettoyer_cv(cv)
    db.cv_set(nettoye, current_uid())
    return jsonify({"ok": True})

def _nettoyer_cv(cv):
    out = {}
    for k in ("titre", "resume", "nom", "ville"):
        out[k] = str(cv.get(k) or "")
    for liste in ("experiences", "formations", "references"):
        items = []
        for it in cv.get(liste) or []:
            if isinstance(it, dict):
                items.append({
                    "date": str(it.get("date") or ""),
                    "titre": str(it.get("titre") or ""),
                    "lieu": str(it.get("lieu") or ""),
                    "description": str(it.get("description") or ""),
                })
        out[liste] = items
    for liste in ("competences", "langues"):
        out[liste] = [str(x) for x in (cv.get(liste) or []) if str(x).strip()]
    return out

def charger_cv():
    data = db.cv_get(current_uid())
    if not isinstance(data, dict):
        return json.loads(json.dumps(DEFAULT_CV))
    base = json.loads(json.dumps(DEFAULT_CV))
    base.update(data)
    return base

# ------------------------------------------------------------
# ENTREPRISES
# ------------------------------------------------------------
@bp.route("/api/companies", methods=["GET"])
def api_companies_get():
    return jsonify({"ok": True, "companies": db.companies_get(current_uid())})

@bp.route("/api/companies", methods=["POST"])
def api_companies_add():
    data = request.get_json() or {}
    name    = (data.get("name") or "").strip()
    email   = (data.get("email") or "").strip()
    cat     = (data.get("cat") or "pme").strip()
    context = (data.get("context") or "").strip()
    if not name or not email or "@" not in email:
        return jsonify({"ok": False, "error": "Nom et email valides requis"}), 400
    if cat not in ("grands", "pme", "port"):
        cat = "pme"
    db.companies_add({
        "name": name, "cat": cat, "email": email,
        "context": context, "custom": True,
    }, current_uid())
    return jsonify({"ok": True})

@bp.route("/api/companies/<path:name>", methods=["DELETE"])
def api_companies_delete(name):
    db.companies_delete(name, current_uid())
    return jsonify({"ok": True})

@bp.route("/api/companies/<path:name>", methods=["PUT"])
def api_companies_update(name):
    """Modifie une entreprise : nom (renommage), email, cat, context."""
    data = request.get_json() or {}
    new_name = (data.get("name") or name).strip()
    email    = (data.get("email") or "").strip()
    cat      = (data.get("cat") or "pme").strip()
    context  = (data.get("context") or "").strip()
    if not new_name or not email or "@" not in email:
        return jsonify({"ok": False, "error": "Nom et email valides requis"}), 400
    if cat not in ("grands", "pme", "port"):
        cat = "pme"

    companies = db.companies_get(current_uid())
    idx = next((i for i, c in enumerate(companies) if c["name"] == name), -1)
    if idx < 0:
        return jsonify({"ok": False, "error": "Entreprise introuvable"}), 404
    # Renommage : éviter un doublon avec une autre entreprise
    if new_name != name and any(c["name"] == new_name for c in companies):
        return jsonify({"ok": False, "error": "Une autre entreprise porte déjà ce nom"}), 400
    companies[idx] = {
        "name": new_name, "cat": cat, "email": email,
        "context": context,
        "custom": companies[idx].get("custom", True),
    }
    db.companies_replace(companies, current_uid())

    # Renommage : déplacer l'entrée du journal pour conserver l'historique
    if new_name != name:
        log = charger_log()
        if name in log:
            log[new_name] = log.pop(name)
            sauver_log(log)

    return jsonify({"ok": True})

@bp.route("/api/companies/seed", methods=["POST"])
def api_companies_seed():
    data = request.get_json() or {}
    companies = data.get("companies") or []
    if not isinstance(companies, list) or not companies:
        return jsonify({"ok": False, "error": "Liste invalide"}), 400
    existing = {c["name"] for c in db.companies_get(current_uid())}
    added = 0
    for c in companies:
        name = (c.get("name") or "").strip()
        if not name or name in existing:
            continue
        db.companies_add({
            "name": name,
            "cat": c.get("cat") if c.get("cat") in ("grands", "pme", "port") else "pme",
            "email": c.get("email") or "",
            "context": c.get("context") or "",
            "custom": bool(c.get("custom")),
        }, current_uid())
        existing.add(name)
        added += 1
    return jsonify({"ok": True, "added": added})

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
@bp.route("/api/config", methods=["GET"])
def api_config_get():
    cfg = charger_config()
    safe = json.loads(json.dumps(cfg))
    # Ne jamais exposer la section sécurité (hash + secret de session)
    safe.pop("securite", None)
    # Les comptes Gmail sont stockés dans la config GLOBALE (uid 0) mais
    # charger_config() lit la config de l'utilisateur courant → comptes absents.
    # On expose toujours les comptes globaux (masqués).
    safe["comptes"] = json.loads(json.dumps(_config_globale().get("comptes", [])))
    for i, c in enumerate(safe.get("comptes", [])):
        c["index"] = i   # requis par le front (toggle / delete / reveal)
        if c.get("password"):
            c["password"] = "••••••••"
            c["has_password"] = True
        else:
            c["has_password"] = False

    # Fusion templates
    tous = {}
    for k, v in TEMPLATES.items():
        tous[k] = {"nom": v["nom"], "predefini": True, "categorie": "predefini"}
    for t in cfg.get("templates_perso", []):
        tous[t["id"]] = {
            "nom":       t["nom"],
            "categorie": t.get("categorie", "autre"),
            "predefini": False,
        }
    safe["templates_dispo"] = tous
    return jsonify(safe)

@bp.route("/api/config", methods=["POST"])
def api_config_update():
    data = request.get_json() or {}
    cfg = charger_config()

    if "candidat" in data:
        for k, v in data["candidat"].items():
            if k in cfg["candidat"]:
                cfg["candidat"][k] = str(v).strip()

    if "parametres" in data:
        for k, v in data["parametres"].items():
            if k not in cfg["parametres"]:
                continue
            if k in ("delai_secondes", "max_par_heure", "smtp_timeout",
                     "smtp_retries", "delai_min", "delai_max"):
                try: cfg["parametres"][k] = int(v)
                except (TypeError, ValueError): pass
            elif k == "delai_aleatoire":
                cfg["parametres"][k] = bool(v)
            else:
                cfg["parametres"][k] = str(v)

    sauver_config(cfg)
    return jsonify({"ok": True})

# ------------------------------------------------------------
# COMPTES
# ------------------------------------------------------------
@bp.route("/api/comptes", methods=["GET"])
def api_comptes_list():
    cfg = _config_globale()
    safe = []
    for i, c in enumerate(cfg.get("comptes", [])):
        safe.append({
            "index":        i,
            "email":        c.get("email", ""),
            "actif":        bool(c.get("actif", True)),
            "has_password": bool(c.get("password")),
            "template":     c.get("template", "") or "",
        })
    return jsonify({"comptes": safe})

@bp.route("/api/comptes", methods=["POST"])
def api_comptes_add():
    data = request.get_json() or {}
    email    = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    template = (data.get("template") or "").strip()
    if not email or not password or "@" not in email:
        return jsonify({"ok": False, "error": "Email ou mot de passe invalide"}), 400

    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    for c in comptes:
        if str(c.get("email", "")).lower() == email.lower():
            c["password"] = crypto.chiffrer(password)
            c["actif"] = True
            c["template"] = template
            sauver_config(cfg, 0)
            return jsonify({"ok": True, "updated": True})
    comptes.append({"email": email, "password": crypto.chiffrer(password),
                    "actif": True, "template": template})
    cfg["comptes"] = comptes
    sauver_config(cfg, 0)
    return jsonify({"ok": True, "created": True})

@bp.route("/api/comptes/<int:idx>", methods=["DELETE"])
def api_comptes_delete(idx):
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return jsonify({"ok": False, "error": "Index invalide"}), 404
    comptes.pop(idx)
    cfg["comptes"] = comptes
    sauver_config(cfg, 0)
    return jsonify({"ok": True})

@bp.route("/api/comptes/<int:idx>/template", methods=["POST"])
def api_comptes_template(idx):
    """Définit le template propre d'un compte ('' = template global)."""
    data = request.get_json() or {}
    template = (data.get("template") or "").strip()
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return jsonify({"ok": False, "error": "Index invalide"}), 404
    comptes[idx]["template"] = template
    sauver_config(cfg, 0)
    return jsonify({"ok": True, "template": template})

@bp.route("/api/comptes/<int:idx>/toggle", methods=["POST"])
def api_comptes_toggle(idx):
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return jsonify({"ok": False, "error": "Index invalide"}), 404
    comptes[idx]["actif"] = not comptes[idx].get("actif", True)
    sauver_config(cfg, 0)
    return jsonify({"ok": True, "actif": comptes[idx]["actif"]})

@bp.route("/api/comptes/<int:idx>/reveal", methods=["POST"])
def api_comptes_reveal(idx):
    """Affiche le mot de passe d'application (16 caractères) d'un compte.
    Utilisé uniquement pour vérifier visuellement les identifiants."""
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if idx < 0 or idx >= len(comptes):
        return jsonify({"ok": False, "error": "Index invalide"}), 404
    c = comptes[idx]
    if not c.get("password"):
        return jsonify({"ok": False, "error": "Aucun mot de passe enregistré"}), 400
    try:
        mdp = crypto.dechiffrer(c["password"])
    except Exception as e:
        return jsonify({"ok": False,
                        "error": f"Déchiffrement impossible : {type(e).__name__}"}), 500
    return jsonify({
        "ok": True,
        "email": c.get("email", ""),
        "password": mdp,
        "longueur": len(mdp),
        "actif": bool(c.get("actif", True)),
    })

@bp.route("/api/comptes/test", methods=["POST"])
def api_comptes_test():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    if not password:
        cfg = _config_globale()
        for c in cfg.get("comptes", []):
            if str(c.get("email", "")).lower() == email.lower():
                password = crypto.dechiffrer(c["password"])
                break
        if not password:
            return jsonify({"ok": False, "error": "Compte introuvable"}), 404
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=15) as srv:
            srv.login(email, password)
        return jsonify({"ok": True, "message": f"✅ SMTP OK pour {email}"})
    except smtplib.SMTPAuthenticationError:
        return jsonify({"ok": False, "error": "❌ Auth refusée — vérifie le mot de passe"}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"Erreur : {type(e).__name__}"}), 500

# ------------------------------------------------------------
# PIÈCES JOINTES
# ------------------------------------------------------------
@bp.route("/api/pieces", methods=["GET"])
def api_pieces_list():
    u = current_uid()
    recharger_pieces(u)
    pieces = []
    for k, p in _pieces.get(int(u or 0), {}).items():
        pieces.append({
            "id":           k,
            "nom_original": p.get("nom_original", k),
            "actif":        p.get("actif", True),
            "taille_kb":    Path(p["chemin"]).stat().st_size // 1024
                            if Path(p["chemin"]).exists() else 0,
        })
    return jsonify({"pieces": pieces})

@bp.route("/api/pieces", methods=["POST"])
def api_pieces_add():
    if "fichier" not in request.files:
        return jsonify({"ok": False, "error": "Aucun fichier"}), 400
    f = request.files["fichier"]
    if not f.filename or not f.filename.lower().endswith(".pdf"):
        return jsonify({"ok": False, "error": "PDF requis"}), 400

    uid = current_uid()
    safe_name = f"u{uid}_{int(time.time()*1000)}_{f.filename}"
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._-")
    path = UPLOADS_DIR / safe_name
    f.save(str(path))

    cfg = charger_config()
    cfg.setdefault("pieces_jointes", {})[safe_name] = {
        "nom_original": f.filename,
        "actif":        True,
    }
    sauver_config(cfg)
    recharger_pieces()
    return jsonify({"ok": True, "id": safe_name})

@bp.route("/api/pieces/<piece_id>", methods=["DELETE"])
def api_pieces_delete(piece_id):
    try:
        path = UPLOADS_DIR / piece_id
        if path.exists():
            path.unlink()
        cfg = charger_config()
        cfg.get("pieces_jointes", {}).pop(piece_id, None)
        sauver_config(cfg)
        recharger_pieces()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@bp.route("/api/pieces/<piece_id>/toggle", methods=["POST"])
def api_pieces_toggle(piece_id):
    cfg = charger_config()
    pj = cfg.get("pieces_jointes", {})
    if piece_id not in pj:
        return jsonify({"ok": False, "error": "Introuvable"}), 404
    pj[piece_id]["actif"] = not pj[piece_id].get("actif", True)
    sauver_config(cfg)
    recharger_pieces()
    return jsonify({"ok": True, "actif": pj[piece_id]["actif"]})
