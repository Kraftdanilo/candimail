"""
Règles de classement Gmail (logique métier pure, sans dépendance web).

Extrait de `web/routes/divers.py` : les routes doivent valider → déléguer →
répondre. Toute la logique des règles de filtres (création, normalisation,
suggestions d'apprentissage) vit ici, testable sans serveur HTTP.
"""
import uuid

from candimail.core.noyau import _txt
from candimail.services.imap import _ACTIONS_VALIDES


# Règles de classement par défaut (priorité 1 = évaluée en premier)
# Mots-clés réels : expéditeurs + sujets courants, français et anglais.
REGLES_DEFAUT = [
    {"name": "Bourse",       "icon": "📈", "color": "#f39c12",
     "items": [{"champ": "from",   "valeur": "boursorama"},
                {"champ": "from",   "valeur": "saxobank"},
                {"champ": "from",   "valeur": "trading212"},
                {"champ": "from",   "valeur": "degiro"},
                {"champ": "from",   "valeur": "e*trade"},
                {"champ": "from",   "valeur": "interactivebrokers"},
                {"champ": "sujet",  "valeur": "bourse"},
                {"champ": "sujet",  "valeur": "trading"},
                {"champ": "sujet",  "valeur": "investir"},
                {"champ": "sujet",  "valeur": "investissement"},
                {"champ": "sujet",  "valeur": "portefeuille"},
                {"champ": "sujet",  "valeur": "actions"},
                {"champ": "sujet",  "valeur": "dividende"},
                {"champ": "sujet",  "valeur": "cotations"}],
     "notify": False},
    {"name": "Opportunité",  "icon": "💼", "color": "#27ae60",
     "items": [{"champ": "sujet",  "valeur": "stage"},
                {"champ": "sujet",  "valeur": "stagiaire"},
                {"champ": "sujet",  "valeur": "alternance"},
                {"champ": "sujet",  "valeur": "apprenti"},
                {"champ": "sujet",  "valeur": "opportunité"},
                {"champ": "sujet",  "valeur": "candidature"},
                {"champ": "sujet",  "valeur": "poste"},
                {"champ": "sujet",  "valeur": "recrutement"},
                {"champ": "sujet",  "valeur": "internship"},
                {"champ": "sujet",  "valeur": "opportunity"},
                {"champ": "sujet",  "valeur": "hiring"},
                {"champ": "from",   "valeur": "recrutement"},
                {"champ": "from",   "valeur": "recrute"},
                {"champ": "from",   "valeur": "rh@"},
                {"champ": "from",   "valeur": "jobs@"},
                {"champ": "from",   "valeur": "career"},
                {"champ": "from",   "valeur": "talent"}],
     "notify": True},
    {"name": "Travail",      "icon": "🏢", "color": "#1E5AA8",
     "items": [{"champ": "sujet",  "valeur": "entretien"},
                {"champ": "sujet",  "valeur": "contrat"},
                {"champ": "sujet",  "valeur": "embauche"},
                {"champ": "sujet",  "valeur": "offre d'emploi"},
                {"champ": "sujet",  "valeur": "interview"},
                {"champ": "sujet",  "valeur": "job offer"},
                {"champ": "sujet",  "valeur": "convention de stage"},
                {"champ": "sujet",  "valeur": "votre candidature"},
                {"champ": "from",   "valeur": "noreply@linkedin.com"},
                {"champ": "from",   "valeur": "welcome@linkedin.com"},
                {"champ": "from",   "valeur": "notifications@linkedin.com"},
                {"champ": "from",   "valeur": "hello@indeed.com"},
                {"champ": "from",   "valeur": "welcomemail@welcomemail.welcomekit.co"},
                {"champ": "from",   "valeur": "welcomekit"},
                {"champ": "from",   "valeur": "jobteaser"},
                {"champ": "from",   "valeur": "jobvite"},
                {"champ": "from",   "valeur": "greenhouse.io"},
                {"champ": "from",   "valeur": "workday"},
                {"champ": "from",   "valeur": "lever.co"},
                {"champ": "from",   "valeur": "smartrecruiters"}],
     "notify": True},
    {"name": "Université",   "icon": "🎓", "color": "#8e44ad",
     "items": [{"champ": "from",   "valeur": "univ-"},
                {"champ": "from",   "valeur": "universite"},
                {"champ": "from",   "valeur": "university"},
                {"champ": "from",   "valeur": ".edu"},
                {"champ": "from",   "valeur": "esisalat"},
                {"champ": "from",   "valeur": "imesa"},
                {"champ": "sujet",  "valeur": "examen"},
                {"champ": "sujet",  "valeur": "cours"},
                {"champ": "sujet",  "valeur": "étudiant"},
                {"champ": "sujet",  "valeur": "scolarité"},
                {"champ": "sujet",  "valeur": "mémoire"},
                {"champ": "sujet",  "valeur": "soutenance"},
                {"champ": "sujet",  "valeur": "moodle"},
                {"champ": "sujet",  "valeur": "exam"}],
     "notify": False},
    {"name": "Réseaux sociaux", "icon": "👥", "color": "#2980b9",
     "items": [{"champ": "from",   "valeur": "linkedin.com"},
                {"champ": "from",   "valeur": "facebookmail.com"},
                {"champ": "from",   "valeur": "x.com"},
                {"champ": "from",   "valeur": "twitter"},
                {"champ": "from",   "valeur": "instagram"},
                {"champ": "from",   "valeur": "tiktok"},
                {"champ": "from",   "valeur": "whatsapp"},
                {"champ": "from",   "valeur": "telegram"},
                {"champ": "from",   "valeur": "snapchat"}],
     "notify": False},
    {"name": "Annonce",      "icon": "📢", "color": "#e67e22",
     "items": [{"champ": "sujet",  "valeur": "newsletter"},
                {"champ": "sujet",  "valeur": "promo"},
                {"champ": "sujet",  "valeur": "solde"},
                {"champ": "sujet",  "valeur": "réduction"},
                {"champ": "sujet",  "valeur": "vente flash"},
                {"champ": "sujet",  "valeur": "offres exclusives"},
                {"champ": "from",   "valeur": "newsletter"},
                {"champ": "from",   "valeur": "promo"},
                {"champ": "from",   "valeur": "marketing"},
                {"champ": "from",   "valeur": "noreply"}],
     "notify": False},
]


