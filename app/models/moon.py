from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    size: Mapped[int]
    is_tidal_locked: Mapped[bool]

    # belongs to Planet relationship
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="moons")

    def to_dict(self):
        """Return the planet's attributes as a dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size,
            "is_tidal_locked": self.is_tidal_locked
        }
    
    @classmethod
    def from_dict(cls, moon_data):
        planet_id = moon_data.get("planet_id")

        new_moon = cls(
            name=moon_data["name"],
            size=moon_data["size"],
            description=moon_data["description"],
            is_tidal_locked=moon_data["is_tidal_locked"],
            planet_id=planet_id
        )

        return new_moon