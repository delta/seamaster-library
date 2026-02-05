from oceanmaster.botbase import BotController
from oceanmaster.translate import move, self_destruct
from oceanmaster.constants import Ability, Direction
from oceanmaster.api import GameAPI


class Saboteur(BotController):
    """
    looks for enemies and self destructs
    """
    
    ABILITIES = [Ability.SELF_DESTRUCT]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.target = None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        close = ctx.sense_enemies_in_radius(loc, radius=1)
        if close:
            return self_destruct()

        if self.target is None:
            for r in range(2, 11):
                enemies = ctx.sense_enemies_in_radius(loc, radius=r)
                if enemies:
                    self.target = enemies[0].location
                    break
                
        if self.target:
            d = ctx.move_target(loc, self.target)
            if d:
                return move(d)
            self.target = None

        return move(Direction.NORTH)

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)