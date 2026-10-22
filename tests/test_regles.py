"""Tests de la logique métier (core/regles) — sans réseau ni SMTP."""
from candimail.core import regles


def test_seed_regles_premier_lancement():
    cfg = {}
    regles.seed_regles(cfg)
    assert cfg["filtres_init"] == 2
    assert len(cfg["filtres_gmail"]) == 6
    noms = [r["name"] for r in cfg["filtres_gmail"]]
    assert "Bourse" in noms and "Travail" in noms
    # priorités 1..6
    assert [r["priority"] for r in cfg["filtres_gmail"]] == [1, 2, 3, 4, 5, 6]


def test_seed_regles_idempotent():
    cfg = {}
    regles.seed_regles(cfg)
    avant = [dict(r) for r in cfg["filtres_gmail"]]
    regles.seed_regles(cfg)  # 2e appel → aucun changement
    assert cfg["filtres_gmail"] == avant


def test_seed_regles_preserve_apprentissage():
    """Les règles source='apprentissage' ne sont JAMAIS écrasées par la v2."""
    cfg = {"filtres_init": 1, "filtres_gmail": [
        {"name": "Travail", "icon": "x", "color": "#000", "items": [],
         "notify": False, "actions": [], "source": "apprentissage"}]}
    regles.seed_regles(cfg)
    f = cfg["filtres_gmail"][0]
    assert f["items"] == []          # ses items perso préservés
    assert cfg["filtres_init"] == 2


def test_normaliser_regle_nouveau():
    r = regles.normaliser_regle({
        "name": "MA règle", "champ": "from", "valeur": "rh@ex.com",
        "actions": ["label", "notify", "PAS_UNE_ACTION"],
    })
    assert r["name"] == "MA règle"
    assert r["items"] == [{"champ": "from", "valeur": "rh@ex.com"}]
    assert r["actions"] == ["label", "notify"]      # action invalide filtrée
    assert r["notify"] is True
    assert r["enabled"] is True


def test_normaliser_regle_items_multiples():
    r = regles.normaliser_regle({
        "name": "r", "items": [
            {"champ": "sujet", "valeur": "stage"},
            {"champ": "invalide", "valeur": "x"},     # champ refusé
            {"champ": "from", "valeur": ""},          # valeur vide refusée
            "pas-un-dict",                            # type refusé
        ]})
    assert r["items"] == [{"champ": "sujet", "valeur": "stage"}]


def test_normaliser_regle_update_preserve_existant():
    base = {"id": "rule-001", "name": "Origine", "items":
            [{"champ": "from", "valeur": "a@b.c"}], "priority": 3}
    r = regles.normaliser_regle({"name": "Renommée"}, existante=base)
    assert r["id"] == "rule-001"          # id conservé
    assert r["name"] == "Renommée"        # nom changé
    assert r["items"] == base["items"]    # items conservés


def test_reindexer_priorites():
    filtres = [{"priority": 7}, {"priority": 2}, {"priority": 99}]
    assert [f["priority"] for f in regles.reindexer_priorites(filtres)] == [1, 2, 3]


def test_appliquer_apprentissage_nouvelle_regle():
    cfg = {"filtres_gmail": []}
    regles.appliquer_apprentissage(cfg, "x@ex.com", "Mes Contacts")
    apprise = [f for f in cfg["filtres_gmail"] if f.get("source") == "apprentissage"]
    assert len(apprise) == 1
    r = apprise[0]
    assert r["priority"] == 0                     # gagne sur tout
    assert r["items"] == [{"champ": "from", "valeur": "x@ex.com"}]
    assert r["label"] == r["name"] == "Mes Contacts"
    assert cfg["apprentissage"]["x@ex.com"]["corrections"] == 0


def test_appliquer_apprentissage_compte_corrections():
    cfg = {"filtres_gmail": []}
    regles.appliquer_apprentissage(cfg, "x@ex.com", "A")
    regles.appliquer_apprentissage(cfg, "x@ex.com", "B")   # change de label
    assert cfg["apprentissage"]["x@ex.com"]["corrections"] == 1
    regles.appliquer_apprentissage(cfg, "x@ex.com", "B")   # même label → reset
    assert cfg["apprentissage"]["x@ex.com"]["corrections"] == 0


def test_appliquer_apprentissage_reutilise_regle():
    """2e apprentissage du MÊME expéditeur → réutilise la règle, pas de doublon."""
    cfg = {"filtres_gmail": []}
    regles.appliquer_apprentissage(cfg, "x@ex.com", "A")
    regles.appliquer_apprentissage(cfg, "x@ex.com", "B")
    apprise = [f for f in cfg["filtres_gmail"] if f.get("source") == "apprentissage"]
    assert len(apprise) == 1
    assert apprise[0]["label"] == "B"


def test_calculer_suggestions_expediteur_frequent():
    cfg = {"apprentissage": {"a@b.c": {"label": "L", "corrections": 3},
                             "d@e.f": {"label": "M", "corrections": 2}}}
    s = regles.calculer_suggestions(cfg)
    assert len(s) == 1
    assert s[0] == {"email": "a@b.c", "label": "L",
                    "corrections": 3, "type": "expediteur_frequent"}


def test_calculer_suggestions_regle_faible():
    cfg = {"filtres_gmail": [
        {"name": "R", "id": "r1", "nb_classements": 10, "nb_corrections": 3},
        {"name": "S", "id": "r2", "nb_classements": 10, "nb_corrections": 1},
    ]}
    s = regles.calculer_suggestions(cfg)
    assert len(s) == 1
    assert s[0]["regle"] == "R" and s[0]["type"] == "regle_faible"


def test_export_sans_secrets():
    cfg = {"comptes": [{"email": "x@gmail.com", "password": "enc$SECRET"}],
           "securite": {"secret_key": "xyz"}, "templates_perso": [{"id": "t1"}]}
    data, texte = regles.export_sans_secrets(cfg, lambda: {"E1": {"envoye": True}})
    assert "comptes" not in data["config"]
    assert "securite" not in data["config"]
    assert data["config"]["templates_perso"] == [{"id": "t1"}]
    assert "SECRET" not in texte
    assert data["log"] == {"E1": {"envoye": True}}


def test_export_sans_secrets_detecte_fuite():
    """Un secret qui a survécu au filtrage → RuntimeError (jamais exporté)."""
    import pytest
    cfg = {"filtre_special": [{"pwd": "enc$FUITE"}]}   # clé non filtrée
    with pytest.raises(RuntimeError):
        regles.export_sans_secrets(cfg, lambda: {})
