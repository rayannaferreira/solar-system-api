import math
from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from app.models.moon import Moon
from ..db import db

planet_moons_bp = Blueprint("planet_moons_bp", __name__)



@planet_moons_bp.get("")
def get_moons_from_planet(planet_id):
    pass

@planet_moons_bp.post("")
def add_moon_to_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()
    request_body["planet_id"] = planet.id

    try:
        new_moon = Moon.from_dict(request_body)
    except:
        response = {"message": f"Invalid request: mising {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_moon)
    db.session.commit()

    return make_response(new_moon.to_dict(), 201)