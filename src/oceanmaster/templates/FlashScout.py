from oceanmaster.botbase import BotController
from oceanmaster.translate import move, move_speed
from oceanmaster.constants import Direction, Ability


class FlashScout(BotController):
    """
    A scout bot that moves quickly towards algae to find out its type. It doesn't harvest algae, just scouts them out. It dies upon reaching a poisonous algae.
    """

    DEFAULT_ABILITIES = [Ability.SCOUT.value, Ability.SPEED.value]

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.getLocation()

        # sense algae like forager (no harvest)
        visible = ctx.senseAlgae()
        if visible:
            d, steps = ctx.moveTargetSpeed(bot_pos, visible[0].location)
            if d:
                return move_speed(d, steps)

        radius = 2
        while radius <= 10:
            visible = ctx.senseAlgae(radius=radius)
            if visible:
                d, steps = ctx.moveTargetSpeed(bot_pos, visible[0].location)
                if d:
                    return move_speed(d, steps)
            radius += 1

        return move(Direction.NORTH)
