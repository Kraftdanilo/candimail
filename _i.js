
/* ENTREPRISES */
let COMPANIES = [
  { cat:'grands', name:'SOGEA-SATOM (VINCI)', email:'sogea-satom.cote-ivoire@vinci-construction.com',
    context:`Membre du groupe VINCI, SOGEA-SATOM est un acteur de référence des travaux publics en Côte d'Ivoire. C'est précisément cette expertise sur les grands projets d'infrastructure routière et d'ouvrages d'art qui motive ma candidature.` },
  { cat:'grands', name:'PFO Africa', email:'recrutement@pfoafrica.com',
    context:`Je suis avec un vif intérêt les activités de PFO Africa, notamment votre chantier de réhabilitation de l'axe San-Pédro – Soubré. Résidant à Soubré même, je vois quotidiennement l'avancement de vos travaux.` },
  { cat:'grands', name:'PFO Construction', email:'recrutement@pfo-construction.com',
    context:`Filiale du groupe PFO Africa, PFO Construction incarne l'excellence ivoirienne dans le secteur du bâtiment et des travaux publics.` },
  { cat:'grands', name:'Bouygues Travaux Publics', email:'byes.ci@bouygues-es.com',
    context:`Rejoindre Bouygues Travaux Publics représenterait pour moi une opportunité exceptionnelle de me former aux standards internationaux du génie civil.` },
  { cat:'grands', name:'SICMA', email:'c2a@aviso.ci',
    context:`Le Groupe SICMA est reconnu pour son engagement en faveur de la formation et de l'insertion professionnelle des jeunes ivoiriens.` },
  { cat:'grands', name:'SETAO', email:'setao@setao.ci',
    context:`Membre du groupe Bouygues, SETAO est l'un des acteurs historiques du BTP en Côte d'Ivoire.` },
  { cat:'grands', name:'RAZEL', email:'recrutement.razel.ci@razel.fr',
    context:`La réputation de RAZEL dans les travaux publics et le génie civil n'est plus à démontrer.` },
  { cat:'grands', name:'COLAS Afrique', email:'colasci@colasafrique.com',
    context:`Spécialiste mondial des routes, COLAS Afrique est une référence dans la construction et l'entretien d'infrastructures routières.` },
  { cat:'grands', name:'H2C Africa', email:'recrutement@h2c-africa.com',
    context:`Votre implantation à San-Pédro et votre dynamisme dans le secteur du BTP en Côte d'Ivoire retiennent toute mon attention.` },
  { cat:'pme', name:'B-Constructions (B-Group)', email:'info@b-groupci.com',
    context:`Depuis votre création en 2015, B-Constructions s'est imposée comme un acteur dynamique du bâtiment et des travaux publics.` },
  { cat:'pme', name:'S.I.E TRAVAUX', email:'me_ngoran_ake@yahoo.fr',
    context:`L'expertise de la S.I.E TRAVAUX dans l'adduction en eau potable et l'assainissement est un domaine technique qui m'intéresse particulièrement.` },
  { cat:'pme', name:'Magnon Construction & TP', email:'recrutements@mctp.ci',
    context:`Vous recherchez régulièrement des profils d'ingénieurs travaux et d'études. C'est précisément l'orientation que je souhaite donner à ma carrière.` },
  { cat:'pme', name:'SOTIC', email:'info@sotici.com',
    context:`SOTIC s'est construit une solide réputation dans le bâtiment et l'ingénierie en Côte d'Ivoire.` },
  { cat:'pme', name:'SOGENAM-CI', email:'sogenam@sogenam.com',
    context:`La double casquette de SOGENAM — génie civil et négoce de matériaux — offre une vision complète du secteur de la construction.` },
  { cat:'pme', name:'CORIAS', email:'secretariatcorias@gmail.com',
    context:`Vous proposez un stage de perfectionnement au sein de votre Direction Technique, avec des missions de suivi de chantiers, appels d'offres et contrôle qualité.` },
  { cat:'pme', name:"MATRELEC Côte d'Ivoire", email:'secretariat@matrelec-ci.com',
    context:`Votre offre de stage en Génie Civil à Marcory correspond parfaitement à mes compétences actuelles de licencié.` },
  { cat:'pme', name:'BEESHOP GENIUS', email:'meyerlansky225@gmail.com',
    context:`La dimension technico-commerciale du BTP est une facette du métier que je souhaite découvrir.` },
  { cat:'pme', name:'OCEANE INTERNATIONAL', email:'oceaneinternational@gmail.com',
    context:`Votre structure basée à Cocody recherche un stagiaire en Génie Civil Bâtiment.` },
  { cat:'pme', name:'ITB Group', email:'itbgroupci@gmail.com',
    context:`La double approche d'ITB Group — architecture et génie civil — rejoint ma propre ambition de carrière.` },
  { cat:'pme', name:'EGTP SARL', email:'egtp.btp@gmail.com',
    context:`Votre implantation dans la région des Montagnes (Man) témoigne d'une capacité à intervenir sur des terrains complexes.` },
  { cat:'pme', name:'UNISERV BTP', email:'recrutement@uniservci.net',
    context:`Votre couverture nationale et votre expérience depuis 2013 dans le bâtiment et le génie civil vous positionnent comme un partenaire de confiance.` },
  { cat:'pme', name:'Porteo BTP', email:'recrutement@porteo-btp.com',
    context:`Je suis attentif à vos projets d'asphaltage et de réhabilitation routière, notamment dans la région de Korhogo.` },
  { cat:'pme', name:'ETRAKO-BTP', email:'etrakobtpsarl@gmail.com',
    context:`ETRAKO-BTP fait partie des entreprises dynamiques qui contribuent au développement du Nord ivoirien.` },
  { cat:'pme', name:"NEUCE Côte d'Ivoire", email:'cote.ivoire@neuce.com',
    context:`NEUCE Côte d'Ivoire combine construction et travaux publics, avec une présence régionale notamment à Daloa.` },
  { cat:'port', name:'Port Autonome de San-Pédro (PASP)', email:'pasp@pasp.ci',
    context:`Le Port Autonome de San-Pédro, classé parmi les plus performants de la zone UEMOA, est un acteur stratégique du développement économique ivoirien.` },
  { cat:'port', name:'PASP — Direction Stratégie', email:'pzahabi@pasp.ci',
    context:`Je me permets de vous contacter directement, en votre qualité de responsable de la Direction Stratégie du PASP.` },
  { cat:'port', name:'PASP — Partenariats Public-Privé', email:'kkoffi@pasp.ci',
    context:`Les Partenariats Public-Privé sont au cœur du développement des infrastructures portuaires modernes.` },
  { cat:'port', name:'IDM', email:'nziakissivictorine@yahoo.fr',
    context:`Votre entreprise IDM intervient dans le BTP à San-Pédro, une ville en pleine expansion.` },
  { cat:'port', name:'Groupe Cacao', email:'groupecacao@gmail.com',
    context:`Vos activités à la croisée du BTP et de la gestion immobilière m'intéressent.` },
  { cat:'port', name:'San Pedro Truck (Groupe CIERA)', email:'sanpedrotrucks007@gmail.com',
    context:`La logistique et le transport sont le prolongement naturel du BTP.` },
  { cat:'port', name:'LBTP San-Pédro', email:'lbtp@aviso.ci',
    context:`Le Laboratoire du Bâtiment et des Travaux Publics est une référence dans le contrôle qualité des matériaux et des ouvrages.` },
  { cat:'port', name:"Les Grands Moulins d'Abidjan", email:'recrutement@gma.ci',
    context:`Les Grands Moulins d'Abidjan sont une entreprise industrielle majeure, et votre présence à San-Pédro m'intéresse.` },
];

const CATEGORIES = {
  grands:'🏢 Grands groupes', pme:'🏗️ PME dynamiques', port:'⚓ San-Pédro & Port',
};

/* ÉTAT */
let serverLog = {};
let TEMPLATES_DISPO = {};
let piecesActives = 0;
let rateLimit = { utilises: 0, max: 30, ok: true };
let activeFilter = 'all';
let searchQuery = '';
let bulkPollTimer = null;
let currentSendCompany = null;
let templatesCache = [];
let predefinis = {};
let groupesCache = [];

/* STATUS */
async function refreshStatus() {
  try {
    const r = await fetch('/api/status');
    if (r.status === 401) { window.location.href = '/login'; return; }
    const data = await r.json();
    serverLog = data.log || {};
    piecesActives = data.pieces_count || 0;
    rateLimit = data.rate_limit || rateLimit;

    const cvBadge = document.getElementById('cv-badge');
    if (piecesActives > 0) {
      cvBadge.textContent = `📎 ${piecesActives} pièce(s)`;
      cvBadge.className = 'badge-cv ok';
    } else {
      cvBadge.textContent = '📎 0 pièce';
      cvBadge.className = 'badge-cv';
    }

    const cptBadge = document.getElementById('comptes-badge');
    const nb = data.comptes_actifs || 0;
    cptBadge.textContent = `📧 ${nb}`;
    cptBadge.className = 'badge-cv ' + (nb > 0 ? 'ok' : 'warn');
    const sideCpt = document.getElementById('side-comptes');
    if (sideCpt) sideCpt.textContent = nb;

    const rlBadge = document.getElementById('rate-badge');
    rlBadge.textContent = `⏱️ ${rateLimit.utilises}/${rateLimit.max}`;
    rlBadge.className = 'badge-cv ' + (rateLimit.ok ? 'ok' : 'warn');

    const warn = document.getElementById('pj-warning');
    if (warn) warn.style.display = piecesActives === 0 ? 'block' : 'none';
    const pjWarn = document.getElementById('pj-warn-badge');
    if (pjWarn) pjWarn.style.display = piecesActives === 0 ? '' : 'none';

    updateStats();
    render();
  } catch (e) { console.error(e); }
}

/* CONFIG */
async function loadConfig() {
  try {
    const r = await fetch('/api/config');
    const cfg = await r.json();
    const cand = cfg.candidat || {};
    const params = cfg.parametres || {};
    document.getElementById('cfg-nom').value      = cand.nom || '';
    document.getElementById('cfg-tel').value      = cand.tel || '';
    document.getElementById('cfg-email').value    = cand.email || '';
    document.getElementById('cfg-ville').value    = cand.ville || '';
    document.getElementById('cfg-diplome').value  = cand.diplome || '';
    document.getElementById('cfg-spec').value     = cand.spec || '';

    if (!params.delai_aleatoire) {
      document.getElementById('cfg-delai').value = params.delai_secondes || 40;
    }
    document.getElementById('cfg-delai-alea').checked = !!params.delai_aleatoire;
    document.getElementById('cfg-maxh').value = params.max_par_heure || 100;

    updateHeaderSub();
    TEMPLATES_DISPO = cfg.templates_dispo || {};
    renderComptes(cfg.comptes || []);
  } catch (e) { console.error(e); }
}

