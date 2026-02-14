from seamaster.botbase import BotController
from seamaster.translate import move, self_destruct
from seamaster.constants import Ability, Direction
from seamaster.api import GameAPI
from seamaster.utils import manhattan_distance


class Saboteur(BotController):
    """
    Saboteur is an aggressive combat bot designed to eliminate enemy bots
    via self-destruction.

    Interaction model:
    - Self-destruction is triggered when an enemy bot is within a Manhattan
      distance of 1.
    - Energy pad interaction is only possible when the Saboteur is at a
      Manhattan distance of exactly 1 from the pad.
    - After an interaction action, the engine resolves the interaction and
      moves the bot onto the object tile in the next tick.

    High-level behavior:
    - Actively searches for nearby enemies.
    - Moves toward the closest detected enemy.
    - Self-destructs immediately when an enemy is within blast radius.
    - Retreats to recharge if energy drops below a threshold.
    """

    ABILITIES = [Ability.SELF_DESTRUCT]

    ENERGY_THRESHOLD = 10

    def __init__(self, ctx):
        """
        Initializes the Saboteur bot.

        State variables:
        - target:
            Location of the enemy bot currently being pursued
        - status:
            * "active"   → enemy hunting and pursuit
            * "charging" → recharging energy at an energy pad
        - target_pad_id:
            ID of the energy pad currently being targeted for recharge
        """
        super().__init__(ctx)
        self.target = None
        self.status = "active"
        self.target_pad_id = None

    def act(self):
        """
        Main decision loop executed every tick.

        Priority order:
        1. Resolve charging behavior if currently recharging
        2. Initiate charging if energy falls below threshold
        3. Self-destruct if an enemy is within blast radius
        4. Acquire and pursue the nearest enemy
        5. Default movement if no enemy is found
        """
        ctx = self.ctx
        loc = ctx.get_location()

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

        if ctx.get_energy() < self.ENERGY_THRESHOLD:
            pad = ctx.get_nearest_energy_pad()
            self.status = "charging"
            self.target_pad_id = pad.id
            self.target = None
            return None

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
        """
        Determines whether the Saboteur can be spawned given current resources.

        Returns:
            bool: True if sufficient scraps are available to spawn the bot
        """
        return api.can_spawn(cls.ABILITIES)
