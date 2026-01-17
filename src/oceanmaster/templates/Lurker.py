from oceanmaster.botbase import BotController
from oceanmaster.Translate import *
from oceanmaster.Constants import Direction

class Lurker(BotController):
    TEMPLATE="Lurker"
    
    def act(self):
        ctx = self.ctx
        enemies = ctx.senseEnemyNearby()
        if enemies:
            e = enemies[0]
            # return attack(ctx.getID(), e.location.x, e.location.y)
        return move(ctx.getID(), Direction.SOUTH)

