
def test_get_all_planets_with_no_records(client):
    response = client.get("/planets")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_a_404_response(client):
    response = client.get("/planets/1")

    assert response.status_code == 404
    assert response.get_json() == {"message": "planet 1 not found"}


def test_get_one_planet(client, add_one_planet):
    response = client.get("/planets/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Mercury",
        "description": "Smallest planet, closest to the Sun",
        "distance_from_sun": 57910000,
    }


def test_get_second_planet(client, add_two_planet):
    response = client.get("/planets/2")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 2,
        "name": "Earth",
        "description": "Third planet from the Sun, with liquid water on its surface",
        "distance_from_sun": 149600000,
    }


def test_get_all_planets(client, add_two_planet):
    response = client.get("/planets")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun",
            "distance_from_sun": 57910000,
        },
        {
            "id": 2,
            "name": "Earth",
            "description": "Third planet from the Sun, with liquid water on its surface",
            "distance_from_sun": 149600000,
        },
    ]


def test_create_one_planet(client):
    response = client.post(
        "/planets",
        json={
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun",
            "distance_from_sun": 57910000,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Mercury",
        "description": "Smallest planet, closest to the Sun",
        "distance_from_sun": 57910000,
    }


def test_create_planet_missing_field(client):
    response = client.post(
        "/planets",
        json={"name": "Earth"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing field: description"}


def test_create_planet_without_json_object(client):
    response = client.post("/planets", json=["Earth"])

    assert response.status_code == 400
    assert response.get_json() == {"message": "Expected a JSON object"}


def test_update_one_planet(client, add_one_planet):
    response = client.put(
        "/planets/1",
        json={
            "name": "Mercury Updated",
            "description": "Updated description",
            "distance_from_sun": 58000000,
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Mercury Updated",
        "description": "Updated description",
        "distance_from_sun": 58000000,
    }


def test_update_planet_missing_field(client, add_one_planet):
    response = client.put(
        "/planets/1",
        json={"name": "Mercury Updated"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing field: description"}


def test_delete_one_planet(client, add_one_planet):
    response = client.delete("/planets/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "planet 1 deleted successfully"
    }


def test_delete_planet_not_found(client):
    response = client.delete("/planets/1")

    assert response.status_code == 404
    assert response.get_json() == {"message": "planet 1 not found"}


def test_invalid_planet_id(client):
    response = client.get("/planets/abc")

    assert response.status_code == 400
    assert response.get_json() == {"message": "planet abc invalid"}


def test_filter_planets_by_description(client, add_two_planet):
    response = client.get("/planets?description=water")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 2,
            "name": "Earth",
            "description": "Third planet from the Sun, with liquid water on its surface",
            "distance_from_sun": 149600000,
        }
    ]


def test_filter_planets_by_max_distance(client, add_two_planet):
    response = client.get("/planets?max_distance=60000000")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun",
            "distance_from_sun": 57910000,
        }
    ]


def test_filter_planets_by_min_distance(client, add_two_planet):
    response = client.get("/planets?min_distance=100000000")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 2,
            "name": "Earth",
            "description": "Third planet from the Sun, with liquid water on its surface",
            "distance_from_sun": 149600000,
        }
    ]