function updateHeaderSub() {
  const nom   = document.getElementById('cfg-nom').value || 'HOBA Koutoua Daniel';
  const ville = document.getElementById('cfg-ville').value || 'Soubré';
  document.getElementById('header-sub').textContent = `${nom} · ${ville}, Côte d'Ivoire`;
}

async function saveCandidatConfig() {
  const payload = {
    candidat: {
      nom:     document.getElementById('cfg-nom').value.trim(),
      tel:     document.getElementById('cfg-tel').value.trim(),
      email:   document.getElementById('cfg-email').value.trim(),
      ville:   document.getElementById('cfg-ville').value.trim(),
      diplome: document.getElementById('cfg-diplome').value.trim(),
      spec:    document.getElementById('cfg-spec').value.trim(),
    },
    parametres: {
      template: document.getElementById('cfg-template').value,
    }
  };
  try {
    const r = await fetch('/api/config', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    if (data.ok) {
      toast('Configuration enregistrée', 'ok');
      updateHeaderSub();
    }
  } catch (e) { toast('Erreur réseau', 'err'); }
}

/* COMPTES */
function renderComptes(comptes) {
  const el = document.getElementById('comptes-list');
  const actifs = comptes.filter(c => c.actif).length;
  document.getElementById('comptes-count').textContent = `${actifs} actif(s)`;
  if (!comptes.length) {
    el.innerHTML = `<div class="empty-box">⚠️ Aucun compte Gmail configuré.</div>`;
    return;
  }
  const tplOptions = Object.entries(TEMPLATES_DISPO)
    .map(([id, t]) => `<option value="${escapeHtml(id)}">${escapeHtml(t.nom || id)}</option>`)
    .join('');
  el.innerHTML = comptes.map(c => `
    <div class="compte-row ${c.actif ? 'active' : 'inactive'}">
      <span style="font-size:18px">${c.actif ? '✅' : '⏸️'}</span>
      <div style="flex:1;min-width:180px">
        <div style="font-weight:700;font-size:13px">${escapeHtml(c.email)}
          <span style="font-size:10px;font-weight:800;text-transform:uppercase;
                color:${c.actif ? '#1E7A3C' : 'var(--muted)'}">${c.actif ? '• actif' : '• en pause'}</span>
        </div>
        <div style="font-size:11px;color:var(--muted)">
          ${c.has_password
            ? `🔑 <span class="compte-mdp" data-index="${c.index}" data-email="${escapeHtml(c.email)}"
                   title="Cliquer pour afficher/masquer le mot de passe d'application (16 caractères)"
                   style="cursor:pointer;user-select:all;font-family:Consolas,monospace;
                          letter-spacing:1px;background:#F2E7CE;border:1px solid var(--border);
                          padding:1px 6px;border-radius:4px;">••••••••••••••••</span>`
            : '❌ mot de passe manquant'}
        </div>
      </div>
      <select class="compte-tpl" data-index="${c.index}" title="Message utilisé par ce compte"
              style="padding:6px 8px;font-size:12px;font-weight:600;border:2px solid var(--border);
                     background:#fff;max-width:220px">
        <option value="" ${!c.template ? 'selected' : ''}>📨 Message global</option>
        ${tplOptions}
      </select>
      <button class="btn small" data-action="test-compte" data-email="${escapeHtml(c.email)}">🧪 Tester</button>
      <button class="btn small" data-action="reveal-compte" data-index="${c.index}">👁️ Voir</button>
      <button class="btn small" data-action="toggle-compte" data-index="${c.index}">
        ${c.actif ? '⏸️' : '▶️'}
      </button>
      <button class="btn small danger" data-action="delete-compte" data-index="${c.index}">🗑️</button>
    </div>
  `).join('');

  el.querySelectorAll('.compte-tpl').forEach(sel => {
    sel.addEventListener('change', async () => {
      const r = await fetch(`/api/comptes/${sel.dataset.index}/template`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ template: sel.value })
      });
      const d = await r.json();
      if (d.ok) {
        const label = sel.selectedOptions[0].textContent;
        toast(`${label} pour ce compte`, 'ok');
      } else toast(d.error || 'Erreur', 'err');
    });
  });

  el.querySelectorAll('[data-action="test-compte"]').forEach(b => {
    b.addEventListener('click', async () => {
      const orig = b.textContent; b.textContent = '⏳'; b.disabled = true;
      try {
        const r = await fetch('/api/comptes/test', { method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ email: b.dataset.email })
        });
        const data = await r.json();
        toast(data.message || data.error, data.ok ? 'ok' : 'err');
      } catch (e) { toast('Erreur réseau', 'err'); }
      b.textContent = orig; b.disabled = false;
    });
  });
  el.querySelectorAll('[data-action="toggle-compte"]').forEach(b => {
    b.addEventListener('click', async () => {
      await fetch(`/api/comptes/${b.dataset.index}/toggle`, { method:'POST' });
      await loadConfig(); await refreshStatus();
    });
  });
  el.querySelectorAll('[data-action="delete-compte"]').forEach(b => {
    b.addEventListener('click', async () => {
      if (!confirm('Supprimer ce compte ?')) return;
      await fetch(`/api/comptes/${b.dataset.index}`, { method:'DELETE' });
      await loadConfig(); await refreshStatus();
    });
  });
  el.querySelectorAll('[data-action="reveal-compte"]').forEach(b => {
    b.addEventListener('click', () => afficherIdentifiantsOnglet(b));
  });

  // ── Mot de passe 16 car. affiché en ligne dans le dashboard (cliquer pour révéler) ──
  el.querySelectorAll('.compte-mdp').forEach(s => {
    s.addEventListener('click', async () => {
      if (s.dataset.mdp) {                       // déjà chargé → basculer masqué/visible
        s.textContent = s.textContent.startsWith('•') ? s.dataset.mdp : '•'.repeat(16);
        return;
      }
      const old = s.textContent; s.textContent = '⏳';
      try {
        const r = await fetch(`/api/comptes/${s.dataset.index}/reveal`, { method:'POST' });
        const d = await r.json();
        if (!d.ok) { s.textContent = old; toast('❌ ' + (d.error || 'Erreur'), 'err'); return; }
        s.dataset.mdp = d.password;
        s.textContent = d.password;
        s.title = d.longueur === 16
          ? '✅ 16 caractères — mot de passe d\'application correct'
          : `⚠️ ${d.longueur} caractères — ce n\'est pas un mot de passe d\'application`;
        toast(d.longueur === 16 ? '✅ 16 caractères — format correct'
                                : `⚠️ ${d.longueur} caractères`, d.longueur === 16 ? 'ok' : 'err');
      } catch (e) { s.textContent = old; toast('❌ Erreur réseau', 'err'); }
    });
  });
}

// ── Ouvre les identifiants dans un NOUVEL ONGLET (vérification visuelle) ──
async function afficherIdentifiantsOnglet(btn) {
  const libelle = btn.textContent;
  btn.disabled = true; btn.textContent = '⏳ Chargement…';
  try {
    const r = await fetch(`/api/comptes/${btn.dataset.index}/reveal`, { method:'POST' });
    const d = await r.json();
    if (!d.ok) { toast('❌ ' + (d.error || 'Erreur'), 'err'); return; }

    const ok16 = d.longueur === 16;
    const html = `<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<title>Identifiants — ${d.email}</title>
<style>
 body{font-family:Arial,Helvetica,sans-serif;display:flex;align-items:center;
      justify-content:center;min-height:100vh;margin:0;background:#F2E7CE;}
 .box{background:#fff;border:3px solid #43161C;box-shadow:8px 8px 0 #43161C;
      padding:30px 28px;width:min(460px,92vw);border-top:8px solid #1E5AA8;}
 h1{margin:0 0 4px;font-size:20px;text-transform:uppercase;}
 p.sub{margin:0 0 20px;font-size:12px;color:#7A6E5B;font-weight:600;}
 label{display:block;font-size:11px;font-weight:800;text-transform:uppercase;margin:14px 0 4px;}
 .val{border:2px solid #43161C;padding:10px 12px;font-size:15px;background:#F2E7CE;
      user-select:all;word-break:break-all;}
 .mdp{font-family:Consolas,monospace;font-size:18px;letter-spacing:3px;}
 .etat{margin:16px 0 0;font-size:13px;font-weight:700;}
 button{margin-top:18px;width:100%;padding:10px;font-weight:800;cursor:pointer;
        background:#1E5AA8;color:#fff;border:2px solid #43161C;}
</style></head><body><div class="box">
 <h1>🔑 Identifiants du compte</h1>
 <p class="sub">Vérification — mot de passe d'application Gmail</p>
 <label>Compte Gmail</label>
 <div class="val">${d.email}</div>
 <label>Mot de passe d'application</label>
 <div class="val mdp">${d.password}</div>
 <p class="etat">${ok16
   ? '✅ 16 caractères — format correct'
   : `⚠️ ${d.longueur} caractères — ce n'est pas un mot de passe d'application (il doit faire exactement 16 caractères)`}</p>
 <button onclick="window.close()">Fermer cet onglet</button>
</div></body></html>`;

    const win = window.open('', '_blank');
    if (win) {
      win.document.write(html);
      win.document.close();
    } else {
      // Popup bloqué → repli sur le modal dans la page courante
      afficherIdentifiants(d.email, d.password, d.longueur);
    }
  } catch (e) { toast('❌ Erreur réseau', 'err'); }
  // Restauration garantie du bouton, même en cas d'erreur
  btn.disabled = false; btn.textContent = libelle;
}

