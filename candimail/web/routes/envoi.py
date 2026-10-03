#!/usr/bin/env python3
"""Routes Flask — envoi unitaire, envoi de masse, groupes (blueprint)."""
import time, threading, uuid

from flask import Blueprint, jsonify, request

from candimail.core.noyau import current_uid, charger_config, sauver_config, charger_log, sauver_log, get_delai, check_rate_limit, maintenant_str, parse_emails, get_comptes_actifs, compte_suivant, build_letter, build_subject, get_pieces_actives, recharger_pieces, _send_lock, _log_send_lock, _bulk_lock, _bulk_running, _bulk_state, _send_timestamps, _last_send_time, _email_valide
from candimail.services.smtp import envoyer_email, _envoyer_un_email

bp = Blueprint("envoi", __name__)


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------
@bp.route("/api/status")
def api_status():
    log = charger_log()
    recharger_pieces()
    ok_rl, cnt, mx = check_rate_limit()
    return jsonify({
        "cv_loaded":      len(get_pieces_actives()) > 0,
        "pieces_count":   len(get_pieces_actives()),
        "sent_count":     len([x for x in log.values() if x.get("envoye")]),
        "log":            log,
        "rate_limit":     {"utilises": cnt, "max": mx, "ok": ok_rl},
        "comptes_actifs": len(get_comptes_actifs()),
        "delai_actuel":   get_delai(),
    })

# ------------------------------------------------------------
# APERÇU / ENVOI
# ------------------------------------------------------------
@bp.route("/api/preview", methods=["POST"])
def api_preview():
    data = request.get_json() or {}
    company  = (data.get("company") or "").strip()
    context  = (data.get("context") or "").strip()
    template = data.get("template") or charger_config()["parametres"]["template"]
    if not company:
        return jsonify({"ok": False, "error": "company requis"}), 400
    return jsonify({
        "ok": True,
        "subject":  build_subject(template, company),
        "body":     build_letter(template, company, context),
        "template": template,
    })

@bp.route("/api/send", methods=["POST"])
def api_send():
    data = request.get_json() or {}
    dest     = (data.get("email") or "").strip()
    company  = (data.get("company") or "").strip()
    subject  = (data.get("subject") or "").strip()
    body     = (data.get("body") or "").strip()
    pieces   = data.get("pieces")
    mode_grp = bool(data.get("mode_groupe", False))

    if not dest or not company or not body:
        return jsonify({"ok": False, "error": "Champs manquants"}), 400
    if not get_comptes_actifs():
        return jsonify({"ok": False, "error": "Aucun compte Gmail actif"}), 400
    # Validation des destinataires AVANT tout envoi (400 = erreur client,
    # pas un échec serveur SMTP). Validation stricte + rejet si aucun email valide.
    emails_dest = [e for e in parse_emails(dest) if _email_valide(e)]
    if not emails_dest:
        return jsonify({"ok": False,
                        "error": "Aucun destinataire valide"}), 400

    ok_rl, cnt, mx = check_rate_limit()
    if not ok_rl:
        return jsonify({"ok": False, "error": f"Rate limit {cnt}/{mx}"}), 429

    with _send_lock:
        delay = get_delai()
        ecoule = time.time() - _last_send_time[0]
        if ecoule < delay:
            return jsonify({"ok": False,
                            "error": f"Attends {int(delay-ecoule)+1}s",
                            "attente": int(delay-ecoule)+1}), 429
        _last_send_time[0] = time.time()

    # Choisir le compte ici pour le tracer dans le journal
    # et appliquer son template propre s'il en a un.
    compte = compte_suivant()
    if compte and compte.get("template"):
        template_id = compte["template"]
        context = (data.get("context") or "").strip()
        subject = build_subject(template_id, company)
        body = build_letter(template_id, company, context)

    ok, msg = envoyer_email(dest, subject, body,
                             pieces_selectionnees=pieces,
                             mode_groupe=mode_grp, compte=compte)

    with _log_send_lock:
        _send_timestamps.append(time.time())

    if ok:
        emails_list = parse_emails(dest)
        log = charger_log()
        sans_pj = len(get_pieces_actives()) == 0 and not pieces
        log[company] = {
            "email":   dest,
            "emails":  emails_list,
            "envoye":  True,
            "date":    maintenant_str(),
            "compte":  (compte or {}).get("email", ""),
            "repondu": False,
            "sans_pj": sans_pj,
            "groupe":  mode_grp,
        }
        sauver_log(log)
        return jsonify({"ok": True, "message": msg, "sans_pj": sans_pj,
                        "nb_destinataires": len(emails_list)})
    return jsonify({"ok": False, "error": msg}), 500

