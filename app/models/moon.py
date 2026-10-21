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