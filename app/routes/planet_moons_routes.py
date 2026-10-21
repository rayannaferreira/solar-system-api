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
def add_moon_to_planet(planet_id, moon_data):
    pass