"""
Represents an energy pad in the game.
"""

from seamaster.models.point import Point


class EnergyPad:
    """
    Represents an energy pad in the game.
    """

    id: int
    location: Point
    available: int
    ticksleft: int

    @classmethod
    def from_dict(cls, data: dict):
        e = cls()
        e.id = data["id"]
        e.location = Point(**data["location"])
        e.available = data["available"]
        e.ticksleft = data["ticks_left"]
        return e