// ── Panneau de vérification des identifiants (Gmail + mot de passe 16 car.) ──
function afficherIdentifiants(email, mdp, longueur) {
  let ov = document.getElementById('ov-identifiants');
  if (!ov) {
    ov = document.createElement('div');
    ov.id = 'ov-identifiants';
    ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.55);'
      + 'display:flex;align-items:center;justify-content:center;z-index:9999;';
    document.body.appendChild(ov);
  }
  const ok16 = (longueur === 16);
  ov.innerHTML = `
    <div style="background:#fff;border:3px solid #43161C;box-shadow:8px 8px 0 #43161C;
                padding:26px 24px;width:min(420px,92vw);border-top:8px solid #1E5AA8;">
      <h2 style="margin:0 0 4px;font-size:17px;text-transform:uppercase;">🔑 Identifiants du compte</h2>
      <p style="margin:0 0 16px;font-size:12px;color:#7A6E5B;font-weight:600;">
        Vérification — mot de passe d'application Gmail</p>
      <label style="display:block;font-size:11px;font-weight:800;text-transform:uppercase;">Compte Gmail</label>
      <div style="border:2px solid #43161C;padding:8px 10px;font-size:14px;margin:4px 0 12px;
                  user-select:all;background:#F2E7CE;">${escapeHtml(email)}</div>
      <label style="display:block;font-size:11px;font-weight:800;text-transform:uppercase;">
        Mot de passe d'application (16 caractères)</label>
      <div style="border:2px solid #43161C;padding:8px 10px;font-size:16px;letter-spacing:2px;
                  margin:4px 0 8px;user-select:all;background:#F2E7CE;
                  font-family:Consolas,monospace;word-break:break-all;">${escapeHtml(mdp)}</div>
      <p style="margin:0 0 14px;font-size:12px;font-weight:700;">
        ${ok16 ? '✅ 16 caractères — format correct'
               : `⚠️ ${longueur} caractères — ce n\u2019est pas un mot de passe d\u2019application\n                     (il doit faire exactement 16 caractères)`.replace(/\n +/, ' ')}
      </p>
      <div style="display:flex;gap:8px;">
        <button id="cop-mdp" style="flex:1;padding:10px;font-weight:800;cursor:pointer;
                background:#1E5AA8;color:#fff;border:2px solid #43161C;">📋 Copier</button>
        <button id="ferm-idf" style="flex:1;padding:10px;font-weight:800;cursor:pointer;
                background:#fff;border:2px solid #43161C;">Fermer</button>
      </div>
    </div>`;
  ov.querySelector('#ferm-idf').onclick = () => ov.remove();
  ov.addEventListener('click', e => { if (e.target === ov) ov.remove(); });
  ov.querySelector('#cop-mdp').onclick = async () => {
    try { await navigator.clipboard.writeText(mdp); toast('📋 Mot de passe copié', 'ok'); }
    catch (e) { toast('❌ Copie impossible', 'err'); }
  };
}

async function addCompte() {
  const email = document.getElementById('new-email').value.trim();
  const password = document.getElementById('new-password').value.trim();
  if (!email || !password) { toast('Email et mot de passe requis', 'err'); return; }
  const btn = document.getElementById('btn-add-compte');
  btn.disabled = true; btn.textContent = '⏳';
  try {
    const r = await fetch('/api/comptes', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    });
    const data = await r.json();
    if (data.ok) {
      toast(data.updated ? 'Mis à jour' : 'Ajouté', 'ok');
      document.getElementById('new-email').value = '';
      document.getElementById('new-password').value = '';
      await loadConfig(); await refreshStatus();
    } else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
  btn.disabled = false; btn.textContent = '+ Ajouter';
}

/* PIÈCES */
async function loadPieces() {
  try {
    const r = await fetch('/api/pieces');
    const data = await r.json();
    renderPieces(data.pieces || []);
  } catch (e) { console.error(e); }
}

function renderPieces(pieces) {
  const el = document.getElementById('pieces-list');
  const actives = pieces.filter(p => p.actif).length;
  document.getElementById('pieces-count').textContent = `${actives} active(s)`;
  if (!pieces.length) {
    el.innerHTML = `<div class="empty-box">⚠️ Aucune pièce jointe.</div>`;
    return;
  }
  el.innerHTML = pieces.map(p => `
    <div class="piece-item ${p.actif ? '' : 'inactive'}">
      <input type="checkbox" ${p.actif ? 'checked' : ''}
             data-action="toggle-piece" data-id="${escapeHtml(p.id)}"
             style="width:18px;height:18px;accent-color:var(--ok);cursor:pointer">
      <div style="flex:1;min-width:0">
        <div style="font-weight:600;font-size:13px">📄 ${escapeHtml(p.nom_original)}</div>
        <div style="font-size:11px;color:var(--muted)">${p.taille_kb} Ko</div>
      </div>
      <button class="btn small danger" data-action="del-piece" data-id="${escapeHtml(p.id)}">🗑️</button>
    </div>
  `).join('');

  el.querySelectorAll('[data-action="toggle-piece"]').forEach(cb => {
    cb.addEventListener('change', async () => {
      await fetch(`/api/pieces/${cb.dataset.id}/toggle`, { method:'POST' });
      await loadPieces(); await refreshStatus();
    });
  });
  el.querySelectorAll('[data-action="del-piece"]').forEach(b => {
    b.addEventListener('click', async () => {
      if (!confirm('Supprimer ce fichier ?')) return;
      await fetch(`/api/pieces/${b.dataset.id}`, { method:'DELETE' });
      await loadPieces(); await refreshStatus();
    });
  });
}

async function uploadPieces(files) {
  let nb = 0;
  for (const file of files) {
    if (!file.name.toLowerCase().endsWith('.pdf')) continue;
    const form = new FormData();
    form.append('fichier', file);
    try {
      const r = await fetch('/api/pieces', { method:'POST', body: form });
      const data = await r.json();
      if (data.ok) nb++;
    } catch (e) {}
  }
  await loadPieces(); await refreshStatus();
  if (nb > 0) toast(`${nb} fichier(s) ajouté(s)`, 'ok');
}

/* TEMPLATES */
const CAT_ICONS = { candidature:'💼', parents:'👨‍👩‍👧', collegues:'👥', amis:'🎉', autre:'📌' };

async function loadTemplates() {
  try {
    const r = await fetch('/api/templates');
    const data = await r.json();
    templatesCache = data.templates || [];
    const r2 = await fetch('/api/config');
    const cfg = await r2.json();
    predefinis = {};
    for (const [k, v] of Object.entries(cfg.templates_dispo || {})) {
      if (v.predefini) predefinis[k] = v;
    }
    renderTemplates();
    populateTemplateSelects();
  } catch (e) { console.error(e); }
}

function renderTemplates() {
  const el = document.getElementById('tpl-list');
  const total = templatesCache.length + Object.keys(predefinis).length;
  document.getElementById('tpl-count').textContent = total;

  if (!templatesCache.length) {
    el.innerHTML = `<div class="empty-box">
      Aucun message perso. Les prédéfinis restent disponibles dans les menus.
    </div>`;
    return;
  }
  el.innerHTML = templatesCache.map(t => `
    <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;
                background:#FBF6EA;border:1px solid var(--border);border-radius:8px;flex-wrap:wrap">
      <span style="font-size:20px">${CAT_ICONS[t.categorie] || '📝'}</span>
      <div style="flex:1;min-width:180px">
        <div style="font-weight:600;font-size:14px">${escapeHtml(t.nom)}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:2px;
                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap">
          ${escapeHtml(t.objet)}
        </div>
      </div>
      <button class="btn small" data-action="edit-tpl" data-id="${escapeHtml(t.id)}">✏️</button>
      <button class="btn small" data-action="dup-tpl" data-id="${escapeHtml(t.id)}">📋</button>
      <button class="btn small danger" data-action="del-tpl" data-id="${escapeHtml(t.id)}">🗑️</button>
    </div>
  `).join('');

  el.querySelectorAll('[data-action="edit-tpl"]').forEach(b => {
    b.addEventListener('click', () => openEditTpl(b.dataset.id));
  });
  el.querySelectorAll('[data-action="dup-tpl"]').forEach(b => {
    b.addEventListener('click', async () => {
      await fetch(`/api/templates/${b.dataset.id}/duplicate`, { method:'POST' });
      await loadTemplates();
      toast('Template dupliqué', 'ok');
    });
  });
  el.querySelectorAll('[data-action="del-tpl"]').forEach(b => {
    b.addEventListener('click', async () => {
      const t = templatesCache.find(x => x.id === b.dataset.id);
      if (!confirm(`Supprimer "${t.nom}" ?`)) return;
      await fetch(`/api/templates/${b.dataset.id}`, { method:'DELETE' });
      await loadTemplates();
      toast('Supprimé', 'ok');
    });
  });
}

function populateTemplateSelects() {
  const html = [];
  if (templatesCache.length) {
    html.push('<optgroup label="✨ Mes messages">');
    templatesCache.forEach(t => {
      html.push(`<option value="${escapeHtml(t.id)}">${CAT_ICONS[t.categorie] || '📝'} ${escapeHtml(t.nom)}</option>`);
    });
    html.push('</optgroup>');
  }
  html.push('<optgroup label="📚 Prédéfinis">');
  for (const [k, v] of Object.entries(predefinis)) {
    html.push(`<option value="${escapeHtml(k)}">${escapeHtml(v.nom)}</option>`);
  }
  html.push('</optgroup>');

  ['cfg-template', 'custom-template', 'grp-send-template'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (id === 'grp-send-template') {
      el.innerHTML = '<option value="">— Message libre —</option>' + html.join('');
    } else {
      el.innerHTML = html.join('');
    }
  });
}

function openNewTpl() {
  document.getElementById('tpl-id').value = '';
  document.getElementById('tpl-nom').value = '';
  document.getElementById('tpl-categorie').value = 'candidature';
  document.getElementById('tpl-objet').value = '';
  document.getElementById('tpl-corps').value = '';
  document.getElementById('tpl-modal-title').textContent = '📝 Nouveau message';
  document.getElementById('tpl-modal').classList.add('visible');
}

function openEditTpl(id) {
  const t = templatesCache.find(x => x.id === id);
  if (!t) return;
  document.getElementById('tpl-id').value = t.id;
  document.getElementById('tpl-nom').value = t.nom;
  document.getElementById('tpl-categorie').value = t.categorie || 'autre';
  document.getElementById('tpl-objet').value = t.objet;
  document.getElementById('tpl-corps').value = t.corps;
  document.getElementById('tpl-modal-title').textContent = `✏️ Éditer : ${t.nom}`;
  document.getElementById('tpl-modal').classList.add('visible');
}

function closeTplModal() {
  document.getElementById('tpl-modal').classList.remove('visible');
}

async function saveTpl() {
  const id    = document.getElementById('tpl-id').value;
  const nom   = document.getElementById('tpl-nom').value.trim();
  const cat   = document.getElementById('tpl-categorie').value;
  const objet = document.getElementById('tpl-objet').value.trim();
  const corps = document.getElementById('tpl-corps').value;
  if (!nom || !objet || !corps) { toast('Champs requis', 'err'); return; }
  try {
    const r = await fetch('/api/templates', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ id, nom, categorie: cat, objet, corps })
    });
    const data = await r.json();
    if (data.ok) {
      toast(id ? 'Mis à jour' : 'Créé', 'ok');
      closeTplModal();
      await loadTemplates();
    } else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
}

/* GROUPES */
async function loadGroupes() {
  try {
    const r = await fetch('/api/groupes');
    const data = await r.json();
    groupesCache = data.groupes || [];
    renderGroupes();
  } catch (e) { console.error(e); }
}

