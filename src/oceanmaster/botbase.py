from abc import ABC, abstractmethod

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
    def spawn(cls, abilities: list[str] | None = None, location: int = 0):
        """
        User-facing spawn helper.

        Args:
            abilities (list[str] | None): Extra abilities to stack.
            location (int): Spawn location index.

        Returns:
            dict: Spawn specification for wrapper.
        """
        return {
            "strategy": cls,
            "extra_abilities": abilities or [],
            "location": location,
        }
