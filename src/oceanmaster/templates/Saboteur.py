from oceanmaster.botbase import BotController
from oceanmaster.Translate import *
from oceanmaster.Constants import Ability, Direction

class Saboteur(BotController):
    """"
    A bot that seeks out enemy bots and self-destructs near them to destroy them. It remembers its target enemy bot's location until it reaches it or the target is no longer visible."""
    DEFAULT_ABILITIES = [
        Ability.SELF_DESTRUCT.value
    ]
    def __init__(self, ctx):
        super().__init__(ctx)
        self.target = None   # persistent memory

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.getLocation()

        close_enemies = ctx.senseEnemyinRadius(bot_pos, radius=1)
        if close_enemies:
            return self_destruct()

        if self.target is None:
            radius = 2
            while radius <= 10:
                enemies = ctx.senseEnemyinRadius(bot_pos, radius)
                if enemies:
                    self.target = enemies[0].location
                    break
                radius += 1

        if self.target:
            d = ctx.moveTarget(bot_pos, self.target)
            if d:
                return move( d)
            else:
                self.target = None
                
        return move(Direction.NORTH)
