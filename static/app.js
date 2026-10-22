?t>


/* ENTREPRISES ?? Données de D?MONSTRATION uniquement.


   Aucune référence à une entreprise ou une adresse e-mail réelle.


   Ces exemples servent de modèle : remplacez-les par vos propres cibles. */


let COMPANIES = [


  { cat:'grands', name:'[Démo] Conglomérat BTP Alpha', email:'exemple.grands1@exemple.com',


    context:`Exemple de contexte pour un grand groupe : décrivez ici ce qui vous attire dans cette entreprise (grands projets d'infrastructure, expertise internationale, etc.).` },


  { cat:'grands', name:'[Démo] Infrastructures Beta SA', email:'exemple.grands2@exemple.com',


    context:`Exemple de contexte : mentionnez un projet précis de l'entreprise et votre proximité géographique avec son chantier.` },


  { cat:'grands', name:'[Démo] Groupe Gamma Travaux', email:'exemple.grands3@exemple.com',


    context:`Exemple de contexte : soulignez la réputation du groupe en matière de formation des jeunes ingénieurs.` },


  { cat:'grands', name:'[Démo] Routes & Ouvrages Delta', email:'exemple.grands4@exemple.com',


    context:`Exemple de contexte : référencez le domaine d'activité (routes, ouvrages d'art) qui motive votre candidature.` },


  { cat:'grands', name:'[Démo] Bàtiment Epsilon', email:'exemple.grands5@exemple.com',


    context:`Exemple de contexte : exprimez votre intérêt pour les standards techniques du groupe.` },


  { cat:'grands', name:'[Démo] Holding Zeta Construction', email:'exemple.grands6@exemple.com',


    context:`Exemple de contexte : montrez que vous suivez l'actualité de l'entreprise.` },


  { cat:'grands', name:'[Démo] Voiries et Assainissement Eta', email:'exemple.grands7@exemple.com',


    context:`Exemple de contexte : citez le secteur précis (voiries, assainissement) qui vous intéresse.` },


  { cat:'grands', name:'[Démo] Ingénierie Thêta', email:'exemple.grands8@exemple.com',


    context:`Exemple de contexte : dynamisme de l'entreprise dans le BTP régional.` },


  { cat:'pme', name:'[Démo] PME Construct 1', email:'exemple.pme1@exemple.com',


    context:`Exemple de contexte pour une PME : création récente, projets locaux, polyvalence attendue d'un stagiaire.` },


  { cat:'pme', name:'[Démo] PME Travaux 2', email:'exemple.pme2@exemple.com',


    context:`Exemple de contexte : domaine technique qui vous intéresse (hydraulique, VRD, etc.).` },


  { cat:'pme', name:'[Démo] PME Ingénierie 3', email:'exemple.pme3@exemple.com',


    context:`Exemple de contexte : orientation de carrière que l'entreprise peut vous offrir.` },


  { cat:'pme', name:'[Démo] PME Bàtiment 4', email:'exemple.pme4@exemple.com',


    context:`Exemple de contexte : réputation de l'entreprise dans le bâtiment local.` },


  { cat:'pme', name:'[Démo] PME Matériaux 5', email:'exemple.pme5@exemple.com',


    context:`Exemple de contexte : double activité (génie civil + négoce) qui offre une vision complète du secteur.` },


  { cat:'pme', name:'[Démo] PME Suivi Chantier 6', email:'exemple.pme6@exemple.com',


    context:`Exemple de contexte : stage de perfectionnement en direction technique, suivi de chantiers, contrôle qualité.` },


  { cat:'pme', name:'[Démo] PME ?lectrotech 7', email:'exemple.pme7@exemple.com',


    context:`Exemple de contexte : offre de stage correspondant à votre niveau de formation.` },


  { cat:'pme', name:'[Démo] PME Commerce 8', email:'exemple.pme8@exemple.com',


    context:`Exemple de contexte : dimension technico-commerciale du BTP que vous souhaitez découvrir.` },


  { cat:'pme', name:'[Démo] PME Internationale 9', email:'exemple.pme9@exemple.com',


    context:`Exemple de contexte : structure de taille intermédiaire offrant une formation polyvalente.` },


  { cat:'pme', name:'[Démo] PME Architecture 10', email:'exemple.pme10@exemple.com',


    context:`Exemple de contexte : double approche architecture + génie civil.` },


  { cat:'pme', name:'[Démo] PME Terrains 11', email:'exemple.pme11@exemple.com',


    context:`Exemple de contexte : capacité à intervenir sur des terrains complexes.` },


  { cat:'pme', name:'[Démo] PME Nationale 12', email:'exemple.pme12@exemple.com',


    context:`Exemple de contexte : couverture nationale, expérience du secteur.` },


  { cat:'pme', name:'[Démo] PME Routière 13', email:'exemple.pme13@exemple.com',


    context:`Exemple de contexte : projets d'asphaltage et de réhabilitation routière.` },


  { cat:'pme', name:'[Démo] PME Croissance 14', email:'exemple.pme14@exemple.com',


    context:`Exemple de contexte : entreprise régionale en pleine croissance.` },


  { cat:'pme', name:'[Démo] PME Multi-régions 15', email:'exemple.pme15@exemple.com',


    context:`Exemple de contexte : construction + travaux publics, présence multi-régions.` },


  { cat:'port', name:'[Démo] Port & Logistique 1', email:'exemple.port1@exemple.com',


    context:`Exemple de contexte pour un acteur portuaire : importance stratégique du port dans l'économie régionale.` },


  { cat:'port', name:'[Démo] Port ?? Direction Stratégie', email:'exemple.port2@exemple.com',


    context:`Exemple de contexte : prise de contact directe avec un responsable.` },


  { cat:'port', name:'[Démo] Port ?? Partenariats PPP', email:'exemple.port3@exemple.com',


    context:`Exemple de contexte : intérêt pour les partenariats public-privé dans les infrastructures portuaires.` },


  { cat:'port', name:'[Démo] Entreprise Portuaire 2', email:'exemple.port4@exemple.com',


    context:`Exemple de contexte : entreprise locale d'une ville portuaire en expansion.` },


  { cat:'port', name:'[Démo] Groupe Agro-Port 3', email:'exemple.port5@exemple.com',


    context:`Exemple de contexte : activités à la croisée du BTP et de la gestion industrielle.` },


  { cat:'port', name:'[Démo] Transport & Logistique 4', email:'exemple.port6@exemple.com',


    context:`Exemple de contexte : logistique comme prolongement du BTP.` },


  { cat:'port', name:'[Démo] Laboratoire BTP 5', email:'exemple.port7@exemple.com',


    context:`Exemple de contexte : contrôle qualité des matériaux et des ouvrages.` },


  { cat:'port', name:'[Démo] Industrie Port 6', email:'exemple.port8@exemple.com',


    context:`Exemple de contexte : industrie majeure présente dans la zone portuaire.` },


];





/* ?TAT GLOBAL ?? ces déclarations doivent précéder tout rendu.


   Plusieurs d'entre elles avaient disparu : la première lecture


   (getFiltered, refreshStatus, polling?) levait une ReferenceError. */


const CATEGORIES = {


  grands:'Grands groupes', pme:'PME dynamiques', port:'Port & maritime',


};


let TEMPLATES_DISPO = {};


let templatesCache = [];


let predefinis = {};


let groupesCache = [];


let piecesActives = 0;


let rateLimit = { utilises: 0, max: 30, ok: true };


let activeFilter = 'all';


let searchQuery = '';


let bulkPollTimer = null;


let currentSendCompany = null;





/* ---------------------------------------------------------------


   serverLog ?? état d'envoi côté serveur, indexé par NOM d'entreprise.





   BUG CORRIG? : cette variable était lue en 6 endroits (renderCard,


   updateStats, filtres de sélection, bascule réponse/bounce) mais


   n'était JAMAIS déclarée. Lire une variable non déclarée lève


   « ReferenceError: serverLog is not defined » ?? l'exception était


   avalée par le try/catch de syncCompanies(), donc le tableau de


   bord s'affichait vide et les statistiques restaient bloquées,


   sans aucune erreur visible à l'écran.





   Elle est alimentée par /api/suivi (source unique, partagée avec


   la sous-page Suivi des envois).


--------------------------------------------------------------- */


let serverLog = {};        // { "Nom Entreprise": {envoye, repondu, ...} }


let SUIVI = { items: [], total: 0, envoyes: 0, repondus: 0,


              bounces: 0, echecs: 0, sans_pj: 0, jours: [] };





/* STATUS ?? source des badges, des pièces actives et du rate limit. */


async function refreshStatus() {


  try {


    const r = await fetch('/api/status');


    if (r.status === 401) { toast('Session expirée', 'err'); return; }


    const data = await r.json();


    serverLog = data.log || {};


    piecesActives = data.pieces_count || 0;


    rateLimit = data.rate_limit || rateLimit;





    const cvBadge = document.getElementById('cv-badge');


    if (cvBadge) {


      cvBadge.textContent = piecesActives > 0 ? `??? ${piecesActives} pièce(s)` : '??? 0 pièce';


      cvBadge.className = 'badge-cv ' + (piecesActives > 0 ? 'ok' : 'warn');


    }





    const nb = data.comptes_actifs || 0;


    const cptBadge = document.getElementById('comptes-badge');


    if (cptBadge) {


      cptBadge.textContent = `?? ${nb}`;


      cptBadge.className = 'badge-cv ' + (nb > 0 ? 'ok' : 'warn');


    }


    const sideCpt = document.getElementById('side-comptes');


    if (sideCpt) sideCpt.textContent = nb;





    const rlBadge = document.getElementById('rate-badge');


    if (rlBadge) {


      rlBadge.textContent = `⏱ ${rateLimit.utilises}/${rateLimit.max}`;


      rlBadge.className = 'badge-cv ' + (rateLimit.ok ? 'ok' : 'warn');


    }





    const warn = document.getElementById('pj-warning');


    if (warn) warn.style.display = piecesActives === 0 ? 'flex' : 'none';


    const pjWarn = document.getElementById('pj-warn-badge');


    if (pjWarn) pjWarn.style.display = piecesActives === 0 ? '' : 'none';





    updateStats();


    render();


    updateOverview();


  } catch (e) {


    console.error('[candimail] refreshStatus', e);


  }


}





/** Recharge le suivi depuis l'API et reconstruit l'index serverLog. */


async function chargerSuivi() {


  try {


    const r = await fetch('/api/suivi');


    const d = await r.json();


    if (!d.ok) throw new Error(d.error || 'Suivi indisponible');


    SUIVI = d;


    const index = {};


    for (const l of d.items || []) index[l.company] = l;


    serverLog = index;


  } catch (e) {


    console.error('[candimail] chargerSuivi', e);


    // Un suivi indisponible ne doit pas empêcher l'envoi :


    // on laisse serverLog vide et l'interface reste utilisable.


    serverLog = {};


  }


  return serverLog;


}





/* ---------------------------------------------------------------


   Bascule « réponse reçue » ?? source unique partagée par :


     - les cartes du tableau de bord (data-action="toggle-reply")


     - la sous-page Suivi (data-suivi-action)


   L'ancienne version duplicated ce fetch dans le handler des


   cartes : le serverLog n'était jamais mis à jour côté client,


   la carte restait donc visuellement inchangée après un clic.


--------------------------------------------------------------- */


async function toggleReply(company, force) {


  const actuel = !!serverLog[company]?.repondu;


  const cible = typeof force === 'boolean' ? force : !actuel;


  if (actuel === cible) return { ok: true, inchange: true };


  const r = await fetch('/api/mark-response', {


    method: 'POST',


    headers: { 'Content-Type': 'application/json' },


    body: JSON.stringify({ company, repondu: cible }),


  });


  if (r.status === 401) throw new Error('Session expirée');


  const d = await r.json();


  if (!d.ok) throw new Error(d.error || 'Erreur');


  // Mise à jour optimiste : l'interface réagit sans attendre


  // un rechargement complet du suivi.


  if (serverLog[company]) serverLog[company].repondu = cible;


  return d;


}





/* Recharge le back-end (bouton « Actualiser ») ?? resynchronise toutes les données */


