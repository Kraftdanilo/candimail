#!/usr/bin/env python3
"""Routes Flask — pages publiques, application, SEO (blueprint)."""
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
from candimail.web.routes.donnees import charger_cv

bp = Blueprint("pages", __name__)

# ------------------------------------------------------------
# ROUTES PAGES
# ------------------------------------------------------------
@bp.route("/")
def racine():
    """L'app s'ouvre directement sur / (la vitrine vit sur /vitrine)."""
    return redirect("/app")


@bp.route("/vitrine")
def vitrine():
    """Page vitrine publique — accessible sans connexion."""
    return render_template("vitrine.html")

@bp.route("/app")
def index():
    """Application principale."""
    return render_template("index.html", templates=TEMPLATES)

@bp.route("/favicon.ico")
def favicon():
    # Sert le favicon SVG (les navigateurs demandent .ico par défaut)
    return redirect("/static/favicon.svg", code=302)

# ------------------------------------------------------------
# SEO : robots.txt + sitemap.xml
# ------------------------------------------------------------
@bp.route("/robots.txt")
def robots_txt():
    base = request.url_root.rstrip("/")
    contenu = (
        "User-agent: *\n"
        "Allow: /vitrine\n"
        "Allow: /rgpd\n"
        "Allow: /cgu\n"
        "Disallow: /app\n"
        "Disallow: /cv\n"
        "Disallow: /suivi\n"
        "Disallow: /api/\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    return Response(contenu, mimetype="text/plain")

@bp.route("/sitemap.xml")
def sitemap_xml():
    base = request.url_root.rstrip("/")
    pages = ["/vitrine", "/rgpd", "/cgu"]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    )
    for p in pages:
        xml += f" <url><loc>{base}{p}</loc>" \
               f"<changefreq>monthly</changefreq></url>\n"
    xml += "</urlset>\n"
    return Response(xml, mimetype="application/xml")

@bp.route("/rgpd")
def page_rgpd():
    return render_template("rgpd.html", annee=datetime.now().year)

@bp.route("/cgu")
def page_cgu():
    return render_template("cgu.html", annee=datetime.now().year)

# ------------------------------------------------------------
# PAGE 404 PERSONNALISÉE
# ------------------------------------------------------------
@bp.app_errorhandler(404)
def page_404(e):
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "error": "Ressource introuvable"}), 404
    return render_template("404.html"), 404
@bp.route("/suivi")
def suivi():
    log = charger_log()
    items = sorted(log.items(), key=lambda x: x[1].get("date", ""), reverse=True)
    total     = len(items)
    envoyes   = len([x for x in items if x[1].get("envoye")])
    repondus  = len([x for x in items if x[1].get("repondu")])
    bounces   = len([x for x in items if x[1].get("bounce")])
    echecs    = total - envoyes

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

    return render_template(
        "suivi.html",
        items=items, total=total, envoyes=envoyes,
        repondus=repondus, bounces=bounces, echecs=echecs,
        chart_data=json.dumps({
            "envoyes":  envoyes, "echecs": echecs,
            "repondus": repondus, "bounces": bounces,
            "jours":    jours,
        }, ensure_ascii=False),
    )

@bp.route("/cv")
def cv_page():
    data = charger_cv()
    return render_template("cv.html", cv=data)

# ------------------------------------------------------------
