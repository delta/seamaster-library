from seamaster.botbase import BotController
from seamaster.translate import move, lockpick
from seamaster.constants import Ability, BotStatus, lock_pick_ticks
from seamaster.api import GameAPI
from seamaster.models.point import Point
from seamaster.utils import (
    get_direction_in_one_radius,
    get_shortest_distance_between_points,
    manhattan_distance,
)


class Lurker(BotController):
    """
    Bot controller responsible for attempting to lockpick opponent banks.

    The Lurker targets opponent banks where a deposit is currently occurring
    and tries to lockpick them if sufficient deposit time remains. The bot
    moves to a position adjacent to the target bank and initiates a lockpick
    when possible.

    Attributes:
    status : BotStatus
        Current state of the bot (ACTIVE or LOCKPICKING).

    target_pad_id : int | None
        Placeholder for energy pad target (unused in this implementation).

    target_bank_id : int | None
        ID of the bank currently targeted for lockpicking.

    ABILITIES : list[Ability]
        Abilities required to spawn this bot (LOCKPICK).

    Inherits:
    BotController
        Base controller class providing context and movement utilities.
    """

    ABILITIES = [Ability.LOCKPICK]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.status = BotStatus.ACTIVE
        self.target_pad_id = None
        self.target_bank_id = None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()
        # first check if lockpicking
        if self.status == BotStatus.LOCKPICKING:
            bank = next(
                (b for b in ctx.api.banks() if b.id == self.target_bank_id), None
            )
            if bank:
                if bank.lockpick_ticks_left == 0:
                    self.status = BotStatus.ACTIVE
                    self.target_bank = None
                    return None
                # else dont move
                return None
        # if not lockpicking, either set a target or move towards the target bank to lockpick
        if self.target_bank_id is None:
            # set a target bank to lockpick
            banks = ctx.get_opponent_banks()
            if banks:
                for bank in banks:
                    # skip if no of deposit ticks left is less that 20
                    if bank.deposit_ticks_left < lock_pick_ticks:
                        continue

                    # skip if one of my bots is already lockpicking it
                    if (
                        bank.lockpick_occuring
                        and bank.lockpick_botid in ctx.get_my_bot_ids()
                    ):
                        continue
                    self.target_bank_id = bank.id
                    break
        else:
            # move towards target bank and lockpick if adjacent
            bank = next(
                (b for b in ctx.api.banks() if b.id == self.target_bank_id), None
            )
            if bank:
                if manhattan_distance(loc, bank.location) == 1:
                    if (
                        bank.deposit_occuring
                        and bank.deposit_ticks_left >= lock_pick_ticks
                    ):
                        self.status = BotStatus.LOCKPICKING
                        return lockpick(get_direction_in_one_radius(loc, bank.location))
                    else:
                        self.target_bank_id = None
                        return None
                else:
                    dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
                    s_dist = 1_000_000
                    s_dir = None
                    for d in dirs:
                        adj = Point(bank.location.x + d[0], bank.location.y + d[1])
                        dist = get_shortest_distance_between_points(loc, adj)
                        if dist < s_dist:
                            s_dist = dist
                            s_dir = ctx.move_target(loc, adj)
                    if s_dir:
                        return move(s_dir)
                    return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        """
        Determines whether the Lurker can be spawned given current resources.

        Returns:
            bool: True if sufficient scraps are available to spawn the bot
        """
        return api.can_spawn(cls.ABILITIES)


# to commit
