#!/usr/bin/env python3
"""
Noyau applicatif — verrous, état partagé et logique de gestion :
config par utilisateur, journal d'envois, quotas/délais, comptes Gmail,
templates, pièces jointes, validation d'emails.
"""
import json, random, re, threading, time
from datetime import datetime
from pathlib import Path

from flask import session

from candimail.core import db
from candimail.core.config import UPLOADS_DIR, DEFAULT_CONFIG, TEMPLATES


# ============================================================
# VERROUS
# ============================================================
_config_lock     = threading.RLock()
_config_cache    = [None]
_log_lock        = threading.Lock()
_send_lock       = threading.RLock()
_log_send_lock   = threading.Lock()
_bulk_lock       = threading.Lock()

_pieces          = {}
_send_timestamps = []
_last_send_time  = [0.0]
_bulk_running    = [False]
_bulk_state      = [{
    "en_cours": False, "index": 0, "total": 0,
    "derniere": "", "envoyes": 0, "erreurs": 0, "arrete": False,
}]
_compte_index    = [0]
_auth_attempts   = {}          # {ip: [timestamps]} — anti-bruteforce/spam

# ============================================================
# UTILISATEUR COURANT
# ============================================================
def current_uid():
    """UID de l'utilisateur connecté (0 si hors contexte = global/legacy)."""
    try:
        return int(session.get("uid", 0) or 0)
    except RuntimeError:
        return 0


# ============================================================
# CONFIG
# ============================================================
def _config_globale():
    """Config globale (comptes Gmail, réglages d'envoi) — clé 'main', uid 0."""
    with _config_lock:
        if _config_cache[0] is None:
            db_cfg = db.config_get(0)
            if db_cfg is None:
                _config_cache[0] = json.loads(json.dumps(DEFAULT_CONFIG))
            else:
                cfg = json.loads(json.dumps(DEFAULT_CONFIG))
                for k, v in db_cfg.items():
                    if isinstance(v, dict) and k in cfg:
                        cfg[k].update(v)
                    else:
                        cfg[k] = v
                _config_cache[0] = cfg
        return _config_cache[0]


def charger_config(uid=None):
    """Config de l'utilisateur courant (candidat, templates, groupes, PJ...)."""
    if uid is None:
        uid = current_uid()
    if not uid:
        return _config_globale()
    db_cfg = db.config_get(uid)
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if db_cfg is None:
        # Nouvel utilisateur : profil candidat vide
        cfg["candidat"] = {k: "" for k in cfg["candidat"]}
    else:
        for k, v in db_cfg.items():
            if isinstance(v, dict) and k in cfg:
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg

def sauver_config(cfg, uid=None):
    if uid is None:
        uid = current_uid()
    if not uid:
        with _config_lock:
            _config_cache[0] = cfg
        db.config_set(cfg, 0)
    else:
        db.config_set(cfg, uid)

# ============================================================
# LOG
# ============================================================
def charger_log(uid=None):
    if uid is None:
        uid = current_uid()
    with _log_lock:
        return db.log_get(uid)

def sauver_log(log, uid=None):
    if uid is None:
        uid = current_uid()
    with _log_lock:
        try:
            db.log_set(log, uid)
        except Exception as e:
            print(f"[LOG] {e}")

# ============================================================
# DÉLAI
# ============================================================
def get_delai():
    p = _config_globale()["parametres"]
    if p.get("delai_aleatoire"):
        return random.randint(p.get("delai_min", 35), p.get("delai_max", 55))
    return p.get("delai_secondes", 40)

def check_rate_limit():
    max_h = _config_globale()["parametres"]["max_par_heure"]
    now = time.time()
    cutoff = now - 3600
    _send_timestamps[:] = [t for t in _send_timestamps if t > cutoff]
    return (len(_send_timestamps) < max_h), len(_send_timestamps), max_h

def maintenant_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def parse_emails(dest):
    """Parse une chaîne d'emails séparés par virgule, point-virgule ou saut de ligne."""
    if not dest:
        return []
    parts = re.split(r'[,;\n]+', str(dest))
    emails = [e.strip().lower() for e in parts if e.strip()]
    return [e for e in emails if '@' in e]

