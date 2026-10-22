from flask import abort, make_response
from ..db import db


def validate_model(model, model_id):
    """Validate a model ID and return the matching database instance.
    Converts the ID to an integer, returns a 400 error if the ID
    is invalid, and returns a 404 error if no matching instance exists.
    Accepts a model class as an argument so the same function can
    validate instances of different models, such as Planet or Moon.
    """
    try:
        model_id = int(model_id)
    except (ValueError, TypeError):
        abort(make_response(
            {"message": f"{model.__name__.lower()} {model_id} invalid"},
            400
        ))

    instance = db.session.get(model, model_id)

    if instance is None:
        abort(make_response(
            {"message": f"{model.__name__.lower()} {model_id} not found"},
            404
        ))

    return instance


def create_model(cls, model_data):
    """Create and commit a new model instance from the provided dictionary data.
    Returns the serialized model with HTTP status code 201 if successful.
    Aborts with a 400 Bad Request status code and an error message if model_data is invalid. 
    """
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def get_models_with_filters(cls, filters=None, order_by=None):
    """Construct a select query for the provided model with optional filters
    or order_by column and return a list of matching model dictionaries.
    """
    query = db.select(cls)

    if filters and isinstance(filters, dict):
        for column, value in filters.items():
            if hashattr(cls, column):
                query = query.where(getattr(cls, column).ilike(f"%{value}%"))

    if order_by and hasattr(cls, order_by):
        query = query.order_by(getattr(cls, order_by))
    else:
        query = query.order_by(cls.id)

    models = db.session.scalars(query)
    models_response = [models.to_dict() for model in models]

    return models_response