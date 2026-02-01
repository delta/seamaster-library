from abc import ABC, abstractmethod
from oceanmaster.models.point import Point

class BotController(ABC):
    """
    Base class for all bot strategies.
    """

    DEFAULT_ABILITIES: list[str] = []

    def __init__(self, ctx):
        self.ctx = ctx

    @abstractmethod
    def act(self):
        pass

    @classmethod
    def spawn(cls, abilities: list[str] | None = None, location: int = 0, target: Point = None) -> dict:
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
            "extra_abilities": abilities or [],
            "location": location,
            "target": target,
        }
