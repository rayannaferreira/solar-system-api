from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from .planet_moons_routes import planet_moons_bp
from .route_utilities import validate_model, create_model, get_models_with_filters

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")



@planets_bp.get("")
def get_all_planets():
    """Apply optional name and description filters and minimum or
    maximum distance filters. Validate distance parameters as finite
    numbers, returning HTTP 400 - Bad Request if invalid. Order results 
    by planet ID and return the matching planets as dictionaries with
    HTTP 200 - OK.
    """
    
    response = get_models_with_filters(Planet, request.args)

    return response



@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    """Calls validate_planet() to convert the supplied ID to an integer
    and retrieve the corresponding database record.
    """

    planet = validate_model(Planet, planet_id)

    return planet.to_dict(), 200


@planets_bp.post("")
def create_planet():
    """Validate the incoming JSON data and check for required fields.
    Create a Planet instance using from_dict(), add it to the database
    session, and commit the transaction. Return the planet's dictionary
    representation with HTTP 201 - Created.
    """

    request_body = request.get_json()

    required_fields = ("name", "description", "distance_from_sun")
    
    if not isinstance(request_body, dict):
        return {"message": "Expected a JSON object"}, 400

    for field in required_fields:
        if field not in request_body:
            return {"message": f"Missing field: {field}"}, 400

    return create_model(Planet, request_body)


@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    """ Updates the planet's name, description, and distance from
    the Sun, commits the changes, and returns the updated planet
    as JSON with HTTP 200 - OK.
    """

    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()
    required_fields = ("name", "description", "distance_from_sun")

            
    if not isinstance(request_body, dict):
        return {"message": "Expected a JSON object"}, 400
        
    for field in required_fields:
        if field not in request_body:
            return {"message": f"Missing field: {field}"}, 400
            
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    planet.name = name
    planet.description = description
    planet.distance_from_sun = distance_from_sun

    db.session.commit()

    return planet.to_dict(), 200


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    """Validate the planet ID and retrieve the matching Planet instance.
    Delete the planet from the database session, commit the transaction,
    and return an empty response with HTTP 204 - No Content.
    """

    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

"""
PLANET NESTED ROUTES REGISTRATION
"""
planets_bp.register_blueprint(planet_moons_bp, url_prefix="/<planet_id>/moons")
