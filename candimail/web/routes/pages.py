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
# SÉCURITÉ : mot de passe d'accès à l'interface
# ------------------------------------------------------------
PAGE_LOGIN = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Connexion — Candimail</title>
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
<link rel="stylesheet" href="/static/brutalist.css">
<style>
  body{ display:flex; align-items:center; justify-content:center;
        min-height:100vh; margin:0; font-family:Arial, Helvetica, sans-serif; }
  .box{ background:#fff; border:3px solid #43161C; box-shadow:8px 8px 0 #43161C;
        padding:34px 30px; width:min(400px, 92vw); border-top:8px solid #1E5AA8; }
  .box h1{ margin:0 0 6px; font-size:22px; text-transform:uppercase; }
  .box p.sub{ margin:0 0 22px; font-size:12px; color:#7A6E5B; font-weight:600; }
  label{ display:block; font-size:12px; font-weight:800; text-transform:uppercase;
         margin:14px 0 6px; }
  input{ width:100%; box-sizing:border-box; padding:10px 12px; font-size:15px;
         border:2px solid #43161C; background:#fff; }
  input:focus{ outline:none; border-color:#1E5AA8; }
  button{ width:100%; margin-top:18px; padding:12px; font-size:14px; font-weight:800;
          text-transform:uppercase; cursor:pointer; background:#1E5AA8; color:#fff;
          border:2px solid #43161C; box-shadow:4px 4px 0 #43161C;
          transition:transform .1s; }
  button:hover{ transform:translate(1px,1px); box-shadow:2px 2px 0 #43161C; }
  .msg{ margin-top:14px; font-size:13px; font-weight:700; min-height:18px; }
  .badge{ display:inline-block; background:#F2E7CE; border:2px solid #43161C;
          font-size:11px; font-weight:800; text-transform:uppercase; padding:2px 8px; }
</style>
</head>
<body>
<div class="box">
  <h1>📧 Candimail</h1>
  <p class="sub" id="sous-titre">Accès protégé</p>
  <div id="champs"></div>
  <button id="go">Entrer</button>
  <div class="msg" id="msg"></div>
  <p style="margin:18px 0 0; font-size:12px; font-weight:700; text-align:center;">
    <a href="#" id="bascule" style="color:#1E5AA8;">Créer un compte</a>
  </p>
  <p style="margin:10px 0 0; font-size:12px; font-weight:700; text-align:center;">
    <a href="/" style="color:#7A6E5B; text-decoration:none;">← Retour à la vitrine</a>
  </p>
</div>
<script>
(async () => {
  const champs = document.getElementById('champs');
  const msg    = document.getElementById('msg');
  const btn    = document.getElementById('go');
  const basc   = document.getElementById('bascule');
  let mode = 'login';      // login | register | setup
  let pret = false;        // formulaire injecté ?
  let occupe = false;      // soumission en cours ?

  function libelleBtn() {
    return (mode === 'login') ? 'Entrer' : 'Créer mon compte';
  }
  function labelMdp() {
    return (mode === 'setup' || mode === 'register')
      ? 'Mot de passe (6 car. min)' : 'Mot de passe';
  }
  const HONEY = `<input type="text" id="hp" name="website" tabindex="-1"
       autocomplete="off" aria-hidden="true"
       style="position:absolute;left:-9999px;width:1px;height:1px">`;

  function formulaireLogin() {
    champs.innerHTML = `
      <label>Email</label>
      <input type="email" id="em" autocomplete="email" required>
      <label>Mot de passe</label>
      <input type="password" id="p1" autocomplete="current-password" required>
      ${HONEY}`;
    pret = true;
  }
  function formulaireInscription() {
    champs.innerHTML = `
      <label>Email</label>
      <input type="email" id="em" autocomplete="email" required>
      <label>${labelMdp()}</label>
      <input type="password" id="p1" autocomplete="new-password"
             minlength="6" required>
      <label>Confirmer</label>
      <input type="password" id="p2" autocomplete="new-password"
             minlength="6" required>
      ${HONEY}`;
    pret = true;
  }

  // Reconstruit proprement le formulaire selon le mode courant
  function appliquerMode() {
    msg.textContent = '';
    if (mode === 'login') { formulaireLogin(); } else { formulaireInscription(); }
    btn.textContent = libelleBtn();
    basc.textContent = (mode === 'login') ? 'Créer un compte'
                                          : 'J\u2019ai déjà un compte';
    const em = document.getElementById('em');
    if (em) em.focus();
  }

  basc.addEventListener('click', e => {
    e.preventDefault();
    // Premier utilisateur : création forcée, pas d'alternative « connexion »
    if (mode === 'setup' || occupe || !pret) return;
    const emActuel = document.getElementById('em');
    const emailSauve = emActuel ? emActuel.value.trim() : '';
    mode = (mode === 'login') ? 'register' : 'login';
    appliquerMode();
    // On conserve l'email saisi d'un mode à l'autre
    if (emailSauve) document.getElementById('em').value = emailSauve;
  });

  // Détermination du mode initial
  try {
    const s = await (await fetch('/api/auth/status')).json();
    if (s.setup_necessaire) {
      mode = 'setup';
      basc.style.display = 'none';
      document.getElementById('sous-titre').innerHTML =
        'Premier utilisateur — <span class="badge">crée ton compte</span>';
      formulaireInscription();
    } else {
      formulaireLogin();
    }
    if (s.crypto_actif === false)
      msg.textContent = '⚠️ cryptography absent : secrets non chiffrés';
  } catch (e) {
    // API injoignable → on affiche quand même l'écran de connexion
    formulaireLogin();
  }
  const em0 = document.getElementById('em');
  if (em0) em0.focus();

  async function envoyer() {
    if (!pret || occupe) return;
    const emEl = document.getElementById('em');
    const p1El = document.getElementById('p1');
    const p2El = document.getElementById('p2');
    const hp   = document.getElementById('hp');
    if (!emEl || !p1El) return;
    const em = emEl.value.trim();
    const p1 = p1El.value;
    // Anti-spam : un robot remplit le champ caché → on bloque en silence
    if (hp && hp.value) { return; }
    if ((mode === 'setup' || mode === 'register') && p2El && p1 !== p2El.value) {
      msg.textContent = '❌ Les mots de passe diffèrent'; return;
    }
    if (!em || !p1) { msg.textContent = 'Saisis email et mot de passe'; return; }
    if (!/^[^@]+@[^@]+[.][^@]+$/.test(em)) {
      msg.textContent = '❌ Adresse email invalide'; return;
    }
    if ((mode === 'setup' || mode === 'register') && p1.length < 6) {
      msg.textContent = '❌ Mot de passe : 6 caractères minimum'; return;
    }
    occupe = true; btn.disabled = true; btn.textContent = '⏳';
    try {
      const r = await fetch(`/api/auth/${mode}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: em, password: p1,
                               website: (hp ? hp.value : '') })
      });
      const d = await r.json();
      if (d.ok) { window.location.href = '/app'; return; }
      if (d.setup) { location.reload(); return; }
      msg.textContent = '❌ ' + (d.error || 'Erreur');
      // Email déjà pris → retour propre à l'écran de connexion, email conservé
      if (mode === 'register' && r.status === 409) {
        mode = 'login';
        appliquerMode();
        document.getElementById('em').value = em;
        msg.textContent = '❌ ' + (d.error || 'Email déjà utilisé');
        const p1n = document.getElementById('p1');
        if (p1n) p1n.focus();
      }
    } catch (e) { msg.textContent = 'Erreur réseau'; }
    occupe = false; btn.disabled = false; btn.textContent = libelleBtn();
  }
  btn.addEventListener('click', envoyer);
  document.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !btn.disabled) envoyer();
  });
})();
</script>
</body>
</html>"""

@bp.route("/login", methods=["GET"])
def page_login():
    # Déjà connecté → accès direct
    if session.get("uid"):
        return redirect("/app")
    return PAGE_LOGIN

# ------------------------------------------------------------
# ROUTES PAGES
# ------------------------------------------------------------
@bp.route("/")
def vitrine():
    """Page vitrine publique — accessible sans connexion."""
    return render_template("vitrine.html")

@bp.route("/app")
def index():
    """Application principale — protégée par le gardien d'accès."""
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
        "Allow: /$\n"
        "Allow: /rgpd\n"
        "Allow: /cgu\n"
        "Disallow: /app\n"
        "Disallow: /cv\n"
        "Disallow: /suivi\n"
        "Disallow: /login\n"
        "Disallow: /api/\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    return Response(contenu, mimetype="text/plain")

@bp.route("/sitemap.xml")
def sitemap_xml():
    base = request.url_root.rstrip("/")
    pages = ["/", "/rgpd", "/cgu"]
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
