/* ============================================================
   Candimail — client API + interface (front complet, 2026)
   Branché EXACTEMENT sur les routes du backend (candimail/web/api.py).
   Sources : docs/API.md + candimail/web/api.py.
   ============================================================ */
'use strict';

/* ------------------------------------------------------------
   Helpers réseau
   ------------------------------------------------------------ */
async function api(url, opts = {}) {
  const init = { headers: { 'X-UID': uidHeader() }, ...opts };
  if (opts.body !== undefined && !(opts.body instanceof FormData)) {
    init.headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(opts.body);
  }
  const r = await fetch(url, init);
  let data = {};
  try { data = await r.json(); } catch { /* réponse non-JSON (fichiers) */ }
  if (!r.ok && !data.error) data = { ok: false, error: 'Erreur ' + r.status };
  return { status: r.status, ...data };
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g,
    c => ({ '&': '&', '<': '<', '>': '>', '"': '"', "'": '&#39;' }[c]));
}

function toast(msg, kind = '') {
  let el = document.getElementById('toast');
  if (!el) { el = document.createElement('div'); el.id = 'toast'; el.className = 'toast'; document.body.appendChild(el); }
  el.textContent = msg;
  el.className = 'toast show ' + kind;
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3200);
}

const $ = id => document.getElementById(id);
function uidHeader() { return sessionStorage.getItem('uid') || '0'; }
/* Le profil 0 est le profil SYSTÈME (démo) : lecture seule.
   Pour utiliser l'application, il faut créer un vrai profil (uid >= 1). */
function profilSysteme() { return uidHeader() === '0'; }

/* ------------------------------------------------------------
   État global
   ------------------------------------------------------------ */
const CATEGORIES = { grands: 'Grands groupes', pme: 'PME dynamiques', port: 'Port & maritime' };
const TEMPLATES_PREDEF = { standard: { nom: 'Standard' }, formel: { nom: 'Formel' }, direct: { nom: 'Direct' } };

let companies = [];
let serverLog = {};                 // { "Entreprise": {envoye, repondu, ...} }
let comptes = [];
let templatesList = [];             // templates_perso du backend
let templatesDispo = {};            // {id: {nom, predefini}}
let groupes = [];
let pieces = [];
let filtres = [];
let bulkTimer = null;
let activeFilter = 'all';
let searchQuery = '';

/* ------------------------------------------------------------
   ÉTAT + SUIVI
   GET /api/status, GET /api/suivi
   ------------------------------------------------------------ */
async function refreshStatus() {
  const d = await api('/api/status');
  serverLog = d.log || {};
  updateBadges(d);
}

async function chargerSuivi() {
  const d = await api('/api/suivi');
  if (!d.ok) { serverLog = {}; return {}; }
  const idx = {};
  for (const l of d.items || []) idx[l.company] = l;
  serverLog = idx;
  return d;
}

function updateBadges(d) {
  const nbPieces = d.pieces_count ?? 0;
  const nbCpt = d.comptes_actifs ?? 0;
  const rl = d.rate_limit || { utilises: 0, max: 0, ok: true };
  const set = (id, txt, cls) => { const el = $(id); if (el) { el.textContent = txt; el.className = 'badge ' + cls; } };
  set('cv-badge', `📎 ${nbPieces} pièce(s)`, nbPieces > 0 ? 'ok' : 'warn');
  set('comptes-badge', `📧 ${nbCpt}`, nbCpt > 0 ? 'ok' : 'warn');
  set('rate-badge', `⏱ ${rl.utilises}/${rl.max}`, rl.ok ? 'ok' : 'err');
  const warn = $('pj-warning');
  if (warn) warn.style.display = nbPieces === 0 ? 'block' : 'none';
}

/* Bannière « mot de passe d'application manquant » : au moins un compte
   actif n'a pas de mot de passe → l'automatisation ne marchera pas. */
function majBanniereMdp() {
  const b = $('compte-sans-mdp-banniere');
  if (!b) return;
  const manque = comptes.some(c => c.actif && !c.has_password);
  b.style.display = manque ? 'block' : 'none';
}

/* Marquer une réponse — POST /api/mark-response */
async function toggleReply(company, force) {
  const cur = !!serverLog[company]?.repondu;
  const target = typeof force === 'boolean' ? force : !cur;
  if (cur === target) return true;
  const d = await api('/api/mark-response', { method: 'POST', body: { company, repondu: target } });
  if (!d.ok) { toast(d.error || 'Erreur', 'err'); return false; }
  if (serverLog[company]) serverLog[company].repondu = target;
  return true;
}

/* ------------------------------------------------------------
   ENTREPRISES — GET/POST/PUT/DELETE /api/companies
   ------------------------------------------------------------ */
async function loadCompanies() {
  const d = await api('/api/companies');
  companies = d.companies || [];
  renderCompanies();
}

function companyStatut(name) {
  const l = serverLog[name];
  if (!l) return { cls: '', tag: '', tagCls: '' };
  if (l.repondu) return { cls: 'responded', tag: 'Réponse', tagCls: '' };
  if (l.bounce) return { cls: 'error', tag: 'Bounce', tagCls: 'err' };
  if (l.envoye) return { cls: 'sent', tag: 'Envoyé', tagCls: 'ok' };
  if (l.erreur) return { cls: 'error', tag: 'Échec', tagCls: 'err' };
  return { cls: '', tag: '', tagCls: '' };
}

function renderCompanies() {
  const list = $('list');
  if (!list) return;
  let shown = companies;
  if (activeFilter !== 'all') shown = shown.filter(c => c.cat === activeFilter);
  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    shown = shown.filter(c => c.name.toLowerCase().includes(q) || (c.email || '').toLowerCase().includes(q));
  }

  const stats = { total: companies.length, sent: 0, pending: 0, responded: 0 };
  for (const c of companies) {
    const l = serverLog[c.name];
    if (l?.repondu) stats.responded++;
    else if (l?.envoye) stats.sent++;
    else stats.pending++;
  }
  const setN = (id, v) => { const el = $(id); if (el) el.textContent = v; };
  setN('stat-total', stats.total);
  setN('stat-sent', stats.sent);
  setN('stat-pending', stats.pending);
  setN('stat-responded', stats.responded);

  if (!shown.length) {
    list.innerHTML = '<div class="empty-box">Aucune entreprise. Ajoute ta première cible avec « + Entreprise ».</div>';
    return;
  }

  list.innerHTML = shown.map(c => {
    const s = companyStatut(c.name);
    return `
    <div class="card ${s.cls}" data-name="${esc(c.name)}">
      <div class="card-head" data-action="toggle-card">
        <input type="checkbox" data-select-company="${esc(c.name)}" style="width:auto">
        <span class="tag">${esc(c.cat || '?')}</span>
        <span class="name">${esc(c.name)}</span>
        <span class="email">${esc(c.email)}</span>
        ${s.tag ? `<span class="tag ${s.tagCls}">${s.tag}</span>` : ''}
        <span class="tag">▼</span>
      </div>
      <div class="card-body">
        <p class="help">${esc(c.context || 'Aucun contexte défini.')}</p>
        <div class="actions">
          <button class="btn primary small" data-action="send-one" data-name="${esc(c.name)}">✉ Envoyer</button>
          <button class="btn small" data-action="preview-one" data-name="${esc(c.name)}">👁 Aperçu</button>
          <button class="btn small" data-action="toggle-reply" data-name="${esc(c.name)}">↔ Réponse</button>
          <button class="btn small" data-action="edit-company" data-name="${esc(c.name)}">✎ Modifier</button>
          <button class="btn danger small" data-action="del-company" data-name="${esc(c.name)}">✖ Supprimer</button>
        </div>
        <div class="preview-zone" data-preview style="display:none;margin-top:10px">
          <label>Objet</label><input data-preview-subject readonly>
          <label>Corps</label><textarea data-preview-body rows="10" readonly></textarea>
        </div>
      </div>
    </div>`;
  }).join('');
  updateSelection();
}

