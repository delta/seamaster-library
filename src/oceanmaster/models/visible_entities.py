"""
Initialization of VisibleEntities model.
"""

from typing import List
from oceanmaster.models.bot import Bot
from oceanmaster.models.visible_scrap import VisibleScrap

class VisibleEntities:
    """
    Represents entities visible to the player.
    """
    enemies: List[Bot]
    scraps: List[VisibleScrap]
