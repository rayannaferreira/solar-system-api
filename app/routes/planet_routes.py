from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")



@planets_bp.get("")
def get_all_planets():
    """Applies optional filters for partial name matches, partial
    description matches, and minimum or maximum distance from the Sun.
    Converts distance parameters to floats and returns HTTP 400 if
    either value is not numeric. Orders the results by planet ID,
    executes the query, and returns the matching planets as a JSON
    list with HTTP 200.
    """
    
    query = db.select(Planet)

    name = request.args.get("name")
    if name:
        query = query.where(Planet.name.ilike(f"%{name}%"))

    description = request.args.get("description")
    if description:
        query = query.where(Planet.description.ilike(f"%{description}%"))

    max_distance = request.args.get("max_distance")
    min_distance = request.args.get("min_distance")

    if max_distance is not None:
        try:
            max_distance = float(max_distance)
        except ValueError:
            abort(make_response({
                "message": "max_distance must be a number"
            }, 400))

        query = query.where(
            Planet.distance_from_sun <= max_distance
        )

    if min_distance is not None:
        try:
            min_distance = float(min_distance)
        except ValueError:
            abort(make_response({
                "message": "min_distance must be a number"
            }, 400))

        query = query.where(
            Planet.distance_from_sun >= min_distance
        )

    query = query.order_by(Planet.id)
    planets = db.session.execute(query).scalars()

    return [
        {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "distance_from_sun": planet.distance_from_sun,
        }
        for planet in planets
    ], 200



@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    """Calls validate_planet() to convert the supplied ID to an integer
    and retrieve the corresponding database record.
    """

    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }, 200


@planets_bp.post("")
def create_planet():
    """Reads the incoming JSON data and checks that it is a dictionary
    containing the required name, description, and distance_from_sun
    fields. Creates a Planet instance using these values, adds it to
    the database session, and commits the transaction.
    """

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


@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    """ Updates the planet's name, description, and distance from
    the Sun, commits the changes, and returns the updated planet
    as JSON with HTTP 200.
    """

    planet = validate_planet(planet_id)

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

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }, 200


@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    """Calls validate_planet() to ensure the ID is valid and the planet
    exists. Deletes the planet from the database session, commits the
    transaction, and returns an empty response with HTTP 204 No Content.
    """

    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_planet(id):
    """Attempts to convert the supplied ID to an integer. If conversion
    fails, aborts the request with HTTP 400. Otherwise, creates a
    SQLAlchemy query to find a planet with the matching ID and retrieves
    it using db.session.scalar(). If no planet exists, aborts with HTTP 404. 
    Returns the Planet instance when validation succeeds.
    """

    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"planet {id} invalid"}, 400))

    query = db.select(Planet).where(Planet.id == id)
    planet = db.session.scalar(query)

    if not planet:
        abort(make_response({"message": f"planet {id} not found"}, 404))

    return planet