/* POST /api/companies */
async function addCompany(payload) {
  const d = await api('/api/companies', { method: 'POST', body: payload });
  if (d.ok) { toast('Entreprise ajoutée', 'ok'); await loadCompanies(); }
  else toast(d.error || 'Erreur', 'err');
}

/* PUT /api/companies/<name> */
async function updateCompany(name, payload) {
  const d = await api('/api/companies/' + encodeURIComponent(name), { method: 'PUT', body: payload });
  if (d.ok) { toast('Entreprise modifiée', 'ok'); await loadCompanies(); }
  else toast(d.error || 'Erreur', 'err');
}

/* DELETE /api/companies/<name> */
async function delCompany(name) {
  if (!confirm(`Supprimer « ${name} » ?`)) return;
  const d = await api('/api/companies/' + encodeURIComponent(name), { method: 'DELETE' });
  if (d.ok) { toast('Entreprise supprimée', 'ok'); await Promise.all([loadCompanies(), refreshStatus()]); }
  else toast(d.error || 'Erreur', 'err');
}

/* ------------------------------------------------------------
   MODALE ENTREPRISE (ajout / édition)
   ------------------------------------------------------------ */
function openCompanyModal(name = null) {
  if (profilSysteme()) { toast('Profil système en lecture seule — crée un vrai profil.', 'err'); return; }
  const c = name ? companies.find(x => x.name === name) : null;
  const overlay = $('modal-overlay');
  $('modal-title').textContent = c ? 'Modifier l\u2019entreprise' : 'Nouvelle entreprise';
  $('modal-body').innerHTML = `
    <label>Nom *</label><input id="m-name" value="${esc(c?.name || '')}">
    <label>Email de contact *</label><input id="m-email" type="email" value="${esc(c?.email || '')}">
    <label>Catégorie</label>
    <select id="m-cat">
      <option value="grands" ${c?.cat === 'grands' ? 'selected' : ''}>Grands groupes</option>
      <option value="pme" ${!c || c?.cat === 'pme' ? 'selected' : ''}>PME dynamiques</option>
      <option value="port" ${c?.cat === 'port' ? 'selected' : ''}>Port & maritime</option>
    </select>
    <label>Contexte personnalisé</label>
    <textarea id="m-context" rows="4">${esc(c?.context || '')}</textarea>`;
  $('modal-ok').textContent = c ? 'Enregistrer' : 'Ajouter';
  $('modal-ok').onclick = async () => {
    const payload = {
      name: $('m-name').value.trim(),
      email: $('m-email').value.trim(),
      cat: $('m-cat').value,
      context: $('m-context').value.trim(),
    };
    if (!payload.name || !payload.email.includes('@')) { toast('Nom et email valides requis', 'err'); return; }
    overlay.classList.remove('visible');
    if (c) await updateCompany(c.name, payload);
    else await addCompany(payload);
  };
  overlay.classList.add('visible');
}

/* ------------------------------------------------------------
   TEMPLATES — GET/POST/DELETE /api/templates
   ------------------------------------------------------------ */
async function loadTemplates() {
  const d = await api('/api/templates');
  templatesList = d.templates || [];
  fillTemplateSelects();
  renderTemplates();
}

function renderTemplates() {
  const el = $('tpl-list');
  if (!el) return;
  if ($('tpl-count')) $('tpl-count').textContent = templatesList.length;
  if (!templatesList.length) {
    el.innerHTML = '<div class="empty-box">Aucun modèle personnalisé. Les modèles prédéfinis restent utilisables.</div>';
    return;
  }
  el.innerHTML = templatesList.map(t => `
    <div class="list-item">
      <span class="tag">${esc(t.categorie || 'autre')}</span>
      <span class="grow"><b>${esc(t.nom)}</b><br><span class="help">${esc(t.objet)}</span></span>
      <button class="btn small" data-action="edit-tpl" data-id="${esc(t.id)}">✎</button>
      <button class="btn small" data-action="dup-tpl" data-id="${esc(t.id)}">⧉</button>
      <button class="btn danger small" data-action="del-tpl" data-id="${esc(t.id)}">✖</button>
    </div>`).join('');
}

function fillTemplateSelects() {
  templatesDispo = {};
  for (const t of templatesList) templatesDispo[t.id] = { nom: t.nom, predefini: false };
  for (const [id, t] of Object.entries(TEMPLATES_PREDEF)) templatesDispo[id] = { nom: t.nom, predefini: true };
  for (const selId of ['cfg-template', 'custom-template']) {
    const sel = $(selId);
    if (!sel) continue;
    const cur = sel.value;
    sel.innerHTML = Object.entries(templatesDispo)
      .map(([id, t]) => `<option value="${esc(id)}">${esc(t.nom || id)}${t.predefini ? ' (prédéfini)' : ''}</option>`).join('');
    if (cur) sel.value = cur;
  }
}

function openTplModal(t = null) {
  $('modal-title').textContent = t ? 'Modifier le modèle' : 'Nouveau modèle';
  $('modal-body').innerHTML = `
    <p class="help">Variables : {entreprise} {contexte} {nom} {tel} {email} {ville} {diplome} {spec}</p>
    <label>Nom *</label><input id="t-nom" value="${esc(t?.nom || '')}">
    <label>Objet *</label><input id="t-objet" value="${esc(t?.objet || '')}">
    <label>Catégorie</label>
    <select id="t-cat">
      <option value="candidature" ${t?.categorie === 'candidature' ? 'selected' : ''}>Candidature</option>
      <option value="relation" ${t?.categorie === 'relation' ? 'selected' : ''}>Relation</option>
      <option value="autre" ${!t || t?.categorie === 'autre' ? 'selected' : ''}>Autre</option>
    </select>
    <label>Corps *</label><textarea id="t-corps" rows="10">${esc(t?.corps || '')}</textarea>`;
  $('modal-ok').textContent = 'Enregistrer';
  $('modal-ok').onclick = async () => {
    const body = {
      id: t?.id || '',
      nom: $('t-nom').value.trim(),
      objet: $('t-objet').value.trim(),
      corps: $('t-corps').value.trim(),
      categorie: $('t-cat').value,
    };
    if (!body.nom || !body.objet || !body.corps) { toast('Nom, objet et corps requis', 'err'); return; }
    const d = await api('/api/templates', { method: 'POST', body });
    $('modal-overlay').classList.remove('visible');
    if (d.ok) { toast('Modèle enregistré', 'ok'); await loadTemplates(); }
    else toast(d.error || 'Erreur', 'err');
  };
  $('modal-overlay').classList.add('visible');
}

async function dupTpl(id) {
  const d = await api(`/api/templates/${encodeURIComponent(id)}/duplicate`, { method: 'POST' });
  if (d.ok) { toast('Modèle dupliqué', 'ok'); await loadTemplates(); }
  else toast(d.error || 'Erreur', 'err');
}

async function delTpl(id) {
  if (!confirm('Supprimer ce modèle ?')) return;
  const d = await api('/api/templates/' + encodeURIComponent(id), { method: 'DELETE' });
  if (d.ok) { toast('Modèle supprimé', 'ok'); await loadTemplates(); }
  else toast(d.error || 'Erreur', 'err');
}

/* ------------------------------------------------------------
   APERÇU — POST /api/preview
   ------------------------------------------------------------ */
async function previewLetter(company, context, template) {
  const d = await api('/api/preview', { method: 'POST', body: { company, context, template } });
  if (!d.ok) { toast(d.error || 'Aperçu impossible', 'err'); return null; }
  return d;
}

/* ------------------------------------------------------------
   COMPTES — GET/POST/DELETE /api/comptes
   ------------------------------------------------------------ */
async function loadComptes() {
  const d = await api('/api/comptes');
  comptes = d.comptes || [];
  renderComptes();
  majBanniereMdp();
}

