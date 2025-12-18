def test_get_package_types(client):
    response = client.get("/package-types/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)

    # Базовая проверка структуры
    if body["data"]:
        item = body["data"][0]
        assert "id" in item
        assert "name" in item


def test_create_package(client):
    payload = {
        "name": "Test package",
        "weight_kg": 2.5,
        "type_id": 1,
        "content_price_usd": 100,
    }

    response = client.post("/packages", json=payload)

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True

    data = body["data"]
    assert data["name"] == payload["name"]
    assert data["delivery_calculated"] is False
    assert data["delivery_status"] == "Не рассчитано"


def test_session_cookie_persisted(client):
    response = client.get("/packages")

    assert response.status_code == 200

    # cookie должен быть установлен
    cookies = client.cookies
    assert "session_id" in cookies


def test_get_packages_list(client):
    response = client.get("/packages")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    data = body["data"]
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


def test_get_package_by_id(client):
    payload = {
        "name": "Package for get",
        "weight_kg": 1.2,
        "type_id": 1,
        "content_price_usd": 50,
    }

    create_resp = client.post("/packages", json=payload)
    package_id = create_resp.json()["data"]["id"]

    response = client.get(f"/packages/{package_id}")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    data = body["data"]
    assert data["id"] == package_id
    assert data["delivery_calculated"] is False
    assert data["delivery_status"] == "Не рассчитано"


def test_calculate_delivery(client):
    payload = {
        "name": "Package for calculation",
        "weight_kg": 3,
        "type_id": 1,
        "content_price_usd": 200,
    }

    create_resp = client.post("/packages", json=payload)
    package_id = create_resp.json()["data"]["id"]

    response = client.post(f"/packages/{package_id}/calculate")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    data = body["data"]
    assert data["delivery_calculated"] is True
    assert data["delivery_price_rub"] is not None
    assert data["delivery_status"] != "Не рассчитано"


def test_calculate_delivery_twice_returns_409(client):
    payload = {
        "name": "Package double calc",
        "weight_kg": 2,
        "type_id": 1,
        "content_price_usd": 100,
    }

    create_resp = client.post("/packages", json=payload)
    package_id = create_resp.json()["data"]["id"]

    client.post(f"/packages/{package_id}/calculate")
    second_resp = client.post(f"/packages/{package_id}/calculate")

    assert second_resp.status_code == 409

    body = second_resp.json()
    assert body["success"] is False


def test_get_only_calculated_packages(client):
    response = client.get("/packages?only_calculated=true")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    for item in body["data"]["items"]:
        assert item["delivery_calculated"] is True


def test_get_only_not_calculated_packages(client):
    response = client.get("/packages?only_calculated=false")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    for item in body["data"]["items"]:
        assert item["delivery_calculated"] is False
