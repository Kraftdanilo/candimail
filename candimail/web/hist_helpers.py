"""Aide à l'annulation / rétablissement des actions utilisateur.

Chaque action réversible est décrite par un petit dictionnaire :
    {"op": "supprimer_entreprise", "nom": "ACME", ...}
`appliquer()` exécute l'opération et renvoie (succès, message).

Sécurité : ce module n'est appelé QUE depuis les routes FastAPI
(`/api/historique/<id>/undo`). Le front ne fournit que l'identifiant de
l'action à rejouer — jamais les données à exécuter.
"""
from candimail.core import db
from candimail.core.noyau import charger_config, sauver_config, modifier_log


def _trouver(lst, cle, valeur):
    return next((x for x in lst if x.get(cle) == valeur), None)


def _maj_reponse(company, repondu):
    def _f(l):
        if company in l:
            l[company]["repondu"] = repondu
    return _f


# ------------------------------------------------------------
# Opérations sur les entreprises
# ------------------------------------------------------------
def _op_supprimer_entreprise(d, uid):
    nom = d.get("nom")
    if not nom:
        return False, "Données incomplètes"
    companies = db.companies_get(uid)
    reste = [c for c in companies if c["name"] != nom]
    if len(reste) == len(companies):
        return False, "Entreprise déjà absente"
    db.companies_replace(reste, uid)
    return True, f"Entreprise « {nom} » supprimée"


def _op_ajouter_entreprise(d, uid):
    """Restaure une entreprise supprimée.

    ⚠️ Tolérant : `data` peut être un dict (ancienne forme) OU une liste
    d'entreprises (suppression groupée). Les entrées d'historique déjà
    enregistrées utilisent la forme liste — sans ce repli, leur annulation
    échouerait avec une TypeError.
    """
    if isinstance(d.get("data"), list):
        return _op_ajouter_entreprises(d, uid)
    nom = d.get("nom")
    if not nom:
        return False, "Données incomplètes"
    companies = db.companies_get(uid)
    if any(c["name"] == nom for c in companies):
        return False, "Entreprise déjà présente"
    companies.append(d.get("data") or {"name": nom})
    db.companies_replace(companies, uid)
    return True, f"Entreprise « {nom} » restaurée"


def _op_renommer_entreprise(d, uid):
    avant, apres = d.get("avant"), d.get("apres")
    if not avant or not apres:
        return False, "Données incomplètes"
    companies = db.companies_get(uid)
    cible = (_trouver(companies, "name", apres)
             or _trouver(companies, "name", avant))
    if not cible:
        return False, "Entreprise introuvable"
    cible["name"] = avant
    db.companies_replace(companies, uid)

    def _rename(l):
        if apres in l:
            l[avant] = l.pop(apres)
    modifier_log(_rename, uid)
    return True, f"Entreprise renommée en « {avant} »"


# ------------------------------------------------------------
# Opérations sur les groupes et modèles
# ------------------------------------------------------------
def _liste_config(uid, cle):
    return charger_config(uid).get(cle, [])


def _set_liste_config(uid, cle, valeurs):
    cfg = charger_config(uid)
    cfg[cle] = valeurs
    sauver_config(cfg, uid)


def _op_supprimer_groupe(d, uid):
    gid = d.get("id")
    groupes = _liste_config(uid, "groupes")
    cible = _trouver(groupes, "id", gid)
    if not cible:
        return False, "Groupe introuvable"
    _set_liste_config(uid, "groupes",
                      [g for g in groupes if g.get("id") != gid])
    return True, f"Groupe « {cible.get('nom', '')} » supprimé"


def _op_ajouter_groupe(d, uid):
    data = d.get("data")
    if not isinstance(data, dict):
        return False, "Données incomplètes"
    groupes = _liste_config(uid, "groupes")
    if any(g.get("id") == data.get("id") for g in groupes):
        return False, "Groupe déjà présent"
    _set_liste_config(uid, "groupes", [*groupes, data])
    return True, f"Groupe « {data.get('nom', '')} » restauré"


def _op_supprimer_template(d, uid):
    tid = d.get("id")
    templates = _liste_config(uid, "templates_perso")
    cible = _trouver(templates, "id", tid)
    if not cible:
        return False, "Modèle introuvable"
    _set_liste_config(uid, "templates_perso",
                      [t for t in templates if t.get("id") != tid])
    return True, f"Modèle « {cible.get('nom', '')} » supprimé"


def _op_ajouter_template(d, uid):
    data = d.get("data")
    if not isinstance(data, dict):
        return False, "Données incomplètes"
    templates = _liste_config(uid, "templates_perso")
    if any(t.get("id") == data.get("id") for t in templates):
        return False, "Modèle déjà présent"
    _set_liste_config(uid, "templates_perso", [*templates, data])
    return True, f"Modèle « {data.get('nom', '')} » restauré"


# ------------------------------------------------------------
# Bascules (comptes, pièces, règles, paramètres, journal)
# ------------------------------------------------------------
def _op_toggle_compte(d, uid):
    from candimail.core.noyau import _config_globale
    idx = d.get("index")
    if idx is None:
        return False, "Données incomplètes"
    cfg = _config_globale()
    comptes = cfg.get("comptes", [])
    if not (0 <= int(idx) < len(comptes)):
        return False, "Compte introuvable"
    comptes[int(idx)]["actif"] = bool(d.get("actif", True))
    sauver_config(cfg, 0)
    actif = bool(d.get("actif", True))
    return True, f"Compte {'activé' if actif else 'mis en pause'}"


