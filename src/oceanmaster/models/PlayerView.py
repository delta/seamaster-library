from oceanmaster.models.Bot import Bot
from oceanmaster.models.VisibleEntities import VisibleEntities
from oceanmaster.models.PermanentEntities import PermanentEntities
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
