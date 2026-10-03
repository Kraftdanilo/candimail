#!/usr/bin/env python3
"""
Service SMTP — envoi d'emails via Gmail (SSL) : pièces jointes,
tentatives (retries) et rotation de comptes.
"""
import socket, smtplib, ssl, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid

from candimail.core import crypto
from candimail.core.noyau import (charger_config, _config_globale, parse_emails,
                                  compte_suivant, get_pieces_actives,
                                  current_uid, _pieces)


# ============================================================
# ENVOI SMTP
# ============================================================
def _envoyer_un_email(dest, subject, body, compte, pieces,
                       nom_exp, params, max_retries,
                       groupe=None, bcc_mode=False):
    """Envoie un email unitaire. bcc_mode=True : tous en Cci (invisible)."""
    gmail_user = compte["email"]
    gmail_pass = crypto.dechiffrer(compte["password"])
    dernier_msg = ""

    for tentative in range(1, max_retries + 1):
        try:
            msg = MIMEMultipart()
            msg["From"]       = f"{nom_exp} <{gmail_user}>"
            msg["Date"]       = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain=gmail_user.split("@")[-1])
            msg["Subject"]    = subject

            if bcc_mode and groupe and len(groupe) > 1:
                # ✅ Le "À" est l'expéditeur, tous les autres en Cci
                msg["To"]  = f"{nom_exp} <{gmail_user}>"
                msg["Bcc"] = ", ".join(groupe)
            else:
                msg["To"] = dest

            msg.attach(MIMEText(body, "plain", "utf-8"))

            for p in pieces:
                try:
                    with open(p["chemin"], "rb") as f:
                        pdf = MIMEApplication(f.read(), _subtype="pdf")
                        pdf.add_header("Content-Disposition", "attachment",
                                       filename=p["nom_original"])
                        msg.attach(pdf)
                except Exception as e:
                    print(f"[PJ] {p['nom_original']}: {e}")

            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                                  context=ctx, timeout=params["smtp_timeout"]) as srv:
                srv.login(gmail_user, gmail_pass)
                srv.send_message(msg)

            suffixe = f"({len(pieces)} PJ)" if pieces else "(sans PJ)"
            if bcc_mode and groupe:
                suffixe = f"({len(groupe)} Cci, {len(pieces)} PJ)"
            return True, f"Envoyé via {gmail_user} {suffixe}"

        except smtplib.SMTPAuthenticationError:
            return False, f"Auth refusée pour {gmail_user}"
        except smtplib.SMTPRecipientsRefused:
            return False, "Destinataire refusé"
        except (smtplib.SMTPServerDisconnected, socket.timeout, TimeoutError):
            dernier_msg = "Réseau"
            if tentative < max_retries:
                time.sleep(2 ** tentative)
                continue
            return False, f"Réseau instable après {max_retries} essais"
        except Exception as e:
            return False, f"{type(e).__name__} — {str(e)[:120]}"
    return False, f"Échec après {max_retries} tentatives"

def envoyer_email(dest, subject, body, max_retries=None, compte=None,
                  pieces_selectionnees=None, mode_groupe=False, uid=None):
    """
    dest : email unique OU liste d'emails séparés par ',' ';' ou '\\n'
    mode_groupe :
      - False (défaut) → 1 email PAR destinataire (personnalisé)
      - True          → 1 seul email avec tous en Cci (invisible)
    """
    cfg = charger_config(uid)   # utilisateur : nom_exp
    params = _config_globale()["parametres"]
    if max_retries is None:
        max_retries = params["smtp_retries"]

    if compte is None:
        compte = compte_suivant()
    if not compte:
        return False, "Aucun compte Gmail actif"

    emails = parse_emails(dest)
    if not emails:
        return False, "Aucun destinataire valide"

    nom_exp = cfg["candidat"]["nom"] or "Candidat"

    if pieces_selectionnees is None:
        pieces = get_pieces_actives(uid)
    else:
        pieces = [p for k, p in
                  _pieces.get(int(uid if uid is not None else current_uid() or 0), {}).items()
                  if k in pieces_selectionnees]

    # Mode groupé BCC
    if mode_groupe:
        return _envoyer_un_email(
            ", ".join(emails), subject, body, compte, pieces,
            nom_exp, params, max_retries,
            groupe=emails, bcc_mode=True,
        )

    # Mode individuel
    total_ok = 0
    for e in emails:
        ok, msg = _envoyer_un_email(
            e, subject, body, compte, pieces,
            nom_exp, params, max_retries,
        )
        if ok:
            total_ok += 1

    if total_ok == len(emails):
        return True, f"{total_ok} envoi(s) réussi(s)"
    elif total_ok > 0:
        return True, f"{total_ok}/{len(emails)} envoi(s) réussi(s)"
    return False, "Aucun envoi réussi"