async function refreshBackend(btn) {


  const label = btn.textContent;


  btn.disabled = true;


  btn.textContent = '?';


  try {


    const r = await fetch('/api/refresh-backend', { method: 'POST' });


    const data = await r.json();


    if (!data.ok) throw new Error(data.error || 'Erreur');


    toast(`??? Back-end rechargé (${data.heure})`, 'ok');


    // Tout re-synchroniser avec le serveur fraîchement rechargé


    await Promise.all([loadConfig(), loadTemplates(), loadPieces(),


                       loadGroupes(), loadIMAPStatus()]);


    await refreshStatus();


    await syncCompanies();


  } catch (e) {


    console.error(e);


    toast('? Impossible de recharger le back-end', 'err');


  } finally {


    btn.disabled = false;


    btn.textContent = label;


  }


}





/* CONFIG */


async function loadConfig() {


  try {


    const r = await fetch('/api/config');


    const cfg = await r.json();


    const cand = cfg.candidat || {};


    const params = cfg.parametres || {};


    document.getElementById('cfg-nom').value      = cand.nom || '';


    const telFull = cand.tel || '';


    const m = telFull.match(/^(\+\d+)\s?(.*)$/);


    if (m) {


      document.getElementById('cfg-tel-indicatif').value = m[1];


      document.getElementById('cfg-tel').value = m[2];


    } else {


      document.getElementById('cfg-tel-indicatif').value = '+33';


      document.getElementById('cfg-tel').value = telFull;


    }


    document.getElementById('cfg-email').value    = cand.email || '';


    document.getElementById('cfg-ville').value    = cand.ville || '';





    if (!params.delai_aleatoire) {


      document.getElementById('cfg-delai').value = params.delai_secondes || 40;


    }


    document.getElementById('cfg-delai-alea').checked = !!params.delai_aleatoire;


    document.getElementById('cfg-maxh').value = params.max_par_heure || 100;





    updateHeaderSub();


    updateSignaturePreview();


    TEMPLATES_DISPO = cfg.templates_dispo || {};


    renderComptes(cfg.comptes || []);


    updateOverview();


  } catch (e) { console.error(e); }


}





function initialesDe(nom) {


  const mots = String(nom || '').trim().split(/\s+/).filter(Boolean);


  if (!mots.length) return 'CA';


  return (mots[0][0] + (mots.length > 1 ? mots[mots.length - 1][0] : '')).toUpperCase();


}





function updateHeaderSub() {


  const nom   = document.getElementById('cfg-nom').value.trim()   || 'Candidat';


  const ville = document.getElementById('cfg-ville').value.trim() || '??';


  const sub = document.getElementById('header-sub');


  if (sub) sub.textContent = `${nom} · ${ville}`;





  const nomSide = document.getElementById('sidebar-nom');


  if (nomSide) nomSide.textContent = nom;


  const ini = initialesDe(nom);


  ['sidebar-avatar', 'top-avatar'].forEach(id => {


    const el = document.getElementById(id);


    if (el) el.textContent = ini;


  });


}





/* Aperçu live de la signature : montre l'effet du profil sur les lettres. */


function updateSignaturePreview() {


  const el = document.getElementById('cfg-apercu');


  if (!el) return;


  const nom   = document.getElementById('cfg-nom').value.trim();


  const tel   = (document.getElementById('cfg-tel-indicatif').value.trim() + ' ' + document.getElementById('cfg-tel').value.trim()).trim();


  const ville = document.getElementById('cfg-ville').value.trim();


  if (!nom && !ville) { el.textContent = '??'; return; }


  const lieu = [ville].filter(Boolean).join(', ');


  el.textContent = [nom, tel, lieu].filter(Boolean).join(' · ');


}





async function saveCandidatConfig() {


  const payload = {


    candidat: {


      nom:     document.getElementById('cfg-nom').value.trim(),


      tel:     (document.getElementById('cfg-tel-indicatif').value.trim() + ' ' + document.getElementById('cfg-tel').value.trim()).trim(),


      email:   document.getElementById('cfg-email').value.trim(),


      ville:   document.getElementById('cfg-ville').value.trim(),


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


      toast('Profil enregistré ?? les lettres utiliseront ces informations', 'ok');


      updateHeaderSub();


      updateSignaturePreview();


      loadConfig();          // réaligne les champs sur la valeur réellement stockée


    } else {


      toast(data.error || 'Enregistrement impossible', 'err');


    }


  } catch (e) { toast('Erreur réseau', 'err'); }


}





/* Restaure les valeurs d'origine du profil (modifiable ensuite / annulable). */


function reinitialiserProfil() {


  const D = {


    'cfg-nom':             'Candidat Démo',


    'cfg-tel-indicatif':   '+33',


    'cfg-tel':             '00 00 00 00 00',


    'cfg-email':           'candidat.demo@exemple.com',


    'cfg-ville':           'Ma Ville',


  };


  Object.entries(D).forEach(([id, val]) => {


    const el = document.getElementById(id);


    if (el) el.value = val;


  });


  updateHeaderSub();


  updateSignaturePreview();


  toast('Valeurs d\'origine restaurées ?? cliquez sur « Enregistrer le profil »', 'ok');


}





/* COMPTES */


function renderComptes(comptes) {


  const el = document.getElementById('comptes-list');


  const actifs = comptes.filter(c => c.actif).length;


  document.getElementById('comptes-count').textContent = `${actifs} actif(s)`;


  if (typeof updateOverview === 'function') updateOverview();


  if (!comptes.length) {


    el.innerHTML = `<div class="empty-box">?️ Aucun compte Gmail configuré.</div>`;


    return;


  }


  const tplOptions = Object.entries(TEMPLATES_DISPO)


    .map(([id, t]) => `<option value="${escapeHtml(id)}">${escapeHtml(t.nom || id)}</option>`)


    .join('');


  el.innerHTML = comptes.map(c => `


    <div class="compte-row ${c.actif ? 'active' : 'inactive'}">


      <span style="font-size:18px">${c.actif ? '??' : '⏸️'}</span>


      <div style="flex:1;min-width:180px">


        <div style="font-weight:700;font-size:13px">${escapeHtml(c.email)}


          <span style="font-size:10px;font-weight:800;text-transform:uppercase;


                color:${c.actif ? '#1E7A3C' : 'var(--muted)'}">${c.actif ? '? actif' : '? en pause'}</span>


        </div>


        <div style="font-size:11px;color:var(--muted)">


          ${c.has_password


            ? (c.devoiler


              ? `??? <span class="compte-mdp" data-index="${c.index}" data-email="${escapeHtml(c.email)}"


                   title="Cliquer pour afficher/masquer le mot de passe d'application (16 caractères)"


                   style="cursor:pointer;user-select:all;font-family:Consolas,monospace;


                          letter-spacing:1px;background:#F2E7CE;border:1px solid var(--border);


                          padding:1px 6px;border-radius:4px;">????????????????</span>`


              : '??? mot de passe enregistré (masqué)')


            : '? mot de passe manquant'}


        </div>


      </div>


      <select class="compte-tpl" data-index="${c.index}" title="Message utilisé par ce compte"


              style="padding:6px 8px;font-size:12px;font-weight:600;border:2px solid var(--border);


                     background:#fff;max-width:220px">


        <option value="" ${!c.template ? 'selected' : ''}>?? Message global</option>


        ${tplOptions}


      </select>


      <button class="btn small" data-action="test-compte" data-email="${escapeHtml(c.email)}">? Tester</button>


      ${c.devoiler ? `<button class="btn small" data-action="reveal-compte" data-index="${c.index}" title="Révélation autorisée pour ce compte">??️ Voir</button>` : ''}


      <button class="btn small" data-action="toggle-compte" data-index="${c.index}">


        ${c.actif ? '⏸️' : '?️'}


      </button>


      <button class="btn small danger" data-action="delete-compte" data-index="${c.index}">???️</button>


    </div>


  `).join('');





  Motion.cascade(el, ':scope > div');   // apparition en cascade


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





  // ???? Mot de passe 16 car. affiché en ligne dans le dashboard (cliquer pour révéler) ????


  el.querySelectorAll('.compte-mdp').forEach(s => {


    s.addEventListener('click', async () => {


      if (s.dataset.mdp) {                       // déjà chargé ?? basculer masqué/visible


        s.textContent = s.textContent.startsWith('?') ? s.dataset.mdp : '?'.repeat(16);


        return;


      }


      const old = s.textContent; s.textContent = '⏳';


      try {


        const d = await revelerMotDePasse(s.dataset.index);


        if (!d.ok) { s.textContent = old; toast('? ' + (d.error || 'Erreur'), 'err'); return; }


        s.dataset.mdp = d.password;


        s.textContent = d.password;


        s.title = d.longueur === 16


          ? '?? 16 caractères ?? mot de passe d\'application correct'


          : `?️ ${d.longueur} caractères ?? ce n\'est pas un mot de passe d\'application`;


        toast(d.longueur === 16 ? '?? 16 caractères ?? format correct'


                                : `?️ ${d.longueur} caractères`, d.longueur === 16 ? 'ok' : 'err');


      } catch (e) { s.textContent = old; toast('? Erreur réseau', 'err'); }


    });


  });


}





// ???? Révélation d'un mot de passe d'application (double contrôle serveur) ????


// Le serveur exige (1) un opt-in `devoiler` sur le compte et (2) un nonce


// anti-CSRF lié à la session. Le nonce n'est jamais renvoyé ailleurs.


let _nonceCache = null, _nonceExpiry = 0;


async function getNonce() {


  const now = Date.now();


  if (_nonceCache && now < _nonceExpiry) return _nonceCache;


  const r = await fetch('/api/comptes/nonce', {


    method: 'POST', headers: { 'Content-Type': 'application/json' }


  });


  const d = await r.json();


  if (!d.ok || !d.nonce) return null;


  _nonceCache = d.nonce;


  _nonceExpiry = now + 10 * 60 * 1000;   // marge sur les 15 min serveur


  return _nonceCache;


}





async function revelerMotDePasse(index) {


  const nonce = await getNonce();


  if (!nonce) return { ok: false, error: 'Session expirée ?? recharge la page' };


  const r = await fetch(`/api/comptes/${index}/reveal`, {


    method: 'POST',


    headers: { 'Content-Type': 'application/json' },


    body: JSON.stringify({ nonce })


  });


  if (!r.ok) { _nonceCache = null; }        // nonce consommé ?? on en-demandera un autre


  const d = await r.json();


  if (!d.ok) _nonceCache = null;


  return d;


}





// ???? Ouvre les identifiants dans un NOUVEL ONGLET (vérification visuelle) ????


async function afficherIdentifiantsOnglet(btn) {


  const libelle = btn.textContent;


  btn.disabled = true; btn.textContent = '⏳ Chargement?';


  try {


    const d = await revelerMotDePasse(btn.dataset.index);


    if (!d.ok) { toast('? ' + (d.error || 'Erreur'), 'err'); return; }





    const ok16 = d.longueur === 16;


    const html = `<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">


<title>Identifiants ?? ${d.email}</title>


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


 <h1>??? Identifiants du compte</h1>


 <p class="sub">Vérification ?? mot de passe d'application Gmail</p>


 <label>Compte Gmail</label>


 <div class="val">${d.email}</div>


 <label>Mot de passe d'application</label>


 <div class="val mdp">${d.password}</div>


 <p class="etat">${ok16


   ? '?? 16 caractères ?? format correct'


   : `?️ ${d.longueur} caractères ?? ce n'est pas un mot de passe d'application (il doit faire exactement 16 caractères)`}</p>


 <button onclick="window.close()">Fermer cet onglet</button>


</div></body></html>`;





    const win = window.open('', '_blank');


    if (win) {


      win.document.write(html);


      win.document.close();


    } else {


      // Popup bloqué ?? repli sur le modal dans la page courante


      afficherIdentifiants(d.email, d.password, d.longueur);


    }


  } catch (e) { toast('? Erreur réseau', 'err'); }


  // Restauration garantie du bouton, même en cas d'erreur


  btn.disabled = false; btn.textContent = libelle;


}