function renderComptes() {
  const el = $('comptes-list');
  if (!el) return;
  const actifs = comptes.filter(c => c.actif).length;
  if ($('comptes-count')) $('comptes-count').textContent = `${actifs} actif(s) sur ${comptes.length}`;
  if (!comptes.length) {
    el.innerHTML = '<div class="empty-box">Aucun compte Gmail. Ajoute ton adresse d\u2019envoi ci-dessous.</div>';
    return;
  }
  const tplOptions = Object.entries(templatesDispo)
    .map(([id, t]) => `<option value="${esc(id)}">${esc(t.nom || id)}</option>`).join('');
  el.innerHTML = comptes.map(c => `
    <div class="list-item ${c.actif ? '' : 'inactive'}">
      <span class="tag ${c.actif ? 'ok' : ''}">${c.actif ? 'Actif' : 'Pause'}</span>
      <span class="grow"><b>${esc(c.email)}</b><br>
        <span class="help">${c.has_password ? (c.devoiler ? '🔑 cliquer Voir' : '🔑 enregistré (masqué)') : '⚠ mot de passe manquant'}</span>
      </span>
      <select data-action="compte-template" data-index="${c.index}" style="width:auto;min-width:150px">
        <option value="">Message global</option>${tplOptions}
      </select>
      <button class="btn small" data-action="test-compte" data-email="${esc(c.email)}">🔌 Tester</button>
      ${c.devoiler ? `<button class="btn small" data-action="reveal-compte" data-index="${c.index}">🔑 Voir</button>` : ''}
      <button class="btn small" data-action="toggle-compte" data-index="${c.index}">${c.actif ? '⏸' : '▶'}</button>
      <button class="btn danger small" data-action="del-compte" data-index="${c.index}">✖</button>
    </div>`).join('');

  el.querySelectorAll('[data-action="compte-template"]').forEach(sel => {
    sel.value = comptes.find(c => c.index == sel.dataset.index)?.template || '';
    sel.addEventListener('change', async () => {
      const d = await api(`/api/comptes/${sel.dataset.index}/template`, { method: 'POST', body: { template: sel.value } });
      d.ok ? toast('Modèle du compte mis à jour', 'ok') : toast(d.error || 'Erreur', 'err');
    });
  });
}

/* POST /api/comptes */
async function addCompte(email, password) {
  const d = await api('/api/comptes', { method: 'POST', body: { email, password } });
  if (d.ok) { toast('Compte enregistré (mot de passe chiffré)', 'ok'); $('new-password').value = ''; await Promise.all([loadComptes(), refreshStatus()]); }
  else toast(d.error || 'Erreur', 'err');
}

/* POST /api/comptes/test */
async function testCompte(email) {
  toast('Test SMTP en cours…');
  const d = await api('/api/comptes/test', { method: 'POST', body: { email } });
  d.ok ? toast(d.message || 'SMTP OK', 'ok') : toast(d.error || 'Échec', 'err');
}

/* Double contrôle reveal : POST /api/comptes/nonce puis /api/comptes/<idx>/reveal */
async function revealCompte(idx) {
  const n = await api('/api/comptes/nonce', { method: 'POST' });
  if (!n.ok) { toast(n.error || 'Nonce impossible', 'err'); return; }
  const d = await api(`/api/comptes/${idx}/reveal`, { method: 'POST', body: { nonce: n.nonce } });
  if (d.ok) toast(`🔑 ${d.email} : ${d.password}`, 'ok');
  else toast(d.error || 'Révélation refusée', 'err');
}

/* ------------------------------------------------------------
   PIÈCES — GET/POST/DELETE /api/pieces
   ------------------------------------------------------------ */
async function loadPieces() {
  const d = await api('/api/pieces');
  pieces = d.pieces || [];
  renderPieces();
}

function renderPieces() {
  const el = $('pieces-list');
  if (!el) return;
  const actifs = pieces.filter(p => p.actif).length;
  if ($('pieces-count')) $('pieces-count').textContent = `${actifs} active(s) sur ${pieces.length}`;
  if (!pieces.length) {
    el.innerHTML = '<div class="empty-box">Aucune pièce jointe. Ajoute un PDF (CV, lettre…).</div>';
    return;
  }
  el.innerHTML = pieces.map(p => `
    <div class="list-item ${p.actif ? '' : 'inactive'}">
      <span class="tag ${p.actif ? 'ok' : ''}">${p.actif ? 'Active' : 'Inactive'}</span>
      <span class="grow"><b>${esc(p.nom_original || p.id)}</b><br><span class="help">${p.taille_kb} Ko</span></span>
      <button class="btn small" data-action="toggle-piece" data-id="${esc(p.id)}">${p.actif ? '⏸' : '▶'}</button>
      <button class="btn danger small" data-action="del-piece" data-id="${esc(p.id)}">✖</button>
    </div>`).join('');
}

/* POST /api/pieces (multipart, PDF uniquement) */
async function uploadPieces(files) {
  for (const f of files) {
    if (!f.name.toLowerCase().endsWith('.pdf')) { toast('PDF requis : ' + f.name, 'err'); continue; }
    const fd = new FormData();
    fd.append('fichier', f);
    const d = await api('/api/pieces', { method: 'POST', body: fd });
    d.ok ? toast('PDF ajouté', 'ok') : toast(d.error || 'Erreur', 'err');
  }
  await Promise.all([loadPieces(), refreshStatus()]);
}

/* ------------------------------------------------------------
   GROUPES — GET/POST/DELETE /api/groupes
   ------------------------------------------------------------ */
async function loadGroupes() {
  const d = await api('/api/groupes');
  groupes = d.groupes || [];
  renderGroupes();
}

function renderGroupes() {
  const el = $('groupes-list');
  if (!el) return;
  if ($('groupes-count')) $('groupes-count').textContent = groupes.length;
  if (!groupes.length) {
    el.innerHTML = '<div class="empty-box">Aucun groupe. Crée-en un pour écrire à plusieurs contacts d\u2019un coup.</div>';
    return;
  }
  el.innerHTML = groupes.map(g => `
    <div class="list-item">
      <span class="tag">${g.emails.length} contact(s)</span>
      <span class="grow"><b>${esc(g.nom)}</b><br><span class="help">${esc(g.description || g.emails.join(', '))}</span></span>
      <button class="btn primary small" data-action="send-groupe" data-id="${esc(g.id)}">✉ Envoyer</button>
      <button class="btn danger small" data-action="del-groupe" data-id="${esc(g.id)}">✖</button>
    </div>`).join('');
}

function openGroupeModal(g = null) {
  if (profilSysteme()) { toast('Profil système en lecture seule — crée un vrai profil.', 'err'); return; }
  $('modal-title').textContent = g ? 'Modifier le groupe' : 'Nouveau groupe';
  $('modal-body').innerHTML = `
    <label>Nom *</label><input id="g-nom" value="${esc(g?.nom || '')}">
    <label>Description</label><input id="g-desc" value="${esc(g?.description || '')}">
    <label>Emails (un par ligne) *</label>
    <textarea id="g-emails" rows="6">${esc((g?.emails || []).join('\n'))}</textarea>`;
  $('modal-ok').textContent = 'Enregistrer';
  $('modal-ok').onclick = async () => {
    const body = {
      id: g?.id || '',
      nom: $('g-nom').value.trim(),
      description: $('g-desc').value.trim(),
      emails: $('g-emails').value.split('\n').map(e => e.trim()).filter(Boolean),
    };
    if (!body.nom || !body.emails.length) { toast('Nom et au moins un email requis', 'err'); return; }
    const d = await api('/api/groupes', { method: 'POST', body });
    $('modal-overlay').classList.remove('visible');
    if (d.ok) { toast('Groupe enregistré', 'ok'); await loadGroupes(); }
    else toast(d.error || 'Erreur', 'err');
  };
  $('modal-overlay').classList.add('visible');
}

