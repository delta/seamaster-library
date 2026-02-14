from abc import ABC, abstractmethod
from seamaster.constants import Ability
from seamaster.models.action import Action


class BotController(ABC):
    """
    Base class for all bot strategies.
    """

    ABILITIES: list[Ability]

    def __init__(self, ctx, args: dict | None = None):
        self.ctx = ctx
        self.args = args or {}

    @abstractmethod
    def act(self) -> Action | None:
        pass

    @classmethod
    def spawn(cls, location: int = 0, args: dict | None = None) -> dict:
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
            "abilities": cls.ABILITIES or [],
            "location": location,
            "args": args,
        }
