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

        for radius in range(3, 20):
            visible = ctx.sense_algae_in_radius(loc,radius=radius)
            unknown = [a for a in visible if a.is_poison == AlgaeType.UNKNOWN.value]

            if unknown:
                d, steps = ctx.move_target_speed(loc, unknown[0].location)
                if d:
                    print(f"Moving to unknown algae at {unknown[0].location}")
                    print(f"Direction {d}")
                    return move_speed(d, steps)

        return move(Direction.NORTH)



    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)