/* POST /api/groupes/<id>/send */
async function sendGroupe(grpId) {
  const g = groupes.find(x => x.id === grpId);
  if (!g) return;
  $('modal-title').textContent = `Envoyer à « ${g.nom} »`;
  $('modal-body').innerHTML = `
    <p class="help">${g.emails.length} contact(s) — destinataires du groupe.</p>
    <label>Objet *</label><input id="s-subject">
    <label>Corps *</label><textarea id="s-body" rows="10"></textarea>
    <label>Mode</label>
    <select id="s-mode">
      <option value="individuel">Individuel (1 email par contact)</option>
      <option value="groupe">Groupe (tous en Cci)</option>
    </select>
    <label><input type="checkbox" id="s-pieces" checked style="width:auto"> Joindre les pièces actives</label>`;
  $('modal-ok').textContent = 'Envoyer';
  $('modal-ok').onclick = async () => {
    const body = {
      subject: $('s-subject').value.trim(),
      body: $('s-body').value.trim(),
      mode: $('s-mode').value,
      joindre_pieces: $('s-pieces').checked,
    };
    if (!body.subject || !body.body) { toast('Objet et corps requis', 'err'); return; }
    $('modal-overlay').classList.remove('visible');
    toast('Envoi en cours…');
    const d = await api(`/api/groupes/${encodeURIComponent(grpId)}/send`, { method: 'POST', body });
    if (d.message) toast(d.message, d.envoyes > 0 ? 'ok' : 'err');
    else toast(d.error || 'Échec', 'err');
    await refreshStatus();
  };
  $('modal-overlay').classList.add('visible');
}

/* ------------------------------------------------------------
   CONFIG — GET/POST /api/config
   ------------------------------------------------------------ */
async function loadConfig() {
  const d = await api('/api/config');
  const cand = d.candidat || {};
  const p = d.parametres || {};
  const setV = (id, v) => { const el = $(id); if (el) el.value = v ?? ''; };
  setV('cfg-nom', cand.nom);
  setV('cfg-tel', cand.tel);
  setV('cfg-email', cand.email);
  setV('cfg-ville', cand.ville);
  setV('cfg-pays', cand.pays);
  setV('cfg-diplome', cand.diplome);
  setV('cfg-spec', cand.spec);
  setV('cfg-template', p.template);
  setV('cfg-delai', p.delai_secondes);
  setV('cfg-maxh', p.max_par_heure);
  const chk = $('cfg-delai-alea');
  if (chk) chk.checked = !!p.delai_aleatoire;
  updateHeaderSub();
  fillTemplateSelects();
}

async function saveConfig() {
  const body = {
    candidat: {
      nom: $('cfg-nom').value.trim(),
      tel: $('cfg-tel').value.trim(),
      email: $('cfg-email').value.trim(),
      ville: $('cfg-ville').value.trim(),
      pays: $('cfg-pays').value.trim(),
      diplome: $('cfg-diplome').value.trim(),
      spec: $('cfg-spec').value.trim(),
    },
    parametres: {
      template: $('cfg-template').value,
      delai_secondes: parseInt($('cfg-delai').value, 10) || 40,
      max_par_heure: parseInt($('cfg-maxh').value, 10) || 100,
      delai_aleatoire: $('cfg-delai-alea').checked,
    },
  };
  if (!body.candidat.nom) { toast('Le nom du profil est obligatoire', 'err'); return; }
  const d = await api('/api/config', { method: 'POST', body });
  if (d.ok) { toast('Profil enregistré — les lettres utiliseront ces infos', 'ok'); await loadConfig(); }
  else toast(d.error || 'Erreur', 'err');
}

function updateHeaderSub() {
  const sub = $('header-sub');
  if (sub) sub.textContent = `${$('cfg-nom')?.value.trim() || 'Candidat'} · ${$('cfg-ville')?.value.trim() || 'Ma ville'}`;
}

/* ------------------------------------------------------------
   ENVOI UNITAIRE — POST /api/send
   ------------------------------------------------------------ */
async function sendOne(company) {
  const c = companies.find(x => x.name === company);
  const piecesActives = pieces.filter(p => p.actif).map(p => p.id);
  $('modal-title').textContent = `Envoyer à « ${company} »`;
  $('modal-body').innerHTML = `
    <p class="help">${esc(c?.email || '')}${c?.context ? ' — ' + esc(c.context) : ''}</p>
    <label>Destinataire(s) * (séparés par une virgule possible)</label>
    <textarea id="s-email" rows="2">${esc(c?.email || '')}</textarea>
    <label>Template</label><select id="s-template"></select>
    <label>Pièces jointes</label>
    <p class="help">${piecesActives.length ? piecesActives.map(p => '📄 ' + esc(p)).join('<br>') : '⚠ Aucune pièce active — envoi sans CV.'}</p>
    <div class="actions">
      <button class="btn small" data-action="do-preview">👁 Aperçu</button>
    </div>
    <div data-preview-zone style="display:none">
      <label>Objet</label><input data-preview-subject readonly>
      <label>Corps</label><textarea data-preview-body rows="10" readonly></textarea>
    </div>`;
  const selT = $('s-template');
  selT.innerHTML = Object.entries(templatesDispo).map(([id, t]) => `<option value="${esc(id)}">${esc(t.nom || id)}</option>`).join('');
  $('modal-body').querySelector('[data-action="do-preview"]').addEventListener('click', async () => {
    const d = await previewLetter(company, c?.context || '', selT.value);
    if (!d) return;
    const z = $('modal-body').querySelector('[data-preview-zone]');
    z.style.display = 'block';
    z.querySelector('[data-preview-subject]').value = d.subject;
    z.querySelector('[data-preview-body]').value = d.body;
  });
  $('modal-ok').textContent = 'Envoyer';
  $('modal-ok').onclick = async () => {
    const dest = $('s-email').value.trim();
    if (!dest || !dest.includes('@')) { toast('Destinataire valide requis', 'err'); return; }
    $('modal-overlay').classList.remove('visible');
    toast('Envoi en cours…');
    const d = await api('/api/send', {
      method: 'POST',
      body: { email: dest, company, pieces: piecesActives },
    });
    if (d.ok) {
      toast(d.message || 'Envoyé' + (d.sans_pj ? ' ⚠ sans pièce jointe' : ''), 'ok');
      await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]);
    } else toast(d.error || 'Échec', 'err');
  };
  $('modal-overlay').classList.add('visible');
}

/* Envoi express (formulaire libre de la page « Nouvel envoi ») */
async function sendCustom() {
  const dest = $('custom-email').value.trim();
  const company = $('custom-company').value.trim();
  const context = $('custom-context').value.trim();
  const template = $('custom-template').value;
  if (!dest || !company) { toast('Destinataire et entreprise requis', 'err'); return; }
  const pv = await previewLetter(company, context, template);
  if (!pv) return;
  $('custom-preview-zone').style.display = 'block';
  $('custom-preview-subject').value = pv.subject;
  $('custom-preview-body').value = pv.body;
  $('custom-info').textContent = 'Aperçu généré — vérifie puis envoie.';
}

async function sendCustomConfirm() {
  const dest = $('custom-email').value.trim();
  const company = $('custom-company').value.trim();
  const context = $('custom-context').value.trim();
  const template = $('custom-template').value;
  const pv = await previewLetter(company, context, template);
  if (!pv) return;
  const piecesActives = pieces.filter(p => p.actif).map(p => p.id);
  toast('Envoi en cours…');
  const d = await api('/api/send', {
    method: 'POST',
    body: { email: dest, company, subject: pv.subject, body: pv.body, pieces: piecesActives },
  });
  if (d.ok) { toast(d.message || 'Envoyé', 'ok'); await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]); }
  else toast(d.error || 'Échec', 'err');
}

/* ------------------------------------------------------------
   ENVOI DE MASSE — POST /api/send-bulk + status + stop
   ------------------------------------------------------------ */