// ???? Panneau de vérification des identifiants (Gmail + mot de passe 16 car.) ????


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


      <h2 style="margin:0 0 4px;font-size:17px;text-transform:uppercase;">??? Identifiants du compte</h2>


      <p style="margin:0 0 16px;font-size:12px;color:#7A6E5B;font-weight:600;">


        Vérification ?? mot de passe d'application Gmail</p>


      <label style="display:block;font-size:11px;font-weight:800;text-transform:uppercase;">Compte Gmail</label>


      <div style="border:2px solid #43161C;padding:8px 10px;font-size:14px;margin:4px 0 12px;


                  user-select:all;background:#F2E7CE;">${escapeHtml(email)}</div>


      <label style="display:block;font-size:11px;font-weight:800;text-transform:uppercase;">


        Mot de passe d'application (16 caractères)</label>


      <div style="border:2px solid #43161C;padding:8px 10px;font-size:16px;letter-spacing:2px;


                  margin:4px 0 8px;user-select:all;background:#F2E7CE;


                  font-family:Consolas,monospace;word-break:break-all;">${escapeHtml(mdp)}</div>


      <p style="margin:0 0 14px;font-size:12px;font-weight:700;">


        ${ok16 ? '?? 16 caractères ?? format correct'


               : `?️ ${longueur} caractères ?? ce n\u2019est pas un mot de passe d\u2019application\n                     (il doit faire exactement 16 caractères)`.replace(/\n +/, ' ')}


      </p>


      <div style="display:flex;gap:8px;">


        <button id="cop-mdp" style="flex:1;padding:10px;font-weight:800;cursor:pointer;


                background:#1E5AA8;color:#fff;border:2px solid #43161C;">??? Copier</button>


        <button id="ferm-idf" style="flex:1;padding:10px;font-weight:800;cursor:pointer;


                background:#fff;border:2px solid #43161C;">Fermer</button>


      </div>


    </div>`;


  ov.querySelector('#ferm-idf').onclick = () => ov.remove();


  ov.addEventListener('click', e => { if (e.target === ov) ov.remove(); });


  ov.querySelector('#cop-mdp').onclick = async () => {


    try { await navigator.clipboard.writeText(mdp); toast('??? Mot de passe copié', 'ok'); }


    catch (e) { toast('? Copie impossible', 'err'); }


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





/* PI?CES */


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


    el.innerHTML = `<div class="empty-box">?️ Aucune pièce jointe.</div>`;


    return;


  }


  el.innerHTML = pieces.map(p => `


    <div class="piece-item ${p.actif ? '' : 'inactive'}">


      <input type="checkbox" ${p.actif ? 'checked' : ''}


             data-action="toggle-piece" data-id="${escapeHtml(p.id)}"


             style="width:18px;height:18px;accent-color:var(--ok);cursor:pointer">


      <div style="flex:1;min-width:0">


        <div style="font-weight:600;font-size:13px">??? ${escapeHtml(p.nom_original)}</div>


        <div style="font-size:11px;color:var(--muted)">${p.taille_kb} Ko</div>


      </div>


      <button class="btn small danger" data-action="del-piece" data-id="${escapeHtml(p.id)}">???️</button>


    </div>


  `).join('');





  Motion.cascade(el, ':scope > div');   // apparition en cascade


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


    } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


  }


  await loadPieces(); await refreshStatus();


  if (nb > 0) toast(`${nb} fichier(s) ajouté(s)`, 'ok');


}





/* TEMPLATES */


const CAT_ICONS = { candidature:'??', parents:'????????', collegues:'??', amis:'???', autre:'???' };





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


      <span style="font-size:20px">${CAT_ICONS[t.categorie] || '??'}</span>


      <div style="flex:1;min-width:180px">


        <div style="font-weight:600;font-size:14px">${escapeHtml(t.nom)}</div>


        <div style="font-size:11px;color:var(--muted);margin-top:2px;


                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap">


          ${escapeHtml(t.objet)}


        </div>


      </div>


      <button class="btn small" data-action="edit-tpl" data-id="${escapeHtml(t.id)}">?️</button>


      <button class="btn small" data-action="dup-tpl" data-id="${escapeHtml(t.id)}">???</button>


      <button class="btn small danger" data-action="del-tpl" data-id="${escapeHtml(t.id)}">???️</button>


    </div>


  `).join('');





  Motion.cascade(el, ':scope > div');   // apparition en cascade


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


    html.push('<optgroup label="? Mes messages">');


    templatesCache.forEach(t => {


      html.push(`<option value="${escapeHtml(t.id)}">${CAT_ICONS[t.categorie] || '??'} ${escapeHtml(t.nom)}</option>`);


    });


    html.push('</optgroup>');


  }


  html.push('<optgroup label="??? Prédéfinis">');


  for (const [k, v] of Object.entries(predefinis)) {


    // Les prédéfinis semés dans « Mes messages » ne doivent pas apparaître deux fois


    if (templatesCache.some(t => t.id === `tpl_predef_${k}`)) continue;


    html.push(`<option value="${escapeHtml(k)}">${escapeHtml(v.nom)}</option>`);


  }


  html.push('</optgroup>');





  ['cfg-template', 'custom-template', 'grp-send-template'].forEach(id => {


    const el = document.getElementById(id);


    if (!el) return;


    if (id === 'grp-send-template') {


      el.innerHTML = '<option value="">?? Message libre ??</option>' + html.join('');


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


  document.getElementById('tpl-modal-title').textContent = '?? Nouveau message';


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


  document.getElementById('tpl-modal-title').textContent = `?️ ?diter : ${t.nom}`;


  document.getElementById('tpl-modal').classList.add('visible');


}





function closeTplModal() {


  Motion.fermerModale(document.getElementById('tpl-modal'));


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


      Aucun groupe ?? clique sur <strong>+ Nouveau groupe</strong>


    </div>`;


    return;


  }


  el.innerHTML = groupesCache.map(g => `


    <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;


                background:#FBF6EA;border:1px solid var(--border);border-radius:8px;flex-wrap:wrap">


      <span style="font-size:22px">??</span>


      <div style="flex:1;min-width:180px">


        <div style="font-weight:600;font-size:14px">${escapeHtml(g.nom)}</div>


        <div style="font-size:11px;color:var(--muted);margin-top:2px">


          ${g.emails.length} membre(s)


          ${g.description ? ` · ${escapeHtml(g.description)}` : ''}


        </div>


      </div>


      <button class="btn primary small" data-action="send-groupe" data-id="${escapeHtml(g.id)}">?? Envoyer</button>


      <button class="btn small" data-action="edit-groupe" data-id="${escapeHtml(g.id)}">?️</button>


      <button class="btn small danger" data-action="del-groupe" data-id="${escapeHtml(g.id)}">???️</button>


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


  document.getElementById('grp-modal-title').textContent = '?? Nouveau groupe';


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


  document.getElementById('grp-modal-title').textContent = `?️ ?diter : ${g.nom}`;


  updateGrpEmailCount();


  document.getElementById('grp-modal').classList.add('visible');


}





function closeGrpModal() {


  Motion.fermerModale(document.getElementById('grp-modal'));


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


  document.getElementById('grp-send-title').textContent = `?? Envoyer à : ${g.nom}`;


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


  Motion.fermerModale(document.getElementById('grp-send-modal'));


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


    ? `?? GROUP? (Cci) ?? 1 email`


    : `?? INDIVIDUEL ?? ${g.emails.length} emails`;





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


      toast(`?? ${data.envoyes}/${data.total}`, 'ok');


      document.getElementById('grp-send-status').textContent = `${data.envoyes}/${data.total}`;


      setTimeout(() => { closeGrpSendModal(); refreshStatus(); }, 1200);


    } else {


      toast(data.error || 'Erreur', 'err');


      btn.disabled = false; btn.textContent = '?? Envoyer';


    }


  } catch (e) {


    toast('Erreur réseau', 'err');


    btn.disabled = false; btn.textContent = '?? Envoyer';


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


      toast(`?? ${data.reponses} rép · ${data.bounces} bounce`, 'ok');


      badge.textContent = `${data.reponses} rép · ${data.bounces} bnc`;


      toast(`?? ${data.reponses} réponse(s) · ${data.bounces} bounce(s)`, 'ok');


      await refreshStatus();


      await loadIMAPStatus();


    } else toast(data.error || 'Erreur', 'err');


  } catch (e) { toast('Erreur réseau', 'err'); }


  btn.disabled = false; btn.textContent = '??? Vérifier maintenant';


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


  } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


}





/* R?GLES DE CLASSEMENT */


let filtresCache = [];


let apprentissageCache = {};





const FLT_LABELS = { from: 'Expéditeur', sujet: 'Sujet', motcle: 'Mot-clé' };


const ACT_ICONS = { label: '?️', marquer_lu: '??️', archive: '??', supprimer: '???️', notify: '???' };





async function loadFiltres() {


  try {


    const r = await fetch('/api/filtres');


    const data = await r.json();


    if (data.ok) { filtresCache = data.filtres || []; renderFiltres(); }


  } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


  try {


    const r = await fetch('/api/filtres/suggestions');


    const d = await r.json();


    if (d.ok) { apprentissageCache = d.apprentissage || {}; renderApprentissage(); }


  } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


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


    const lbl = f.label ? ` ?? « ${escapeHtml(f.label)} »` : '';


    const icone = f.icon || '?️';


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


          ${f.source === 'apprentissage' ? '<span title="Apprise de tes corrections">?</span>' : ''}


        </div>


        <div style="font-size:11px;color:var(--muted)">Si ${conds}</div>


      </div>


      <button class="btn small" data-action="toggle-regle" data-idx="${i}"


        title="${off ? 'Réactiver' : 'Mettre en pause'}">${off ? '?️' : '⏸️'}</button>


      <button class="btn small" data-action="edit-regle" data-idx="${i}" title="Modifier">?️</button>


      <button class="btn small danger" data-action="del-regle" data-idx="${i}" title="Supprimer">???️</button>


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


  document.getElementById('filter-modal-title').textContent = editRegleIdx == null ? '?? Nouvelle règle' : '?️ Modifier la règle';


  document.getElementById('filter-f-name').value = f.name || '';


  const champ = f.items?.[0]?.champ || 'sender';


  document.getElementById('filter-f-type').value = champ;


  document.getElementById('filter-f-value').value = f.items?.map(it => it.valeur).join(', ') || '';


  document.getElementById('filter-f-label').value = f.label || '';


  document.getElementById('filter-modal').classList.add('visible');


}





function closeRegleModal() {


  editRegleIdx = null;


  document.getElementById('filter-modal').classList.remove('visible');


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


        toast(editRegleIdx == null ? 'Règle ajoutée ??' : 'Règle modifiée ??', 'ok');


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


    toast('Règle ajoutée ??', 'ok');


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


      toast(`?️ ${d.libelles.length} libellé(s) vérifié(s) sur ${ok.length} compte(s) ?? ${nb} créé(s)`, 'ok');


    } else toast(d.error || 'Erreur', 'err');


  } catch (e) { toast('Erreur réseau', 'err'); }


  btn.disabled = false; btn.textContent = '?️ Créer les libellés dans Gmail';


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


      toast(`?? ${total} mail(s) classé(s)${errs ? `, ${errs} erreur(s)` : ''}`, errs ? 'warn' : 'ok');


      await chargerNotifs();


    } else toast(data.error || 'Erreur', 'err');


  } catch (e) { toast('Erreur réseau', 'err'); }


  btn.disabled = false; btn.textContent = '? Appliquer maintenant';


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


    toast(`? Appris : ${email} ?? ${label}`, 'ok');


  } else toast(d.error || 'Erreur', 'err');


}





function renderApprentissage() {


  const box = document.getElementById('app-liste');


  const entrees = Object.entries(apprentissageCache || {});


  if (!entrees.length) { box.textContent = 'Aucune correction apprise pour l\'instant.'; return; }


  box.innerHTML = entrees.map(([email, e]) =>


    `<div>? ${escapeHtml(email)} ?? <b>${escapeHtml(e.label || '')}</b>


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


        ??? <b>${escapeHtml(n.regle || '')}</b> ?? ${n.nombre} mail(s) sur ${escapeHtml(n.email || '')}


        <span style="color:var(--muted)">${new Date((n.date || 0) * 1000).toLocaleString('fr-FR')}</span>


      </div>`).join('')


      : '<span style="color:var(--muted)">Aucune notification.</span>';


    // Notification desktop pour les nouvelles non vues


    if (d.non_vues > 0 && 'Notification' in window


        && Notification.permission === 'granted' && list.length) {


      const n = list[0];


      new Notification(`??? ${n.regle}`, {


        body: `${n.nombre} mail(s) classé(s) ?? ${n.label || n.regle}` });


    }


    if (d.non_vues > 0) await fetch('/api/notifications/vue', { method: 'POST' });


  } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


}





function activerNotifs() {


  if (!('Notification' in window)) { toast('Notifications non supportées', 'err'); return; }


  Notification.requestPermission().then(p => {


    toast(p === 'granted' ? '?? Notifications activées'


                          : '? Notifications refusées', p === 'granted' ? 'ok' : 'err');


  });


}





/* D?LAI */


