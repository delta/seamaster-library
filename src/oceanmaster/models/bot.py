"""
Initialization of Bot model.
"""

from typing import List
from oceanmaster.models.point import Point
from oceanmaster.constants import Ability


class Bot:
    """
    Represents a bot in the game.
    """

    id: int
    owner_id: int
    location: Point
    energy: float
    scraps: int
    abilities: List[Ability]
    algae_held: int
    
    @classmethod
    def from_dict(cls, data: dict) :
        b = cls()
        b.id = data['id']
        b.owner_id = data['owner_id']
        b.location = Point(**data['location'])
        b.energy = data['energy']
        b.scraps = data['scraps']
        b.abilities = data['abilities']
        b.algae_held = data['algae_held']
        return b