async function startBulk(onlySelection) {
  let selected;
  if (onlySelection) {
    const names = new Set([...document.querySelectorAll('[data-select-company]:checked')].map(x => x.dataset.selectCompany));
    selected = companies.filter(c => names.has(c.name));
  } else {
    selected = companies.filter(c => !serverLog[c.name]?.envoye);
  }
  if (!selected.length) { toast('Aucune entreprise à contacter', 'err'); return; }
  const d = await api('/api/send-bulk', { method: 'POST', body: { companies: selected } });
  if (!d.ok) { toast(d.error || 'Impossible de lancer l\u2019envoi', 'err'); return; }
  toast(`Envoi de masse lancé (${d.total})`, 'ok');
  $('bulk-start').style.display = 'none';
  $('bulk-stop').style.display = '';
  if (bulkTimer) clearInterval(bulkTimer);
  bulkTimer = setInterval(pollBulk, 1200);
}

async function pollBulk() {
  const s = await api('/api/send-bulk-status');
  const bar = $('bulk-bar');
  if (bar) bar.style.width = s.total ? (100 * (s.index || 0) / s.total) + '%' : '0%';
  if ($('bulk-desc')) $('bulk-desc').textContent =
    s.en_cours ? `${s.index}/${s.total} — ${s.derniere || '…'} ✅ ${s.envoyes} ⚠ ${s.erreurs}` : 'Envoie aux entreprises non contactées';
  if (!s.en_cours) {
    clearInterval(bulkTimer);
    bulkTimer = null;
    $('bulk-start').style.display = '';
    $('bulk-stop').style.display = 'none';
    toast(`Envoi terminé : ${s.envoyes} OK, ${s.erreurs} erreur(s)`, s.erreurs ? 'err' : 'ok');
    await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]);
  }
}

async function stopBulk() {
  await api('/api/send-bulk-stop', { method: 'POST' });
  toast('Arrêt demandé', 'err');
}

/* ------------------------------------------------------------
   IMAP + FILTRES — /api/imap, /api/filtres
   ------------------------------------------------------------ */
async function loadFiltres() {
  const d = await api('/api/filtres');
  filtres = d.filtres || [];
  renderFiltres();
}

function filtresActions(f) {
  const icons = { label: '🏷', archive: '📦', marquer_lu: '👁', supprimer: '✖', notify: '🔔' };
  return (f.actions || []).map(a => icons[a] || a).join(' ');
}

function renderFiltres() {
  const el = $('regles-liste');
  if (!el) return;
  if ($('regles-count')) $('regles-count').textContent = filtres.length;
  if (!filtres.length) {
    el.innerHTML = '<div class="empty-box">Aucune règle. Les 6 règles par défaut sont créées au premier lancement du backend.</div>';
    return;
  }
  el.innerHTML = filtres.map((f, i) => `
    <div class="list-item ${f.enabled ? '' : 'inactive'}" draggable="true" data-id="${esc(f.id)}">
      <span class="tag">${f.priority}</span>
      <span class="grow"><b>${esc(f.icon || '')} ${esc(f.name)}</b><br>
        <span class="help">${(f.items || []).map(it => `${esc(it.champ)}~${esc(it.valeur)}`).join(' & ')} → ${filtresActions(f)}</span></span>
      <button class="btn small" data-action="toggle-filtre" data-idx="${i}">${f.enabled ? '⏸' : '▶'}</button>
      <button class="btn danger small" data-action="del-filtre" data-idx="${i}">✖</button>
    </div>`).join('');

  /* drag & drop → POST /api/filtres/reorder */
  let dragged = null;
  el.querySelectorAll('.list-item').forEach(item => {
    item.addEventListener('dragstart', () => { dragged = item; });
    item.addEventListener('dragover', e => e.preventDefault());
    item.addEventListener('drop', async e => {
      e.preventDefault();
      if (!dragged || dragged === item) return;
      dragged.parentNode.insertBefore(dragged, item);
      const ordre = [...el.querySelectorAll('.list-item')].map(x => x.dataset.id);
      const d = await api('/api/filtres/reorder', { method: 'POST', body: { ordre } });
      if (d.ok) await loadFiltres();
    });
  });
}

async function toggleFiltre(idx) {
  const d = await api(`/api/filtres/${idx}/toggle`, { method: 'POST' });
  if (d.ok) await loadFiltres();
}

async function delFiltre(idx) {
  if (!confirm('Supprimer cette règle ?')) return;
  const d = await api('/api/filtres/' + idx, { method: 'DELETE' });
  if (d.ok) await loadFiltres();
}

async function addFiltre() {
  const actions = [];
  if ($('act-label').checked) actions.push('label');
  if ($('act-lu').checked) actions.push('marquer_lu');
  if ($('act-notif').checked) actions.push('notify');
  if ($('act-archive').checked) actions.push('archive');
  if ($('act-supprimer').checked) actions.push('supprimer');
  const body = {
    name: $('flt-nom').value.trim(),
    label: $('flt-label').value.trim(),
    items: [{ champ: $('flt-champ').value, valeur: $('flt-valeur').value.trim() }],
    actions,
  };
  if (!body.name || !body.items[0].valeur) { toast('Nom et valeur requis', 'err'); return; }
  const d = await api('/api/filtres', { method: 'POST', body });
  if (d.ok) { toast('Règle ajoutée', 'ok'); await loadFiltres(); }
  else toast(d.error || 'Règle invalide', 'err');
}

/* POST /api/imap/check */
async function imapCheck() {
  toast('Vérification IMAP en cours (peut prendre une minute)…');
  const d = await api('/api/imap/check', { method: 'POST', body: { jours: 30 } });
  d.ok !== false ? toast('Vérification terminée', 'ok') : toast(d.error || 'Échec', 'err');
  await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]);
}

/* Apprentissage — POST /api/filtres/corriger */
async function apprendreFiltre() {
  const body = { email: $('app-email').value.trim(), label: $('app-label').value.trim(), notify: false };
  if (!body.email.includes('@') || !body.label) { toast('Email et libellé requis', 'err'); return; }
  const d = await api('/api/filtres/corriger', { method: 'POST', body });
  if (d.ok) { toast('Règle apprise et créée', 'ok'); await loadFiltres(); }
  else toast(d.error || 'Erreur', 'err');
}

/* GET /api/filtres/suggestions */
async function suggestionsFiltres() {
  const d = await api('/api/filtres/suggestions');
  const el = $('app-liste');
  if (!el) return;
  el.innerHTML = (d.suggestions || []).map(s =>
    `<div class="list-item"><span class="grow">${esc(typeof s === 'string' ? s : (s.message || s.texte || JSON.stringify(s)))}</span></div>`
  ).join('') || '<p class="help">Aucune suggestion pour le moment.</p>';
}

/* ------------------------------------------------------------
   NOTIFICATIONS — GET /api/notifications, POST /api/notifications/vue
   ------------------------------------------------------------ */
async function loadNotifications() {
  const d = await api('/api/notifications');
  const el = $('notifs-liste');
  if (!el) return;
  if ($('notifs-badge')) $('notifs-badge').textContent = d.non_vues || 0;
  el.innerHTML = (d.notifications || []).map(n =>
    `<div class="list-item"><span class="tag">${esc(n.type || 'info')}</span>
     <span class="grow">${esc(n.message || JSON.stringify(n))}</span></div>`
  ).join('') || '<p class="help">Aucune notification.</p>';
  if (d.non_vues) await api('/api/notifications/vue', { method: 'POST' });
}

/* ------------------------------------------------------------
   PROFILS — GET/POST /api/profils
   ------------------------------------------------------------ */
