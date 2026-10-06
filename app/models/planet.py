from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    distance_from_sun: Mapped[float]

    #def __init__(self, id, name, description, distance_from_sun):
    #    self.id = id
    #    self.name = name
    #    self.description = description
    #    self.distance_from_sun = distance_from_sun


planets = [
    Planet(1, "Mercury", "The closest planet to the Sun", 57.9),
    Planet(2, "Venus", "The second planet from the Sun", 108.2),
    Planet(3, "Earth", "Our home planet", 149.6)
]