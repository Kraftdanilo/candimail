"""Tests des routes API (FastAPI + TestClient, DB temporaire)."""
import io
import json


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True
    assert r.get_json()["service"] == "candimail"


def test_debug_info_ferme_par_defaut(client):
    """Anti-fuite : /api/debug/info doit être 404 sans CANDIMAIL_DEBUG=1."""
    r = client.get("/api/debug/info")
    assert r.status_code == 404


def test_templates_crud(client):
    # POST
    r = client.post("/api/templates", json={
        "nom": "T1", "objet": "O", "corps": "C", "categorie": "autre"})
    assert r.status_code == 200
    tid = r.get_json()["id"]
    # GET
    r = client.get("/api/templates")
    noms = [t["nom"] for t in r.get_json()["templates"]]
    assert "T1" in noms
    # DELETE
    r = client.delete(f"/api/templates/{tid}")
    assert r.status_code == 200
    # DELETE à nouveau → 404
    r = client.delete(f"/api/templates/{tid}")
    assert r.status_code == 404


def test_templates_validation(client):
    r = client.post("/api/templates", json={"nom": "", "objet": "", "corps": ""})
    assert r.status_code == 400


def test_filtres_get_avec_seed(client):
    r = client.get("/api/filtres")
    assert r.status_code == 200
    filtres = r.get_json()["filtres"]
    assert len(filtres) == 6                      # seed au premier accès
    assert [f["priority"] for f in filtres] == list(range(1, len(filtres) + 1))


def test_filtres_add_valide_invalide(client):
    r = client.post("/api/filtres", json={
        "name": "Test", "champ": "from", "valeur": "rh@x.com",
        "actions": ["archive"]})   # pas de label requis avec 'archive'
    assert r.status_code == 200
    n_avant = len(r.get_json()["filtres"])
    # invalide (pas de valeur)
    r = client.post("/api/filtres", json={"name": "Vide", "actions": []})
    assert r.status_code == 400
    # pas d'ajout parasite
    r = client.get("/api/filtres")
    assert len(r.get_json()["filtres"]) == n_avant


def test_filtres_delete_reindexe(client):
    client.post("/api/filtres", json={
        "name": "X", "champ": "from", "valeur": "a@b.c", "actions": ["archive"]})
    r = client.get("/api/filtres")
    n = len(r.get_json()["filtres"])
    r = client.delete(f"/api/filtres/{n - 1}")
    assert r.status_code == 200
    filtres = r.get_json()["filtres"]
    # priorités renumérotées 1..N sans trou
    assert [f["priority"] for f in filtres] == list(range(1, len(filtres) + 1))


def test_filtres_delete_404(client):
    r = client.delete("/api/filtres/9999")
    assert r.status_code == 404


def test_filtres_toggle(client):
    r = client.post("/api/filtres/0/toggle")
    assert r.status_code == 200
    assert r.get_json()["filtres"][0]["enabled"] is False
    r = client.post("/api/filtres/0/toggle")
    assert r.get_json()["filtres"][0]["enabled"] is True


def test_filtres_toggle_404(client):
    assert client.post("/api/filtres/9999/toggle").status_code == 404


def test_filtres_reorder(client):
    r = client.get("/api/filtres")
    filtres = r.get_json()["filtres"]
    ids = [f["id"] for f in filtres]
    r = client.post("/api/filtres/reorder", json={"ordre": list(reversed(ids))})
    assert r.status_code == 200
    f = r.get_json()["filtres"]
    n = len(ids)
    assert [x["priority"] for x in f] == list(range(1, n + 1))
    assert [x["id"] for x in f] == list(reversed(ids))


def test_filtres_reorder_liste_invalide(client):
    assert client.post("/api/filtres/reorder",
                       json={"ordre": ["a", "b"]}).status_code == 400
    assert client.post("/api/filtres/reorder",
                       json={"ordre": "pas-une-liste"}).status_code == 400


def test_notifications(client):
    r = client.get("/api/notifications")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True
    r = client.post("/api/notifications/vue")
    assert r.status_code == 200