function renderGroupes() {
  const el = document.getElementById('groupes-list');
  document.getElementById('groupes-count').textContent = groupesCache.length;
  if (!groupesCache.length) {
    el.innerHTML = `<div class="empty-box">
      Aucun groupe — clique sur <strong>+ Nouveau groupe</strong>
    </div>`;
    return;
  }
  el.innerHTML = groupesCache.map(g => `
    <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;
                background:#FBF6EA;border:1px solid var(--border);border-radius:8px;flex-wrap:wrap">
      <span style="font-size:22px">👥</span>
      <div style="flex:1;min-width:180px">
        <div style="font-weight:600;font-size:14px">${escapeHtml(g.nom)}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:2px">
          ${g.emails.length} membre(s)
          ${g.description ? ` · ${escapeHtml(g.description)}` : ''}
        </div>
      </div>
      <button class="btn primary small" data-action="send-groupe" data-id="${escapeHtml(g.id)}">📤 Envoyer</button>
      <button class="btn small" data-action="edit-groupe" data-id="${escapeHtml(g.id)}">✏️</button>
      <button class="btn small danger" data-action="del-groupe" data-id="${escapeHtml(g.id)}">🗑️</button>
    </div>
  `).join('');

  el.querySelectorAll('[data-action="send-groupe"]').forEach(b => {
    b.addEventListener('click', () => openSendGroupe(b.dataset.id));
  });
  el.querySelectorAll('[data-action="edit-groupe"]').forEach(b => {
    b.addEventListener('click', () => openEditGroupe(b.dataset.id));
  });
  el.querySelectorAll('[data-action="del-groupe"]').forEach(b => {
    b.addEventListener('click', async () => {
      const grp = groupesCache.find(g => g.id === b.dataset.id);
      if (!confirm(`Supprimer "${grp.nom}" ?`)) return;
      await fetch(`/api/groupes/${b.dataset.id}`, { method:'DELETE' });
      await loadGroupes();
      toast('Supprimé', 'ok');
    });
  });
}

function openNewGroupe() {
  document.getElementById('grp-id').value = '';
  document.getElementById('grp-nom').value = '';
  document.getElementById('grp-desc').value = '';
  document.getElementById('grp-emails').value = '';
  document.getElementById('grp-modal-title').textContent = '👥 Nouveau groupe';
  updateGrpEmailCount();
  document.getElementById('grp-modal').classList.add('visible');
}

function openEditGroupe(id) {
  const g = groupesCache.find(x => x.id === id);
  if (!g) return;
  document.getElementById('grp-id').value = g.id;
  document.getElementById('grp-nom').value = g.nom;
  document.getElementById('grp-desc').value = g.description || '';
  document.getElementById('grp-emails').value = g.emails.join('\n');
  document.getElementById('grp-modal-title').textContent = `✏️ Éditer : ${g.nom}`;
  updateGrpEmailCount();
  document.getElementById('grp-modal').classList.add('visible');
}

function closeGrpModal() {
  document.getElementById('grp-modal').classList.remove('visible');
}

function updateGrpEmailCount() {
  const raw = document.getElementById('grp-emails').value;
  const emails = raw.split(/[,;\n]+/).map(e => e.trim()).filter(e => e.includes('@'));
  document.getElementById('grp-email-count').textContent =
    emails.length ? `${emails.length} email(s) valide(s)` : '';
}

async function saveGroupe() {
  const id    = document.getElementById('grp-id').value;
  const nom   = document.getElementById('grp-nom').value.trim();
  const desc  = document.getElementById('grp-desc').value.trim();
  const raw   = document.getElementById('grp-emails').value;
  const emails = raw.split(/[,;\n]+/).map(e => e.trim()).filter(e => e.includes('@'));
  if (!nom || !emails.length) { toast('Nom et emails requis', 'err'); return; }
  const payload = { nom, description: desc, emails };
  if (id) payload.id = id;
  try {
    const r = await fetch('/api/groupes', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    if (data.ok) {
      toast(data.updated ? 'Mis à jour' : 'Créé', 'ok');
      closeGrpModal();
      await loadGroupes();
    } else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
}

function openSendGroupe(id) {
  const g = groupesCache.find(x => x.id === id);
  if (!g) return;
  document.getElementById('grp-send-id').value = id;
  document.getElementById('grp-send-title').textContent = `📤 Envoyer à : ${g.nom}`;
  document.getElementById('grp-send-subject').value = '';
  document.getElementById('grp-send-body').value = '';
  document.getElementById('grp-send-pj').checked = false;
  document.getElementById('grp-send-template').value = '';
  document.querySelector('input[name="grp-mode"][value="individuel"]').checked = true;
  document.getElementById('grp-send-status').textContent = '';
  majGrpSendInfo(g);
  document.getElementById('grp-send-modal').classList.add('visible');
}

function closeGrpSendModal() {
  document.getElementById('grp-send-modal').classList.remove('visible');
}

function majGrpSendInfo(g) {
  const mode = document.querySelector('input[name="grp-mode"]:checked').value;
  const joindre = document.getElementById('grp-send-pj').checked;
  let info = `${g.emails.length} destinataire(s)`;
  if (mode === 'individuel') {
    info += ` · 1 email par personne · délai ${parseInt(document.getElementById('cfg-delai').value) || 40}s`;
  } else {
    info += ` · 1 email groupé (Cci)`;
  }
  if (joindre) info += ` · ${piecesActives} PJ`;
  document.getElementById('grp-send-info').textContent = info;
}

/* Applique un template au formulaire groupe */
function appliquerTemplateGroupe() {
  const tid = document.getElementById('grp-send-template').value;
  if (!tid) return;
  // Cherche le template
  const t = templatesCache.find(x => x.id === tid);
  const tpl = t || predefinis[tid] ? (t || { objet:'', corps:'' }) : null;

  if (t) {
    document.getElementById('grp-send-subject').value = t.objet || '';
    document.getElementById('grp-send-body').value = t.corps || '';
  }
}

async function envoyerGroupe() {
  const id = document.getElementById('grp-send-id').value;
  const g = groupesCache.find(x => x.id === id);
  if (!g) return;
  const subject = document.getElementById('grp-send-subject').value.trim();
  const body = document.getElementById('grp-send-body').value.trim();
  const mode = document.querySelector('input[name="grp-mode"]:checked').value;
  const joindre = document.getElementById('grp-send-pj').checked;
  if (!subject) { toast('Objet requis', 'err'); return; }
  if (!body) { toast('Message requis', 'err'); return; }

  const modeTxt = mode === 'groupe'
    ? `👥 GROUPÉ (Cci) — 1 email`
    : `📧 INDIVIDUEL — ${g.emails.length} emails`;

  if (!confirm(`Envoyer à "${g.nom}" ?\n\n${modeTxt}\nDestinataires : ${g.emails.length}\n${joindre ? `${piecesActives} PJ` : 'Sans PJ'}\n\nConfirmer ?`)) return;

  const btn = document.getElementById('grp-send-go');
  btn.disabled = true; btn.textContent = '⏳ Envoi...';
  document.getElementById('grp-send-status').textContent = 'Envoi...';

  try {
    const r = await fetch(`/api/groupes/${id}/send`, { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ subject, body, mode, joindre_pieces: joindre })
    });
    const data = await r.json();
    if (data.ok) {
      toast(`✅ ${data.envoyes}/${data.total}`, 'ok');
      document.getElementById('grp-send-status').textContent = `${data.envoyes}/${data.total}`;
      setTimeout(() => { closeGrpSendModal(); refreshStatus(); }, 1200);
    } else {
      toast(data.error || 'Erreur', 'err');
      btn.disabled = false; btn.textContent = '📤 Envoyer';
    }
  } catch (e) {
    toast('Erreur réseau', 'err');
    btn.disabled = false; btn.textContent = '📤 Envoyer';
  }
}

/* IMAP */
async function checkIMAP() {
  const btn = document.getElementById('btn-imap-check');
  const badge = document.getElementById('imap-status-badge');
  btn.disabled = true; btn.textContent = '⏳ Analyse...';
  badge.textContent = 'En cours...';
  try {
    const r = await fetch('/api/imap/check', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ jours: 30 })
    });
    const data = await r.json();
    if (data.ok) {
      toast(`✅ ${data.reponses} rép · ${data.bounces} bounce`, 'ok');
      badge.textContent = `${data.reponses} rép · ${data.bounces} bnc`;
      histAjouter({ type: 'IMAP', detail: `${data.reponses} rép · ${data.bounces} bounce` });
      await refreshStatus();
      await loadIMAPStatus();
    } else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
  btn.disabled = false; btn.textContent = '🔄 Vérifier maintenant';
}

async function loadIMAPStatus() {
  try {
    const r = await fetch('/api/imap/status');
    const data = await r.json();
    const badge = document.getElementById('imap-status-badge');
    if (data.derniere_verif) {
      const d = new Date(data.derniere_verif * 1000);
      const mins = Math.floor((Date.now() - d) / 60000);
      badge.textContent = `Dernière : ${mins < 1 ? 'instant' : mins < 60 ? `${mins}min` : `${Math.floor(mins/60)}h`}`;
    } else badge.textContent = 'Jamais';
  } catch (e) {}
}

/* RÈGLES DE CLASSEMENT */
let filtresCache = [];
let apprentissageCache = {};

const FLT_LABELS = { from: 'Expéditeur', sujet: 'Sujet', motcle: 'Mot-clé' };
const ACT_ICONS = { label: '🏷️', marquer_lu: '👁️', archive: '📦', supprimer: '🗑️', notify: '🔔' };

async function loadFiltres() {
  try {
    const r = await fetch('/api/filtres');
    const data = await r.json();
    if (data.ok) { filtresCache = data.filtres || []; renderFiltres(); }
  } catch (e) {}
  try {
    const r = await fetch('/api/filtres/suggestions');
    const d = await r.json();
    if (d.ok) { apprentissageCache = d.apprentissage || {}; renderApprentissage(); }
  } catch (e) {}
}

