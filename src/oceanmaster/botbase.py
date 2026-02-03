from abc import ABC, abstractmethod
from oceanmaster.constants import Ability
from oceanmaster.models.point import Point
from oceanmaster.models.action import Action

class BotController(ABC):
    """
    Base class for all bot strategies.
    """

    ABILITIES: list[Ability] = []

    def __init__(self, ctx):
        self.ctx = ctx

    @abstractmethod
    def act(self) ->Action | None:
        pass

    @classmethod
    def spawn(cls, location: int = 0) -> dict:
        """
        User-facing spawn helper.

        Args:
            abilities (list[str] | None): Extra abilities to stack.
            location (int): Spawn location index.
            target (Point | None): Target point for certain strategies.

        Returns:
            dict: Spawn specification for wrapper.
        """
        return {
            "strategy": cls,
            "extra_abilities": cls.ABILITIES or [],                
            "location": location,
        }