# ============================================================
# COMPTES
# ============================================================
def get_comptes_actifs():
    return [c for c in _config_globale().get("comptes", [])
            if c.get("email") and c.get("password") and c.get("actif", True)]

def compte_suivant():
    comptes = get_comptes_actifs()
    if not comptes:
        return None
    with _send_lock:
        idx = _compte_index[0] % len(comptes)
        _compte_index[0] = (_compte_index[0] + 1) % len(comptes)
        return comptes[idx]

# ============================================================
# TEMPLATES
# ============================================================
def _get_template(template_id, uid=None):
    """Cherche dans les templates perso d'abord, puis dans les prédéfinis."""
    cfg = charger_config(uid)
    for t in cfg.get("templates_perso", []):
        if t["id"] == template_id:
            return t
    if template_id in TEMPLATES:
        return TEMPLATES[template_id]
    return TEMPLATES["standard"]

def build_letter(template_id, company_name, context, uid=None):
    cfg = charger_config(uid)
    cand = cfg["candidat"]
    tpl = _get_template(template_id)
    try:
        return tpl["corps"].format(
            contexte=context, entreprise=company_name,
            nom=cand["nom"], tel=cand["tel"], email=cand["email"],
            ville=cand["ville"], diplome=cand["diplome"], spec=cand["spec"],
        )
    except KeyError as e:
        return f"[Erreur template : variable {e} inconnue]\n\n" + tpl["corps"]

def build_subject(template_id, company_name, uid=None):
    tpl = _get_template(template_id, uid)
    try:
        return tpl["objet"].format(entreprise=company_name)
    except KeyError:
        return tpl["objet"]

# ============================================================
# PIÈCES JOINTES
# ============================================================
def get_pieces_actives(uid=None):
    if uid is None:
        uid = current_uid()
    return [p for p in _pieces.get(int(uid or 0), {}).values()
            if p.get("actif", True) and Path(p["chemin"]).exists()]

def recharger_pieces(uid=None):
    if uid is None:
        uid = current_uid()
    u = int(uid or 0)
    _pieces.setdefault(u, {}).clear()
    if not UPLOADS_DIR.exists():
        return
    cfg = charger_config(uid)
    meta = cfg.get("pieces_jointes", {})
    pref = f"u{int(uid or 0)}_"
    for f in UPLOADS_DIR.glob("*.pdf"):
        nom_unique = f.name
        # Isolation par utilisateur :
        #  - les nouveaux fichiers sont préfixés u<uid>_
        #  - les fichiers sans préfixe (legacy) n'appartiennent qu'à l'uid
        #    qui possède la config migrée (migrate_legacy_user)
        if nom_unique.startswith("u") and nom_unique.split("_", 1)[0][1:].isdigit():
            if not nom_unique.startswith(pref):
                continue
        elif int(uid or 0) not in (0, 1):
            # legacy (sans préfixe) : réservé à l'utilisateur d'origine (uid 1)
            continue
        m = meta.get(nom_unique, {})
        _pieces[u][nom_unique] = {
            "nom_original": m.get("nom_original", f.name),
            "chemin":       str(f),
            "actif":        m.get("actif", True),
        }


def _txt(v):
    """Texte issu d'un JSON : None/entiers/objets -> '' (jamais de crash)."""
    return v if isinstance(v, str) else ""


_RX_EMAIL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


def _email_valide(email):
    """Validation stricte : refuse '', espaces, '@exemple.fr', 'a@.fr'..."""
    if not email or len(email) > 254 or " " in email:
        return False
    if email.startswith((".", "@", "-")) or ".." in email:
        return False
    if "@" not in email:
        return False
    local, _, domaine = email.rpartition("@")
    if not local or not domaine or "." not in domaine:
        return False
    if domaine.startswith(("-", ".")) or domaine.endswith(("-", ".")):
        return False
    return bool(_RX_EMAIL.match(email))

