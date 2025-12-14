from app.db.session import SessionLocal
from app.models.parish import Parish


def _create_parish(name: str) -> Parish:
    db = SessionLocal()
    parish = Parish(
        name=name,
        address_line1="123 Church St",
        city="Springfield",
        state="IL",
        zip_code="62701",
    )
    db.add(parish)
    db.commit()
    db.refresh(parish)
    db.close()
    return parish


def test_list_and_get_parishes(client):
    parish = _create_parish("St. Mary Parish")
    _create_parish("St. Joseph Parish")

    list_resp = client.get("/api/v1/parishes/")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 2
    names = {p["name"] for p in data}
    assert "St. Mary Parish" in names

    detail_resp = client.get(f"/api/v1/parishes/{parish.id}")
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["id"] == parish.id
    assert detail["name"] == parish.name