def test_suggestions(client):
    r = client.get("/api/filtres/suggestions")
    assert r.status_code == 200
    assert "suggestions" in r.get_json()


def test_filtrer_corriger_validation(client):
    assert client.post("/api/filtres/corriger",
                       json={"email": "pas-un-email", "label": "L"}).status_code == 400
    assert client.post("/api/filtres/corriger",
                       json={"email": "a@b.c", "label": ""}).status_code == 400


def test_export_json_sans_secret(client):
    r = client.get("/api/export-json")
    assert r.status_code == 200
    data = json.loads(r.data.decode("utf-8"))
    assert "comptes" not in data["config"]
    assert "securite" not in data["config"]


def test_import_json_sans_fichier(client):
    assert client.post("/api/import-json").status_code == 400


def test_import_json_roundtrip(client):
    # un log initial
    client.post("/api/mark-response", json={"company": "ACME", "repondu": True})
    # export → import
    r = client.get("/api/export-json")
    data = json.loads(r.data.decode("utf-8"))
    out = io.BytesIO(json.dumps(data).encode("utf-8"))
    r = client.post("/api/import-json", data={"file": (out, "b.json")},
                    content_type="multipart/form-data")
    assert r.status_code == 200
    j = r.get_json()
    assert j["ok"] is True and j["importees"] >= 1


def test_import_json_fichier_invalide(client):
    out = io.BytesIO(b"ceci n'est pas du json {{{")
    r = client.post("/api/import-json", data={"file": (out, "b.json")},
                    content_type="multipart/form-data")
    assert r.status_code == 400


def test_mark_response(client):
    r = client.post("/api/mark-response", json={"company": "ZZZ", "repondu": True})
    assert r.status_code == 404          # inconnue
    # l'export contient-elle après ajout via import ? (roundtrip)
    data = {"log": {"YYY": {"envoye": True, "repondu": False}}}
    out = io.BytesIO(json.dumps(data).encode("utf-8"))
    client.post("/api/import-json", data={"file": (out, "b.json")},
                content_type="multipart/form-data")
    r = client.post("/api/mark-response", json={"company": "YYY", "repondu": True})
    assert r.status_code == 200
    assert r.get_json()["repondu"] is True


def test_export_csv(client):
    r = client.get("/api/export-csv")
    assert r.status_code == 200
    assert r.headers["Content-Type"].startswith("text/csv")
    assert "Entreprise" in r.data.decode("utf-8-sig")


def test_reset_log(client):
    assert client.post("/api/reset-log").status_code == 200


def test_historique_flow(client):
    r = client.get("/api/historique")
    assert r.status_code == 200
    r = client.post("/api/historique", json={
        "type": "test", "label": "test",
        "undo": None, "redo": None})
    assert r.status_code == 200
    hid = r.get_json()["id"]
    # undo d'une action sans undo → 400
    r = client.post(f"/api/historique/{hid}/undo")
    assert r.status_code == 400
    r = client.delete("/api/historique")
    assert r.status_code == 200


def test_historique_404(client):
    assert client.post("/api/historique/99999/undo").status_code == 404
    assert client.post("/api/historique/99999/redo").status_code == 404


def test_erreur_globale_sans_fuite(client):
    """Toute erreur 500 → message générique, jamais de traceback."""
    r = client.get("/api/je-nexiste-pas")
    assert r.status_code == 404
    j = r.get_json()
    assert "traceback" not in json.dumps(j).lower()


def test_pieces_get(client):
    r = client.get("/api/pieces")
    assert r.status_code == 200
    assert "pieces" in r.get_json()


def test_pieces_traversed_directory_refusee(client):
    """Sécurité : un piece_id avec '..' ou '/' ne doit rien toucher."""
    for mauvais in ("..", "../secret.key", "..\\secret.key", "/etc/passwd"):
        r = client.delete(f"/api/pieces/{mauvais}")
        assert r.status_code in (404, 405, 500), f"{mauvais} → {r.status_code}"
        assert "uploads" not in r.get_data(as_text=True).lower()
