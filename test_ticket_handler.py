def test_required_fields():
    body = {"title": "VPN issue"}
    assert not body.get("description")

def test_default_priority():
    body = {"title": "Printer", "description": "Offline"}
    assert body.get("priority", "Medium") == "Medium"
