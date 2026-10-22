import math
from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from app.models.moon import Moon
from .route_utilities import validate_model, create_model
from ..db import db

planet_moons_bp = Blueprint("planet_moons_bp", __name__)



@planet_moons_bp.get("")
def get_moons_from_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    response = [moon.to_dict() for moon in planet.moons]
    return response

@planet_moons_bp.post("")
def add_moon_to_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()
    request_body["planet_id"] = planet.id

    return create_model(Moon, request_body)