# ------------------------------------------------------------
# BULK
# ------------------------------------------------------------
def _bulk_worker(companies, template, owner_uid=0):
    log = charger_log(owner_uid)
    try:
        for i, c in enumerate(companies):
            if not _bulk_running[0]:
                break
            with _bulk_lock:
                _bulk_state[0]["index"]    = i + 1
                _bulk_state[0]["derniere"] = c["name"]

            # Choisir le compte AVANT de construire le message, pour
            # appliquer le template propre du compte s'il en a un.
            compte = compte_suivant()
            tpl = template
            if compte and compte.get("template"):
                tpl = compte["template"]

            delay = get_delai()
            with _send_lock:
                ecoule = time.time() - _last_send_time[0]
                if ecoule < delay:
                    time.sleep(delay - ecoule)

            # Attente intelligente du rate limit : au lieu de marquer
            # l'entreprise en erreur, on attend que la fenêtre d'1h se
            # libère puis on réessaie la même entreprise.
            ok_rl, cnt, mx = check_rate_limit()
            while not ok_rl and _bulk_running[0]:
                reste = 60
                if _send_timestamps:
                    reste = int(_send_timestamps[0] + 3600 - time.time()) + 5
                reste = max(5, min(reste, 300))
                with _bulk_lock:
                    _bulk_state[0]["derniere"] = \
                        f"{c['name']} — ⏳ attente rate limit {reste}s ({cnt}/{mx})"
                time.sleep(reste)
                ok_rl, cnt, mx = check_rate_limit()
            if not _bulk_running[0]:
                break

            try:
                sujet = build_subject(tpl, c["name"], owner_uid)
                corps = build_letter(tpl, c["name"], c.get("context", ""), owner_uid)
                ok, msg = envoyer_email(c["email"], sujet, corps, compte=compte,
                                        uid=owner_uid)
            except Exception as e:
                ok, msg = False, f"{type(e).__name__}: {str(e)[:100]}"

            with _log_send_lock:
                _send_timestamps.append(time.time())
                _last_send_time[0] = time.time()

            sans_pj = len(get_pieces_actives(owner_uid)) == 0
            if ok:
                log[c["name"]] = {
                    "email": c["email"], "envoye": True,
                    "date": maintenant_str(), "repondu": False,
                    "sans_pj": sans_pj,
                    "compte": (compte or {}).get("email", ""),
                    "template": tpl,
                }
                with _bulk_lock: _bulk_state[0]["envoyes"] += 1
            else:
                log[c["name"]] = {
                    "email": c["email"], "envoye": False,
                    "date": maintenant_str(), "erreur": msg,
                }
                with _bulk_lock: _bulk_state[0]["erreurs"] += 1

            sauver_log(log, owner_uid)
    except Exception as e:
        print(f"[BULK] {e}")
    finally:
        with _bulk_lock:
            _bulk_state[0]["en_cours"] = False
            _bulk_state[0]["arrete"]   = not _bulk_running[0]
        _bulk_running[0] = False
        try: sauver_log(log, owner_uid)
        except Exception: pass

@bp.route("/api/send-bulk", methods=["POST"])
def api_send_bulk():
    with _bulk_lock:
        if _bulk_running[0]:
            return jsonify({"ok": False, "error": "Déjà en cours"}), 409

    data = request.get_json() or {}
    companies = data.get("companies") or []
    template  = data.get("template") or charger_config()["parametres"]["template"]

    if not companies:
        return jsonify({"ok": False, "error": "Aucune entreprise"}), 400
    if not get_comptes_actifs():
        return jsonify({"ok": False, "error": "Aucun compte Gmail actif"}), 400

    cfg = charger_config()
    cfg["parametres"]["template"] = template
    sauver_config(cfg)

    _bulk_running[0] = True
    _bulk_state[0] = {
        "en_cours": True, "index": 0, "total": len(companies),
        "derniere": "", "envoyes": 0, "erreurs": 0, "arrete": False,
        "sans_pj":  len(get_pieces_actives()) == 0,
    }
    t = threading.Thread(target=_bulk_worker,
                         args=(companies, template, current_uid()),
                         daemon=True)
    t.start()
    return jsonify({"ok": True, "total": len(companies)})

@bp.route("/api/send-bulk-status")
def api_send_bulk_status():
    with _bulk_lock:
        return jsonify(dict(_bulk_state[0]))

@bp.route("/api/send-bulk-stop", methods=["POST"])
def api_send_bulk_stop():
    _bulk_running[0] = False
    with _bulk_lock:
        _bulk_state[0]["en_cours"] = False
        _bulk_state[0]["arrete"]   = True
    return jsonify({"ok": True})

# ------------------------------------------------------------
# GROUPES
# ------------------------------------------------------------
@bp.route("/api/groupes", methods=["GET"])
def api_groupes_list():
    cfg = charger_config()
    return jsonify({"groupes": cfg.get("groupes", [])})

