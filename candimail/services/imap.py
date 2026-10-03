#!/usr/bin/env python3
"""
Service IMAP — vérification des boîtes Gmail : réponses reçues,
bounces, et règles de classement automatique (filtres Gmail).
"""
import base64, email, imaplib, time
from datetime import datetime, timedelta
from email.header import decode_header
from email.utils import parseaddr

from candimail.core import crypto
from candimail.core.noyau import charger_config, sauver_config, charger_log, sauver_log, get_comptes_actifs


# ============================================================
# IMAP
# ============================================================
def _decode_header_safe(raw):
    if not raw:
        return ""
    try:
        parts = decode_header(raw)
        out = []
        for content, charset in parts:
            if isinstance(content, bytes):
                out.append(content.decode(charset or "utf-8", errors="ignore"))
            else:
                out.append(content)
        return " ".join(out)
    except Exception:
        return str(raw)

def _extraire_email(from_header):
    _, addr = parseaddr(from_header or "")
    return addr.lower().strip()

def check_imap_compte(compte, jours=30, uid=None):
    result = {"reponses": {}, "bounces": {}}
    mail = None
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=20)
        mail.login(compte["email"], crypto.dechiffrer(compte["password"]))
        mail.select("INBOX")

        since = (datetime.now() - timedelta(days=jours)).strftime("%d-%b-%Y")
        status, msgs = mail.search(None, f'(SINCE "{since}")')
        if status != "OK" or not msgs[0]:
            return result

        log = charger_log(uid)
        emails_contactes = {}
        for k, v in log.items():
            for e in (v.get("emails") or [v.get("email", "")]):
                if e:
                    emails_contactes[e.lower()] = k

        for num in msgs[0].split():
            try:
                status, data = mail.fetch(num, "(BODY.PEEK[HEADER])")
                if status != "OK" or not data or not data[0]:
                    continue
                msg = email.message_from_bytes(data[0][1])

                from_addr = _extraire_email(msg.get("From", ""))
                subject   = _decode_header_safe(msg.get("Subject", ""))

                if any(x in from_addr for x in ("mailer-daemon", "postmaster",
                                                 "mail-daemon", "mailerdaemon")):
                    failed = ""
                    xfail = msg.get("X-Failed-Recipients", "")
                    if xfail:
                        failed = xfail.split(",")[0].strip().lower()
                    if failed:
                        result["bounces"][failed] = {
                            "sujet":  subject[:200],
                            "date":   msg.get("Date", ""),
                            "raison": "Adresse invalide ou boîte pleine",
                        }
                    continue

                if from_addr in emails_contactes:
                    company = emails_contactes[from_addr]
                    result["reponses"][company] = {
                        "email":  from_addr,
                        "sujet":  subject[:200],
                        "date":   msg.get("Date", ""),
                    }
            except Exception:
                continue
    except imaplib.IMAP4.error as e:
        print(f"[IMAP] {compte['email']}: {e}")
        result["erreur"] = f"Connexion refusée pour {compte['email']} : {e}"
    except Exception as e:
        print(f"[IMAP] {type(e).__name__}: {e}")
        result["erreur"] = f"{type(e).__name__} : {e}"
    finally:
        if mail:
            try: mail.logout()
            except Exception: pass
    return result

