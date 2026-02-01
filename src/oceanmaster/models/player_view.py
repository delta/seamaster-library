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
    
    @classmethod
    def from_dict(cls, data: dict):
        view = cls()
        view.tick = data["tick"]
        view.scraps = data["scraps"]
        view.algae = data["algae"]
        view.bot_count = data["bot_count"]
        view.max_bots = data["max_bots"]
        view.width = data["width"]
        view.height = data["height"]

        # decode bots, visible_entities, permanent_entities
        # (use exactly the constructors you already wrote)

        return view
