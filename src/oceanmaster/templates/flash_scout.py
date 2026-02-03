import sys
from oceanmaster.api.game_api import GameAPI
from oceanmaster.botbase import BotController
from oceanmaster.translate import move, move_speed
from oceanmaster.constants import Direction, Ability


class FlashScout(BotController):
    """
    A scout bot that moves quickly towards algae to find out its type. It doesn't harvest algae, just scouts them out. It dies upon reaching a poisonous algae.
    """

    ABILITIES = [Ability.SCOUT, Ability.SPEED_BOOST]

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.get_location()

        # sense algae like forager (no harvest)
        visible = ctx.sense_algae()
        if visible:
            d, steps = ctx.move_target_speed(bot_pos, visible[0].location)
            if d:
                return move_speed(d, steps)

        radius = 2
        while radius <= 10:
            visible = ctx.sense_algae(radius=radius)
            if visible:
                d, steps = ctx.move_target_speed(bot_pos, visible[0].location)
                if d:
                    return move_speed(d, steps)
            radius += 1
        return move(Direction.NORTH)

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)
