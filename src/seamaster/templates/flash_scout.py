from seamaster.api.game_api import GameAPI
from seamaster.botbase import BotController
from seamaster.translate import move, move_speed
from seamaster.constants import Direction, Ability, AlgaeType



class FlashScout(BotController):
    """
    A fast scout bot that rushes to algae to identify them.
    Does NOT harvest.
    Automatically recharges when energy is low.
    Dies if it reaches poisonous algae.
    """

    ABILITIES = [Ability.SCOUT, Ability.SPEED_BOOST, Ability.SELF_DESTRUCT]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.status = "active"
        self.target_pad_id = None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        unknown = ctx.sense_unknown_algae(loc)

        if unknown:
            d, algae = unknown[0]
            direction, steps = ctx.move_target_speed(loc, algae.location)
            if direction:
                return move_speed(direction, steps)

        return move(Direction.NORTH)



    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)
