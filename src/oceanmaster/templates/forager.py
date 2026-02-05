from oceanmaster.botbase import BotController
from oceanmaster.translate import harvest, move
from oceanmaster.constants import Ability
from oceanmaster.utils import direction_from_point


class Forager(BotController):
    """
    Looks for algae/scrap, harvests them.
    If energy is low → goes to an energy pad and waits.
    If algae held is high → goes to a bank and waits until deposit completes.
    """

    ABILITIES = [Ability.HARVEST, Ability.SCOUT, Ability.DEPOSIT]

    def __init__(self, ctx, args=None):
        super().__init__(ctx, args)
        self.status = "active"          # active | charging | depositing
        self.target_pad_id = None
        self.target_bank_id = None

    def act(self):
        ctx = self.ctx
        loc = ctx.get_location()

        if self.status == "charging":
            pads = ctx.api.energypads()
            pad = next((p for p in pads if p.id == self.target_pad_id), None)

            # pad gone or charging finished
            if pad is None or pad.ticksleft == 0:
                self.status = "active"
                self.target_pad_id = None
                return None

            # on pad → WAIT
            if loc == pad.location:
                return None

            # move toward pad
            d = ctx.move_target(loc, pad.location)
            if d:
                return move(d)
            return None

        if self.status == "depositing":
            banks = ctx.api.banks()
            bank = next((b for b in banks if b.id == self.target_bank_id), None)

            if bank is None or bank.deposit_ticks_left == 0:
                self.status = "active"
                self.target_bank_id = None
                return None

            if loc == bank.location:
                return None

            d = ctx.move_target(loc, bank.location)
            if d:
                return move(d)
            return None

        if ctx.get_energy() < 10:
            pad = ctx.get_nearest_energy_pad()
            self.status = "charging"
            self.target_pad_id = pad.id
            return None

        if ctx.get_algae_held() >= 5:
            bank = ctx.get_nearest_bank()
            self.status = "depositing"
            self.target_bank_id = bank.id
            return None

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
