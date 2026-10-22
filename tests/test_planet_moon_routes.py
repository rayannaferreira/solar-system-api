def test_get_moons_from_planet_with_no_moons(client, add_one_planet):
    response = client.get("/planets/1/moons")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_moons_from_planet(client, add_two_planets_and_one_moon):
    response = client.get("/planets/2/moons")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "name": "Luna",
            "size": 3475,
            "description": "Earth's only natural satellite",
            "is_tidal_locked": True,
            "planet_id": 2,
        }
    ]


def test_get_moons_from_planet_not_found(client):
    response = client.get("/planets/1/moons")

    assert response.status_code == 404
    assert response.get_json() == {"message": "planet 1 not found"}


def test_get_moons_with_invalid_planet_id(client):
    response = client.get("/planets/abc/moons")

    assert response.status_code == 400
    assert response.get_json() == {"message": "planet abc invalid"}


def test_add_moon_to_planet(client, add_two_planet):
    response = client.post(
        "/planets/2/moons",
        json={
            "name": "Luna",
            "size": 3475,
            "description": "Earth's only natural satellite",
            "is_tidal_locked": True,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Luna",
        "size": 3475,
        "description": "Earth's only natural satellite",
        "is_tidal_locked": True,
        "planet_id": 2,
    }


def test_add_moon_to_planet_not_found(client):
    response = client.post(
        "/planets/1/moons",
        json={
            "name": "Luna",
            "size": 3475,
            "description": "Earth's only natural satellite",
            "is_tidal_locked": True,
        },
    )

    assert response.status_code == 404
    assert response.get_json() == {"message": "planet 1 not found"}


def test_add_moon_to_planet_uses_correct_planet_id(client, add_two_planets_and_one_moon):
    response = client.post(
        "/planets/2/moons",
        json={
            "name": "Luna",
            "size": 3475,
            "description": "Earth's only natural satellite",
            "is_tidal_locked": True,
            "planet_id": 1,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["planet_id"] == 2