def verifier_toutes_boites(jours=30, uid=None):
    comptes = get_comptes_actifs()
    if not comptes:
        return {"ok": False, "error": "Aucun compte actif"}

    log = charger_log(uid)
    nb_reponses = 0
    nb_bounces = 0
    erreurs = []

    for compte in comptes:
        res = check_imap_compte(compte, jours=jours, uid=uid)
        if res.get("erreur"):
            erreurs.append(res["erreur"])
        for company, info in res["reponses"].items():
            if company in log and not log[company].get("repondu"):
                log[company]["repondu"] = True
                log[company]["date_reponse"] = info["date"][:20]
                log[company]["sujet_reponse"] = info["sujet"]
                nb_reponses += 1
        for email_bounce, info in res["bounces"].items():
            for company, entry in log.items():
                emails_entry = entry.get("emails") or [entry.get("email", "")]
                if any(e.lower() == email_bounce for e in emails_entry):
                    if not entry.get("bounce"):
                        entry["bounce"] = True
                        entry["bounce_raison"] = info["raison"]
                        entry["bounce_date"] = info["date"][:20]
                        nb_bounces += 1

    sauver_log(log, uid)
    cfg = charger_config(uid)
    cfg["imap"]["derniere_verif"] = int(time.time())
    sauver_config(cfg, uid)

    return {
        "ok": not erreurs,
        "erreurs": erreurs,
        "reponses": nb_reponses,
        "bounces": nb_bounces,
        "comptes_verifies": len(comptes),
    }


# ------------------------------------------------------------
# FILTRES GMAIL (règles de classement automatique)
# ------------------------------------------------------------
_ACTIONS_VALIDES = {"label", "archive", "marquer_lu", "supprimer", "notify"}


def _items_regles(f):
    """Liste de conditions [(champ, valeur)] d'une règle (format étendu ou simple)."""
    items = f.get("items")
    if isinstance(items, list) and items:
        out = []
        for it in items:
            if not isinstance(it, dict):
                continue
            champ = it.get("champ") if it.get("champ") in ("from", "sujet", "motcle") else it.get("field")
            if champ not in ("from", "sujet", "motcle"):
                continue
            val = it.get("valeur") or it.get("value") or ""
            if isinstance(val, str) and val.strip():
                out.append((champ, val.strip()))
        if out:
            return out
    champ = f.get("champ")
    val = f.get("valeur")
    if champ in ("from", "sujet", "motcle") and isinstance(val, str) and val.strip():
        return [(champ, val.strip())]
    return []


def _filtre_valide(f):
    """Règle = {items: [{champ, valeur}...] ou champ+valeur, actions: [...]}.
    Format étendu : id, priority, enabled, name, label, notify."""
    if not isinstance(f, dict):
        return False
    if f.get("enabled") is False:
        return False
    if not _items_regles(f):
        return False
    acts = f.get("actions")
    if not isinstance(acts, list) or not acts:
        return False
    if not all(a in _ACTIONS_VALIDES for a in acts):
        return False
    if "label" in acts and not (f.get("label") or "").strip():
        return False
    return True


