from flask import Flask
from .routes.planet_routes import planets_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(planets_bp)

    return app
