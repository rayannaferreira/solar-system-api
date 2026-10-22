"""Seed the database with the nine traditional planets and notable moons.

Run from the project root:
    python seed.py

To replace existing planet and moon data:
    python seed.py --reset

Distances from the Sun and moon diameters are in kilometers.
Moon diameters are approximate mean diameters.
"""

import argparse

from app import create_app
from app.db import db
from app.models.planet import Planet
from app.models.moon import Moon


PLANETS = [
    {
        "name": "Mercury",
        "description": (
            "The smallest planet and the closest planet to the Sun. "
            "It has no known natural moons."
        ),
        "distance_from_sun": 57_910_000,
    },
    {
        "name": "Venus",
        "description": (
            "A rocky planet with an extremely hot, dense atmosphere. "
            "It has no known natural moons."
        ),
        "distance_from_sun": 108_210_000,
    },
    {
        "name": "Earth",
        "description": (
            "A rocky planet with liquid water on its surface and the "
            "only world currently known to support life."
        ),
        "distance_from_sun": 149_600_000,
    },
    {
        "name": "Mars",
        "description": (
            "A cold, rocky planet known for its reddish surface, "
            "polar ice caps, and evidence of ancient liquid water."
        ),
        "distance_from_sun": 227_920_000,
    },
    {
        "name": "Jupiter",
        "description": (
            "The largest planet in the Solar System, a gas giant "
            "with a vast atmosphere and many natural moons."
        ),
        "distance_from_sun": 778_570_000,
    },
    {
        "name": "Saturn",
        "description": (
            "A gas giant famous for its extensive ring system "
            "and numerous natural moons."
        ),
        "distance_from_sun": 1_433_530_000,
    },
    {
        "name": "Uranus",
        "description": (
            "An ice giant with a blue-green atmosphere and an "
            "extreme axial tilt."
        ),
        "distance_from_sun": 2_872_460_000,
    },
    {
        "name": "Neptune",
        "description": (
            "A distant ice giant with a blue atmosphere, powerful "
            "winds, and a large moon named Triton."
        ),
        "distance_from_sun": 4_495_060_000,
    },
    {
        "name": "Pluto",
        "description": (
            "A dwarf planet in the Kuiper Belt. Once classified as "
            "the ninth planet, it remains a nostalgic member of the "
            "traditional nine-planet Solar System."
        ),
        "distance_from_sun": 5_906_380_000,
    },
]


