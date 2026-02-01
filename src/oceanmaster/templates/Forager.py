from oceanmaster.botbase import BotController
from oceanmaster.translate import harvest, move
from oceanmaster.constants import Ability
from oceanmaster.utils import direction_from_point


class Forager(BotController):
    DEFAULT_ABILITIES = [Ability.HARVEST.value, Ability.SCOUT.value]

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        if ctx.get_algae_held() >= 5:
            bank = ctx.get_nearest_bank()
            d = ctx.move_target(loc, bank.location)
            if d:
                return move(d)

        visible = ctx.sense_algae() + ctx.sense_scraps_in_radius()
        if visible:
            d = direction_from_point(loc, visible[0].location)
            return harvest(d)
        
        for r in range(2, 11):
            visible = (
                ctx.sense_algae(radius=r)
                + ctx.sense_scraps_in_radius(radius=r)
            )
            if visible:
                d = ctx.move_target(loc, visible[0].location)
                if d:
                    return move(d)

        return None