def seed_regles(cfg):
    """Crée les 6 règles par défaut au premier lancement.
    Version 2 : met à jour les mots-clés des règles par défaut existantes
    (sans toucher aux règles perso ni aux règles d'apprentissage)."""
    if not cfg.get("filtres_init"):
        regles = []
        for i, d in enumerate(REGLES_DEFAUT, 1):
            regles.append({
                "id":       f"rule-{i:03d}",
                "priority": i,
                "enabled":  True,
                "name":     d["name"],
                "icon":     d["icon"],
                "color":    d["color"],
                "items":    d["items"],
                "label":    d["name"],
                "actions":  ["label"] + (["notify"] if d["notify"] else []),
                "notify":   d["notify"],
            })
        cfg["filtres_gmail"] = regles
        cfg["filtres_init"] = 2
        return
    if cfg.get("filtres_init", 0) < 2:
        for d in REGLES_DEFAUT:
            for f in cfg.get("filtres_gmail", []):
                if f.get("name") == d["name"] and f.get("source") != "apprentissage":
                    f["items"] = d["items"]
                    f["icon"] = d["icon"]
                    f["color"] = d["color"]
                    f["notify"] = d["notify"]
                    acts = [a for a in (f.get("actions") or []) if a != "notify"]
                    if d["notify"]:
                        acts.append("notify")
                    f["actions"] = acts
        cfg["filtres_init"] = 2


def normaliser_regle(data, existante=None):
    """Construit/normalise une règle depuis un payload front."""
    r = dict(existante or {})
    r.setdefault("id", f"rule-{uuid.uuid4().hex[:8]}")
    items = data.get("items")
    if isinstance(items, list) and items:
        propres = []
        for it in items:
            if not isinstance(it, dict):
                continue
            champ = it.get("champ") if it.get("champ") in ("from", "sujet", "motcle") else None
            val = (it.get("valeur") or "").strip()
            if champ and val:
                propres.append({"champ": champ, "valeur": val})
        r["items"] = propres
    else:
        champ = _txt(data.get("champ")) or "motcle"
        val = _txt(data.get("valeur")).strip()
        r["items"] = ([{"champ": champ, "valeur": val}] if val
                      else r.get("items", []))
    r["name"]  = _txt(data.get("name")).strip() or r.get("name", "règle")
    r["label"] = _txt(data.get("label")).strip() or r.get("label", "")
    if data.get("icon"):
        r["icon"] = _txt(data.get("icon"))
    if data.get("color"):
        r["color"] = _txt(data.get("color"))
    if "enabled" in data:
        r["enabled"] = bool(data.get("enabled"))
    else:
        r.setdefault("enabled", True)
    if isinstance(data.get("priority"), int):
        r["priority"] = data["priority"]
    else:
        r.setdefault("priority", 999)
    acts = data.get("actions") if isinstance(data.get("actions"), list) else r.get("actions", [])
    acts = [a for a in acts if a in _ACTIONS_VALIDES]
    r["actions"] = acts
    r["notify"] = "notify" in acts
    return r