function bindDelaiUI() {


  const cb = document.getElementById('cfg-delai-alea');


  const input = document.getElementById('cfg-delai');


  const info = document.getElementById('delai-info');


  function maj() {


    if (cb.checked) { input.disabled = true; info.textContent = '?? 35-55s'; }


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





/* MODAL APER?U */


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


    const pj = piecesActives === 0 ? '?️ Aucune PJ' : `${piecesActives} PJ`;


    document.getElementById('modal-info').textContent = `${pj}`;


    document.getElementById('modal').classList.add('visible');


  })


  .catch(() => toast('Erreur aperçu', 'err'));


}





function closeModal() {


  Motion.fermerModale(document.getElementById('modal'));


  currentSendCompany = null;


  // Réinitialise le bouton d'envoi pour la prochaine ouverture


  const btn = document.getElementById('modal-send');


  if (btn) { btn.disabled = false; btn.textContent = '?? Envoyer'; }


}





async function sendFromModal() {


  if (!currentSendCompany) return;


  const subject = document.getElementById('modal-subject').value.trim();


  const body = document.getElementById('modal-body').value.trim();


  if (!subject || !body) { toast('Objet et corps requis', 'err'); return; }


  if (piecesActives === 0) {


    if (!confirm('?️ AUCUNE PJ\n\nContinuer ?')) return;


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


      toast(`?? Envoyé`, 'ok');


      closeModal(); await refreshStatus();


    } else {


      toast(data.error || 'Erreur', 'err');


    }


  } catch (e) {


    toast('Erreur réseau', 'err');


  } finally {


    // Toujours réinitialiser le bouton, même si closeModal a échoué


    btn.disabled = false; btn.textContent = '?? Envoyer';


  }


}





/* ENVOI PERSONNALIS? */


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


  if (!rateLimit.ok) { toast('Rate limit ?? attends 1h', 'err'); return; }


  const nbComptes = parseInt(document.getElementById('comptes-badge').textContent.replace(/\D/g, '')) || 0;


  if (nbComptes === 0) { toast('Ajoute un compte Gmail', 'err'); return; }





  let avertissementPJ = '';


  if (piecesActives === 0) avertissementPJ = '\n\n?️ AUCUNE PJ ?? emails sans CV';





  const destPreview = emails.slice(0, 3).join('\n');


  const plus = emails.length > 3 ? `\n... +${emails.length - 3}` : '';


  if (!confirm(`?? ${emails.length} email(s) INDIVIDUEL(S)\n\nDestinataires :\n${destPreview}${plus}\n\nEntreprise : ${company}\nPièces : ${piecesActives}${avertissementPJ}\n\nConfirmer ?`)) return;





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


      toast(`?? ${emails.length} envoi(s)`, piecesActives === 0 ? 'warn' : 'ok');


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


    btn.disabled = false; btn.textContent = '?? Envoyer maintenant';


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


  const delBtn = document.getElementById('sel-del');


  if (delBtn) delBtn.disabled = n === 0;


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





/* ---------------------------------------------------------


   SUPPRESSION D'ENTREPRISES


   Toute suppression est inscrite dans l'historique : le


   toast propose un « Annuler » immédiat, et l'action reste


   annulable depuis la fenêtre /historique.


   --------------------------------------------------------- */


async function supprimerEntreprise(name) {


  const cible = COMPANIES.find(c => c.name === name);


  const envoye = !!serverLog[name];


  const info = [


    `Entreprise : ${name}`,


    cible?.email ? `Email : ${cible.email}` : null,


    envoye ? '?️ Un e-mail a déjà été envoyé à cette entreprise' : null,


  ].filter(Boolean).join('\n');


  if (!confirm(`???️ SUPPRIMER\n\n${info}\n\nCette action est annulable depuis ??◷ Historique.\nConfirmer ?`)) return;





  try {


    const r = await fetch(`/api/companies/${encodeURIComponent(name)}`,


                          { method:'DELETE' });


    const d = await r.json();


    if (!r.ok || !d.ok) { toast(d.error || 'Suppression impossible', 'err'); return; }


    selectedCompanies.delete(name);


    await syncCompanies();


    toastUndo(`« ${name} » supprimée`, async () => {


      const b = await fetch(`/api/companies/${encodeURIComponent(name)}`,


                            { method:'PUT',


                              headers:{'Content-Type':'application/json'},


                              body: JSON.stringify(cible || { name, email:'' }) });


      const bb = await b.json();


      if (bb.ok) { await syncCompanies(); toast('Entreprise restaurée', 'ok'); }


      else toast('Restauration impossible ?? utilisez ??◷ Historique', 'err');


    });


  } catch (e) { toast('Erreur réseau', 'err'); }


}





async function supprimerSelection() {


  const noms = [...selectedCompanies];


  if (!noms.length) { toast('Aucune entreprise sélectionnée', 'warn'); return; }


  const preview = noms.slice(0, 10).map(n => `  ? ${n}`).join('\n');


  const suite = noms.length > 10 ? `\n  ? et ${noms.length - 10} autre(s)` : '';


  if (!confirm(


    `???️ SUPPRIMER ${noms.length} ENTREPRISE(S)\n\n${preview}${suite}\n\n` +


    `Cette action est annulable depuis ??◷ Historique.\nConfirmer ?`)) return;





  try {


    const r = await fetch('/api/companies', {


      method:'DELETE',


      headers:{'Content-Type':'application/json'},


      body: JSON.stringify({ names: noms })


    });


    const d = await r.json();


    if (!r.ok || !d.ok) { toast(d.error || 'Suppression impossible', 'err'); return; }


    selectedCompanies.clear();


    await syncCompanies();


    toastUndo(`${d.supprimees} entreprise(s) supprimée(s)`, null,


              'Ouvrez ??◷ Historique pour tout rétablir');


  } catch (e) { toast('Erreur réseau', 'err'); }


}





/* Toast avec action cliquable (défaut 6 s au lieu de 3,5 s). */


function toastUndo(msg, action, hint) {


  const t = document.getElementById('toast');


  t.textContent = '';


  t.className = 'toast show ok';


  t.appendChild(document.createTextNode(msg + ' '));


  if (action) {


    const b = document.createElement('button');


    b.className = 'toast-action';


    b.textContent = '?? Annuler';


    b.addEventListener('click', async () => {


      clearTimeout(t._timer);


      t.classList.add('hiding');


      setTimeout(() => t.classList.remove('show', 'hiding'), 260);


      await action();


    });


    t.appendChild(b);


  }


  if (hint) {


    const h = document.createElement('span');


    h.className = 'toast-hint';


    h.textContent = hint;


    t.appendChild(h);


  }


  Motion.rebondir(t);


  clearTimeout(t._timer);


  t._timer = setTimeout(() => {


    t.classList.add('hiding');


    setTimeout(() => t.classList.remove('show', 'hiding'), 260);


  }, action ? 6000 : 4000);


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


  if (piecesActives === 0) avertissementPJ = '\n\n?️ AUCUNE PJ ?? emails sans CV';


  if (!confirm(`Envoyer ${pending.length} emails ?\n\nTemplate : ${template}\nDélai : ${delaiTxt}\nPièces : ${piecesActives}\n~${minutes} min${avertissementPJ}\n\nConfirmer ?`)) return;


  try {


    const r = await fetch('/api/send-bulk', { method:'POST',


      headers:{'Content-Type':'application/json'},


      body: JSON.stringify({ companies: pending, template })


    });


    const data = await r.json();


    if (!data.ok) { toast(data.error, 'err'); return; }


    setBulkUIRunning(true); startBulkPolling();


    toast(`?? Envoi de masse lancé (${pending.length} e-mails)`, 'ok');


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


        toast(`Terminé : ${s.envoyes} ?? / ${s.erreurs} ?`, s.erreurs ? 'warn' : 'ok');


      }


    } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }


  }, 2000);


}





function updateBulkUI(s) {


  document.getElementById('bulk-title').textContent =


    s.en_cours ? `⏳ ${s.index}/${s.total}` : '??? Envoi en masse';


  document.getElementById('bulk-desc').textContent = s.en_cours


    ? `${s.derniere} ?? ?? ${s.envoyes} · ? ${s.erreurs}`


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


  if (isReplied) badgeStatus = '<span class="badge response">? Réponse</span>';


  else if (isBounce) badgeStatus = '<span class="badge bounce">?️ Bounce</span>';


  else if (sansPJ && isSent) badgeStatus = '<span class="badge nopj">?️ Sans PJ</span>';





  return `


    <div class="card ${cardCls}" data-name="${escapeHtml(c.name)}">


      <div class="card-head" role="button" tabindex="0" aria-expanded="false"


           onclick="this.parentElement.classList.toggle('open');this.setAttribute('aria-expanded',this.parentElement.classList.contains('open'))">


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


        <span class="toggle">?</span>


      </div>


      <div class="card-body">


        <div style="font-size:12px;color:var(--muted);line-height:1.6">


          ${escapeHtml(c.context)}


        </div>


        ${entry?.compte ? `<div class="via-compte" title="Compte Gmail utilisé">?? envoyé via ${escapeHtml(entry.compte)}</div>` : ''}


        <div class="actions">


          <button class="btn primary" data-action="preview"


                  data-name="${escapeHtml(c.name)}" ${isSent ? 'disabled' : ''}>


            ${isSent ? '?? Envoyé' : (isError ? '??? Réessayer' : '?️ Aperçu & envoyer')}


          </button>


          <button class="btn small" data-action="edit-company"


                  data-name="${escapeHtml(c.name)}" title="Modifier">?️</button>


          <button class="btn small danger" data-action="delete-company"


                  data-name="${escapeHtml(c.name)}" title="Supprimer">???️</button>


          ${isSent ? `


            <button class="btn small ${isReplied ? 'ok' : ''}"


                    data-action="toggle-reply" data-name="${escapeHtml(c.name)}">


              ${isReplied ? '?? Répondu' : 'Marquer réponse'}


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


      supprimerEntreprise(name);


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


      try {


        // toggleReply applique la bascule et met à jour serverLog


        await toggleReply(name);


        toast('Réponse enregistrée', 'ok');


        render();          // la carte reprend sa couleur « réponse »


        updateStats();


        if (typeof rendreSuivi === 'function') rendreSuivi();


        refreshStatus();


      } catch (err) {


        toast(err.message === 'Session expirée'


          ? '? Session expirée' : 'Erreur réseau', 'err');


      }


    });


  });


}





/* MODALE ENTREPRISE : ajout / édition */


let companyEditName = null; // null = ajout





function openCompanyModal(c) {


  companyEditName = c ? c.name : null;


  document.getElementById('company-modal-title').textContent =


    c ? `?️ Modifier : ${c.name}` : '?? Nouvelle entreprise';


  document.getElementById('company-f-name').value    = c ? c.name : '';


  document.getElementById('company-f-email').value   = c ? c.email : '';


  document.getElementById('company-f-cat').value     = c ? c.cat : 'pme';


  document.getElementById('company-f-context').value = c ? c.context : '';


  document.getElementById('company-modal').classList.add('visible');


  setTimeout(() => document.getElementById('company-f-name').focus(), 50);


}





function closeCompanyModal() {


  Motion.fermerModale(document.getElementById('company-modal'));


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


  // serverLog doit etre a jour AVANT le rendu : render() et


  // updateStats() le lisent pour colorer les cartes et compter les


  // envois. Le Declarer en amont evite le ReferenceError.


  await chargerSuivi();


  try { render(); updateStats(); }


  catch (e) { console.error('syncCompanies render:', e); }


  // Rafraichit aussi la sous-page Suivi si elle est ouverte.


  if (typeof rendreSuivi === 'function') rendreSuivi();


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


  const responded = COMPANIES.filter(c => serverLog[c.name]?.repondus || serverLog[c.name]?.repondu).length;


  animateCount('stat-total', total);


  animateCount('stat-sent', sent);


  animateCount('stat-pending', total - sent);


  animateCount('stat-responded', responded);





  const side = document.getElementById('side-entreprises');


  if (side) side.textContent = total;





  updateOverview();


}





/* ============================================================


   VUE D'ENSEMBLE ?? compteurs, onboarding, activité et readiness


   ============================================================ */


function _setText(id, valeur) {


  const el = document.getElementById(id);


  if (el) el.textContent = valeur;


}





function _setStatus(id, classe, texte) {


  const el = document.getElementById(id);


  if (!el) return;


  el.className = 'status ' + classe;


  el.textContent = texte;


}