function renderFiltres() {
  const box = document.getElementById('regles-liste');
  document.getElementById('regles-count').textContent =
    `${filtresCache.filter(f => f.enabled !== false).length} active(s)`;
  if (!filtresCache.length) {
    box.innerHTML = '<span style="color:var(--muted)">Aucune règle pour l\'instant.</span>';
    return;
  }
  const tries = [...filtresCache].sort((a, b) => (a.priority ?? 999) - (b.priority ?? 999));
  box.innerHTML = tries.map((f) => {
    const i = filtresCache.indexOf(f);
    const off = f.enabled === false;
    const acts = (f.actions || []).map(a => ACT_ICONS[a] || a).join(' ');
    const conds = (f.items || []).map(it =>
      `${FLT_LABELS[it.champ] || it.champ} = <b>${escapeHtml(it.valeur)}</b>`).join(' OU ');
    const lbl = f.label ? ` → « ${escapeHtml(f.label)} »` : '';
    const icone = f.icon || '🏷️';
    const couleur = f.color || 'var(--muted)';
    return `<div class="regle-row ${off ? 'regle-off' : ''}" draggable="true"
        data-idx="${i}" style="display:flex;align-items:center;gap:8px;
        padding:7px 9px;border:1px solid var(--border);border-radius:8px;margin-bottom:6px;
        background:${off ? '#f6f2ea' : '#fff'};cursor:grab;opacity:${off ? '.6' : '1'}">
      <span style="font-weight:900;color:${couleur};min-width:20px">${f.priority ?? i + 1}</span>
      <span style="font-size:16px">${icone}</span>
      <div style="flex:1;min-width:0">
        <div style="font-weight:700;font-size:13px;color:${couleur}">${escapeHtml(f.name || '')}
          <span style="color:var(--muted);font-weight:600">${lbl} ${acts}</span>
          ${f.source === 'apprentissage' ? '<span title="Apprise de tes corrections">🧠</span>' : ''}
        </div>
        <div style="font-size:11px;color:var(--muted)">Si ${conds}</div>
      </div>
      <button class="btn small" data-action="toggle-regle" data-idx="${i}"
        title="${off ? 'Réactiver' : 'Mettre en pause'}">${off ? '▶️' : '⏸️'}</button>
      <button class="btn small" data-action="edit-regle" data-idx="${i}" title="Modifier">✏️</button>
      <button class="btn small danger" data-action="del-regle" data-idx="${i}" title="Supprimer">🗑️</button>
    </div>`;
  }).join('');
  activerDragDrop();
  box.querySelectorAll('[data-action="toggle-regle"]').forEach(b =>
    b.addEventListener('click', async () => {
      const r = await fetch(`/api/filtres/${b.dataset.idx}/toggle`, { method: 'POST' });
      const d = await r.json();
      if (d.ok) { filtresCache = d.filtres; renderFiltres(); }
    }));
  box.querySelectorAll('[data-action="edit-regle"]').forEach(b =>
    b.addEventListener('click', () => editerRegle(+b.dataset.idx)));
  box.querySelectorAll('[data-action="del-regle"]').forEach(b =>
    b.addEventListener('click', async () => {
      if (!confirm('Supprimer cette règle ?')) return;
      const r = await fetch(`/api/filtres/${b.dataset.idx}`, { method: 'DELETE' });
      const d = await r.json();
      if (d.ok) { filtresCache = d.filtres; renderFiltres(); }
    }));
}

/* MODALE règle : ajout ou édition */
let editRegleIdx = null;   // null = ajout, sinon index de la règle à modifier

function openRegleModal(idx) {
  const f = idx == null ? {} : (filtresCache[idx] || {});
  editRegleIdx = idx ?? null;
  document.getElementById('filter-modal-title').textContent = editRegleIdx == null ? '➕ Nouvelle règle' : '✏️ Modifier la règle';
  document.getElementById('filter-f-name').value = f.name || '';
  const champ = f.items?.[0]?.champ || 'sender';
  document.getElementById('filter-f-type').value = champ;
  document.getElementById('filter-f-value').value = f.items?.map(it => it.valeur).join(', ') || '';
  document.getElementById('filter-f-label').value = f.label || '';
  document.getElementById('filter-modal').classList.add('open');
}

function closeRegleModal() {
  editRegleIdx = null;
  document.getElementById('filter-modal').classList.remove('open');
}

function editerRegle(idx) { openRegleModal(idx); }

function soumettreRegle() {
  const nom  = document.getElementById('filter-f-name').value.trim();
  const champ = document.getElementById('filter-f-type').value;
  const brut = document.getElementById('filter-f-value').value.trim();
  const label = document.getElementById('filter-f-label').value.trim();
  if (!nom) { toast('Le nom de la règle est requis', 'err'); return; }
  const items = brut.split(',').map(v => v.trim()).filter(Boolean)
                     .map(v => ({ champ, valeur: v }));
  if (!items.length) { toast('Au moins une valeur est requise', 'err'); return; }
  if (!label) { toast('Le libellé Gmail est requis', 'err'); return; }
  const body = { name: nom, items, label, actions: ['label'] };
  const url = editRegleIdx == null ? '/api/filtres' : `/api/filtres/${editRegleIdx}`;
  const method = editRegleIdx == null ? 'POST' : 'PUT';
  fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
    .then(r => r.json())
    .then(d => {
      if (d.ok) {
        filtresCache = d.filtres;
        renderFiltres();
        toast(editRegleIdx == null ? 'Règle ajoutée ✅' : 'Règle modifiée ✅', 'ok');
        closeRegleModal();
      } else toast(d.error || 'Erreur', 'err');
    })
    .catch(() => toast('Erreur réseau', 'err'));
}

function activerDragDrop() {
  const box = document.getElementById('regles-liste');
  let enCours = null;
  box.querySelectorAll('.regle-row').forEach(row => {
    row.addEventListener('dragstart', () => { enCours = row; row.style.opacity = '.4'; });
    row.addEventListener('dragend', () => { row.style.opacity = ''; enCours = null; });
    row.addEventListener('dragover', e => { e.preventDefault(); });
    row.addEventListener('drop', async e => {
      e.preventDefault();
      if (!enCours || enCours === row) return;
      box.insertBefore(enCours, row);
      const ordre = [...box.querySelectorAll('.regle-row')]
        .map(r => filtresCache[+r.dataset.idx].id);
      const resp = await fetch('/api/filtres/reorder', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ordre }) });
      const d = await resp.json();
      if (d.ok) { filtresCache = d.filtres; renderFiltres(); toast('Priorité mise à jour', 'ok'); }
    });
  });
}

async function addFiltre() {
  const actions = [];
  if (document.getElementById('act-label').checked) actions.push('label');
  if (document.getElementById('act-lu').checked) actions.push('marquer_lu');
  if (document.getElementById('act-notif').checked) actions.push('notify');
  if (document.getElementById('act-archive').checked) actions.push('archive');
  if (document.getElementById('act-supprimer').checked) actions.push('supprimer');
  const body = {
    name: document.getElementById('flt-nom').value.trim(),
    champ: document.getElementById('flt-champ').value,
    valeur: document.getElementById('flt-valeur').value.trim(),
    label: document.getElementById('flt-label').value.trim(),
    actions,
  };
  if (!body.valeur) { toast('Valeur manquante', 'err'); return; }
  if (!actions.length) { toast('Coche au moins une action', 'err'); return; }
  const r = await fetch('/api/filtres', { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const data = await r.json();
  if (data.ok) {
    filtresCache = data.filtres; renderFiltres();
    document.getElementById('flt-valeur').value = '';
    toast('Règle ajoutée ✅', 'ok');
  } else toast(data.error || 'Erreur', 'err');
}

async function creerLibelles() {
  const btn = document.getElementById('btn-flt-libelles');
  btn.disabled = true; btn.textContent = '⏳ Création...';
  try {
    const r = await fetch('/api/filtres/creer-libelles', { method: 'POST' });
    const d = await r.json();
    if (d.ok) {
      const ok = d.resultats.filter(x => x.ok);
      const nb = ok.reduce((s, x) => s + (x.crees || []).length, 0);
      toast(`🏷️ ${d.libelles.length} libellé(s) vérifié(s) sur ${ok.length} compte(s) — ${nb} créé(s)`, 'ok');
    } else toast(d.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
  btn.disabled = false; btn.textContent = '🏷️ Créer les libellés dans Gmail';
}

async function appliquerFiltres() {
  const btn = document.getElementById('btn-flt-appliquer');
  btn.disabled = true; btn.textContent = '⏳ Application...';
  try {
    const r = await fetch('/api/filtres/appliquer', { method: 'POST' });
    const data = await r.json();
    if (data.ok) {
      const total = (data.resultats || []).reduce((s, x) => s + (x.trouves || 0), 0);
      const errs = (data.resultats || []).filter(x => !x.ok).length;
      toast(`✅ ${total} mail(s) classé(s)${errs ? `, ${errs} erreur(s)` : ''}`, errs ? 'warn' : 'ok');
      await chargerNotifs();
    } else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
  btn.disabled = false; btn.textContent = '⚡ Appliquer maintenant';
}

/* APPRENTISSAGE */
async function apprendre() {
  const email = document.getElementById('app-email').value.trim();
  const label = document.getElementById('app-label').value.trim();
  if (!email || !label) { toast('Email et libellé requis', 'err'); return; }
  const r = await fetch('/api/filtres/corriger', { method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, label }) });
  const d = await r.json();
  if (d.ok) {
    filtresCache = d.filtres; apprentissageCache = d.apprentissage || {};
    renderFiltres(); renderApprentissage();
    document.getElementById('app-email').value = '';
    document.getElementById('app-label').value = '';
    toast(`🧠 Appris : ${email} → ${label}`, 'ok');
  } else toast(d.error || 'Erreur', 'err');
}

function renderApprentissage() {
  const box = document.getElementById('app-liste');
  const entrees = Object.entries(apprentissageCache || {});
  if (!entrees.length) { box.textContent = 'Aucune correction apprise pour l\'instant.'; return; }
  box.innerHTML = entrees.map(([email, e]) =>
    `<div>🧠 ${escapeHtml(email)} → <b>${escapeHtml(e.label || '')}</b>
      (${e.corrections || 0} correction(s))</div>`).join('');
}

/* NOTIFICATIONS (Web Notification API + panneau) */
async function chargerNotifs() {
  try {
    const r = await fetch('/api/notifications');
    const d = await r.json();
    if (!d.ok) return;
    const box = document.getElementById('notifs-liste');
    const badge = document.getElementById('notifs-badge');
    badge.textContent = `${d.non_vues} non vue(s)`;
    const list = d.notifications || [];
    box.innerHTML = list.length ? list.map(n =>
      `<div style="padding:5px 8px;border-bottom:1px solid #eee">
        🔔 <b>${escapeHtml(n.regle || '')}</b> — ${n.nombre} mail(s) sur ${escapeHtml(n.email || '')}
        <span style="color:var(--muted)">${new Date((n.date || 0) * 1000).toLocaleString('fr-FR')}</span>
      </div>`).join('')
      : '<span style="color:var(--muted)">Aucune notification.</span>';
    // Notification desktop pour les nouvelles non vues
    if (d.non_vues > 0 && 'Notification' in window
        && Notification.permission === 'granted' && list.length) {
      const n = list[0];
      new Notification(`🔔 ${n.regle}`, {
        body: `${n.nombre} mail(s) classé(s) — ${n.label || n.regle}` });
    }
    if (d.non_vues > 0) await fetch('/api/notifications/vue', { method: 'POST' });
  } catch (e) {}
}

function activerNotifs() {
  if (!('Notification' in window)) { toast('Notifications non supportées', 'err'); return; }
  Notification.requestPermission().then(p => {
    toast(p === 'granted' ? '✅ Notifications activées'
                          : '❌ Notifications refusées', p === 'granted' ? 'ok' : 'err');
  });
}

/* HISTORIQUE NAVIGATEUR (localStorage) */
const HIST_KEY = 'candimail_historique';
const HIST_MAX = 200;

function histLire() {
  try { return JSON.parse(localStorage.getItem(HIST_KEY)) || []; }
  catch (e) { return []; }
}

function histAjouter(entree) {
  const h = histLire();
  h.unshift({ ...entree, t: Date.now() });
  localStorage.setItem(HIST_KEY, JSON.stringify(h.slice(0, HIST_MAX)));
  renderHistorique();
}

function histVider() {
  localStorage.removeItem(HIST_KEY);
  renderHistorique();
}

function renderHistorique() {
  const box = document.getElementById('hist-liste');
  if (!box) return;
  const h = histLire();
  if (!h.length) {
    box.innerHTML = '<span style="color:var(--muted)">Aucune action enregistrée sur cet appareil.</span>';
    return;
  }
  box.innerHTML = h.map(e => {
    const d = new Date(e.t);
    const heure = d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR', {hour:'2-digit',minute:'2-digit'});
    return `<div style="padding:4px 8px;border-bottom:1px solid #eee;font-size:12px">
      <b>${escapeHtml(e.type || 'action')}</b> ${escapeHtml(e.detail || '')}
      <span style="color:var(--muted);float:right">${heure}</span>
    </div>`;
  }).join('');
}

/* DÉLAI */
function bindDelaiUI() {
  const cb = document.getElementById('cfg-delai-alea');
  const input = document.getElementById('cfg-delai');
  const info = document.getElementById('delai-info');
  function maj() {
    if (cb.checked) { input.disabled = true; info.textContent = '🎲 35-55s'; }
    else { input.disabled = false; info.textContent = ''; }
  }
  cb.addEventListener('change', async () => {
    maj();
    await fetch('/api/config', { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ parametres: { delai_aleatoire: cb.checked } })
    });
  });
  input.addEventListener('change', async () => {
    const d = parseInt(input.value) || 40;
    await fetch('/api/config', { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ parametres: { delai_secondes: d } })
    });
    toast(`Délai : ${d}s`, 'ok');
  });
  maj();
}

