from flask import Blueprint, abort, make_response, request
from app.models.planet import Planet
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.execute(query).scalars()

    planets_response = []

    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun": planet.distance_from_sun
            }
        )

    return planets_response


@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return {"message": f"planet {planet_id} invalid"}, 400

    for planet in planets:
        if planet.id == planet_id:
            return {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun": planet.distance_from_sun
            }

    return {"message": f"planet {planet_id} not found"}, 404

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    new_planet = Planet(name=name, description=description, distance_from_sun=distance_from_sun)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance_from_sun": new_planet.distance_from_sun
    }

    return response, 201