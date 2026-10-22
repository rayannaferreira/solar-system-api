from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from app.models.planet import Planet

def test_get_models_with_filters_one_matching_planet(add_two_planet):
    result = get_models_with_filters(Planet, {"name": "Mercury"})

    assert result == [
        {
            "id": 1,
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun",
            "distance_from_sun": 57910000,
        }
    ]

def test_get_models_with_filters_no_matches(add_two_planet):
    result = get_models_with_filters(Planet, {"name": "Omicron Persei 8"})

    assert result == []