/* RESET / IMPORT */
async function resetLog() {
  if (!confirm('Effacer tout l\'historique ?')) return;
  try {
    const r = await fetch('/api/reset-log', { method:'POST' });
    const data = await r.json();
    if (data.ok) { toast('Log réinitialisé', 'ok'); refreshStatus(); }
    else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
}

async function importJSON(file) {
  const form = new FormData();
  form.append('file', file);
  try {
    const r = await fetch('/api/import-json', { method:'POST', body: form });
    const data = await r.json();
    if (data.ok) { toast(`${data.importees} importées`, 'ok'); refreshStatus(); }
    else toast(data.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
}

/* MODAL APERÇU */
function openModal(company) {
  currentSendCompany = company;
  const template = document.getElementById('cfg-template').value || 'standard';
  fetch('/api/preview', { method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ company: company.name, context: company.context, template })
  })
  .then(r => r.json())
  .then(data => {
    if (!data.ok) { toast(data.error, 'err'); return; }
    document.getElementById('modal-dest').value = company.email;
    document.getElementById('modal-subject').value = data.subject;
    document.getElementById('modal-body').value = data.body;
    const pj = piecesActives === 0 ? '⚠️ Aucune PJ' : `${piecesActives} PJ`;
    document.getElementById('modal-info').textContent = `${pj}`;
    document.getElementById('modal').classList.add('visible');
  })
  .catch(() => toast('Erreur aperçu', 'err'));
}

function closeModal() {
  document.getElementById('modal').classList.remove('visible');
  currentSendCompany = null;
  // Réinitialise le bouton d'envoi pour la prochaine ouverture
  const btn = document.getElementById('modal-send');
  if (btn) { btn.disabled = false; btn.textContent = '📤 Envoyer'; }
}

async function sendFromModal() {
  if (!currentSendCompany) return;
  const subject = document.getElementById('modal-subject').value.trim();
  const body = document.getElementById('modal-body').value.trim();
  if (!subject || !body) { toast('Objet et corps requis', 'err'); return; }
  if (piecesActives === 0) {
    if (!confirm('⚠️ AUCUNE PJ\n\nContinuer ?')) return;
  }
  const btn = document.getElementById('modal-send');
  btn.disabled = true; btn.textContent = '⏳';
  try {
    const r = await fetch('/api/send', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        email: currentSendCompany.email,
        company: currentSendCompany.name,
        subject, body
      })
    });
    const data = await r.json();
    if (data.ok) {
      toast(`✅ Envoyé`, 'ok');
      closeModal(); await refreshStatus();
    } else {
      toast(data.error || 'Erreur', 'err');
    }
  } catch (e) {
    toast('Erreur réseau', 'err');
  } finally {
    // Toujours réinitialiser le bouton, même si closeModal a échoué
    btn.disabled = false; btn.textContent = '📤 Envoyer';
  }
}

/* ENVOI PERSONNALISÉ */
async function previewCustom() {
  const emailsRaw = document.getElementById('custom-email').value.trim();
  const company   = document.getElementById('custom-company').value.trim();
  const context   = document.getElementById('custom-context').value.trim();
  const template  = document.getElementById('custom-template').value;
  const emails = emailsRaw.split(/[,;\n]+/).map(e => e.trim()).filter(e => e.includes('@'));
  if (!emails.length || !company) { toast('Email valide + nom requis', 'err'); return; }
  const ctx = context || `Je me permets de vous contacter car je suis très intéressé
par les activités de ${company} et par les opportunités de stage.`;
  try {
    const r = await fetch('/api/preview', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ company, context: ctx, template })
    });
    const data = await r.json();
    if (!data.ok) { toast(data.error, 'err'); return; }
    document.getElementById('custom-preview-body').value = data.body;
    document.getElementById('custom-preview-zone').style.display = 'block';
    document.getElementById('custom-info').textContent = `${emails.length} dest · ${piecesActives} PJ`;
  } catch (e) { toast('Erreur réseau', 'err'); }
}

async function sendCustom() {
  const emailsRaw = document.getElementById('custom-email').value.trim();
  const company   = document.getElementById('custom-company').value.trim();
  const context   = document.getElementById('custom-context').value.trim();
  const template  = document.getElementById('custom-template').value;
  const emails = emailsRaw.split(/[,;\n]+/).map(e => e.trim()).filter(e => e.includes('@'));
  if (!emails.length) { toast('Au moins un email valide requis', 'err'); return; }
  if (!company) { toast('Nom requis', 'err'); return; }
  if (!rateLimit.ok) { toast('Rate limit — attends 1h', 'err'); return; }
  const nbComptes = parseInt(document.getElementById('comptes-badge').textContent.replace(/\D/g, '')) || 0;
  if (nbComptes === 0) { toast('Ajoute un compte Gmail', 'err'); return; }

  let avertissementPJ = '';
  if (piecesActives === 0) avertissementPJ = '\n\n⚠️ AUCUNE PJ — emails sans CV';

  const destPreview = emails.slice(0, 3).join('\n');
  const plus = emails.length > 3 ? `\n... +${emails.length - 3}` : '';
  if (!confirm(`📧 ${emails.length} email(s) INDIVIDUEL(S)\n\nDestinataires :\n${destPreview}${plus}\n\nEntreprise : ${company}\nPièces : ${piecesActives}${avertissementPJ}\n\nConfirmer ?`)) return;

  const btn = document.getElementById('btn-custom-send');
  btn.disabled = true; btn.textContent = '⏳ Envoi...';

  const ctx = context || `Je me permets de vous contacter car je suis très intéressé
par les activités de ${company} et par les opportunités de stage.`;

  try {
    const r1 = await fetch('/api/preview', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ company, context: ctx, template })
    });
    const preview = await r1.json();
    if (!preview.ok) { toast(preview.error, 'err'); return; }

    const r2 = await fetch('/api/send', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        email: emails.join(', '),
        company, subject: preview.subject, body: preview.body,
        mode_groupe: false,
      })
    });
    const data = await r2.json();
    if (data.ok) {
      toast(`✅ ${emails.length} envoi(s)`, piecesActives === 0 ? 'warn' : 'ok');
      document.getElementById('custom-email').value = '';
      document.getElementById('custom-company').value = '';
      document.getElementById('custom-context').value = '';
      document.getElementById('custom-preview-zone').style.display = 'none';
      document.getElementById('custom-info').textContent = '';
      await refreshStatus();
    } else {
      toast(data.error || 'Erreur', 'err');
    }
  } catch (e) {
    toast('Erreur réseau', 'err');
  } finally {
    // Toujours réinitialiser le bouton, quoi qu'il arrive
    btn.disabled = false; btn.textContent = '📤 Envoyer maintenant';
  }
}

/* BULK */
function getPendingCompanies() {
  return COMPANIES.filter(c => !serverLog[c.name]?.envoye);
}

const selectedCompanies = new Set();

function updateSelectionUI() {
  const n = selectedCompanies.size;
  const countEl = document.getElementById('sel-count');
  if (countEl) countEl.textContent = `${n} sélectionnée(s)`;
  const sendBtn = document.getElementById('sel-send');
  if (sendBtn) sendBtn.disabled = n === 0;
}

function toggleSelect(name, checked, cardEl) {
  if (checked) selectedCompanies.add(name); else selectedCompanies.delete(name);
  if (cardEl) cardEl.classList.toggle('selected', checked);
  updateSelectionUI();
}

function selectAllFiltered() {
  getFiltered().forEach(c => selectedCompanies.add(c.name));
  render();
}

function clearSelection() {
  selectedCompanies.clear();
  render();
}

async function sendSelected() {
  const target = COMPANIES.filter(c => selectedCompanies.has(c.name));
  if (!target.length) { toast('Aucune entreprise cochée', 'warn'); return; }
  await startBulk(target);
  selectedCompanies.clear();
  render();
}

