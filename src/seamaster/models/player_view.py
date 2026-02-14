from seamaster.models.bot import Bot
from seamaster.models.visible_entities import VisibleEntities
from seamaster.models.permanent_entities import PermanentEntities


class PlayerView:
    tick: int
    scraps: int
    algae: int
    bot_id_seed: int
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
        view.scraps = data["scraps"]
        view.algae = data["algae"]
        view.bot_id_seed = data["bot_id_seed"]
        view.max_bots = data["max_bots"]
        view.width = data["width"]
        view.height = data["height"]

        view.bots = {int(k): Bot.from_dict(v) for k, v in data["bots"].items()}

        view.visible_entities = VisibleEntities.from_dict(data["visible_entities"])

        view.permanent_entities = PermanentEntities.from_dict(
            data["permanent_entities"]
        )

        return view