@bp.route("/api/groupes", methods=["POST"])
def api_groupes_add():
    data = request.get_json() or {}
    nom     = (data.get("nom") or "").strip()
    desc    = (data.get("description") or "").strip()
    grp_id  = (data.get("id") or "").strip()

    emails_raw = data.get("emails") or []
    if isinstance(emails_raw, str):
        emails = parse_emails(emails_raw)
    else:
        emails = [str(e).strip().lower() for e in emails_raw if str(e).strip()]
        emails = [e for e in emails if "@" in e]

    if not nom:
        return jsonify({"ok": False, "error": "Nom requis"}), 400
    if not emails:
        return jsonify({"ok": False, "error": "Au moins un email valide requis"}), 400

    cfg = charger_config()
    groupes = cfg.get("groupes", [])

    if grp_id:
        for i, g in enumerate(groupes):
            if g["id"] == grp_id:
                groupes[i].update({
                    "nom": nom,
                    "emails": emails,
                    "description": desc,
                    "maj_le": maintenant_str(),
                })
                cfg["groupes"] = groupes
                sauver_config(cfg)
                return jsonify({"ok": True, "updated": True, "id": grp_id})
        return jsonify({"ok": False, "error": "Introuvable"}), 404

    new_id = f"grp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    groupes.append({
        "id":          new_id,
        "nom":         nom,
        "emails":      emails,
        "description": desc,
        "cree_le":     maintenant_str(),
    })
    cfg["groupes"] = groupes
    sauver_config(cfg)
    return jsonify({"ok": True, "created": True, "id": new_id})

@bp.route("/api/groupes/<grp_id>", methods=["DELETE"])
def api_groupes_delete(grp_id):
    cfg = charger_config()
    groupes = cfg.get("groupes", [])
    avant = len(groupes)
    groupes = [g for g in groupes if g["id"] != grp_id]
    if len(groupes) == avant:
        return jsonify({"ok": False, "error": "Introuvable"}), 404
    cfg["groupes"] = groupes
    sauver_config(cfg)
    return jsonify({"ok": True})

@bp.route("/api/groupes/<grp_id>/send", methods=["POST"])
def api_groupes_send(grp_id):
    cfg = charger_config()
    groupes = cfg.get("groupes", [])
    grp = next((g for g in groupes if g["id"] == grp_id), None)
    if not grp:
        return jsonify({"ok": False, "error": "Groupe introuvable"}), 404

    data = request.get_json() or {}
    subject = (data.get("subject") or "").strip()
    body    = (data.get("body") or "").strip()
    mode    = (data.get("mode") or "individuel").lower()
    joindre = bool(data.get("joindre_pieces", False))

    if not subject or not body:
        return jsonify({"ok": False, "error": "Objet et corps requis"}), 400

    emails = grp.get("emails", [])
    if not emails:
        return jsonify({"ok": False, "error": "Groupe vide"}), 400
    if not get_comptes_actifs():
        return jsonify({"ok": False, "error": "Aucun compte Gmail actif"}), 400

    pieces = get_pieces_actives() if joindre else []
    nom_exp = cfg["candidat"]["nom"]
    params = cfg["parametres"]
    max_retries = params["smtp_retries"]

    with _send_lock:
        delay = get_delai()
        ecoule = time.time() - _last_send_time[0]
        if ecoule < delay:
            return jsonify({
                "ok": False,
                "error": f"Attends {int(delay-ecoule)+1}s",
                "attente": int(delay-ecoule)+1,
            }), 429
        _last_send_time[0] = time.time()

    if mode == "groupe":
        ok, msg = _envoyer_un_email(
            ", ".join(emails), subject, body,
            compte_suivant(), pieces,
            nom_exp, params, max_retries,
            groupe=emails, bcc_mode=True,
        )
        nb_ok = len(emails) if ok else 0
    else:
        nb_ok = 0
        for idx_e, e in enumerate(emails):
            ok, msg = _envoyer_un_email(
                e, subject, body,
                compte_suivant(), pieces,
                nom_exp, params, max_retries,
            )
            if ok: nb_ok += 1
            if idx_e < len(emails) - 1:
                time.sleep(delay)

    with _log_send_lock:
        _send_timestamps.append(time.time())

    log = charger_log()
    log[f"[GROUPE] {grp['nom']}"] = {
        "email":      ", ".join(emails[:3]) + (f" +{len(emails)-3}" if len(emails) > 3 else ""),
        "emails":     emails,
        "envoye":     nb_ok > 0,
        "date":       maintenant_str(),
        "repondu":    False,
        "sans_pj":    not joindre,
        "groupe_nom": grp["nom"],
        "nb_envoyes": nb_ok,
        "nb_total":   len(emails),
        "mode":       mode,
    }
    sauver_log(log)

    return jsonify({
        "ok":      nb_ok > 0,
        "envoyes": nb_ok,
        "total":   len(emails),
        "message": f"{nb_ok}/{len(emails)} envoyé(s)",
    })
