#!/usr/bin/env python3
"""Routes Flask — authentification et sécurité d'accès (blueprint)."""
import io, csv, json, os, re, socket, time, threading, uuid
from datetime import datetime, timedelta
from pathlib import Path

from flask import (Blueprint, jsonify, request, render_template, Response,
                   send_file, session, redirect)

from candimail.core import db, crypto
from candimail.core.config import (BASE_DIR, UPLOADS_DIR, CONFIG_FILE, LOG_FILE,
                        DEFAULT_CONFIG, DEFAULT_CV, TEMPLATES)
from candimail.core.noyau import (current_uid, charger_config, sauver_config, _config_globale,
                   charger_log, sauver_log, get_delai, check_rate_limit,
                   maintenant_str, parse_emails, get_comptes_actifs,
                   compte_suivant, _get_template, build_letter, build_subject,
                   get_pieces_actives, recharger_pieces, _pieces,
                   _config_lock, _config_cache, _log_lock, _send_lock,
                   _log_send_lock, _bulk_lock, _bulk_running, _bulk_state,
                   _compte_index, _auth_attempts, _send_timestamps,
                   _last_send_time, _txt, _email_valide)
from candimail.services.smtp import envoyer_email, _envoyer_un_email
from candimail.services.imap import (check_imap_compte, verifier_toutes_boites,
                          appliquer_filtres_compte, _filtre_valide,
                          _ACTIONS_VALIDES)

bp = Blueprint("auth", __name__)

# ============================================================
# MODE SANS AUTHENTIFICATION (dev / usage local mono-utilisateur)
# Passer AUTH_DESACTIVEE à False pour réactiver la connexion.
# ============================================================
AUTH_DESACTIVEE = True
AUTH_UID_AUTO = 1
AUTH_EMAIL_AUTO = "battiment64@gmail.com"


@bp.route("/api/auth/status", methods=["GET"])
def api_auth_status():
    if AUTH_DESACTIVEE:
        return jsonify({
            "setup_necessaire": False,
            "connecte": True,
            "email": AUTH_EMAIL_AUTO,
            "crypto_actif": crypto.DISPONIBLE,
            "auth_desactivee": True,
        })
    return jsonify({
        "setup_necessaire": db.users_count() == 0,
        "connecte": bool(session.get("uid")),
        "email": session.get("uemail", ""),
        "crypto_actif": crypto.DISPONIBLE,
    })

def _creer_utilisateur_et_connecter(email, mdp):
    premier = db.users_count() == 0
    uid = db.users_create(email, crypto.hash_mdp(mdp))
    if uid is None:
        return None
    # Le premier compte récupère les données legacy (avant multi-utilisateurs)
    if premier and db.migrate_legacy_user(uid):
        print(f"[AUTH] Données legacy transférées à l'utilisateur {uid} ({email})")
    session.clear()
    session["uid"] = uid
    session["uemail"] = email.lower().strip()
    return uid

def _auth_rate_limit(maxi=10, fenetre=300):
    # Anti-spam / anti-bruteforce : max N tentatives auth par IP / fenêtre
    ip = request.remote_addr or "?"
    now = time.time()
    hist = [t for t in _auth_attempts.get(ip, []) if t > now - fenetre]
    if len(hist) >= maxi:
        _auth_attempts[ip] = hist
        return False
    hist.append(now)
    _auth_attempts[ip] = hist
    return True