function updateOverview() {


  const total = COMPANIES.length;


  const sent = COMPANIES.filter(c => serverLog[c.name]?.envoye).length;


  const responded = COMPANIES.filter(c => serverLog[c.name]?.repondu).length;





  _setText('ov-total', total);


  _setText('ov-sent', sent);


  _setText('ov-responded', responded);


  _setText('hero-envoyes', sent);


  _setText('hero-reponses', responded);





  const comptes = parseInt((document.getElementById('comptes-badge')?.textContent || '').replace(/\D/g, '')) || 0;


  const piecesOk = piecesActives > 0;





  _setStatus('ov-comptes-status', comptes > 0 ? 'ok' : 'orange', comptes > 0 ? 'Prêt' : '? faire');


  _setStatus('ov-pieces-status', piecesOk ? 'ok' : 'orange', piecesOk ? 'Prêt' : '? faire');


  _setText('ov-ready-maj', `MAJ ${new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`);


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





/* ============================================================


   MICRO-INTERACTIONS ?? module d'animation (motion.css)


   ============================================================ */


const Motion = {


  /** Respecte la préférence système « motions réduites ». */


  get reduit() {


    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;


  },





  /** Active l'état de chargement sur un bouton (spinner inline). */


  loading(btn, actif = true) {


    if (!btn) return;


    btn.classList.toggle('is-loading', actif);


    btn.disabled = actif;


  },





  /** Ferme une modale avec une animation de sortie (~110 ms). */


  fermerModale(el) {


    if (!el) return;


    if (Motion.reduit) { el.classList.remove('visible'); return; }


    el.classList.add('closing');


    setTimeout(() => {


      el.classList.remove('closing', 'visible');


    }, 120);


  },





  /** Fait vibrer un élément (erreur / action refusée). */


  secouer(el) {


    if (!el || Motion.reduit) return;


    el.animate(


      [{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' },


       { transform: 'translateX(6px)' }, { transform: 'translateX(-3px)' },


       { transform: 'translateX(0)' }],


      { duration: 280, easing: 'ease-in-out' }


    );


  },





  /** Petit rebond de confirmation sur un élément. */


  rebondir(el) {


    if (!el || Motion.reduit) return;


    el.animate(


      [{ transform: 'scale(1)' }, { transform: 'scale(1.06)' },


       { transform: 'scale(1)' }],


      { duration: 220, easing: 'cubic-bezier(.34,1.56,.64,1)' }


    );


  },





  /** Applique une cascade d'apparition aux enfants d'un conteneur. */


  cascade(parent, selecteur = ':scope > *', pas = 35) {


    if (!parent || Motion.reduit) return;


    [...parent.querySelectorAll(selecteur)].forEach((el, i) => {


      el.style.animation = 'none';


      void el.offsetWidth;                       // force le reflow


      el.style.animation = `riseIn 260ms cubic-bezier(.22,1,.36,1) ${i * pas}ms both`;


    });


  },





  /** Empêche le double-clic sur une action asynchrone. */


  async once(btn, fn) {


    if (!btn || btn.disabled) return;


    Motion.loading(btn, true);


    try {


      await fn();


    } finally {


      Motion.loading(btn, false);


    }


  },


};





/* Fermeture au clavier (Escape) sur toutes les modales */


document.addEventListener('keydown', (e) => {


  if (e.key === 'Escape') {


    const ouverte = document.querySelector('.modal-overlay.visible');


    if (ouverte) Motion.fermerModale(ouverte);


  }


});





/* Carte entreprise : le .card-head est un bouton (deplie/replie).


   Il etait declenche au clic uniquement -> inatteignable au clavier.


   Delegation : les cartes sont recreees a chaque rendu, on attache


   donc l'ecouteur une seule fois sur le document. */


document.addEventListener('keydown', (e) => {


  if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;


  const tete = e.target.closest?.('.card-head[role="button"]');


  // On n'agit que si le .card-head lui-meme est focus (il porte le


  // tabindex) : pas si un enfant (case a cocher) a le focus.


  if (!tete || e.target !== tete) return;


  e.preventDefault();          // Espace ne doit pas faire scroller


  const carte = tete.parentElement;


  carte.classList.toggle('open');


  tete.setAttribute('aria-expanded', carte.classList.contains('open'));


});





function toast(msg, type='') {


  const t = document.getElementById('toast');


  t.textContent = msg;


  t.className = 'toast show ' + type;


  // Retour haptique visuel : secousse sur erreur, rebond sur succès


  if (type === 'err') Motion.secouer(t);


  else if (type === 'ok') Motion.rebondir(t);


  clearTimeout(t._timer);


  t._timer = setTimeout(() => {


    t.classList.add('hiding');


    setTimeout(() => t.classList.remove('show', 'hiding'), 260);


  }, 3500);


}





/* ---------------------------------------------------------------


   SPLASH ?? animation de démarrage + préchargement des paramètres


   ---------------------------------------------------------------


   Deux problemes corriges ici :





   1. L'animation etait un clignotement. Les 6 appels de préchargement


      répondent en ~25 ms sur localhost : la barre sautait de 10 % à


      100 % en quelques images et le splash disparaissait en 375 ms,


      donc rien n'était visible. On impose maintenant une durée


      MINIMALE d'affichage, et la barre se REMPLIT en douceur


      (requestAnimationFrame + easeOutCubic) au lieu de sauter.





   2. Le splash pouvait rester bloqué POUR TOUJOURS. La fermeture


      n'était atteignable que si les 6 awaited aboutissaient, et


      bindSearch/renderFilters/bindDelaiUI n'étaient pas protégés.


      Un seul throw => splash figé, fenêtre inutilisable, sans issue.


      On corrige par : try/finally, chien de garde (watchdog),


      progression monotone, et dismissal sur erreur globale.


   --------------------------------------------------------------- */


const SPLASH_MIN_MS = 900;    // durée minimale d'affichage


const SPLASH_MAX_MS = 8000;   // chien de garde : au-delà, on force





let splashT0 = performance.now();


let splashPct = 0;


let splashFerme = false;


let splashWatchdog = null;





/** Avance la barre. La progression est monotone et bornée [0,100]. */


function splashAvancer(pct, etat) {


  const cible = Math.max(0, Math.min(100, Number(pct) || 0));


  // Monotone : une étape plus lente ne fait jamais reculer la barre.


  if (cible > splashPct) splashPct = cible;


  const p = document.getElementById('splash-prog');


  const e = document.getElementById('splash-etat');


  if (p) p.style.width = splashPct + '%';


  if (e && etat) e.textContent = etat;


}





/** Remplit la barre jusqu'à 100 % en douceur sur `duree` ms. */


function splashRemplir(duree) {


  const p = document.getElementById('splash-prog');


  if (!p) return Promise.resolve();


  if (duree <= 0 || Motion.reduit) { p.style.width = '100%'; return Promise.resolve(); }


  return new Promise(resolve => {


    const depart = performance.now();


    const largeur = p.parentElement ? p.parentElement.clientWidth : 220;


    const actuel = Math.min(100, (parseFloat(getComputedStyle(p).width) /


                                  (largeur || 220)) * 100);


    (function tick(now) {


      const t = Math.min(1, (now - depart) / duree);


      const ease = 1 - Math.pow(1 - t, 3);      // easeOutCubic


      p.style.width = (actuel + (100 - actuel) * ease) + '%';


      if (t < 1) requestAnimationFrame(tick); else resolve();


    })(performance.now());


  });


}





/** Ferme le splash. Idempotent : appelable depuis l'init ET le watchdog. */


async function splashFermer(message) {


  if (splashFerme) return;


  splashFerme = true;


  if (splashWatchdog) { clearTimeout(splashWatchdog); splashWatchdog = null; }


  // Le minuteur de secours du <head> n'a plus lieu d'être : on


  // l'annule pour qu'il ne réapparaisse pas après la fermeture.


  if (window.__candimailSauvetage) {


    clearTimeout(window.__candimailSauvetage);


    window.__candimailSauvetage = null;


  }


  splashAvancer(100, message || 'Prêt !');


  // On respecte la durée minimale AVANT de masquer, sinon le


  // splash disparaîtrait dès la fin réelle du chargement (~25 ms).


  const restant = Math.max(0, SPLASH_MIN_MS - (performance.now() - splashT0));


  await splashRemplir(Math.max(restant, Motion.reduit ? 0 : 220));


  const s = document.getElementById('splash');


  if (!s) return;


  s.classList.add('hidden');


  // Marquer que l'app a été ouverte au moins une fois : le splash


  // n'apparaîtra plus aux lancements suivants.


  try { localStorage.setItem('candimail.splashVu', '1'); } catch (e) {}


  setTimeout(() => s.remove(), 600);


}





/** Filet de sécurité : si l'init se bloque, on libère quand même. */


function splashWatchdogArmer() {


  splashWatchdog = setTimeout(() => {


    if (!splashFerme) splashFermer('Chargement prolongé ?? ouverture?');


  }, SPLASH_MAX_MS);


}





/**


 * Exécute une étape de préchargement.


 * Un échec isolé N'INTERROMPT PAS les étapes suivantes : on journalise


 * et on continue, exactement comme le faisait le code d'origine


 * (try/catch par étape). Le splash est fermé quoi qu'il arrive.


 */


async function splashEtape(pct, etat, fn) {


  splashAvancer(pct, etat);


  try {


    await fn();


  } catch (e) {


    console.error(`[candimail] ${etat}`, e);


  }


}





/* ==============================================================


   SOUS-PAGE « SUIVI DES ENVOIS »


   ==============================================================


   Données : /api/suivi (source unique, partagée avec la page


   /suivi et avec l'index serverLog du tableau de bord).





   Graphiques : SVG écrit à la main. Chart.js était chargé depuis


   cdn.jsdelivr.net ?? dépendance Internet inacceptable pour une


   application de bureau sur 127.0.0.1 qui doit fonctionner hors


   ligne. Sans CDN, plus aucun aller-retour réseau au démarrage.


   ============================================================== */


let suiviFiltre = 'all';


let suiviRecherche = '';





const SUIVI_COULEURS = {


  envoyes: '#1E5AA8', echecs: '#722F37',


  repondus: '#3A2E63', bounces: '#C98F0D',


};





/** ?chappe une valeur avant insertion dans le HTML. */


function echapperSuivi(s) {


  return String(s == null ? '' : s).replace(/[&<>"']/g, m => ({


    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',


  }[m]));


}





/** Badge de statut, avec l'info utile en infobulle. */


function badgeSuivi(l) {


  if (l.repondu) {


    const t = l.sujet_reponse ? ` title="${echapperSuivi(l.sujet_reponse)}"` : '';


    return `<span class="status purple"${t}>? Réponse</span>`;


  }


  if (l.bounce) {


    const t = l.bounce_raison ? ` title="${echapperSuivi(l.bounce_raison)}"` : '';


    return `<span class="status orange"${t}>?️ Bounce</span>`;


  }


  if (l.envoye) return '<span class="status ok">?? Envoyé</span>';


  const t = l.erreur ? ` title="${echapperSuivi(l.erreur)}"` : '';


  return `<span class="status err"${t}>? ?chec</span>`;


}





/** Une ligne du tableau. */


function ligneSuivi(l) {


  const groupe = l.groupe_nom


    ? `<br><small style="color:var(--muted);font-size:11px">


         ?? ${echapperSuivi(l.groupe_nom)}</small>`


    : '';


  const pj = l.sans_pj


    ? '<span class="pj-badge" title="Envoyé sans pièce jointe">?️</span>'


    : '<span class="pj-badge" title="Avec pièces jointes">??</span>';


  // Action : même sémantique que la page /suivi.


  const action = l.repondu


    ? `<button class="icon-btn purple" data-suivi-action="unmark-reply"


         data-company="${echapperSuivi(l.company)}"


         title="Retirer la réponse">?️</button>`


    : (l.envoye


      ? `<button class="icon-btn purple" data-suivi-action="mark-reply"


           data-company="${echapperSuivi(l.company)}"


           title="Marquer comme réponse reçue">?</button>`


      : '');


  return `<tr>


    <td><strong>${echapperSuivi(l.company)}</strong>${groupe}</td>


    <td class="email-cell hide-mobile">${echapperSuivi(l.email || '??')}</td>


    <td class="hide-mobile">${pj}</td>


    <td class="hide-mobile" style="font-size:12px;color:var(--muted)">


      ${echapperSuivi(l.date || '??')}</td>


    <td>${badgeSuivi(l)}</td>


    <td style="text-align:right"><div class="actions-cell">${action}</div></td>


  </tr>`;


}





/** Applique filtre + recherche, puis repeint le tableau. */


function rendreTableauSuivi() {


  const tbody = document.getElementById('suivi-tbody');


  const vide = document.getElementById('suivi-vide');


  if (!tbody) return;





  const q = suiviRecherche.trim().toLowerCase();


  const lignes = (SUIVI.items || []).filter(l => {


    if (suiviFiltre === 'sans_pj') { if (!l.sans_pj) return false; }


    else if (suiviFiltre !== 'all' && l.statut !== suiviFiltre) return false;


    if (!q) return true;


    return ((l.company || '') + ' ' + (l.email || ''))


      .toLowerCase().includes(q);


  });





  tbody.innerHTML = lignes.map(ligneSuivi).join('');


  const aucun = lignes.length === 0;


  if (vide) {


    vide.style.display = aucun ? '' : 'none';


    vide.querySelector('p').textContent =


      (SUIVI.items || []).length ? 'Aucun envoi ne correspond au filtre'


                                 : "Aucun envoi pour l'instant";


  }


}





/** Compteurs affichés en haut de la sous-page. */


function rendreStatsSuivi() {


  const map = {


    'suivi-total': SUIVI.total, 'suivi-envoyes': SUIVI.envoyes,


    'suivi-repondus': SUIVI.repondus, 'suivi-bounces': SUIVI.bounces,


    'suivi-echecs': SUIVI.echecs,


  };


  for (const [id, v] of Object.entries(map)) {


    const el = document.getElementById(id);


    if (el) el.textContent = v ?? 0;


  }


}





/** Anneau de répartition (SVG pur, sans librairie). */


function svgRepartition() {


  const parts = [


    { cle: 'envoyes', label: 'Envoyés', v: SUIVI.envoyes },


    { cle: 'repondus', label: 'Réponses', v: SUIVI.repondus },


    { cle: 'bounces', label: 'Bounces', v: SUIVI.bounces },


    { cle: 'echecs', label: '?checs', v: SUIVI.echecs },


  ].filter(p => p.v > 0);


  const total = parts.reduce((s, p) => s + p.v, 0);


  const R = 60, C = 2 * Math.PI * R, cx = 80, cy = 80;


  let offset = 0;





  if (!total) {


    return `<svg viewBox="0 0 160 160" role="img"


      aria-label="Aucun envoi enregistré">


      <circle cx="${cx}" cy="${cy}" r="${R}" fill="none"


        stroke="#E8DCC4" stroke-width="22"/>


      <text x="${cx}" y="${cy + 5}" text-anchor="middle"


        font-size="13" fill="#7A6E5B">Aucun envoi</text>


    </svg>`;


  }





  const anneaux = parts.map(p => {


    const frac = p.v / total;


    const dash = C * frac;


    const seg = `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none"


      stroke="${SUIVI_COULEURS[p.cle]}" stroke-width="22"


      stroke-dasharray="${dash} ${C - dash}"


      stroke-dashoffset="${-offset}" transform="rotate(-90 ${cx} ${cy})">


      <title>${p.label} : ${p.v}</title></circle>`;


    offset += dash;


    return seg;


  }).join('');





  const legende = `<div class="chart-legend">` + parts.map(p =>


    `<span><i style="background:${SUIVI_COULEURS[p.cle]}"></i>


       ${p.label} · ${p.v}</span>`).join('') + `</div>`;





  return `<svg viewBox="0 0 160 160" role="img"


    aria-label="Répartition des envois">${anneaux}


    <text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="24"


      font-weight="700" fill="#2A141A">${total}</text>


    <text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="10"


      fill="#7A6E5B">ENVOIS</text></svg>${legende}`;


}





/** Barres d'activité sur 7 jours (SVG pur). */


function svgActivite() {


  const jours = SUIVI.jours || [];


  if (!jours.length) return '';


  const W = 320, H = 160, pad = 26;


  const max = Math.max(1, ...jours.map(j => j.total));


  const pas = (W - pad * 2) / jours.length;


  const larg = Math.min(34, pas * 0.6);





  const labelJour = iso => {


    const d = new Date(iso + 'T00:00:00');


    return d.toLocaleDateString('fr-FR', { weekday: 'short' }).slice(0, 3);


  };





  const barres = jours.map((j, i) => {


    const h = ((H - 52) * j.total) / max;


    const x = pad + i * pas + (pas - larg) / 2;


    const y = H - 26 - h;


    return `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}"


      width="${larg.toFixed(1)}" height="${Math.max(h, j.total ? 2 : 0).toFixed(1)}"


      rx="3" fill="${j.total ? '#1E5AA8' : '#E8DCC4'}">


      <title>${j.date} : ${j.total} envoi(s)</title></rect>


      <text x="${(x + larg / 2).toFixed(1)}" y="${(y - 5).toFixed(1)}"


        text-anchor="middle" font-size="10" fill="#463D31"


        font-weight="700">${j.total || ''}</text>


      <text x="${(x + larg / 2).toFixed(1)}" y="${H - 10}"


        text-anchor="middle" font-size="9" fill="#7A6E5B">${labelJour(j.date)}</text>`;


  }).join('');





  return `<svg viewBox="0 0 ${W} ${H}" role="img"


    aria-label="Activité des 7 derniers jours">


    <line x1="${pad - 6}" y1="${H - 26}" x2="${W - pad + 6}" y2="${H - 26}"


      stroke="#DED2BC" stroke-width="1"/>${barres}</svg>`;


}





/** Peint toute la sous-page. */


function rendreSuivi() {


  rendreStatsSuivi();


  const a = document.getElementById('suivi-repartition');


  const b = document.getElementById('suivi-activite');


  if (a) a.innerHTML = svgRepartition();


  if (b) b.innerHTML = svgActivite();


  rendreTableauSuivi();


}





/** Recharge depuis l'API puis repeint. */


async function rafraichirSuivi() {


  await chargerSuivi();


  rendreSuivi();


}





/** Câble les contrôles de la sous-page (une seule fois, au chargement). */


function initSuiviUI() {


  const btn = document.getElementById('btn-suivi-rafraichir');


  if (btn) {


    btn.addEventListener('click', async () => {


      btn.disabled = true;


      try { await rafraichirSuivi(); } finally { btn.disabled = false; }


    });


  }


  const barre = document.getElementById('suivi-filtres');


  if (barre) {


    barre.querySelectorAll('.chip').forEach(c => {


      c.addEventListener('click', () => {


        barre.querySelectorAll('.chip')


          .forEach(x => x.classList.remove('active'));


        c.classList.add('active');


        suiviFiltre = c.dataset.f || 'all';


        rendreTableauSuivi();


      });


    });


  }


  const rech = document.getElementById('suivi-search');


  if (rech) {


    let t;


    rech.addEventListener('input', () => {


      clearTimeout(t);


      t = setTimeout(async () => {


        suiviRecherche = rech.value;


        // Recherche côté backend (endpoint /api/suivi/recherche) : rapide


        // même sur des milliers d'envois, et cohérente avec les statuts.


        if (suiviRecherche.trim().length >= 2) {


          try {


            const u = '/api/suivi/recherche?q=' + encodeURIComponent(suiviRecherche.trim());


            const d = await (await fetch(u)).json();


            if (d.ok && Array.isArray(d.items)) {


              // Remplace la vue locale par le résultat serveur


              SUIVI = { ...(SUIVI || {}), items: d.items, total_filtré: d.total };


              rendreTableauSuivi();


              return;


            }


          } catch (e) { /* fallback : filtre local ci-dessous */ }


        }


        rendreTableauSuivi();


      }, 180);


    });


  }


  const tbody = document.getElementById('suivi-tbody');


  if (tbody) {


    tbody.addEventListener('click', async (ev) => {


      const b = ev.target.closest('[data-suivi-action]');


      if (!b) return;


      const company = b.dataset.company;


      try {


        await toggleReply(company);


        toast('Réponse enregistrée', 'ok');


        await rafraichirSuivi();   // tableau + graphiques à jour


        render(); updateStats();   // tableau de bord aussi


      } catch (e) {


        toast(e.message === 'Session expirée'


          ? '? Session expirée' : 'Erreur réseau', 'err');


      }


    });


  }


  // Premier remplissage (données déjà chargées par l'init).


  rendreSuivi();


}


function appliquerTheme(theme, persister) {


  document.documentElement.dataset.theme = 'neo';


}





function basculerTheme() {


  // Thème fixe : pas de basculement


}





document.addEventListener('DOMContentLoaded', async () => {


  splashWatchdogArmer();


  try {


    await splashEtape(10, 'Chargement du profil?', loadConfig);


    await splashEtape(30, 'Chargement des messages?', loadTemplates);


    await splashEtape(48, 'Chargement des pièces jointes?', loadPieces);


    await splashEtape(62, 'Chargement des groupes?', loadGroupes);


    await splashEtape(76, 'Vérification IMAP?', loadIMAPStatus);


    await splashEtape(90, 'Chargement des entreprises?', syncCompanies);


    // Câble les contrôles de la sous-page Suivi (filtres, recherche,


    // bouton d'actualisation) et premier rendu avec les données


    // déjà chargées par syncCompanies -> chargerSuivi().


    initSuiviUI();


    // Ces 3 liaisons ne sont pas critiques : si l'une échoue,


    // l'utilisateur doit quand même obtenir l'application.


    for (const [nom, fn] of [


      ['bindSearch', bindSearch],


      ['renderFilters', renderFilters],


      ['bindDelaiUI', bindDelaiUI],


    ]) {


      try { fn(); }


      catch (e) { console.error(`[candimail] ${nom}()`, e); }


    }


  } catch (e) {


    console.error('[candimail] init incomplet :', e);


  } finally {


    await splashFermer();


  }





  // Back-end : bouton d'actualisation (ralentissement / bug)


  const btnRB = document.getElementById('btn-refresh-backend');


  if (btnRB) btnRB.addEventListener('click', () => refreshBackend(btnRB));


  // 2e bouton identique dans le panneau Paramètres (id suffixé -2 :


  // deux éléments ne peuvent pas partager le même id).


  const btnRB2 = document.getElementById('btn-refresh-backend-2');


  if (btnRB2) btnRB2.addEventListener('click', () => refreshBackend(btnRB2));





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


document.getElementById('sel-del').addEventListener('click', supprimerSelection);


  updateSelectionUI();





  // Config


  document.getElementById('btn-save-config').addEventListener('click', saveCandidatConfig);


document.getElementById('btn-reinit-profil').addEventListener('click', reinitialiserProfil);





/* Aperçu + en-tête réactifs pendant la saisie du profil */


['cfg-nom', 'cfg-tel-indicatif', 'cfg-tel', 'cfg-ville'].forEach(id => {


  const el = document.getElementById(id);


  if (el) el.addEventListener('input', () => {


    updateHeaderSub();


    updateSignaturePreview();


  });


});


  document.getElementById('cfg-template').addEventListener('change', saveCandidatConfig);





  // Comptes


  document.getElementById('btn-add-compte').addEventListener('click', addCompte);


  document.getElementById('btn-help-password').addEventListener('click', () => {


    document.getElementById('help-modal').classList.add('visible');


  });


  document.getElementById('help-close').addEventListener('click', () => {


    Motion.fermerModale(document.getElementById('help-modal'));


  });


  document.getElementById('help-close-btn').addEventListener('click', () => {


    Motion.fermerModale(document.getElementById('help-modal'));


  });


  document.getElementById('help-modal').addEventListener('click', e => {


    if (e.target.id === 'help-modal') Motion.fermerModale(document.getElementById('help-modal'));


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





  // Navigation par PAGES (routing #hash, transition fluide)


  const PAGES = {


    overview: { id: 'page-overview', titre: "Vue d'ensemble" },


    dash:     { id: 'page-dash',     titre: 'Cibles' },


    envoi:    { id: 'page-envoi',    titre: 'Envoi express' },


    suivi:    { id: 'page-suivi',    titre: 'Suivi des envois' },


    imap:     { id: 'page-imap',     titre: 'Réponses & filtres' },


    comptes:  { id: 'page-comptes',  titre: 'Comptes Gmail & CV' },


    messages: { id: 'page-messages', titre: 'Mes messages' },


    groupes:  { id: 'page-groupes',  titre: 'Mes groupes' },


    profil:   { id: 'page-profil',   titre: 'Profil' },


    params:   { id: 'page-params',   titre: "Paramètres & maintenance" },


    historique:{ id: 'page-historique', titre: 'Historique' },


  };





  const sidebar = document.getElementById('sidebar');


  const backdrop = document.getElementById('mobile-backdrop');


  function fermerSidebar() {


    if (sidebar) sidebar.classList.remove('open');


    if (backdrop) backdrop.classList.remove('visible');


  }


  function ouvrirSidebar() {


    if (sidebar) sidebar.classList.add('open');


    if (backdrop) backdrop.classList.add('visible');


  }





  function montrerPage(nav, sansHash) {


    const page = PAGES[nav] || PAGES.overview;


    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));


    const el = document.getElementById(page.id);


    if (el) el.classList.add('active');


    document.querySelectorAll('.sidebar .nav-item[data-nav]')


      .forEach(x => x.classList.toggle('active', x.dataset.nav === nav));


    _setText('bc-page', page.titre);


    _setText('titre-page', page.titre);


    document.title = `Candimail ?? ${page.titre}`;


    window.scrollTo({ top: 0, behavior: 'instant' });


    fermerSidebar();


    if (nav === 'suivi' && typeof rendreSuivi === 'function') rendreSuivi();


    if (nav === 'overview') updateOverview();


    if (!sansHash) history.replaceState(null, '', '#' + nav);


    try { sessionStorage.setItem('candimail.page', nav); } catch (e) { /* stockage indisponible */ }


  }


  window.montrerPage = montrerPage;


  window.PAGES_CANDIMAIL = PAGES;


  document.querySelectorAll('.sidebar .nav-item[data-nav]').forEach(a => {


    a.addEventListener('click', () => montrerPage(a.dataset.nav));


  });


  document.querySelectorAll('[data-goto]').forEach(b => {


    b.addEventListener('click', () => montrerPage(b.dataset.goto));


  });


  document.getElementById('mobile-toggle')?.addEventListener('click', ouvrirSidebar);


  backdrop?.addEventListener('click', fermerSidebar);


  window.addEventListener('resize', () => {


    if (window.innerWidth > 900) fermerSidebar();


  });


  // Raccourcis clavier Alt+1..9 (une page de plus : Suivi des envois)


  const ORDRE_NAV = Object.keys(PAGES);


  document.addEventListener('keydown', e => {


    if (e.altKey && e.key >= '1' && e.key <= '9') {


      e.preventDefault();


      montrerPage(ORDRE_NAV[parseInt(e.key, 10) - 1]);


    }


  });


  // Restaure la page au chargement + bouton retour navigateur


  window.addEventListener('hashchange', () => {


    montrerPage((location.hash || '#dash').slice(1), true);


  });


  const pageInit = (location.hash || '').slice(1)


    || (() => { try { return sessionStorage.getItem('candimail.page'); } catch (e) { return null; } })()


    || 'overview';


  montrerPage(PAGES[pageInit] ? pageInit : 'overview', true);





  // Palette de commandes


  const cmdOverlay = document.getElementById('cmd-overlay');


  const cmdInput = document.getElementById('cmd-input');


  const cmdList = document.getElementById('cmd-list');


  const commandes = [


    ...Object.entries(PAGES).map(([nav, p]) => ({


      label: p.titre, hint: 'Page', ico: '??', nav,


    })),


    { label: 'Ajouter une entreprise', hint: 'Action', ico: '?',


      action: () => { montrerPage('dash'); openCompanyModal(null); } },


    { label: 'Ajouter un compte Gmail', hint: 'Action', ico: '??',


      action: () => montrerPage('comptes') },


    { label: 'Lancer un envoi groupé', hint: 'Action', ico: '??',


      action: () => montrerPage('dash') },


    { label: 'Recharger le back-end', hint: 'Maintenance', ico: '?',


      action: () => refreshBackend(document.getElementById('btn-refresh-backend')) },


    { label: 'Changer de thème', hint: 'Apparence', ico: '?',


      action: () => basculerTheme() },


  ];


  let cmdFiltrees = [];


  let cmdActif = 0;





  function rendrePalette(q = '') {


    const query = q.trim().toLowerCase();


    cmdFiltrees = commandes.filter(c =>


      c.label.toLowerCase().includes(query) || c.hint.toLowerCase().includes(query));


    cmdActif = 0;


    if (!cmdFiltrees.length) {


      cmdList.innerHTML = '<div class="cmd-empty">Aucun résultat.</div>';


      return;


    }


    cmdList.innerHTML = cmdFiltrees.map((c, i) => `


      <button class="cmd-item ${i === 0 ? 'active' : ''}" type="button" data-cmd="${i}">


        <span class="ci-ico">${c.ico}</span>


        <span>${c.label}</span>


        <span class="ci-hint">${c.hint}</span>


      </button>`).join('');


  }





  function executerCommande(c) {


    if (!c) return;


    fermerPalette();


    if (c.nav) montrerPage(c.nav);


    if (c.action) c.action();


  }





  function ouvrirPalette() {


    if (!cmdOverlay) return;


    cmdOverlay.classList.add('visible');


    cmdOverlay.setAttribute('aria-hidden', 'false');


    cmdInput.value = '';


    rendrePalette('');


    setTimeout(() => cmdInput.focus(), 20);


  }





  function fermerPalette() {


    if (!cmdOverlay) return;


    cmdOverlay.classList.remove('visible');


    cmdOverlay.setAttribute('aria-hidden', 'true');


  }





  document.getElementById('btn-command')?.addEventListener('click', ouvrirPalette);


  cmdOverlay?.addEventListener('click', e => {


    if (e.target === cmdOverlay) fermerPalette();


  });


  cmdInput?.addEventListener('input', () => rendrePalette(cmdInput.value));


  cmdList?.addEventListener('click', e => {


    const b = e.target.closest('[data-cmd]');


    if (b) executerCommande(cmdFiltrees[parseInt(b.dataset.cmd, 10)]);


  });


  cmdInput?.addEventListener('keydown', e => {


    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {


      e.preventDefault();


      if (!cmdFiltrees.length) return;


      cmdActif = (cmdActif + (e.key === 'ArrowDown' ? 1 : -1) + cmdFiltrees.length) % cmdFiltrees.length;


      [...cmdList.querySelectorAll('.cmd-item')].forEach((x, i) => x.classList.toggle('active', i === cmdActif));


    } else if (e.key === 'Enter') {


      e.preventDefault();


      executerCommande(cmdFiltrees[cmdActif]);


    } else if (e.key === 'Escape') {


      fermerPalette();


    }


  });


  document.addEventListener('keydown', e => {


    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {


      e.preventDefault();


      cmdOverlay?.classList.contains('visible') ? fermerPalette() : ouvrirPalette();


    }


    if (e.key === 'Escape') fermerPalette();


  });





  // Recherche sidebar synchronisée + raccourci clavier « / »


  const sMain = document.getElementById('search'), sSide = document.getElementById('search-side');


  sSide.addEventListener('input', () => {


    // La liste est sur le tableau de bord : on y bascule automatiquement


    if ((sSide.value || '').trim()) montrerPage('dash');


    sMain.value = sSide.value; sMain.dispatchEvent(new Event('input'));


  });


  sMain.addEventListener('input', () => { if ((sMain.value||'').trim()) montrerPage('dash'); sSide.value = sMain.value; });


  document.addEventListener('keydown', e => {


    if (e.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) {


      e.preventDefault(); sSide.focus();


    }


  });





  // Règles de classement


  document.getElementById('btn-flt-add').addEventListener('click', addFiltre);


  // Modal de règle (ajout / édition) : les 3 boutons n'étaient câblés


  // à rien, le modal ne pouvait donc jamais être validé ni fermé.


  document.getElementById('filter-save').addEventListener('click', soumettreRegle);


  document.getElementById('filter-cancel').addEventListener('click', closeRegleModal);


  document.getElementById('filter-modal-close').addEventListener('click', closeRegleModal);


  document.getElementById('filter-modal').addEventListener('click', (ev) => {


    if (ev.target === ev.currentTarget) closeRegleModal();


  });


  document.getElementById('btn-flt-appliquer').addEventListener('click', appliquerFiltres);


  document.getElementById('btn-flt-libelles').addEventListener('click', creerLibelles);


  document.getElementById('btn-app-corriger').addEventListener('click', apprendre);


  document.getElementById('btn-notifs-activer').addEventListener('click', activerNotifs);


  await loadFiltres();


  await chargerNotifs();


  setInterval(chargerNotifs, 60000);   // poll toutes les minutes





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


      Motion.fermerModale(document.getElementById('help-modal'));


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


  } catch (e) {


        console.error('[candimail] erreur silencieuse:', e);


      }





  // ============================================================


  // AGENT IA ?? config par tâche, catalogue servi par le backend


  // ============================================================


  let IA_CATALOGUE = { providers: {} };


  let IA_TACHE_ACTIVE = 'rediger';


  try {


    const r = await fetch('/api/ia/catalogue');


    const j = await r.json();


    if (j.ok) IA_CATALOGUE = j;


  } catch (e) { /* catalogue indisponible : listes vides, pas de crash */ }





  const prov = document.getElementById('ia-provider');


  const key  = document.getElementById('ia-api-key');


  const mod  = document.getElementById('ia-model');


  const tsk  = document.getElementById('ia-task');


  const st   = document.getElementById('ia-status');





  function iaLoad() {


    try {


      const raw = localStorage.getItem('candimail.ia');


      return raw ? JSON.parse(raw) : null;


    } catch (e) { return null; }


  }





  async function iaSave(cfg) {


    localStorage.setItem('candimail.ia', JSON.stringify(cfg));


    try {


      await fetch('/api/ia/config', {


        method: 'POST',


        headers: { 'Content-Type': 'application/json' },


        body: JSON.stringify(cfg),


      });


    } catch (e) {}


  }





  function iaRemplirFournisseurs() {


    const ents = Object.entries(IA_CATALOGUE.providers || {});


    prov.innerHTML = ents.map(([id, p]) =>


      `<option value="${id}">${p.label || id}</option>`).join('');


  }





  function iaRemplirModeles(providerId) {


    const p = (IA_CATALOGUE.providers || {})[providerId];


    const liste = (p && p.models) || [];


    mod.innerHTML = liste.map(m => `<option value="${m}">${m}</option>`).join('');


  }





  function iaRender() {


    const cfg = iaLoad() || {};


    // Fournisseurs servis par le backend, jamais codés en dur côté front


    iaRemplirFournisseurs();


    if (cfg.provider && IA_CATALOGUE.providers?.[cfg.provider]) prov.value = cfg.provider;


    iaRemplirModeles(prov.value);


    if (cfg.model && [...mod.options].some(o => o.value === cfg.model)) mod.value = cfg.model;


    if (tsk) tsk.value = cfg.tache || IA_TACHE_ACTIVE;





    st.textContent = cfg.apiKey


      ? `?? ${(IA_CATALOGUE.providers?.[prov.value]||{}).label || prov.value} / ${cfg.model}`


      : 'Aucune clé configurée';


    st.style.color = cfg.apiKey ? 'var(--ok)' : 'var(--muted)';


  }





  prov.addEventListener('change', () => {


    iaRemplirModeles(prov.value);


    mod.dispatchEvent(new Event('change'));


  });





  document.getElementById('ia-api-key').addEventListener('input', () => {


    const cfg = iaLoad() || {};


    cfg.provider = prov.value;


    cfg.apiKey = key.value.trim();


    cfg.model = mod.value;


    if (tsk) cfg.tache = tsk.value;


    iaSave(cfg);


    iaRender();


  });





  mod.addEventListener('change', () => {


    const cfg = iaLoad() || {};


    cfg.provider = prov.value;


    cfg.apiKey = key.value.trim();


    cfg.model = mod.value;


    if (tsk) cfg.tache = tsk.value;


    iaSave(cfg);


    iaRender();


  });





  document.getElementById('ia-btn-test').addEventListener('click', async () => {


    const cfg = iaLoad();


    const btn = document.getElementById('ia-btn-test');


    const st = document.getElementById('ia-status');


    if (!cfg || !cfg.apiKey) { st.textContent = '? Clé manquante'; st.style.color = 'var(--danger)'; return; }


    btn.textContent = '⏳?';


    try {


      const r = await fetch('/api/health');


      st.textContent = r.ok ? '?? Backend joignable ?? clé prête' : '? Backend inaccessible';


      st.style.color = r.ok ? 'var(--ok)' : 'var(--danger)';


    } catch (e) {


      st.textContent = '? Erreur de connexion';


      st.style.color = 'var(--danger)';


    } finally {


      btn.textContent = '? Tester';


    }


  });





  document.getElementById('ia-btn-save').addEventListener('click', () => {


    const cfg = iaLoad() || {};


    cfg.provider = prov.value;


    cfg.apiKey = key.value.trim();


    cfg.model = mod.value;


    iaSave(cfg);


    iaRender();


    const btn = document.getElementById('ia-btn-save');


    const old = btn.textContent;


    btn.textContent = '?? Sauvegardé';


    setTimeout(() => { btn.textContent = old; }, 1000);


  });





  async function iaChargerComptes() {


    try {


      const r = await fetch('/api/comptes');


      const j = await r.json();


      const comptes = (j.comptes || []).filter(c => c.actif);


      const el = document.getElementById('ia-comptes-list');


      if (comptes.length === 0) {


        el.innerHTML = '<span style="color:var(--warn)">Aucun compte Gmail actif ?? configure-en un dans l\'onglet Comptes.</span>';


      } else {


        el.innerHTML = comptes.map(c => `<span style="display:inline-flex;align-items:center;gap:6px;padding:4px 8px;border:2px solid var(--border);background:var(--surface2);margin-right:6px;margin-bottom:4px;font-weight:700;font-size:12px">${c.email} ${c.template ? '<span style="font-size:10px;opacity:.6">tpl:'+c.template+'</span>' : ''}</span>`).join('');


      }


    } catch (e) {


      document.getElementById('ia-comptes-list').textContent = 'Erreur lors du chargement des comptes';


    }


  }





  await iaRender();


  await iaChargerComptes();




  // ============================================================


  // COMPTE GMAIL ?? test IMAP/SMTP + enregistrement depuis le profil


  // ============================================================


  const gmailEmailIn = document.getElementById('gmail-email');


  const gmailPassIn = document.getElementById('gmail-password');


  const gmailBtnTest = document.getElementById('gmail-btn-test');


  const gmailBtnSave = document.getElementById('gmail-btn-save');


  const gmailAlert = document.getElementById('gmail-alert');


  const gmailDetail = document.getElementById('gmail-detail');





  let gmailTestOk = false;





  gmailBtnTest.addEventListener('click', async () => {


    const email = (gmailEmailIn.value || '').trim();


    const password = gmailPassIn.value || '';


    if (!email || !password) {


      gmailAlert.textContent = '? Email et mot de passe requis';


      gmailAlert.style.color = 'var(--danger)';


      gmailDetail.textContent = '';


      gmailBtnSave.disabled = true;


      gmailTestOk = false;


      return;


    }


    gmailBtnTest.textContent = '⏳ Test?';


    gmailAlert.textContent = '';


    gmailDetail.textContent = '';


    try {


      const r = await fetch('/api/comptes/test', {


        method: 'POST',


        headers: { 'Content-Type': 'application/json' },


        body: JSON.stringify({ email, password }),


      });


      const j = await r.json();


      if (r.ok && j.ok) {


        gmailTestOk = true;


        gmailBtnSave.disabled = false;


        gmailAlert.textContent = '?? Compatible IMAP/SMTP ?? compte valide';


        gmailAlert.style.color = 'var(--ok)';


        gmailDetail.textContent = j.message || 'Connexion SMTP OK';


      } else {


        gmailTestOk = false;


        gmailBtnSave.disabled = true;


        gmailAlert.textContent = '? Incompatible ?? vérifie l\'email et le mot de passe d\'application';


        gmailAlert.style.color = 'var(--danger)';


        gmailDetail.textContent = j.error || 'Test échoué';


      }


    } catch (e) {


      gmailTestOk = false;


      gmailBtnSave.disabled = true;


      gmailAlert.textContent = '? Erreur de connexion au serveur';


      gmailAlert.style.color = 'var(--danger)';


      gmailDetail.textContent = '';


    } finally {


      gmailBtnTest.textContent = '? Tester IMAP/SMTP';


    }


  });





  gmailBtnSave.addEventListener('click', async () => {


    if (!gmailTestOk) return;


    const email = (gmailEmailIn.value || '').trim();


    const password = gmailPassIn.value || '';


    gmailBtnSave.textContent = '⏳ Enregistrement?';


    try {


      const r = await fetch('/api/comptes', {


        method: 'POST',


        headers: { 'Content-Type': 'application/json' },


        body: JSON.stringify({ email, password, template: '' }),


      });


      const j = await r.json();


      if (r.ok && j.ok) {


        gmailAlert.textContent = '?? Compte Gmail enregistré';


        gmailAlert.style.color = 'var(--ok)';


        gmailBtnSave.disabled = true;


        gmailBtnSave.textContent = '?? Enregistré';


        try { await iaChargerComptes(); } catch (e) {}


      } else {


        gmailAlert.textContent = '? ' + (j.error || '?chec de l\'enregistrement');


        gmailAlert.style.color = 'var(--danger)';


      }


    } catch (e) {


      gmailAlert.textContent = '? Erreur lors de l\'enregistrement';


      gmailAlert.style.color = 'var(--danger)';


    } finally {


      gmailBtnSave.textContent = '?? Enregistrer le compte';


    }


  });





  // ============================================================


  // COMPTE GMAIL S?LECTIONN? ?? sélecteur dans le topbar


  // ============================================================


  const compteSelect = document.getElementById('compte-select');





  async function chargerComptesSelect() {


    try {


      const r = await fetch('/api/comptes');


      const j = await r.json();


      const comptes = (j.comptes || []).filter(c => c.actif);


      compteSelect.innerHTML = comptes.map((c, i) =>


        `<option value="${i}">${c.email}</option>`


      ).join('');


      const r2 = await fetch('/api/comptes/selected');


      const j2 = await r2.json();


      if (j2.index !== undefined) {


        compteSelect.value = j2.index;


      }


    } catch (e) {


      compteSelect.innerHTML = '<option>Erreur</option>';


    }


  }





  compteSelect.addEventListener('change', async () => {


    const idx = parseInt(compteSelect.value, 10);


    await fetch('/api/comptes/selected', {


      method: 'POST',


      headers: { 'Content-Type': 'application/json' },


      body: JSON.stringify({ index: idx }),


    });


  });





  await chargerComptesSelect();





  // ============================================================


  // HISTORIQUE ?? onglet intégré


  // ============================================================


  function escHtml(s){


    return String(s == null ? '' : s)


      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')


      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');


  }





  const HIST_ICONS = {


    supprimer_entreprise:'?', ajouter_entreprise:'?', renommer_entreprise:'?️',


    supprimer_groupe:'??',      ajouter_groupe:'??',


    supprimer_template:'??',    ajouter_template:'??',


    toggle_compte:'??', toggle_piece:'???', toggle_filtre:'???️',


    parametres:'??️', toggle_reponse:'??️', envoyer:'??',


  };


  const HIST_LABELS = {


    supprimer_entreprise:"Suppression d'entreprise",


    ajouter_entreprise:"Ajout d'entreprise",


    renommer_entreprise:"Renommage d'entreprise",


    supprimer_groupe:'Suppression de groupe', ajouter_groupe:'Ajout de groupe',


    supprimer_template:'Suppression de modèle', ajouter_template:'Ajout de modèle',


    toggle_compte:'Activation / pause de compte',


    toggle_piece:"Activation d'une pièce jointe",


    toggle_filtre:"Activation d'une règle",


    parametres:'Modification des paramètres',


    toggle_reponse:'Changement du statut de réponse',


    envoyer:"Envoi d'e-mail",


  };





  let histActions = [], histFiltre = 'toutes', histRecherche = '';





  async function chargerHistorique() {


    try {


      const r = await fetch('/api/historique');


      const d = await r.json();


      if (d.ok) { histActions = d.actions || []; rendreHistorique(); }


    } catch (e) { /* serveur injoignable */ }


  }





  function majStatsHistorique() {


    const actives = histActions.filter(a => !a.undone).length;


    document.getElementById('hst-total').textContent    = histActions.length;


    document.getElementById('hst-actives').textContent  = actives;


    document.getElementById('hst-annulees').textContent = histActions.length - actives;


    document.getElementById('hst-types').textContent =


      new Set(histActions.map(a => a.type)).size;


  }





  function majBoutonsHistorique() {


    document.getElementById('btn-hist-undo').disabled = !histActions.some(a => !a.undone);


    document.getElementById('btn-hist-redo').disabled = !histActions.some(a => a.undone);


  }





  function rendreFiltresHistorique() {


    const box = document.getElementById('hst-filtres');


    const opts = [['toutes','Toutes'], ['annulees','Annulées'],


                  ['appliquées','Appliquées'],


                  ...[...new Set(histActions.map(a => a.type))]


                    .map(t => [t, HIST_LABELS[t] || t])];


    box.innerHTML = opts.map(([v,l]) =>


      `<button class="chip${histFiltre === v ? ' active' : ''}" data-f="${escHtml(v)}">${escHtml(l)}</button>`


    ).join('');


    box.querySelectorAll('[data-f]').forEach(b =>


      b.addEventListener('click', () => { histFiltre = b.dataset.f; rendreHistorique(); }));


  }





  function visiblesHistorique() {


    const q = histRecherche.trim().toLowerCase();


    return histActions.filter(a => {


      if (histFiltre === 'annulees'   && !a.undone) return false;


      if (histFiltre === 'appliquées' &&  a.undone) return false;


      if (!['toutes','annulees','appliquées'].includes(histFiltre)


          && a.type !== histFiltre) return false;


      if (q && !String(a.label||'').toLowerCase().includes(q)


             && !String(a.type||'').toLowerCase().includes(q)) return false;


      return true;


    });


  }





  function rendreHistorique() {


    rendreFiltresHistorique(); majStatsHistorique(); majBoutonsHistorique();


    const box = document.getElementById('hst-liste');


    const list = visiblesHistorique();


    if (!list.length) {


      box.innerHTML = '<div class="empty">' + (histActions.length


        ? 'Aucune action ne correspond à ce filtre.'


        : 'Aucune action enregistrée pour le moment.<br>'


          + 'Vos suppressions et modifications apparaîtront ici.') + '</div>';


      return;


    }


    box.innerHTML = list.map((a, i) => `


      <div class="h-item${a.undone ? ' undone' : ''}" style="animation-delay:${i*22}ms">


        <span class="h-ico">${HIST_ICONS[a.type] || '?'}</span>


        <span class="h-corps">


          <div class="h-label">${escHtml(a.label || a.type)}</div>


          <div class="h-type">${escHtml(HIST_LABELS[a.type] || a.type)}</div>


        </span>


        <span class="h-date">${escHtml(a.created || '')}</span>


        <button class="btn small" data-id="${a.id}">


          ${a.undone ? '?? Rétablir' : '?? Annuler'}


        </button>


      </div>`).join('');


    box.querySelectorAll('[data-id]').forEach(b =>


      b.addEventListener('click', () => basculerHistorique(b.dataset.id, b)));


  }





  async function basculerHistorique(id, btn) {


    const cible = btn || document.querySelector(`[data-id="${id}"]`);


    if (cible) { cible.disabled = true; cible.textContent = '⏳'; }


    try {


      const r = await fetch(`/api/historique/${id}/undo`, { method:'POST' });


      const d = await r.json();


      toast(d.ok ? '?? ' + (d.message || 'OK') : '? ' + (d.error || 'Impossible'));


      await chargerHistorique();


    } catch (e) {


      toast('? Erreur réseau');


      if (cible) { cible.disabled = false; cible.textContent = '?? Annuler'; }


    }


  }





  document.getElementById('btn-hist-undo').addEventListener('click', () => {


    const a = histActions.find(x => !x.undone);


    if (a) basculerHistorique(a.id, document.querySelector(`[data-id="${a.id}"]`));


  });


  document.getElementById('btn-hist-redo').addEventListener('click', () => {


    const a = histActions.find(x => x.undone);


    if (a) basculerHistorique(a.id, document.querySelector(`[data-id="${a.id}"]`));


  });


  document.getElementById('btn-hist-refresh').addEventListener('click', chargerHistorique);


  document.getElementById('btn-hist-vider').addEventListener('click', async () => {


    if (!confirm("Effacer tout l'historique ? Les actions passées ne seront plus annulables.")) return;


    await fetch('/api/historique', { method:'DELETE' });


    await chargerHistorique();


    toast('???️ Historique vidé');


  });


  document.getElementById('hst-recherche').addEventListener('input', e => {


    histRecherche = e.target.value; rendreHistorique();


  });





  await chargerHistorique();





});





