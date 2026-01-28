from oceanmaster.models.bot import Bot
from oceanmaster.models.visible_entities import VisibleEntities
from oceanmaster.models.permanent_entities import PermanentEntities
from typing import List


class PlayerView:
    tick: int
    scraps: int
    algae: int
    bot_count: int
    max_bots: int
    width: int
    height: int
    bots: List[Bot]
    visible_entities: VisibleEntities
    permanent_entities: PermanentEntities
