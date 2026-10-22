# -*- coding: utf-8 -*-
"""Répare les '?' isolés (caractères Unicode perdus) dans un fichier HTML/JS."""
import re, sys

FIX_CONTEXTUELS = [
    (r'<title>Candimail \?\? ', '<title>Candimail — '),
    (r'\?\? VUE', '\u25c8 VUE'), (r'\?\? MES', '\u25a4 MES'), (r'\?\? RÉPONSES', '\u2341 RÉPONSES'),
    (r'\? Nouvel envoi', '\uff0b Nouvel envoi'),
    (r'\?\? CIBLES', '\u25a6 CIBLES'), (r'\?\? NOUVEL', '\u2709 NOUVEL'),
    (r'\?\? SUIVI', '\u25d4 SUIVI'), (r'\? Gmail', '\u25c9 Gmail'),
    (r'\? Profil', '\u25cb Profil'), (r'\? Paramètres', '\u2699 Paramètres'),
    (r'\? Historique', '\u25f7 Historique'),
    (r'\?\? Candimail', '\U0001f4e7 Candimail'), (r'\?\? Démarrage', '… Démarrage'),
    (r'\?\? ENVOI', '\u2709 ENVOI'),
]

def reparer(chemin):
    texte = open(chemin, encoding='utf-8').read()
    total = 0
    for pat, rep in FIX_CONTEXTUELS:
        texte, n = re.subn(pat, rep, texte)
        total += n
    restes = re.findall(r'\S{0,10}\?(?=\S)', texte)
    open(chemin, 'w', encoding='utf-8').write(texte)
    print(f'{chemin}: {total} corrections contextuelles')
    if restes:
        print(f'  restes ({len(restes)}):', restes[:10])

if __name__ == '__main__':
    for p in sys.argv[1:]:
        reparer(p)
