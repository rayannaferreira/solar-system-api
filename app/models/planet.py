from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance_from_sun: Mapped[float]

    # has many Moon relationship
    moons: Mapped[List["Moon"]] = relationship(back_populates="planet")