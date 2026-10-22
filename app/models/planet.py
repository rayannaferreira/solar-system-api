from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance_from_sun: Mapped[float]

    # has many Moon relationship
    moons: Mapped[List["Moon"]] = relationship(back_populates="planet") # noqa: F821

    
    def to_dict(self):
        """Return the planet's attributes as a dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "distance_from_sun": self.distance_from_sun,
        }

    @classmethod
    def from_dict(cls, planet_data):
        """Create a Planet instance from a dictionary of planet data. 
        Uses cls instead of Planet to create an instance of the class
        that calls this method, allowing subclasses to reuse the method
        and create instances of their own class."""
        return cls(
            name=planet_data["name"],
            description=planet_data["description"],
            distance_from_sun=planet_data["distance_from_sun"],
        )