# Approximate mean diameter in kilometers.
# Tidal locking refers to synchronous rotation with the parent body.
MOONS = [
    # Earth
    {
        "name": "Moon",
        "size": 3475,
        "description": "Earth's only natural satellite.",
        "is_tidal_locked": True,
        "planet_id": 3,
    },

    # Mars
    {
        "name": "Phobos",
        "size": 22,
        "description": (
            "The larger and closer of Mars's two small moons. "
            "It is slowly spiraling toward Mars."
        ),
        "is_tidal_locked": True,
        "planet_id": 4,
    },
    {
        "name": "Deimos",
        "size": 12,
        "description": (
            "The smaller and more distant of Mars's two known moons."
        ),
        "is_tidal_locked": True,
        "planet_id": 4,
    },

    # Jupiter
    {
        "name": "Io",
        "size": 3643,
        "description": (
            "A volcanically active moon with hundreds of volcanoes "
            "driven by tidal heating."
        ),
        "is_tidal_locked": True,
        "planet_id": 5,
    },
    {
        "name": "Europa",
        "size": 3122,
        "description": (
            "An icy moon with a subsurface ocean that may contain "
            "conditions suitable for life."
        ),
        "is_tidal_locked": True,
        "planet_id": 5,
    },
    {
        "name": "Ganymede",
        "size": 5268,
        "description": (
            "The largest moon in the Solar System, larger than "
            "the planet Mercury."
        ),
        "is_tidal_locked": True,
        "planet_id": 5,
    },
    {
        "name": "Callisto",
        "size": 4821,
        "description": (
            "A heavily cratered moon with an ancient, icy surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 5,
    },
    {
        "name": "Amalthea",
        "size": 167,
        "description": (
            "A small, irregular inner moon of Jupiter with a "
            "reddish surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 5,
    },

    # Saturn
    {
        "name": "Mimas",
        "size": 396,
        "description": (
            "A small icy moon recognizable by its enormous "
            "Herschel impact crater."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Enceladus",
        "size": 504,
        "description": (
            "An icy moon that ejects water-rich plumes from "
            "fractures near its south pole."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Tethys",
        "size": 1062,
        "description": (
            "An icy moon with a large impact crater and a "
            "prominent valley system."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Dione",
        "size": 1123,
        "description": (
            "An icy moon with bright fractured terrain and "
            "a heavily cratered surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Rhea",
        "size": 1528,
        "description": (
            "Saturn's second-largest moon, an icy world with "
            "a heavily cratered surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Titan",
        "size": 5150,
        "description": (
            "Saturn's largest moon, with a dense atmosphere "
            "and lakes of liquid methane and ethane."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Iapetus",
        "size": 1469,
        "description": (
            "An unusual moon with contrasting bright and dark "
            "hemispheres and a prominent equatorial ridge."
        ),
        "is_tidal_locked": True,
        "planet_id": 6,
    },
    {
        "name": "Phoebe",
        "size": 213,
        "description": (
            "A dark, irregular outer moon that travels in a "
            "retrograde orbit around Saturn."
        ),
        "is_tidal_locked": False,
        "planet_id": 6,
    },

    # Uranus
    {
        "name": "Miranda",
        "size": 472,
        "description": (
            "A small icy moon with dramatic cliffs, grooves, "
            "and varied geological terrain."
        ),
        "is_tidal_locked": True,
        "planet_id": 7,
    },
    {
        "name": "Ariel",
        "size": 1158,
        "description": (
            "An icy moon with extensive fault valleys and "
            "relatively bright surface terrain."
        ),
        "is_tidal_locked": True,
        "planet_id": 7,
    },
    {
        "name": "Umbriel",
        "size": 1169,
        "description": (
            "A dark, heavily cratered moon of Uranus."
        ),
        "is_tidal_locked": True,
        "planet_id": 7,
    },
    {
        "name": "Titania",
        "size": 1578,
        "description": (
            "The largest moon of Uranus, with large canyons "
            "and an ancient icy surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 7,
    },
    {
        "name": "Oberon",
        "size": 1523,
        "description": (
            "An outer major moon of Uranus with a heavily "
            "cratered surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 7,
    },

    # Neptune
    {
        "name": "Triton",
        "size": 2707,
        "description": (
            "Neptune's largest moon, orbiting in the opposite "
            "direction to Neptune's rotation."
        ),
        "is_tidal_locked": True,
        "planet_id": 8,
    },
    {
        "name": "Proteus",
        "size": 420,
        "description": (
            "A large, irregular inner moon of Neptune with "
            "a dark, heavily cratered surface."
        ),
        "is_tidal_locked": True,
        "planet_id": 8,
    },
    {
        "name": "Nereid",
        "size": 340,
        "description": (
            "An irregular moon of Neptune with an unusually "
            "eccentric orbit."
        ),
        "is_tidal_locked": False,
        "planet_id": 8,
    },

    # Pluto
    {
        "name": "Charon",
        "size": 1212,
        "description": (
            "Pluto's largest moon. Pluto and Charon are tidally "
            "locked to each other and orbit a shared center of mass."
        ),
        "is_tidal_locked": True,
        "planet_id": 9,
    },
    {
        "name": "Nix",
        "size": 49,
        "description": (
            "A small, irregular moon of Pluto with a rapidly "
            "changing, chaotic rotation."
        ),
        "is_tidal_locked": False,
        "planet_id": 9,
    },
    {
        "name": "Hydra",
        "size": 51,
        "description": (
            "A small outer moon of Pluto with an irregular shape "
            "and chaotic rotation."
        ),
        "is_tidal_locked": False,
        "planet_id": 9,
    },
    {
        "name": "Kerberos",
        "size": 19,
        "description": (
            "A small, irregular moon orbiting between Nix and Hydra."
        ),
        "is_tidal_locked": False,
        "planet_id": 9,
    },
    {
        "name": "Styx",
        "size": 16,
        "description": (
            "The smallest known moon of Pluto, orbiting inside "
            "the orbit of Nix."
        ),
        "is_tidal_locked": False,
        "planet_id": 9,
    },
]

def seed_database(reset=False):
    app = create_app()

    with app.app_context():
        existing_planets = db.session.query(Planet).count()
        existing_moons = db.session.query(Moon).count()

        if (existing_planets or existing_moons) and not reset:
            raise RuntimeError(
                "The database already contains planet or moon records. "
                "Run `python seed.py --reset` to replace them."
            )

        if reset:
            # Delete children before parents to respect the foreign key.
            db.session.query(Moon).delete(
                synchronize_session=False
            )
            db.session.query(Planet).delete(
                synchronize_session=False
            )
            db.session.commit()

        try:
            planets = [
                Planet(
                    name=data["name"],
                    description=data["description"],
                    distance_from_sun=data["distance_from_sun"],
                )
                for data in PLANETS
            ]

            db.session.add_all(planets)
            db.session.flush()

            moons = [
                Moon(**data)
                for data in MOONS
            ]

            db.session.add_all(moons)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        print(f"Seeded {len(PLANETS)} planets.")
        print(f"Seeded {len(MOONS)} moons.")
        print("Planet IDs 1–9 assigned in traditional order.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed the Solar System database."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing planet and moon records before seeding.",
    )
    args = parser.parse_args()

    seed_database(reset=args.reset)