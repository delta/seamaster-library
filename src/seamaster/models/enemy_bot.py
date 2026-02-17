"""
Initialization of EnemyBot model.
"""

from typing import List
from seamaster.models.point import Point
from seamaster.constants import Ability


class EnemyBot:
    """
    Represents an enemy bot in the game.
    """

    id: int
    location: Point
    # energy: float
    scraps: int
    abilities: List[Ability]
    # algae_held: int
    # traversal_cost: float
    # status: str
    # vision_radius: float

    @classmethod
    def from_dict(cls, data: dict):
        b = cls()
        b.id = data["id"]
        b.location = Point(**data["location"])
        b.scraps = data["scraps"]
        b.abilities = data["abilities"]
        return b
