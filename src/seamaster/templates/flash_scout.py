from seamaster.api.game_api import GameAPI
from seamaster.botbase import BotController
from seamaster.translate import move, move_speed
from seamaster.constants import Direction, Ability


class FlashScout(BotController):
    """
    A fast scout bot that rushes to algae to identify them.
    Does NOT harvest.
    Automatically recharges when energy is low.
    Dies if it reaches poisonous algae.
    """

    ABILITIES = [Ability.SCOUT, Ability.SPEED_BOOST]

    ENERGY_THRESHOLD = 10

    def __init__(self, ctx):
        super().__init__(ctx)
        self.status = "active"
        self.target_pad_id = None

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.get_location()

        if self.status == "charging":
            pads = ctx.api.energypads()
            pad = next((p for p in pads if p.id == self.target_pad_id), None)

            if pad:
                if pad.ticksleft == 0:
                    self.status = "active"
                    self.target_pad_id = None
                    return None

                if bot_pos == pad.location:
                    return None

                d, steps = ctx.move_target_speed(bot_pos, pad.location)
                if d:
                    return move_speed(d, steps)
                return None

        if ctx.get_energy() < self.ENERGY_THRESHOLD:
            pad = ctx.get_nearest_energy_pad()
            self.status = "charging"
            self.target_pad_id = pad.id
            return None

        visible = ctx.sense_algae()
        if visible:
            d, steps = ctx.move_target_speed(bot_pos, visible[0].location)
            if d:
                return move_speed(d, steps)

        for radius in range(2, 11):
            visible = ctx.sense_algae(radius=radius)
            if visible:
                d, steps = ctx.move_target_speed(bot_pos, visible[0].location)
                if d:
                    return move_speed(d, steps)

        return move(Direction.NORTH)

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)