async function loadProfils() {
  const d = await api('/api/profils');
  const el = $('profil-liste');
  if (!el) return;
  const cur = uidHeader();
  let items = (d.profils || []);
  /* Le profil système #0 est proposé à la fin, marqué comme démo */
  const sysPresent = items.some(p => p.uid === 0);
  if (!sysPresent) items = [...items, { uid: 0, nom: 'Système (démo)' }];
  el.innerHTML = items.map(p => `
    <div class="profil-row ${String(p.uid) === cur ? 'active' : ''}" data-uid="${p.uid}">
      <span class="tag">#${p.uid}</span>
      <b>${esc(p.nom)}</b>
      ${p.uid === 0 ? '<span class="help">démo, lecture seule</span>' : ''}
      ${String(p.uid) === cur ? '<span class="tag" style="margin-left:auto">actif</span>' : ''}
    </div>`).join('')
    || '<p class="help">Aucun profil secondaire : le profil par défaut (#0) est utilisé.</p>';
  el.querySelectorAll('.profil-row').forEach(row => row.addEventListener('click', () => {
    const uid = row.dataset.uid;
    const nom = row.querySelector('b')?.textContent || `#${uid}`;
    sessionStorage.setItem('uid', uid);
    sessionStorage.setItem('uid_nom', nom);
    toast(`Profil « ${nom} » (#${uid}) sélectionné`, 'ok');
    $('profil-overlay').classList.remove('visible');
    init();
  }));
}

async function creerProfil() {
  const nom = $('profil-nom').value.trim();
  if (!nom) { toast('Nom requis', 'err'); return; }
  const d = await api('/api/profils', { method: 'POST', body: { nom } });
  if (d.ok) {
    sessionStorage.setItem('uid', String(d.uid));
    sessionStorage.setItem('uid_nom', nom);
    toast(`Profil « ${nom} » créé (#${d.uid}) — il est maintenant actif, vide et prêt à l'emploi.`, 'ok');
    $('profil-overlay').classList.remove('visible');
    init();
  } else toast(d.error || 'Erreur', 'err');
}

/* ------------------------------------------------------------
   HISTORIQUE — GET/DELETE /api/historique, undo/redo
   ------------------------------------------------------------ */
let historique = [];

async function loadHistorique() {
  const d = await api('/api/historique');
  historique = d.actions || [];
  renderHistorique();
}

function renderHistorique() {
  const el = $('hist-liste');
  if (!el) return;
  if (!historique.length) {
    el.innerHTML = '<div class="empty-box">Aucune action enregistrée.</div>';
    return;
  }
  el.innerHTML = historique.map(h => `
    <div class="list-item">
      <span class="tag">${esc(h.type)}</span>
      <span class="grow"><b>${esc(h.label)}</b><br><span class="help">${esc(h.date || '')}${h.undone ? ' — annulée' : ''}</span></span>
      ${h.undo || h.redo ? `<button class="btn small" data-action="hist-undo" data-id="${h.id}">${h.undone ? '↻ Refaire' : '↩ Annuler'}</button>` : ''}
    </div>`).join('');
}

async function histUndo(id) {
  const h = historique.find(x => x.id === id);
  const url = h?.undone ? `/api/historique/${id}/redo` : `/api/historique/${id}/undo`;
  const d = await api(url, { method: 'POST' });
  if (d.ok) { toast(d.message || 'Action appliquée', 'ok'); await loadHistorique(); await init(); }
  else toast(d.error || 'Erreur', 'err');
}

async function histVider() {
  if (!confirm('Effacer tout l\u2019historique ? Les actions passées ne seront plus annulables.')) return;
  const d = await api('/api/historique', { method: 'DELETE' });
  if (d.ok) { toast('Historique vidé', 'ok'); await loadHistorique(); }
}

/* ------------------------------------------------------------
   IA — GET /api/ia/catalogue, GET/POST /api/ia/config
   Clé API + modèle + température + max_tokens, par tâche.
   (Backend : candimail/services/ia_agent.py — IAConfig)
   ------------------------------------------------------------ */
let IA_CATALOGUE = null;   // {tasks: {...}, providers: {...}}
let IA_CONFIG = {};        // {task: {provider, apiKey, model, temperature, max_tokens}}

async function loadIa() {
  const cat = await api('/api/ia/catalogue');
  const cfg = await api('/api/ia/config');
  const el = $('ia-liste');
  if (!el) return;
  if (!cat.ok) { el.innerHTML = '<p class="help">Catalogue IA indisponible.</p>'; return; }
  IA_CATALOGUE = cat;
  IA_CONFIG = cfg || {};

  /* cat.tasks : le backend renvoie IA_TASKS, un dict {id: {label, default_model}}
     (jamais une liste — voir candimail/services/ia_agent.py). */
  const tasks = cat.tasks && typeof cat.tasks === 'object' && !Array.isArray(cat.tasks)
    ? Object.entries(cat.tasks).map(([id, t]) => ({ id, ...(t || {}) }))
    : [];

  el.innerHTML = tasks.map(t => {
    const cur = IA_CONFIG[t.id] || {};
    const provider = cur.provider || 'groq';
    const models = cat.providers[provider] ? cat.providers[provider].models : [];
    const model = cur.model || t.default_model || (models[0] || '');
    const providerOpts = Object.entries(cat.providers).map(([pid, p]) =>
      `<option value="${pid}" ${provider === pid ? 'selected' : ''}>${esc(p.label)}</option>`).join('');
    const modelOpts = models.map(m =>
      `<option value="${esc(m)}" ${model === m ? 'selected' : ''}>${esc(m)}</option>`).join('');
    return `
    <div class="list-item" data-task="${esc(t.id)}">
      <span class="grow"><b>${esc(t.label || t.id)}</b><br>
        <span class="help">modèle par défaut : ${esc(t.default_model || '—')}</span></span>
      <div>
        <label>Fournisseur</label>
        <select data-ia-provider style="width:auto;min-width:130px">${providerOpts}</select>
        <label>Modèle</label>
        <select data-ia-model style="width:auto;min-width:190px">${modelOpts}</select>
        <label>Clé API</label>
        <input type="password" data-ia-key placeholder="Clé API ${esc((cat.providers[provider] || {}).label || provider)}"
               value="${esc(cur.apiKey || '')}" style="width:220px">
        <div class="row" style="margin-top:6px">
          <div><label>Température</label>
            <input type="number" data-ia-temp min="0" max="2" step="0.1"
                   value="${cur.temperature ?? 0.7}" style="width:80px"></div>
          <div><label>Max tokens</label>
            <input type="number" data-ia-max min="128" max="8192" step="64"
                   value="${cur.max_tokens ?? 2048}" style="width:100px"></div>
        </div>
      </div>
    </div>`;
  }).join('') || '<p class="help">Aucune tâche IA exposée par le backend.</p>';

  el.querySelectorAll('.list-item').forEach(item => {
    const task = item.dataset.task;
    item.querySelector('[data-ia-provider]').addEventListener('change', e => {
      /* changer de fournisseur recharge la liste de modèles pour cette tâche */
      IA_CONFIG[task] = { ...(IA_CONFIG[task] || {}), provider: e.target.value, model: '' };
      loadIa();
    });
    item.querySelector('[data-ia-model]').addEventListener('change', e => saveIaTask(task, { model: e.target.value }));
    item.querySelector('[data-ia-key]').addEventListener('change', e => saveIaTask(task, { apiKey: e.target.value }));
    item.querySelector('[data-ia-temp]').addEventListener('change', e => saveIaTask(task, { temperature: parseFloat(e.target.value) || 0.7 }));
    item.querySelector('[data-ia-max]').addEventListener('change', e => saveIaTask(task, { max_tokens: parseInt(e.target.value, 10) || 2048 }));
  });
}

/* Fusionne les champs modifiés dans la config de la tâche puis POST complet
   (le backend écrit data/ia_config.json tel quel). */
async function saveIaTask(task, patch) {
  IA_CONFIG[task] = { ...(IA_CONFIG[task] || {}), ...patch };
  const d = await api('/api/ia/config', { method: 'POST', body: IA_CONFIG });
  d.ok ? toast('Config IA sauvegardée', 'ok') : toast(d.error || 'Erreur', 'err');
}

