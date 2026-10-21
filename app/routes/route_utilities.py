from flask import abort, make_response
from ..db import db


def validate_model(model, model_id):
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