@bp.route("/api/auth/register", methods=["POST"])
def api_auth_register():
    data = request.get_json() or {}
    # Anti-spam : champ caché (honeypot) rempli par les robots → on rejette
    if _txt(data.get("website")).strip():
        return jsonify({"ok": False, "error": "Requête refusée"}), 400
    if not _auth_rate_limit():
        return jsonify({"ok": False,
                        "error": "Trop de tentatives, réessaie plus tard"}), 429
    email = _txt(data.get("email")).strip().lower()
    mdp   = _txt(data.get("password")).strip()
    if not _email_valide(email):
        return jsonify({"ok": False, "error": "Email invalide"}), 400
    if len(mdp) < 6:
        return jsonify({"ok": False,
                        "error": "Mot de passe : 6 caractères minimum"}), 400
    if db.users_get_by_email(email):
        return jsonify({"ok": False, "error": "Email déjà utilisé — connecte-toi"}), 409
    uid = _creer_utilisateur_et_connecter(email, mdp)
    if uid is None:
        return jsonify({"ok": False, "error": "Création impossible"}), 500
    return jsonify({"ok": True, "uid": uid, "email": email})

# Alias historique du premier écran : création = inscription
@bp.route("/api/auth/setup", methods=["POST"])
def api_auth_setup():
    return api_auth_register()

@bp.route("/api/auth/login", methods=["POST"])
def api_auth_login():
    if AUTH_DESACTIVEE:
        return jsonify({"ok": True, "uid": AUTH_UID_AUTO,
                        "email": AUTH_EMAIL_AUTO,
                        "info": "authentification désactivée"})
    if not _auth_rate_limit(maxi=15, fenetre=300):
        return jsonify({"ok": False,
                        "error": "Trop de tentatives, réessaie plus tard"}), 429
    data = request.get_json() or {}
    email = _txt(data.get("email")).strip().lower()
    mdp   = _txt(data.get("password")).strip()
    u = db.users_get_by_email(email)
    if not u or not crypto.verifier_mdp(mdp, u["pass_hash"]):
        return jsonify({"ok": False, "error": "Email ou mot de passe incorrect"}), 403
    session.clear()
    session["uid"] = u["id"]
    session["uemail"] = u["email"]
    return jsonify({"ok": True, "uid": u["id"], "email": u["email"]})

@bp.route("/api/auth/logout", methods=["POST"])
def api_auth_logout():
    session.clear()
    return jsonify({"ok": True})

@bp.route("/api/auth/change", methods=["POST"])
def api_auth_change():
    if AUTH_DESACTIVEE:
        return jsonify({"ok": False,
                        "error": "Authentification désactivée — rien à modifier"}), 400
    data = request.get_json() or {}
    ancien  = _txt(data.get("ancien")).strip()
    nouveau = _txt(data.get("nouveau")).strip()
    if len(nouveau) < 6:
        return jsonify({"ok": False,
                        "error": "Nouveau mot de passe : 6 caractères minimum"}), 400
    u = db.users_get(session.get("uid", 0))
    if not u or not crypto.verifier_mdp(ancien, u["pass_hash"]):
        return jsonify({"ok": False, "error": "Mot de passe actuel incorrect"}), 403
    with db._lock:
        conn = db._connect()
        try:
            conn.execute("UPDATE users SET pass_hash=? WHERE id=?",
                         (crypto.hash_mdp(nouveau), u["id"]))
            conn.commit()
        finally:
            conn.close()
    return jsonify({"ok": True})

@bp.before_app_request
def _gardien_acces():
    # ----------------------------------------------------------------
    # AUTHENTIFICATION DÉSACTIVÉE : on connecte automatiquement
    # l'utilisateur 1 sur chaque requête. Pour réactiver : passer
    # AUTH_DESACTIVEE = False plus haut dans ce fichier.
    # ----------------------------------------------------------------
    if AUTH_DESACTIVEE:
        if not session.get("uid"):
            session["uid"] = AUTH_UID_AUTO
            session["uemail"] = AUTH_EMAIL_AUTO
        return None
    p = request.path
    if (p == "/" or p.startswith("/static") or p == "/favicon.ico"
            or p in ("/login", "/rgpd", "/cgu", "/robots.txt", "/sitemap.xml")):
        return None
    if p.startswith("/api/auth/"):
        return None
    if not session.get("uid"):
        if p.startswith("/api/"):
            return jsonify({"ok": False, "error": "Session expirée"}), 401
        return redirect("/login")
    return None

