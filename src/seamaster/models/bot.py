"""
Initialization of Bot model.
"""

from typing import List
from seamaster.models.point import Point
from seamaster.constants import Ability


class Bot:
    """
    Represents a bot in the game.
    """

    id: int
    location: Point
    energy: float
    scraps: int
    abilities: List[Ability]
    algae_held: int
    traversal_cost: float
    status: str
    vision_radius: float

    @classmethod
    def from_dict(cls, data: dict):
        b = cls()
        b.id = data["id"]
        b.location = Point(**data["location"])
        b.energy = data["energy"]
        b.scraps = data["scraps"]
        b.abilities = data["abilities"]
        b.algae_held = data["algae_held"]
        b.traversal_cost = data["traversal_cost"]
        b.status = data["status"]
        b.vision_radius = data["vision_radius"]
        return b
