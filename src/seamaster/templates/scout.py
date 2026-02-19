from seamaster.api.game_api import GameAPI
from seamaster.botbase import BotController
from seamaster.translate import move
from seamaster.constants import Ability


class Scout(BotController):
    """
    A fast scout bot that rushes to algae to identify them.
    Does NOT harvest.
    Automatically recharges when energy is low.
    Dies if it reaches poisonous algae.
    """

    ABILITIES = [Ability.SCOUT, Ability.SELF_DESTRUCT]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.status = "active"

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        print("hello from forager")

        unknown = ctx.sense_unknown_algae(loc)

        if unknown:
            d, algae = unknown[0]
            direction = ctx.move_target(loc, algae.location)
            if direction:
                return move(direction)

        return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)
