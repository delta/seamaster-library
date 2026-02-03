"""
Initialization of VisibleEntities model.
"""

from typing import List
from oceanmaster.models.bot import Bot
from oceanmaster.models.scrap import Scrap
from oceanmaster.models.algae import Algae


class VisibleEntities:
    """
    Represents entities visible to the player.
    """

    enemies: List[Bot]
    scraps: List[Scrap]
    algae: List[Algae]
    
    @classmethod
    def from_dict(cls, data: dict):
        v = cls()
        v.enemies = [Bot.from_dict(bot) for bot in data["enemies"]]
        v.scraps = [Scrap.from_dict(scrap) for scrap in data["scraps"]]
        v.algae = [Algae.from_dict(algae) for algae in data["algae"]]
        return v