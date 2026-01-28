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
    energy: int
    scraps: int
    abilities: List[Ability]
    algae_held: int