async function startBulk(target) {
  if (!rateLimit.ok) { toast('Rate limit atteint', 'err'); return; }
  const nbComptes = parseInt(document.getElementById('comptes-badge').textContent.replace(/\D/g, '')) || 0;
  if (nbComptes === 0) { toast('Ajoute un compte Gmail', 'err'); return; }
  const pending = target && target.length ? target : getPendingCompanies();
  if (!pending.length) { toast('Tout est déjà envoyé', 'warn'); return; }
  const delay = parseInt(document.getElementById('cfg-delai').value) || 40;
  const alea = document.getElementById('cfg-delai-alea').checked;
  const template = document.getElementById('cfg-template').value || 'standard';
  const minutes = Math.ceil((pending.length * (alea ? 45 : delay)) / 60);
  const delaiTxt = alea ? '35-55s' : `${delay}s`;
  let avertissementPJ = '';
  if (piecesActives === 0) avertissementPJ = '\n\n⚠️ AUCUNE PJ — emails sans CV';
  if (!confirm(`Envoyer ${pending.length} emails ?\n\nTemplate : ${template}\nDélai : ${delaiTxt}\nPièces : ${piecesActives}\n~${minutes} min${avertissementPJ}\n\nConfirmer ?`)) return;
  try {
    const r = await fetch('/api/send-bulk', { method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ companies: pending, template })
    });
    const data = await r.json();
    if (!data.ok) { toast(data.error, 'err'); return; }
    setBulkUIRunning(true); startBulkPolling();
    histAjouter({ type: 'envoi', detail: `Envoi en masse lancé (${pending.length} emails)` });
  } catch (e) { toast('Erreur réseau', 'err'); }
}

async function stopBulk() {
  try {
    await fetch('/api/send-bulk-stop', { method:'POST' });
    toast('Arrêt demandé', 'warn');
  } catch (e) { toast('Erreur réseau', 'err'); }
}

function setBulkUIRunning(running) {
  document.getElementById('bulk-panel').classList.toggle('running', running);
  document.getElementById('bulk-start').style.display = running ? 'none' : '';
  document.getElementById('bulk-stop').style.display  = running ? '' : 'none';
}

function startBulkPolling() {
  if (bulkPollTimer) clearInterval(bulkPollTimer);
  bulkPollTimer = setInterval(async () => {
    try {
      const r = await fetch('/api/send-bulk-status');
      const s = await r.json();
      updateBulkUI(s);
      if (!s.en_cours) {
        clearInterval(bulkPollTimer);
        bulkPollTimer = null;
        setBulkUIRunning(false);
        await refreshStatus();
        toast(`Terminé : ${s.envoyes} ✅ / ${s.erreurs} ❌`, s.erreurs ? 'warn' : 'ok');
      }
    } catch (e) {}
  }, 2000);
}

function updateBulkUI(s) {
  document.getElementById('bulk-title').textContent =
    s.en_cours ? `⏳ ${s.index}/${s.total}` : '🚀 Envoi en masse';
  document.getElementById('bulk-desc').textContent = s.en_cours
    ? `${s.derniere} — ✅ ${s.envoyes} · ❌ ${s.erreurs}`
    : 'Envoie aux entreprises non contactées';
  const pct = s.total ? Math.round(100 * s.index / s.total) : 0;
  document.getElementById('bulk-bar').style.width = pct + '%';
}

/* RENDU LISTE */
function getFiltered() {
  const q = searchQuery.toLowerCase().trim();
  return COMPANIES.filter(c => {
    if (activeFilter !== 'all' && c.cat !== activeFilter) return false;
    if (!q) return true;
    return c.name.toLowerCase().includes(q) || c.email.toLowerCase().includes(q);
  });
}

function render() {
  const list = document.getElementById('list');
  const filtered = getFiltered();
  if (!filtered.length) {
    list.innerHTML = '<div style="padding:40px;text-align:center;color:var(--muted)">Aucun résultat</div>';
    return;
  }
  const groups = {};
  filtered.forEach(c => {
    if (!groups[c.cat]) groups[c.cat] = [];
    groups[c.cat].push(c);
  });
  list.innerHTML = Object.entries(groups).map(([cat, items]) => `
    <section class="category">
      <div class="category-head">
        <h3>${CATEGORIES[cat] || cat}</h3>
        <span class="count">${items.length}</span>
        <hr>
      </div>
      ${items.map(renderCard).join('')}
    </section>
  `).join('');
  bindEvents();
  updateSelectionUI();
}

function renderCard(c) {
  const entry = serverLog[c.name];
  const isSent = !!entry?.envoye;
  const isError = entry && !entry.envoye;
  const isReplied = !!entry?.repondu;
  const isBounce = !!entry?.bounce;
  const sansPJ = !!entry?.sans_pj;
  const badgeClass = c.cat === 'port' ? 'port' : (c.cat === 'grands' ? 'grand' : '');
  const catLabel = c.cat === 'port' ? 'Port' : (c.cat === 'grands' ? 'Grand' : 'PME');

  let cardCls = '';
  if (isBounce) cardCls = 'bounce';
  else if (isReplied) cardCls = 'responded';
  else if (isSent) cardCls = 'sent';
  else if (isError) cardCls = 'error';

  let badgeStatus = '';
  if (isReplied) badgeStatus = '<span class="badge response">✨ Réponse</span>';
  else if (isBounce) badgeStatus = '<span class="badge bounce">⚠️ Bounce</span>';
  else if (sansPJ && isSent) badgeStatus = '<span class="badge nopj">⚠️ Sans PJ</span>';

  return `
    <div class="card ${cardCls}" data-name="${escapeHtml(c.name)}">
      <div class="card-head" onclick="this.parentElement.classList.toggle('open')">
        <input type="checkbox" class="sel-ck" data-action="toggle-select"
               data-name="${escapeHtml(c.name)}" title="Cocher pour envoi ciblé"
               ${selectedCompanies.has(c.name) ? 'checked' : ''}>
        <div class="title">
          <div class="name">${escapeHtml(c.name)}</div>
          <div class="email">${escapeHtml(c.email)}</div>
        </div>
        ${badgeStatus}
        ${entry?.date ? `<span class="date">${escapeHtml(entry.date)}</span>` : ''}
        <span class="badge ${badgeClass}">${catLabel}</span>
        <span class="toggle">▶</span>
      </div>
      <div class="card-body">
        <div style="font-size:12px;color:var(--muted);line-height:1.6">
          ${escapeHtml(c.context)}
        </div>
        ${entry?.compte ? `<div class="via-compte" title="Compte Gmail utilisé">📨 envoyé via ${escapeHtml(entry.compte)}</div>` : ''}
        <div class="actions">
          <button class="btn primary" data-action="preview"
                  data-name="${escapeHtml(c.name)}" ${isSent ? 'disabled' : ''}>
            ${isSent ? '✅ Envoyé' : (isError ? '🔄 Réessayer' : '✏️ Aperçu & envoyer')}
          </button>
          <button class="btn small" data-action="edit-company"
                  data-name="${escapeHtml(c.name)}" title="Modifier">✏️</button>
          <button class="btn small danger" data-action="delete-company"
                  data-name="${escapeHtml(c.name)}" title="Supprimer">🗑️</button>
          ${isSent ? `
            <button class="btn small ${isReplied ? 'ok' : ''}"
                    data-action="toggle-reply" data-name="${escapeHtml(c.name)}">
              ${isReplied ? '✓ Répondu' : 'Marquer réponse'}
            </button>
          ` : ''}
        </div>
      </div>
    </div>
  `;
}

function bindEvents() {
  document.querySelectorAll('[data-action="preview"]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const c = COMPANIES.find(x => x.name === btn.dataset.name);
      if (c) openModal(c);
    });
  });
  document.querySelectorAll('[data-action="edit-company"]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const c = COMPANIES.find(x => x.name === btn.dataset.name);
      if (c) openCompanyModal(c);
    });
  });
  document.querySelectorAll('[data-action="delete-company"]').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.stopPropagation();
      const name = btn.dataset.name;
      if (!confirm(`Supprimer "${name}" de la liste ?`)) return;
      try {
        const r = await fetch(`/api/companies/${encodeURIComponent(name)}`,
                              { method:'DELETE' });
        const d = await r.json();
        if (d.ok) {
          selectedCompanies.delete(name);
          toast('Entreprise supprimée', 'ok');
          await syncCompanies();
        } else toast(d.error || 'Erreur', 'err');
      } catch (err) { toast('Erreur réseau', 'err'); }
    });
  });
  document.querySelectorAll('[data-action="toggle-select"]').forEach(cb => {
    cb.addEventListener('click', e => e.stopPropagation());
    cb.addEventListener('change', e => {
      e.stopPropagation();
      toggleSelect(cb.dataset.name, cb.checked, cb.closest('.card'));
    });
  });
  document.querySelectorAll('[data-action="toggle-reply"]').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.stopPropagation();
      const name = btn.dataset.name;
      const current = !!serverLog[name]?.repondu;
      try {
        const r = await fetch('/api/mark-response', { method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ company: name, repondu: !current })
        });
        if (r.status === 401) { window.location.href = '/login'; return; }
        const data = await r.json();
        if (data.ok) { toast('OK', 'ok'); refreshStatus(); }
        else toast(data.error || 'Erreur', 'err');
      } catch (err) { toast('Erreur réseau', 'err'); }
    });
  });
}

/* MODALE ENTREPRISE : ajout / édition */
let companyEditName = null; // null = ajout

function openCompanyModal(c) {
  companyEditName = c ? c.name : null;
  document.getElementById('company-modal-title').textContent =
    c ? `✏️ Modifier : ${c.name}` : '➕ Nouvelle entreprise';
  document.getElementById('company-f-name').value    = c ? c.name : '';
  document.getElementById('company-f-email').value   = c ? c.email : '';
  document.getElementById('company-f-cat').value     = c ? c.cat : 'pme';
  document.getElementById('company-f-context').value = c ? c.context : '';
  document.getElementById('company-modal').classList.add('visible');
  setTimeout(() => document.getElementById('company-f-name').focus(), 50);
}

function closeCompanyModal() {
  document.getElementById('company-modal').classList.remove('visible');
}

async function saveCompany() {
  const name    = document.getElementById('company-f-name').value.trim();
  const email   = document.getElementById('company-f-email').value.trim();
  const cat     = document.getElementById('company-f-cat').value;
  const context = document.getElementById('company-f-context').value.trim();
  if (!name || !email || !email.includes('@')) {
    toast('Nom et email valides requis', 'err'); return;
  }
  const btn = document.getElementById('company-save');
  btn.disabled = true;
  try {
    const url = companyEditName
      ? `/api/companies/${encodeURIComponent(companyEditName)}`
      : '/api/companies';
    const method = companyEditName ? 'PUT' : 'POST';
    const r = await fetch(url, {
      method, headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ name, email, cat, context })
    });
    const d = await r.json();
    if (d.ok) {
      toast(companyEditName ? 'Entreprise modifiée' : 'Entreprise ajoutée', 'ok');
      closeCompanyModal();
      await syncCompanies();
    } else toast(d.error || 'Erreur', 'err');
  } catch (e) { toast('Erreur réseau', 'err'); }
  btn.disabled = false;
}

