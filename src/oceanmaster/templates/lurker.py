from oceanmaster.botbase import BotController
from oceanmaster.translate import move, lockpick
from oceanmaster.constants import Direction, Ability
from oceanmaster.api import GameAPI


class Lurker(BotController):
    """
    A Lurker bot targets depositing banks and lockpicks them.
    """

    ABILITIES = [Ability.LOCKPICK]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.target_bank = None
        self.lockpick_ticks = 0

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.get_location()

        # ==================== ACQUIRE TARGET ====================
        if self.target_bank is None:
            banks = ctx.get_depositing_banks_sorted()
            if not banks:
                if not ctx.check_blocked_direction(Direction.NORTH):
                    return move(Direction.NORTH)

                if not ctx.check_blocked_direction(Direction.EAST):
                    return move(Direction.EAST)

                if not ctx.check_blocked_direction(Direction.WEST):
                    return move(Direction.WEST)

                if not ctx.check_blocked_direction(Direction.SOUTH):
                    return move(Direction.SOUTH)

            self.target_bank = banks[0].location
            self.lockpick_ticks = 0

        # ==================== AT BANK, LOCKPICK ====================
        if bot_pos.x == self.target_bank.x and bot_pos.y == self.target_bank.y:
            self.lockpick_ticks += 1

            if self.lockpick_ticks >= 20:
                self.target_bank = None
                self.lockpick_ticks = 0
                return None

            return lockpick(self.target_bank)

        # ==================== MOVE TOWARDS BANK ====================
        direction = ctx.move_target(bot_pos, self.target_bank)
        if direction:
            return move(direction) 
        return None
    
    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        return api.can_spawn(cls.ABILITIES)