def _gimap_ouvre(compte):
    """Connexion IMAP prête à l'emploi pour un compte Gmail de la config."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=25)
    mail.login(compte["email"], crypto.dechiffrer(compte["password"]))
    return mail


def _utf7(s):
    """Encode une chaîne en IMAP UTF-7 (modifié) — requis par IMAP4 pour
    les noms de boîtes/libellés contenant des accents (ex. Opportunité)."""
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


def _depuis_utf7(s):
    """Décode un nom IMAP UTF-7 (modifié) en chaîne Unicode lisible."""
    if "&" not in s:
        return s
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "&":
            fin = s.find("-", i + 1)
            if fin == -1:
                out.append("&")
                i += 1
                continue
            bloc = s[i + 1:fin]
            if not bloc:
                out.append("&")
            else:
                b = bloc.replace(",", "/").encode("ascii")
                b += b"=" * (-len(b) % 4)
                out.append(base64.b64decode(b).decode("utf-16-be"))
            i = fin + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _creer_libelle(mail, lbl):
    """Crée un libellé Gmail (no-op s'il existe déjà). Accepte les accents.
    imaplib.create() casse la commande sur les noms non-ASCII ; on utilise
    donc la commande brute CREATE avec le nom encodé en IMAP UTF-7."""
    try:
        typ, _ = mail._simple_command("CREATE",
                                      b'"' + _utf7(lbl).encode("ascii") + b'"')
        return typ == "OK"
    except Exception:
        return False


def _critere(champ, val):
    val = val.replace('"', '')
    if champ == "from":
        return f'FROM "{val}"'
    if champ == "sujet":
        return f'SUBJECT "{val}"'
    return f'OR SUBJECT "{val}" TEXT "{val}"'   # mot-clé : sujet OU texte


def _imap_recherche(mail, filtre):
    """Construit la requête IMAP SEARCH (OR de toutes les conditions de la règle)."""
    items = _items_regles(filtre)
    criteres = [_critere(c, v) for c, v in items]
    if not criteres:
        return '(ALL)'
    if len(criteres) == 1:
        return f'({criteres[0]})'
    q = f'OR {criteres[-2]} {criteres[-1]}'
    for c in reversed(criteres[:-2]):
        q = f'OR {c} {q}'
    return f'({q})'


def appliquer_filtres_compte(compte, filtres, uid=None):
    """Applique les règles PAR ORDRE DE PRIORITÉ sur la boîte.
    Une règle désactivée est ignorée ; chaque mail n'est classé que par
    la PREMIÈRE règle (priorité la plus haute) qui correspond.
    Actions : label / archive / marquer_lu / supprimer / notify."""
    stats = []
    notifs = []          # notifications à enregistrer (Travail / Opportunité…)
    deja = set()         # ids déjà classés (priorité : la 1re règle gagne)
    regles = sorted(
        [f for f in filtres if _filtre_valide(f)],
        key=lambda f: (f.get("priority", 999), str(f.get("id", "")))
    )
    mail = None
    try:
        mail = _gimap_ouvre(compte)
        for f in regles:
            try:
                mail.select("INBOX")
                status, msgs = mail.search(None, _imap_recherche(mail, f))
                if status != "OK" or not msgs[0]:
                    continue
                tous = msgs[0].split()
                restants = [n for n in tous if n not in deja]
                if not restants:
                    stats.append({"regle": _nom_regle(f), "trouves": 0, "ok": True})
                    continue
                ids = b",".join(restants)
                nb = len(restants)
                deja.update(restants)

                actions = f.get("actions", [])
                if "label" in actions:
                    lbl = (f.get("label") or "").strip()
                    if lbl:
                        _creer_libelle(mail, lbl)
                        mail.store(ids, "+X-GM-LABELS",
                                   b'"' + _utf7(lbl).encode("ascii") + b'"')
                if "marquer_lu" in actions:
                    mail.store(ids, "+FLAGS", "\\\\Seen")
                if "archive" in actions:
                    mail.copy(ids, "[Gmail]/All Mail")
                    mail.store(ids, "+FLAGS", "\\\\Deleted")
                if "supprimer" in actions:
                    mail.store(ids, "+FLAGS", "\\\\Deleted")

                mail.expunge()
                stats.append({"regle": _nom_regle(f), "trouves": nb, "ok": True})
                print(f"[FILTRE] {compte['email']}: {_nom_regle(f)} -> {nb} msg")

                if "notify" in actions and nb:
                    notifs.append({
                        "regle":   _nom_regle(f),
                        "email":   compte.get("email", ""),
                        "label":   (f.get("label") or "").strip(),
                        "nombre":  nb,
                        "date":    int(time.time()),
                    })
            except Exception as e:
                stats.append({"regle": _nom_regle(f), "erreur": str(e), "ok": False})
    except Exception as e:
        stats.append({"erreur": f"Connexion {compte['email']}: {e}", "ok": False})
    finally:
        if mail:
            try: mail.logout()
            except Exception: pass

    if notifs and uid is not None:
        _enregistrer_notifications(notifs, uid)
    return stats


def _nom_regle(f):
    return (f.get("name") or f.get("valeur") or "règle").strip()


def _enregistrer_notifications(notifs, uid):
    """Stocke les notifications dans la config de l'utilisateur (max 50)."""
    try:
        cfg = charger_config(uid)
        pile = cfg.setdefault("notifications", [])
        for n in notifs:
            pile.insert(0, n)
        cfg["notifications"] = pile[:50]
        sauver_config(cfg, uid)
    except Exception as e:
        print(f"[NOTIF] enregistrement impossible : {e}")
