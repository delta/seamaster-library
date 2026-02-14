"""
Initialization of VisibleEntities model.
"""

from typing import List
from seamaster.models.enemy_bot import EnemyBot
from seamaster.models.scrap import Scrap
from seamaster.models.algae import Algae


class VisibleEntities:
    """
    Represents entities visible to the player.
    """

    enemies: List[EnemyBot]
    scraps: List[Scrap]
    algae: List[Algae]

    @classmethod
    def from_dict(cls, data: dict):
        v = cls()
        # TODO: THIS ISN'T AN ACTUAL BOT DICT, it
        v.enemies = [EnemyBot.from_dict(bot) for bot in data["enemies"]]
        # v.scraps = [Scrap.from_dict(scrap) for scrap in data["scraps"]]
        v.scraps = []
        v.algae = [Algae.from_dict(algae) for algae in data["algae"]]
        return v