def _op_toggle_piece(d, uid):
    pid = d.get("id")
    if not pid:
        return False, "Données incomplètes"
    cfg = charger_config(uid)
    pj = cfg.get("pieces_jointes", {})
    if pid not in pj:
        return False, "Pièce jointe introuvable"
    pj[pid]["actif"] = bool(d.get("actif", True))
    cfg["pieces_jointes"] = pj
    sauver_config(cfg, uid)
    return True, "Pièce jointe mise à jour"


def _op_toggle_filtre(d, uid):
    idx = d.get("index")
    if idx is None:
        return False, "Données incomplètes"
    filtres = _liste_config(uid, "filtres_gmail")
    if not (0 <= int(idx) < len(filtres)):
        return False, "Règle introuvable"
    filtres[int(idx)]["enabled"] = bool(d.get("actif", True))
    _set_liste_config(uid, "filtres_gmail", filtres)
    return True, "Règle mise à jour"


def _op_parametres(d, uid):
    apres = d.get("apres")
    if not isinstance(apres, dict):
        return False, "Données incomplètes"
    cfg = charger_config(uid)
    cfg.setdefault("parametres", {}).update(d.get("avant") or apres)
    sauver_config(cfg, uid)
    return True, "Paramètres mis à jour"


def _op_ajouter_entreprises(d, uid):
    """Restaure un LOT d'entreprises supprimées (annulation groupée)."""
    data = d.get("data")
    if not isinstance(data, list) or not data:
        return False, "Données incomplètes"
    companies = db.companies_get(uid)
    noms = {c["name"] for c in companies}
    ajoutes = []
    for c in data:
        if not isinstance(c, dict):
            continue
        nom = (c.get("name") or "").strip()
        if not nom or nom in noms:
            continue                      # déjà présente : on ne duplique pas
        companies.append({"name": nom, "cat": c.get("cat", "pme"),
                          "email": c.get("email", ""),
                          "context": c.get("context", ""),
                          "custom": bool(c.get("custom"))})
        noms.add(nom)
        ajoutes.append(nom)
    if not ajoutes:
        return False, "Aucune entreprise à restaurer"
    db.companies_replace(companies, uid)
    if len(ajoutes) == 1:
        return True, f"Entreprise « {ajoutes[0]} » restaurée"
    return True, f"{len(ajoutes)} entreprises restaurées"


def _op_supprimer_entreprises(d, uid):
    """Supprime un LOT d'entreprises (rétablissement de l'état précédent)."""
    noms = d.get("noms")
    if not isinstance(noms, list) or not noms:
        return False, "Données incomplètes"
    noms = {str(n) for n in noms}
    companies = db.companies_get(uid)
    reste = [c for c in companies if c["name"] not in noms]
    if len(reste) == len(companies):
        return False, "Entreprises déjà absentes"
    db.companies_replace(reste, uid)
    return True, f"{len(companies) - len(reste)} entreprise(s) supprimée(s)"


def _op_profil(d, uid):
    """Restaure le profil candidat (nom, ville, pays, téléphone…)."""
    avant = d.get("avant")
    if not isinstance(avant, dict):
        return False, "Données incomplètes"
    cfg = charger_config(uid)
    cible = cfg.setdefault("candidat", {})
    for k in ("nom", "tel", "email", "ville", "pays", "diplome", "spec"):
        if k in avant:
            cible[k] = str(avant[k] or "")
    sauver_config(cfg, uid)
    return True, f"Profil « {cible.get('nom', '')} » restauré"


def _op_toggle_reponse(d, uid):
    company = d.get("company")
    if not company:
        return False, "Données incomplètes"
    modifier_log(_maj_reponse(company, bool(d.get("repondu", True))), uid)
    return True, "Statut de réponse mis à jour"


def _op_envoyer(d, uid):
    """« Annuler » un envoi = le retirer du journal (l'e-mail reste parti)."""
    company = d.get("company")
    if not company:
        return False, "Données incomplètes"
    avant = modifier_log(lambda l: l.pop(company, None), uid)[0]
    if company not in avant:
        return False, "Envoi introuvable"
    return True, f"Envoi « {company} » retiré du journal"


# ------------------------------------------------------------
# Annuaire des opérations
# ------------------------------------------------------------
OPERATIONS = {
    "supprimer_entreprise": _op_supprimer_entreprise,
    "ajouter_entreprise": _op_ajouter_entreprise,
    "ajouter_entreprises": _op_ajouter_entreprises,
    "supprimer_entreprises": _op_supprimer_entreprises,
    "renommer_entreprise": _op_renommer_entreprise,
    "supprimer_groupe": _op_supprimer_groupe,
    "ajouter_groupe": _op_ajouter_groupe,
    "supprimer_template": _op_supprimer_template,
    "ajouter_template": _op_ajouter_template,
    "toggle_compte": _op_toggle_compte,
    "toggle_piece": _op_toggle_piece,
    "toggle_filtre": _op_toggle_filtre,
    "parametres": _op_parametres,
    "profil": _op_profil,
    "toggle_reponse": _op_toggle_reponse,
    "envoyer": _op_envoyer,
}


def appliquer(donnees, uid=0):
    """Rejoue une opération d'annulation. Renvoie (succès, message)."""
    if not isinstance(donnees, dict):
        return False, "Données invalides"
    fn = OPERATIONS.get(donnees.get("op"))
    if not fn:
        return False, f"Opération inconnue : {donnees.get('op')}"
    return fn(donnees, uid)