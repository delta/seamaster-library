from seamaster.botbase import BotController
from seamaster.translate import deposit, harvest, move
from seamaster.constants import Ability, BotStatus
from seamaster.utils import get_direction_in_one_radius, manhattan_distance
from seamaster.api import GameAPI


class Forager(BotController):
    """
    Forager is an economy-focused bot responsible for gathering algae and scraps.

    Interaction model:
    - The bot can only interact with objects (algae, banks, energy pads)
    when it is at a Manhattan distance of exactly 1.
    - After an interaction action is issued, the engine resolves the interaction
    and moves the bot onto the object tile in the following tick.

    High-level behavior:
    - Actively searches for algae and scraps and harvests them.
    - If carried algae exceeds a threshold, it moves near a bank and deposits.
    - If energy drops below a threshold, it moves near an energy pad and recharges.
    """

    ABILITIES = [Ability.HARVEST, Ability.DEPOSIT]

    def __init__(self, ctx, args=None):
        """
        Initializes the Forager bot.

        State variables:
        - status:
            * "active"     → normal harvesting behavior
            * "charging"   → moving to / waiting near an energy pad
            * "depositing" → moving to / waiting near a bank
        - target_pad_id:
            ID of the energy pad currently being targeted
        - target_bank_id:
            ID of the bank currently being targeted
        """
        super().__init__(ctx, args)
        self.status = BotStatus.ACTIVE
        self.target_pad_id = None
        self.target_bank_id = None
        self.energy_threshold = 20
        self.algae_threshold = 5

    def act(self):
        """
        Main decision loop executed every tick.

        Priority order:
        1. Resolve charging or depositing states if already active
        2. Check for low energy and initiate charging if needed
        3. Check algae capacity and initiate depositing if needed
        4. Harvest nearby algae or scraps if within interaction range
        5. Move toward the nearest unknown resource
        """
        ctx = self.ctx
        loc = ctx.get_location()

        if self.status == BotStatus.CHARGING:
            if ctx.get_energy() > self.energy_threshold:
                self.status = BotStatus.ACTIVE
                self.target_pad_id = None
                return None

            pads = ctx.api.energypads()
            pad = next((p for p in pads if p.id == self.target_pad_id), None)

            if pad:
                if manhattan_distance(loc, pad.location) == 0:
                    return None
            if pad:
                d = ctx.move_target(loc, pad.location)
                if d:
                    return move(d)
            return None

        if self.status == BotStatus.DEPOSITING:
            if ctx.get_algae_held() == 0:
                self.status = BotStatus.ACTIVE
                self.target_bank_id = None
                return None

            banks = ctx.api.banks()
            bank = next((b for b in banks if b.id == self.target_bank_id), None)

            if bank:
                # dist = manhattan_distance(loc, bank.location)
                dist, trg = ctx.min_adjacent_distance_bank(bank, loc)
                if dist > 1 and trg is not None:
                    d = ctx.move_target(loc, trg)
                    if d:
                        return move(d)
                else:
                    return deposit(None)
                    # pass

        if ctx.get_energy() <= self.energy_threshold:
            pad = ctx.get_nearest_energy_pad()
            self.status = BotStatus.CHARGING
            self.target_pad_id = pad.id
            return None

        if ctx.get_algae_held() >= self.algae_threshold:
            bank = ctx.get_my_banks(loc)
            self.status = BotStatus.DEPOSITING
            if bank:
                self.target_bank_id = bank[0].id
            return None

        non_poisonous = ctx.sense_non_poisionous_algae(loc)

        if non_poisonous:
            if manhattan_distance(non_poisonous[0][1].location, loc) == 0:
                return harvest(None)

        if non_poisonous:
            if manhattan_distance(non_poisonous[0][1].location, loc) == 1:
                direction = get_direction_in_one_radius(
                    loc, non_poisonous[0][1].location
                )
                return harvest(direction)

        if non_poisonous:
            d = ctx.move_target(loc, non_poisonous[0][1].location)
            if d:
                return move(d)
        return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        """
        Determines whether the Forager can be spawned given current resources.

        Returns:
            bool: True if sufficient scraps are available to spawn the bot
        """
        return api.can_spawn(cls.ABILITIES)
