# -*- coding: utf-8 -*-
"""Restaure la meilleure version de templates/index.html (fcb84e3)
et y ré-applique les changements de restructuration :
1. Titre/sous-titre génériques
2. Sidebar réorganisée en 3 groupes
3. Doublon KPI supprimé
4. Styles inline "neo" retirés
"""
import subprocess, re

REF = 'fcb84e3'
t = subprocess.run(['git', 'show', REF + ':templates/index.html'],
                   capture_output=True).stdout.decode('utf-8', errors='replace')
print('base fcb84e3 :', len(t), 'chars')

# ---------- 1. Titre & sous-titre ----------
t = re.sub(r'<title>[^<]*</title>',
           '<title>Candimail — Messagerie & suivi</title>', t, count=1)
t = t.replace('Assistant candidatures', 'Messagerie & suivi')
t = t.replace('Candimail · Candidatures', 'Candimail · Messagerie & suivi')

# ---------- 2. Sidebar : 3 groupes ----------
# Cherche le bloc existant des nav-groups de la sidebar
pat = re.compile(
    r'(<nav class="nav-group">.*?</nav>\s*){2,}', re.DOTALL)
blocks = pat.findall(t)
print('blocs nav-group multiples détectés:', len(blocks))
if blocks:
    nouvelle = (
        '<nav class="nav-group">\n'
        '    <div class="nav-label">Messagerie</div>\n'
        "    <a class=\"nav-item active\" data-nav=\"overview\"><span class=\"ico\">◈</span> Vue d'ensemble</a>\n"
        '    <a class="nav-item" data-nav="messages"><span class="ico">▤</span> Mes messages</a>\n'
        '    <a class="nav-item" data-nav="groupes"><span class="ico">◍</span> Mes groupes</a>\n'
        '    <a class="nav-item" data-nav="imap"><span class="ico">⌁</span> Réponses & filtres</a>\n'
        '  </nav>\n\n'
        '  <nav class="nav-group">\n'
        '    <div class="nav-label">Envois</div>\n'
        '    <a class="nav-item" data-nav="dash"><span class="ico">▦</span> Cibles <span class="badge-count" id="side-entreprises">0</span></a>\n'
        '    <a class="nav-item" data-nav="envoi"><span class="ico">✉</span> Nouvel envoi</a>\n'
        '    <a class="nav-item" data-nav="suivi"><span class="ico">◔</span> Suivi des envois</a>\n'
        '  </nav>\n\n'
    )
    # Remplace le premier match multi-blocs seulement
    t = pat.sub(nouvelle, t, count=1)

# ---------- 3. Doublon KPI ----------
# Compte les occurrences de ov-total dans deux blocs kpi-grid adjacents
kpi2 = re.search(r'(<div class="kpi-grid">.*?</div>\s*</div>\s*</div>)\s*\n\s*(<div class="kpi-grid">.*?</div>\s*</div>\s*</div>)', t, re.DOTALL)
if kpi2:
    # Garde le premier bloc (avec ov-rate)
    t = t.replace(kpi2.group(2), '', 1)
    print('doublon KPI supprimé')
else:
    print('pas de doublon KPI adjacent détecté')

# ---------- 4. Styles inline "neo" ----------
avant = t.count('box-shadow:4px 4px 0')
t = re.sub(r';?box-shadow:4px 4px 0 var\(--border\)', '', t)
t = re.sub(r'border:3px solid var\(--border\);background:var\(--surface2\);color:var\(--text\);font-weight:700;border-radius:0', '', t)
print('styles neo nettoyés:', avant)

open('templates/index.html', 'w', encoding='utf-8').write(t)
print('écrit :', len(t), 'chars')
