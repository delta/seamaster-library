"""
Represents an algae entity in the game.
"""

from seamaster.constants import AlgaeType
from .point import Point


class Algae:
    """
    Represents an algae entity in the game.
    """

    location: Point
    is_poison: AlgaeType

    @classmethod
    def from_dict(cls, data: dict):
        a = cls()
        a.location = Point(**data["location"])
        a.is_poison = data["is_poison"]
        return a
