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
    bots: dict[int, Bot]
    visible_entities: VisibleEntities
    permanent_entities: PermanentEntities
    
    @classmethod
    def from_dict(cls, data: dict):
        view = cls()
        view.tick = data["tick"]
        view.scraps = data["scraps"][0]
        view.algae = data["algae_count"][0]
        view.bot_count = data["bot_count"]
        view.max_bots = data["max_bots"]
        view.width = data["width"]
        view.height = data["height"]

        view.bots = {
            int(k): Bot.from_dict(v)
            for k, v in data["bots"].items()
        }

        view.visible_entities = VisibleEntities.from_dict(
            data["visible_entities"]
        )

        view.permanent_entities = PermanentEntities.from_dict(
            data["permanent_entities"]
        )

        return view