/* Synchronise la liste avec la base : seed au 1er lancement, puis lecture */
async function syncCompanies() {
  try {
    await fetch('/api/companies/seed', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ companies: COMPANIES })
    });
    const r = await fetch('/api/companies');
    const d = await r.json();
    if (d.ok && Array.isArray(d.companies) && d.companies.length) {
      COMPANIES = d.companies;
    }
  } catch (e) { console.error('syncCompanies', e); }
  render();
  updateStats();
}

function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, m => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[m]));
}

function updateStats() {
  const total = COMPANIES.length;
  const sent = COMPANIES.filter(c => serverLog[c.name]?.envoye).length;
  const responded = COMPANIES.filter(c => serverLog[c.name]?.repondu).length;
  animateCount('stat-total', total);
  animateCount('stat-sent', sent);
  animateCount('stat-pending', total - sent);
  animateCount('stat-responded', responded);
}

/* Compteur animé : glisse vers la nouvelle valeur */
const _countAnims = {};
function animateCount(id, target) {
  const el = document.getElementById(id);
  if (!el) return;
  const from = parseInt(el.textContent) || 0;
  if (from === target) { el.textContent = target; return; }
  if (_countAnims[id]) cancelAnimationFrame(_countAnims[id]);
  const t0 = performance.now(), dur = 450;
  const step = now => {
    const p = Math.min(1, (now - t0) / dur);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(from + (target - from) * eased);
    if (p < 1) _countAnims[id] = requestAnimationFrame(step);
  };
  _countAnims[id] = requestAnimationFrame(step);
}

function renderFilters() {
  const f = document.getElementById('filters');
  const counts = { all: COMPANIES.length };
  COMPANIES.forEach(c => { counts[c.cat] = (counts[c.cat] || 0) + 1; });
  f.innerHTML = `
    <button class="chip active" data-cat="all">Tout (${counts.all})</button>
    ${Object.entries(CATEGORIES).map(([cat, label]) =>
      `<button class="chip" data-cat="${cat}">${label} (${counts[cat] || 0})</button>`
    ).join('')}
  `;
  f.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      f.querySelectorAll('.chip').forEach(x => x.classList.remove('active'));
      chip.classList.add('active');
      activeFilter = chip.dataset.cat;
      render();
    });
  });
}

function bindSearch() {
  const input = document.getElementById('search');
  let t;
  input.addEventListener('input', () => {
    clearTimeout(t);
    t = setTimeout(() => { searchQuery = input.value; render(); }, 120);
  });
}

function toast(msg, type='') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show ' + type;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 3500);
}

/* INIT */
document.addEventListener('DOMContentLoaded', async () => {
  await loadConfig();
  await loadTemplates();
  await loadPieces();
  await loadGroupes();
  await loadIMAPStatus();
  await syncCompanies();

  bindSearch();
  renderFilters();
  bindDelaiUI();

  // Entreprises : ajout / édition / suppression
  document.getElementById('btn-add-company').addEventListener('click', () => openCompanyModal(null));
  document.getElementById('company-modal-close').addEventListener('click', closeCompanyModal);
  document.getElementById('company-cancel').addEventListener('click', closeCompanyModal);
  document.getElementById('company-save').addEventListener('click', saveCompany);
  document.getElementById('company-modal').addEventListener('click', e => {
    if (e.target.id === 'company-modal') closeCompanyModal();
  });

  // Max par heure
  document.getElementById('cfg-maxh').addEventListener('change', async () => {
    const mx = Math.max(1, Math.min(500, parseInt(document.getElementById('cfg-maxh').value) || 100));
    document.getElementById('cfg-maxh').value = mx;
    await fetch('/api/config', { method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ parametres: { max_par_heure: mx } })
    });
    toast(`Max / heure : ${mx}`, 'ok');
    refreshStatus();
  });

  // Sélection individuelle
  document.getElementById('sel-all').addEventListener('click', selectAllFiltered);
  document.getElementById('sel-none').addEventListener('click', clearSelection);
  document.getElementById('sel-send').addEventListener('click', sendSelected);
  updateSelectionUI();

  // Config
  document.getElementById('btn-save-config').addEventListener('click', saveCandidatConfig);
  document.getElementById('cfg-template').addEventListener('change', saveCandidatConfig);

  // Comptes
  document.getElementById('btn-add-compte').addEventListener('click', addCompte);
  document.getElementById('btn-help-password').addEventListener('click', () => {
    document.getElementById('help-modal').classList.add('visible');
  });
  document.getElementById('help-close').addEventListener('click', () => {
    document.getElementById('help-modal').classList.remove('visible');
  });
  document.getElementById('help-close-btn').addEventListener('click', () => {
    document.getElementById('help-modal').classList.remove('visible');
  });
  document.getElementById('help-modal').addEventListener('click', e => {
    if (e.target.id === 'help-modal') document.getElementById('help-modal').classList.remove('visible');
  });
  document.getElementById('new-password').addEventListener('keydown', e => {
    if (e.key === 'Enter') addCompte();
  });

  // Templates
  document.getElementById('btn-new-tpl').addEventListener('click', openNewTpl);
  document.getElementById('tpl-modal-close').addEventListener('click', closeTplModal);
  document.getElementById('tpl-modal-cancel').addEventListener('click', closeTplModal);
  document.getElementById('tpl-modal-save').addEventListener('click', saveTpl);
  document.getElementById('tpl-modal').addEventListener('click', e => {
    if (e.target.id === 'tpl-modal') closeTplModal();
  });

  // Envoi personnalisé
  document.getElementById('btn-custom-preview').addEventListener('click', previewCustom);
  document.getElementById('btn-custom-send').addEventListener('click', sendCustom);

  // Groupes
  document.getElementById('btn-new-groupe').addEventListener('click', openNewGroupe);
  document.getElementById('grp-modal-close').addEventListener('click', closeGrpModal);
  document.getElementById('grp-modal-cancel').addEventListener('click', closeGrpModal);
  document.getElementById('grp-modal-save').addEventListener('click', saveGroupe);
  document.getElementById('grp-emails').addEventListener('input', updateGrpEmailCount);
  document.getElementById('grp-modal').addEventListener('click', e => {
    if (e.target.id === 'grp-modal') closeGrpModal();
  });
  document.getElementById('grp-send-close').addEventListener('click', closeGrpSendModal);
  document.getElementById('grp-send-cancel').addEventListener('click', closeGrpSendModal);
  document.getElementById('grp-send-go').addEventListener('click', envoyerGroupe);
  document.getElementById('grp-send-modal').addEventListener('click', e => {
    if (e.target.id === 'grp-send-modal') closeGrpSendModal();
  });
  document.querySelectorAll('input[name="grp-mode"]').forEach(r => {
    r.addEventListener('change', () => {
      const id = document.getElementById('grp-send-id').value;
      const g = groupesCache.find(x => x.id === id);
      if (g) majGrpSendInfo(g);
    });
  });
  document.getElementById('grp-send-pj').addEventListener('change', () => {
    const id = document.getElementById('grp-send-id').value;
    const g = groupesCache.find(x => x.id === id);
    if (g) majGrpSendInfo(g);
  });
  document.getElementById('grp-send-template').addEventListener('change', appliquerTemplateGroupe);

  // Pièces
  document.getElementById('pj-input').addEventListener('change', e => {
    if (e.target.files.length) uploadPieces(e.target.files);
    e.target.value = '';
  });

  // IMAP
  document.getElementById('btn-imap-check').addEventListener('click', checkIMAP);

  // Navigation sidebar : active + scroll + fil d'Ariane
  const NAV_TITRES = { dash: 'Tableau de bord', imap: 'Détection des réponses',
                       comptes: 'Comptes Gmail', filtres: 'Filtres Gmail',
                       params: "Paramètres d'envoi", hist: 'Historique' };
  document.querySelectorAll('.sidebar .nav-item[data-nav]').forEach(a => {
    a.addEventListener('click', () => {
      document.querySelectorAll('.sidebar .nav-item').forEach(x => x.classList.remove('active'));
      a.classList.add('active');
      const nav = a.dataset.nav;
      document.getElementById('bc-page').textContent = NAV_TITRES[nav] || 'Tableau de bord';
      const cible = { dash: null, imap: 'sec-imap', comptes: 'sec-comptes',
                      filtres: 'sec-filtres', params: 'sec-params', hist: 'sec-hist' }[nav];
      if (cible) {
        const el = document.getElementById(cible);
        el && el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  // Recherche sidebar synchronisée + raccourci clavier « / »
  const sMain = document.getElementById('search'), sSide = document.getElementById('search-side');
  sSide.addEventListener('input', () => { sMain.value = sSide.value; sMain.dispatchEvent(new Event('input')); });
  document.addEventListener('keydown', e => {
    if (e.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) {
      e.preventDefault(); sSide.focus();
    }
  });

  // Règles de classement
  document.getElementById('btn-flt-add').addEventListener('click', addFiltre);
  document.getElementById('btn-flt-appliquer').addEventListener('click', appliquerFiltres);
  document.getElementById('btn-flt-libelles').addEventListener('click', creerLibelles);
  document.getElementById('btn-app-corriger').addEventListener('click', apprendre);
  document.getElementById('btn-notifs-activer').addEventListener('click', activerNotifs);
  await loadFiltres();
  await chargerNotifs();
  setInterval(chargerNotifs, 60000);   // poll toutes les minutes

  // Historique local
  document.getElementById('btn-hist-vider').addEventListener('click', histVider);
  renderHistorique();
  histAjouter({ type: 'session', detail: 'Ouverture de Candimail' });

  // Import/reset
  document.getElementById('btn-reset-log').addEventListener('click', resetLog);
  document.getElementById('btn-import-json').addEventListener('click',
    () => document.getElementById('import-json-input').click());
  document.getElementById('import-json-input').addEventListener('change', e => {
    if (e.target.files[0]) importJSON(e.target.files[0]);
    e.target.value = '';
  });

  // Bulk
  document.getElementById('bulk-start').addEventListener('click', startBulk);
  document.getElementById('bulk-stop').addEventListener('click', stopBulk);

  // Modal aperçu
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-cancel').addEventListener('click', closeModal);
  document.getElementById('modal-send').addEventListener('click', sendFromModal);
  document.getElementById('modal').addEventListener('click', e => {
    if (e.target.id === 'modal') closeModal();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeModal();
      document.getElementById('help-modal').classList.remove('visible');
      closeGrpModal();
      closeGrpSendModal();
      closeTplModal();
    }
  });

  await refreshStatus();

  try {
    const r = await fetch('/api/send-bulk-status');
    const s = await r.json();
    if (s.en_cours) {
      setBulkUIRunning(true);
      updateBulkUI(s);
      startBulkPolling();
    }
  } catch (e) {}
});
