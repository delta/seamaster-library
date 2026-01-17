from oceanmaster.botbase import BotController
from oceanmaster.Translate import *
from oceanmaster.Constants import Direction, Ability
from oceanmaster.Utils import direction_from_point

class Forager(BotController):
    """
    A bot that forages for algae and scrap. It harvests resources until it holds 5 units, then returns to the nearest bank to deposit them. It prioritizes nearby resources and moves towards them. If no resources are visible, it expands its search radius.
    """
    DEFAULT_ABILITIES = [
        Ability.HARVEST.value,
        Ability.SCOUT.value
    ]
    def act(self):
        ctx = self.ctx
        
        if(ctx.getAlgaeHeld()>=5):
            pos = ctx.getNearestBank()
            dir = ctx.moveTarget(ctx.getLocation(),pos)
            return move(dir)
        
        visible = ctx.senseAlgae()+ctx.senseSacraps()
        if visible:
            dir=direction_from_point(ctx.getLocation(),visible[0].location)
            return harvest(dir);
        i=2;
        while(i<=10):
            visible = ctx.senseAlgae(radius=i)+ctx.senseSacraps(radius=i)
            if visible:
                dir=ctx.moveTarget(ctx.getLocation(),visible[0].location)
                return move(dir)
            i+=1
                
        
        