from seamaster.botbase import BotController
from seamaster.translate import harvest, move, deposit
from seamaster.constants import Ability, AlgaeType
from seamaster.utils import direction_from_point, manhattan_distance
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

    ABILITIES = [Ability.HARVEST, Ability.SCOUT, Ability.DEPOSIT]

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
        self.status = "active"
        self.target_pad_id = None
        self.target_bank_id = None

    def act(self):
        """
        Main decision loop executed every tick.

        Priority order:
        1. Resolve charging or depositing states if already active
        2. Check for low energy and initiate charging if needed
        3. Check algae capacity and initiate depositing if needed
        4. Harvest nearby algae or scraps if within interaction range
        5. Move toward the nearest visible resource
        """
        ctx = self.ctx
        loc = ctx.get_location()
        print(f"my status is {self.status}")
        if self.target_bank_id:
            print(f"target bank id is {self.target_bank_id}")
            
        if self.status == "charging":
            pads = ctx.api.energypads()
            pad = next((p for p in pads if p.id == self.target_pad_id), None)

            if pad is None or pad.ticksleft == 0:
                self.status = "active"
                self.target_pad_id = None
                return None

            if manhattan_distance(loc, pad.location) == 1:
                return None

            d = ctx.move_target(loc, pad.location)
            if d:
                return move(d)
            return None

        if self.status == "depositing":
            banks = ctx.api.banks()
            bank = next((b for b in banks if b.id == self.target_bank_id))

            dist = manhattan_distance(loc, bank.location)

            if dist > 1:
                d = ctx.move_target(loc, bank.location)
                if d:
                    return move(d)

            if not bank.deposit_occuring:
                print("giving deposit instruction")
                return deposit(None)

            if bank.deposit_occuring:
                return None

            if ctx.get_algae_held() == 0:
                self.status = "active"
                self.target_bank_id = None
                return None


        if ctx.get_energy() < 5:
            pad = ctx.get_nearest_energy_pad()
            self.status = "charging"
            self.target_pad_id = pad.id
            return None

        if ctx.get_algae_held() >= 5:
            bank = ctx.get_nearest_bank()
            self.status = "depositing"
            self.target_bank_id = bank.id
            return None

        visible = ctx.sense_algae_in_radius(loc)
        if visible and visible[0].is_poison==AlgaeType.FALSE.value:
            return harvest(None)
            
        visible = ctx.sense_algae_in_radius(loc,1)
        if visible:
            for a in visible:
                if a.is_poison ==AlgaeType.FALSE.value:
                    target = a.location
                    d = direction_from_point(loc, target)
                    return harvest(d)

        for r in range(2, 11):
            visible = ctx.sense_algae_in_radius(loc, radius=r)
            non_poisonous = [a for a in visible if a.is_poison==AlgaeType.FALSE.value]
            if non_poisonous:
                target = non_poisonous[0].location
                d = ctx.move_target(loc, target)
                if d:
                    return move(d)
                return None

        return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        """
        Determines whether the Forager can be spawned given current resources.

        Returns:
            bool: True if sufficient scraps are available to spawn the bot
        """
        return api.can_spawn(cls.ABILITIES)