/* ------------------------------------------------------------
   EXPORTS / IMPORT / RESET
   ------------------------------------------------------------ */
async function importJson(file) {
  const fd = new FormData();
  fd.append('file', file);
  const d = await api('/api/import-json', { method: 'POST', body: fd });
  d.ok ? toast(`${d.importees} entrée(s) importée(s)`, 'ok') : toast(d.error || 'Import impossible', 'err');
  await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]);
}

/* ------------------------------------------------------------
   CV — GET/POST /api/cv (page /cv)
   ------------------------------------------------------------ */
async function saveCv(cv) {
  const d = await api('/api/cv', { method: 'POST', body: { cv } });
  d.ok ? toast('CV enregistré', 'ok') : toast(d.error || 'Erreur', 'err');
}

/* ------------------------------------------------------------
   Navigation
   ------------------------------------------------------------ */
const PAGES = {
  dash: 'Tableau de bord',
  envoi: 'Nouvel envoi',
  comptes: 'Comptes & pièces',
  messages: 'Mes modèles',
  groupes: 'Mes groupes',
  imap: 'Réponses & filtres',
  profil: 'Profil',
  chat: 'Assistant IA',
  historique: 'Historique',
  ia: 'Agent IA',
  params: 'Paramètres',
};

function goto(page) {
  if (!PAGES[page]) page = 'dash';
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const el = $('page-' + page);
  if (el) el.classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.nav === page));
  const bc = $('bc-page');
  if (bc) bc.textContent = PAGES[page];
  /* chargement paresseux des données de la page */
  if (page === 'comptes') { loadComptes(); loadPieces(); }
  if (page === 'messages') loadTemplates();
  if (page === 'groupes') loadGroupes();
  if (page === 'imap') { loadFiltres(); loadNotifications(); suggestionsFiltres(); }
  if (page === 'profil') loadConfig();
  if (page === 'historique') loadHistorique();
  if (page === 'ia') loadIa();
}

/* ------------------------------------------------------------
   Sélection multiple
   ------------------------------------------------------------ */
function updateSelection() {
  const n = document.querySelectorAll('[data-select-company]:checked').length;
  const el = $('sel-count');
  if (el) el.textContent = `${n} sélectionnée(s)`;
  const s = $('sel-send');
  if (s) s.disabled = !n;
  const d = $('sel-del');
  if (d) d.disabled = !n;
}

/* ------------------------------------------------------------
   Délégation d'événements globale
   ------------------------------------------------------------ */
document.addEventListener('click', async e => {
  if (e.target.matches('input[type="checkbox"][data-select-company]')) { updateSelection(); return; }
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const action = btn.dataset.action;
  const name = btn.dataset.name;

  switch (action) {
    case 'toggle-card': btn.closest('.card').classList.toggle('open'); break;
    case 'add-company': openCompanyModal(); break;
    case 'edit-company': openCompanyModal(name); break;
    case 'del-company': delCompany(name); break;
    case 'send-one': sendOne(name); break;
    case 'preview-one': {
      const c = companies.find(x => x.name === name);
      const d = await previewLetter(name, c?.context || '', $('custom-template')?.value || '');
      if (d) {
        const card = btn.closest('.card');
        const zone = card.querySelector('[data-preview]');
        zone.style.display = 'block';
        zone.querySelector('[data-preview-subject]').value = d.subject;
        zone.querySelector('[data-preview-body]').value = d.body;
      }
      break;
    }
    case 'toggle-reply': {
      if (await toggleReply(name)) renderCompanies();
      break;
    }
    case 'add-tpl': openTplModal(); break;
    case 'edit-tpl': openTplModal(templatesList.find(t => t.id === btn.dataset.id)); break;
    case 'dup-tpl': dupTpl(btn.dataset.id); break;
    case 'del-tpl': delTpl(btn.dataset.id); break;
    case 'add-groupe': openGroupeModal(); break;
    case 'del-groupe': {
      if (!confirm('Supprimer ce groupe ?')) break;
      {
        const d = await api('/api/groupes/' + encodeURIComponent(btn.dataset.id), { method: 'DELETE' });
        d.ok ? toast('Groupe supprimé', 'ok') : toast(d.error || 'Erreur', 'err');
        await loadGroupes();
      }
      break;
    }
    case 'send-groupe': sendGroupe(btn.dataset.id); break;
    case 'test-compte': testCompte(btn.dataset.email); break;
    case 'reveal-compte': revealCompte(btn.dataset.index); break;
    case 'toggle-compte': {
      const d = await api(`/api/comptes/${btn.dataset.index}/toggle`, { method: 'POST' });
      if (d.ok) { toast(d.actif ? 'Compte activé' : 'Compte en pause', 'ok'); await Promise.all([loadComptes(), refreshStatus()]); }
      break;
    }
    case 'del-compte': {
      if (!confirm('Supprimer ce compte Gmail ?')) break;
      {
        const d = await api(`/api/comptes/${btn.dataset.index}`, { method: 'DELETE' });
        if (d.ok) { toast('Compte supprimé', 'ok'); await loadComptes(); }
      }
      break;
    }
    case 'toggle-piece': {
      const d = await api(`/api/pieces/${encodeURIComponent(btn.dataset.id)}/toggle`, { method: 'POST' });
      if (d.ok) await Promise.all([loadPieces(), refreshStatus()]);
      break;
    }
    case 'del-piece': {
      if (!confirm('Supprimer ce PDF ?')) break;
      {
        const d = await api(`/api/pieces/${encodeURIComponent(btn.dataset.id)}`, { method: 'DELETE' });
        if (d.ok) await Promise.all([loadPieces(), refreshStatus()]);
      }
      break;
    }
    case 'toggle-filtre': toggleFiltre(btn.dataset.idx); break;
    case 'del-filtre': delFiltre(btn.dataset.idx); break;
    case 'hist-undo': histUndo(Number(btn.dataset.id)); break;
    case 'imap-check': imapCheck(); break;
    case 'filtre-add': addFiltre(); break;
    case 'apprendre': apprendreFiltre(); break;
    case 'filtre-appliquer': {
      toast('Application des règles…');
      const d = await api('/api/filtres/appliquer', { method: 'POST' });
      d.ok ? toast('Règles appliquées', 'ok') : toast(d.error || 'Erreur', 'err');
      break;
    }
    case 'filtre-libelles': {
      toast('Création des libellés…');
      const d = await api('/api/filtres/creer-libelles', { method: 'POST' });
      d.ok ? toast('Libellés créés dans Gmail', 'ok') : toast(d.error || 'Erreur', 'err');
      break;
    }
    case 'modal-close': $('modal-overlay').classList.remove('visible'); break;
    case 'profils-open': $('profil-overlay').classList.add('visible'); loadProfils(); break;
    case 'profils-close': $('profil-overlay').classList.remove('visible'); break;
    case 'profils-creer': creerProfil(); break;
  }
});

/* ------------------------------------------------------------
   Initialisation
   ------------------------------------------------------------ */
function hideSplash() {
  const s = $('splash');
  if (!s) return;
  s.classList.add('hidden');
  setTimeout(() => s.remove(), 300);
}

async function init() {
  try {
    await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies(), loadConfig()]);
    /* mémorise le nom du profil actif pour l'indicateur latéral */
    const pd = await api('/api/profils');
    const cur = uidHeader();
    const p = (pd.profils || []).find(x => String(x.uid) === cur);
    if (cur === '0') sessionStorage.setItem('uid_nom', 'Système (démo)');
    else if (p) sessionStorage.setItem('uid_nom', p.nom);
  } catch (e) {
    console.error('[candimail] init', e);
    toast('Backend injoignable — vérifie que le serveur tourne.', 'err');
  }
  appliquerVerrouProfil();
  hideSplash();
}

/* Profil système (#0) : lecture seule + bannière d'incitation à créer
   un vrai profil. Aucun envoi, aucune saisie possible. */
