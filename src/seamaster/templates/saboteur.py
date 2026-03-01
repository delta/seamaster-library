from seamaster.botbase import BotController
from seamaster.translate import move, self_destruct
from seamaster.constants import Ability, Direction
from seamaster.api import GameAPI
from seamaster.utils import manhattan_distance, get_direction_in_one_radius


class Saboteur(BotController):
    """
    The Saboteur scans for the closest enemy and moves towards them.
    Once it reaches an adjacent tile with an enemy bot(Manhattan distance <= 1), 
    it triggers its SELF_DESTRUCT ability to deal damage.
    """


    ABILITIES = [Ability.SELF_DESTRUCT]

    def __init__(self, ctx):
        try:
            super().__init__(ctx)
        except Exception as e:
            print(f"Error initializing Saboteur: {e}")

    def act(self):
        try:
            ctx = self.ctx
            loc = ctx.get_location()
        except Exception as e:
            print(f"Error getting location in Saboteur: {e}")
            return None

        try:
            enemies = ctx.sense_all_enemies(loc)
        except Exception as e:
            print(f"Error sensing enemies: {e}")
            enemies = []

        if enemies:
            try:
                closest_enemy_loc = enemies[0][1].location
                if manhattan_distance(loc, closest_enemy_loc) <= 1:
                    return self_destruct()
            except Exception as e:
                print(f"Error during self-destruct sequence: {e}")
            
            try:
                closest_enemy_loc = enemies[0][1].location
                d = ctx.move_target(loc, closest_enemy_loc)
                if d:
                    return move(d)
            except Exception as e:
                print(f"Error calculating move target: {e}")

        return None

    @classmethod
    def can_spawn(cls, api: GameAPI) -> bool:
        """
        Determines whether the Saboteur can be spawned given current resources.
        """
        try:
            return api.can_spawn(cls.ABILITIES)
        except Exception as e:
            print(f"Error checking spawn conditions for Saboteur: {e}")
            return False