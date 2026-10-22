# -*- coding: utf-8 -*-
"""Fournit les entreprises de démo via /api/companies/seed."""
import sqlite3, json, urllib.request

DEMO = []
grands = [
    ("Conglomérat BTP Alpha", "exemple.grands1@exemple.com"),
    ("Infrastructures Beta SA", "exemple.grands2@exemple.com"),
    ("Groupe Gamma Travaux", "exemple.grands3@exemple.com"),
    ("Routes & Ouvrages Delta", "exemple.grands4@exemple.com"),
    ("Bâtiment Epsilon", "exemple.grands5@exemple.com"),
    ("Holding Zeta Construction", "exemple.grands6@exemple.com"),
    ("Voiries et Assainissement Eta", "exemple.grands7@exemple.com"),
    ("Ingénierie Thêta", "exemple.grands8@exemple.com"),
]
pme = [
    ("PME Construct 1", "exemple.pme1@exemple.com"),
    ("PME Travaux 2", "exemple.pme2@exemple.com"),
    ("PME Ingénierie 3", "exemple.pme3@exemple.com"),
    ("PME Bâtiment 4", "exemple.pme4@exemple.com"),
    ("PME Matériaux 5", "exemple.pme5@exemple.com"),
    ("PME Suivi Chantier 6", "exemple.pme6@exemple.com"),
    ("PME Électrotech 7", "exemple.pme7@exemple.com"),
    ("PME Commerce 8", "exemple.pme8@exemple.com"),
    ("PME Internationale 9", "exemple.pme9@exemple.com"),
    ("PME Architecture 10", "exemple.pme10@exemple.com"),
    ("PME Terrains 11", "exemple.pme11@exemple.com"),
    ("PME Nationale 12", "exemple.pme12@exemple.com"),
    ("PME Routière 13", "exemple.pme13@exemple.com"),
    ("PME Croissance 14", "exemple.pme14@exemple.com"),
    ("PME Multi-régions 15", "exemple.pme15@exemple.com"),
]
port = [
    ("Port & Logistique 1", "exemple.port1@exemple.com"),
    ("Port — Direction Stratégie", "exemple.port2@exemple.com"),
    ("Port — Partenariats PPP", "exemple.port3@exemple.com"),
    ("Entreprise Portuaire 2", "exemple.port4@exemple.com"),
    ("Groupe Agro-Port 3", "exemple.port5@exemple.com"),
    ("Transport & Logistique 4", "exemple.port6@exemple.com"),
    ("Laboratoire BTP 5", "exemple.port7@exemple.com"),
    ("Industrie Port 6", "exemple.port8@exemple.com"),
]

for cat, lst in (("grands", grands), ("pme", pme), ("port", port)):
    for nom, mail in lst:
        DEMO.append({
            "name": f"[Démo] {nom}", "cat": cat, "email": mail,
            "context": "Exemple de contexte : décrivez ici ce qui motive votre "
                       "candidature auprès de cette entreprise.",
            "custom": False,
        })

req = urllib.request.Request(
    "http://127.0.0.1:9999/api/companies/seed",
    data=json.dumps({"companies": DEMO}).encode("utf-8"),
    headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        print(r.status, r.read().decode())
except Exception as e:
    print("seed échoué:", e)