function appliquerVerrouProfil() {
  const lectureSeule = profilSysteme();
  const banniere = $('profil-systeme-banniere');
  if (banniere) banniere.style.display = lectureSeule ? 'block' : 'none';
  /* indicateur permanent du profil actif dans la barre latérale */
  const nomEl = $('profil-actif-nom');
  if (nomEl) {
    const nom = sessionStorage.getItem('uid_nom');
    nomEl.textContent = nom ? `${nom} (#${uidHeader()})` : `#${uidHeader()}`;
  }
  /* les formulaires de saisie du profil, comptes, PJ et envoi deviennent
     inutilisables sur le profil système */
  const ids = ['cfg-nom', 'cfg-tel', 'cfg-email', 'cfg-ville', 'cfg-pays',
               'cfg-diplome', 'cfg-spec', 'cfg-template', 'btn-save-config',
               'new-email', 'new-password', 'btn-add-compte',
               'pj-input', 'custom-email', 'custom-company',
               'custom-context', 'custom-template',
               'btn-custom-preview', 'btn-custom-send',
               'bulk-start', 'sel-send', 'chat-input', 'btn-chat-envoyer'];
  ids.forEach(id => {
    const el = $(id);
    if (el) el.disabled = lectureSeule;
  });
}

/* --------------------------------------------------------------
   ASSISTANT IA (chat) — POST /api/ia/chat
   -------------------------------------------------------------- */
function chatAjouter(texte, role) {
  const log = $('chat-log');
  if (!log) return;
  const bulle = document.createElement('div');
  bulle.className = 'list-item';
  bulle.style.background = role === 'user' ? '#FFF7CC' : 'var(--blanc)';
  bulle.innerHTML = `<span class="tag">${role === 'user' ? '👤 Toi' : '🤖 IA'}</span>
    <span class="grow" style="white-space:pre-wrap">${esc(texte)}</span>`;
  log.appendChild(bulle);
  log.scrollTop = log.scrollHeight;
}

async function envoyerChat() {
  const input = $('chat-input');
  const message = (input?.value || '').trim();
  if (!message) return;
  input.value = '';
  chatAjouter(message, 'user');
  chatAjouter('…', 'ia');
  const d = await api('/api/ia/chat', { method: 'POST', body: { message } });
  const log = $('chat-log');
  /* remplace la bulle « … » par la vraie réponse */
  if (log && log.lastChild) log.removeChild(log.lastChild);
  chatAjouter(d.ok ? (d.reponse || 'Réponse vide') : (d.error || 'Erreur'), 'ia');
}

/* Garde-fou anti-splash figé */
setTimeout(hideSplash, 10000);

/* ------------------------------------------------------------
   Wiring de la page (une fois le DOM prêt)
   ------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item').forEach(n => n.addEventListener('click', () => goto(n.dataset.nav)));
  goto('dash');

  const search = $('search');
  if (search) search.addEventListener('input', () => { searchQuery = search.value.trim(); renderCompanies(); });
  const chips = $('filters');
  if (chips) {
    chips.innerHTML = ['all', ...Object.keys(CATEGORIES)].map(k =>
      `<button class="chip ${k === 'all' ? 'active' : ''}" data-filter="${k}">${k === 'all' ? 'Tout' : esc(CATEGORIES[k])}</button>`).join('');
    chips.addEventListener('click', e => {
      const c = e.target.closest('[data-filter]');
      if (!c) return;
      activeFilter = c.dataset.filter;
      chips.querySelectorAll('.chip').forEach(x => x.classList.toggle('active', x === c));
      renderCompanies();
    });
  }

  $('bulk-start') && $('bulk-start').addEventListener('click', () => startBulk(false));
  $('bulk-stop') && $('bulk-stop').addEventListener('click', stopBulk);
  $('sel-send') && $('sel-send').addEventListener('click', () => startBulk(true));
  $('sel-del') && $('sel-del').addEventListener('click', async () => {
    const names = [...document.querySelectorAll('[data-select-company]:checked')].map(x => x.dataset.selectCompany);
    if (!names.length) return;
    if (!confirm(`Supprimer ${names.length} entreprise(s) ?`)) return;
    const d = await api('/api/companies', { method: 'DELETE', body: { names } });
    if (d.ok) { toast(`${d.supprimees} entreprise(s) supprimée(s)`, 'ok'); await Promise.all([loadCompanies(), refreshStatus()]); }
    else toast(d.error || 'Erreur', 'err');
  });

  $('btn-add-company') && $('btn-add-company').addEventListener('click', () => openCompanyModal());
  $('btn-add-compte') && $('btn-add-compte').addEventListener('click', () => {
    const email = $('new-email').value.trim();
    const password = $('new-password').value.trim();
    if (!email.includes('@') || !password) { toast('Email et mot de passe requis', 'err'); return; }
    addCompte(email, password);
  });
  $('pj-input') && $('pj-input').addEventListener('change', e => { if (e.target.files.length) uploadPieces([...e.target.files]); });
  $('btn-new-tpl') && $('btn-new-tpl').addEventListener('click', () => openTplModal());
  $('btn-new-groupe') && $('btn-new-groupe').addEventListener('click', () => openGroupeModal());
  $('btn-imap-check') && $('btn-imap-check').addEventListener('click', imapCheck);
  $('btn-flt-add') && $('btn-flt-add').addEventListener('click', addFiltre);
  $('btn-flt-appliquer') && $('btn-flt-appliquer').addEventListener('click', () => api('/api/filtres/appliquer', { method: 'POST' }).then(d => d.ok ? toast('Règles appliquées', 'ok') : toast(d.error, 'err')));
  $('btn-flt-libelles') && $('btn-flt-libelles').addEventListener('click', () => api('/api/filtres/creer-libelles', { method: 'POST' }).then(d => d.ok ? toast('Libellés créés', 'ok') : toast(d.error, 'err')));
  $('btn-app-corriger') && $('btn-app-corriger').addEventListener('click', apprendreFiltre);
  $('btn-save-config') && $('btn-save-config').addEventListener('click', saveConfig);
  $('cfg-nom') && $('cfg-nom').addEventListener('input', updateHeaderSub);
  $('cfg-ville') && $('cfg-ville').addEventListener('input', updateHeaderSub);
  $('custom-template') && $('custom-template').addEventListener('change', () => { $('custom-preview-zone').style.display = 'none'; $('custom-info').textContent = ''; });
  $('btn-custom-preview') && $('btn-custom-preview').addEventListener('click', sendCustom);
  $('btn-custom-send') && $('btn-custom-send').addEventListener('click', sendCustomConfirm);
  $('btn-import-json') && $('btn-import-json').addEventListener('click', () => $('import-json-input').click());
  $('import-json-input') && $('import-json-input').addEventListener('change', e => { if (e.target.files[0]) importJson(e.target.files[0]); });
  $('btn-reset-log') && $('btn-reset-log').addEventListener('click', async () => {
    if (!confirm('Vider le journal des envois ? (une sauvegarde .backup.json est créée)')) return;
    const d = await api('/api/reset-log', { method: 'POST' });
    d.ok ? toast('Journal vidé', 'ok') : toast(d.error, 'err');
    await Promise.all([refreshStatus(), chargerSuivi(), loadCompanies()]);
  });
  $('btn-hist-vider') && $('btn-hist-vider').addEventListener('click', histVider);
  $('btn-ia-reload') && $('btn-ia-reload').addEventListener('click', loadIa);
  $('btn-help-password') && $('btn-help-password').addEventListener('click', () =>
    window.open('https://myaccount.google.com/apppasswords', '_blank'));

  $('modal-overlay') && $('modal-overlay').addEventListener('click', e => { if (e.target === e.currentTarget) e.currentTarget.classList.remove('visible'); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.visible, .profil-overlay.visible').forEach(x => x.classList.remove('visible'));
  });

  init();
});
