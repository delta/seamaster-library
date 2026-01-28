"""
Represents an algae entity in the game.
"""

from oceanmaster.constants import AlgaeType
from .point import Point

class Algae:
    """
    Represents an algae entity in the game.
    """
    location: Point
    is_poison: AlgaeType
