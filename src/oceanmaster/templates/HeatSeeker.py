from oceanmaster.botbase import BotController
from oceanmaster.Translate import *
from oceanmaster.Constants import Ability

class HeatSeeker(BotController):
    """
    A bot that accepts a block as target and self-destructs at that location.
    """
    DEFAULT_ABILITIES=[
        Ability.SELF_DESTRUCT.value
    ]
    def __init__(self, ctx, target):
        super().__init__(ctx)
        self.target = target
    def act(self):
        ctx = self.ctx
        bot_pos = ctx.getLocation()

        if bot_pos.x == self.target.x and bot_pos.y == self.target.y:
            return self_destruct()

        d = ctx.moveTarget(bot_pos, self.target)
        if d:
            return move(d)
        
        return None
