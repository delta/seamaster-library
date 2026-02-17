from seamaster.botbase import BotController
from seamaster.translate import move, lockpick
from seamaster.constants import Direction, Ability
from seamaster.api import GameAPI
from seamaster.utils import manhattan_distance


class Lurker(BotController):
    """
    Lurker is an offensive disruption bot that targets enemy banks
    which are currently undergoing a deposit operation.

    Interaction model:
    - Lockpicking can only be performed when the bot is at a Manhattan
      distance of exactly 1 from the target bank.
    - After issuing a lockpick action, the engine resolves the interaction
      and moves the bot onto the bank tile in the next tick.

    High-level behavior:
    - Searches for the nearest depositing enemy bank.
    - Moves toward the bank and repeatedly lockpicks it.
    - If energy is low, temporarily retreats to recharge at an energy pad.
    """

    ABILITIES = [Ability.LOCKPICK]

    ENERGY_THRESHOLD = 10

    def __init__(self, ctx):
        """
        Initializes the Lurker bot.

        State variables:
        - target_bank:
            Location of the bank currently being targeted for lockpicking
        - lockpick_ticks:
            Number of consecutive ticks spent lockpicking the same bank
        - status:
            * "active"   → normal hunting / lockpicking behavior
            * "charging" → recharging energy at an energy pad
        - target_pad_id:
            ID of the energy pad currently being targeted
        """
        super().__init__(ctx)
        self.target_bank = None
        self.lockpick_ticks = 0
        self.status = "active"
        self.target_pad_id = None

    def act(self):
        """
        Main decision loop executed every tick.

        Priority order:
        1. Resolve charging behavior if currently recharging
        2. Initiate charging if energy falls below threshold
        3. Acquire a depositing bank as a target if none is set
        4. Lockpick the target bank when within interaction range
        5. Move toward the target bank otherwise
        """
        ctx = self.ctx
        bot_pos = ctx.get_location()

        if self.status == "charging":
            pads = ctx.api.energypads()
            pad = next((p for p in pads if p.id == self.target_pad_id), None)

            if pad is None or pad.ticksleft == 0:
                self.status = "active"
                self.target_pad_id = None
                return None

            if manhattan_distance(bot_pos, pad.location) == 1:
                return None

            d = ctx.move_target(bot_pos, pad.location)
            if d:
                return move(d)
            return None

        if ctx.get_energy() < self.ENERGY_THRESHOLD:
            pad = ctx.get_nearest_energy_pad()
            self.status = "charging"
            self.target_pad_id = pad.id
            self.lockpick_ticks = 0
            return None

        if self.target_bank is None:
            banks = ctx.get_depositing_banks_sorted()
            if not banks:
                for d in (
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.WEST,
                    Direction.SOUTH,
                ):
                    if not ctx.check_blocked_direction(d):
                        return move(d)
                return None

            self.target_bank = banks[0].location
            self.lockpick_ticks = 0

        if manhattan_distance(bot_pos, self.target_bank) == 1:
            self.lockpick_ticks += 1
            if self.lockpick_ticks >= 20:
                self.target_bank = None
                self.lockpick_ticks = 0
                return None
            return lockpick(self.target_bank)

        d = ctx.move_target(bot_pos, self.target_bank)
        if d:
            return move(d)
        return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        """
        Determines whether the Lurker can be spawned given current resources.

        Returns:
            bool: True if sufficient scraps are available to spawn the bot
        """
        return api.can_spawn(cls.ABILITIES)