def reindexer_priorites(filtres):
    """Renumérote les priorités 1..N (après suppression/reorder)."""
    for i, f in enumerate(filtres, 1):
        f["priority"] = i
    return filtres


def appliquer_apprentissage(cfg, email, label, notifier=False):
    """L'utilisateur dit : « les mails de X vont dans le libellé Y ».

    Crée/met à jour une règle expéditeur → libellé (priority 0 : gagne sur
    tout), note le nombre de corrections. Mutue `cfg` et le renvoie.
    """
    apprentissage = cfg.setdefault("apprentissage", {})
    entree = apprentissage.get(email, {"label": label, "corrections": 0})
    meme_label = entree.get("label") == label
    entree["label"] = label
    entree["corrections"] = 0 if meme_label else entree.get("corrections", 0) + 1
    entree["derniere"] = None  # rempli par la couche route (datetime UI)
    apprentissage[email] = entree

    filtres = cfg.get("filtres_gmail", [])
    regle = None
    for f in filtres:
        items = f.get("items") or []
        if (f.get("source") == "apprentissage"
                and any(it.get("valeur", "").lower() == email for it in items)):
            regle = f
            break
    if regle is None:
        regle = {"id": f"rule-app-{uuid.uuid4().hex[:6]}", "name": label,
                 "icon": "🧠", "color": "#16a085", "source": "apprentissage"}
        filtres.append(regle)
    regle.update({
        "priority": 0,                    # apprend plus fort que les règles fixes
        "enabled":  True,
        "items":    [{"champ": "from", "valeur": email}],
        "label":    label,
        "name":     label,
    })
    acts = ["label"]
    if notifier:
        acts.append("notify")
    regle["actions"] = acts
    cfg["filtres_gmail"] = sorted(filtres, key=lambda f: f.get("priority", 999))
    return cfg


def calculer_suggestions(cfg):
    """Règles souvent corrigées (>20 % de corrections) → à signaler au front.
    Un expéditeur corrigé 3+ fois en changeant de libellé → suggestion de règle."""
    suggestions = []
    for email, e in cfg.get("apprentissage", {}).items():
        if e.get("corrections", 0) >= 3:
            suggestions.append({"email": email, "label": e.get("label", ""),
                                "corrections": e["corrections"],
                                "type": "expediteur_frequent"})
    for f in cfg.get("filtres_gmail", []):
        total = f.get("nb_classements", 0)
        corr = f.get("nb_corrections", 0)
        if total >= 10 and corr / total > 0.2:
            suggestions.append({"regle": f.get("name", ""), "id": f.get("id"),
                                "taux": round(corr / total, 2),
                                "type": "regle_faible"})
    return suggestions


def export_sans_secrets(cfg_complet, charger_log_fn):
    """Construit la sauvegarde portable : AUCUN secret ne doit y subsister.

    Exclus : `securite`, `comptes`, `admin`, `mots_de_passe` (et variantes de
    casse). Lève RuntimeError si un secret chiffré subsiste malgré tout.
    """
    import json as _json
    INTERDITS = {"securite", "comptes", "admin", "mots_de_passe"}
    config = {k: v for k, v in cfg_complet.items()
              if k not in INTERDITS and k.lower() not in INTERDITS}
    data = {
        "export_le": _now_iso(),
        "config":    config,
        "log":       charger_log_fn(),
    }
    texte = _json.dumps(data, ensure_ascii=False, indent=2)
    if "enc$" in texte:
        raise RuntimeError("un secret chiffré a survécu au filtrage d'export")
    return data, texte


def _now_iso():
    from datetime import datetime
    return datetime.now().isoformat()
