# seamaster/context/bot_context.py
"""
BotContext module provides a read-only interface for bot strategies
to interact with the game engine state safely.
"""

from seamaster.constants import Direction, Ability, SCRAP_COSTS
from seamaster.models.algae import Algae
from seamaster.models.bank import Bank
from seamaster.models.bot import Bot
from seamaster.models.energy_pad import EnergyPad
from seamaster.models.point import Point
from seamaster.models.scrap import Scrap
from seamaster.utils import manhattan_distance
from seamaster.utils import get_optimal_next_hops, get_shortest_distance_between_points


class BotContext:
    """
    BotContext provides a safe, read-only interface between a bot strategy
    and the game engine state.

    It exposes:
    - bot status
    - sensing utilities
    - movement/pathfinding helpers
    - combat and resource actions

    A BotContext instance is created once per bot per tick.
    """

    def __init__(self, api, bot):  # TODO: Fix all the errors after adding type
        """
        Initialize the context for a single bot.

        Args:
            api (GameAPI): Read-only game API wrapper.
            bot (Bot): Bot model instance representing the current bot.
        """
        self.api = api
        self.bot = bot

    # ==================== ROBOT STATUS ====================

    def get_id(self) -> int:
        """
        Get the unique identifier of this bot.

        Returns:
            int: Unique bot ID assigned by the engine.
        """
        return self.bot.id

    def get_energy(self) -> int:
        """
        Get the current energy level of the bot.

        Returns:
            int: Current energy units.
        """
        return self.bot.energy

    def get_location(self) -> Point:
        """
        Get the current grid position of the bot.

        Returns:
            Point: Bot's current location.
        """
        return self.bot.location

    def get_abilities(self) -> list[str]:
        """
        Get the abilities currently equipped by the bot.

        Returns:
            list[str]: List of ability identifiers.
        """
        return self.bot.abilities

    def get_algae_held(self) -> int:
        """
        Get the amount of algae currently carried by the bot.

        Returns:
            int: Algae units held.
        """
        return self.bot.algae_held

    def get_type(self) -> list[str]:
        """
        Get the list of abilities currently equipped by the bot.

        Returns:
            list[str]: Ability identifiers.
        """
        return self.bot.abilities

    def spawn_cost(self, abilities: list[str]) -> int:
        """
        Calculate the resource cost of spawning or upgrading abilities.

        Applies ability synergies where applicable.

        Args:
            abilities (list[str]): List of ability identifiers.

        Returns:
            dict: Dictionary with keys:
                - 'scrap' (int)
                - 'energy' (float)
        """
        total_scrap = 0

        for ability in abilities:
            if ability not in SCRAP_COSTS:
                continue
            total_scrap += SCRAP_COSTS[ability]

        return total_scrap

    # ==================== SENSING ====================

    def sense_enemies(self):
        """
        Get all visible enemy bots.

        Returns:
            list[EnemyBot]: Visible enemy bots.
        """
        return self.api.visible_enemies()

    def sense_enemies_in_radius(self, bot: Point, radius: int = 1) -> list[Bot]:
        """
        Detect enemies within a Manhattan radius of a given point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[EnemyBot]: Enemies within radius.
        """
        return [
            b
            for b in self.api.visible_enemies()
            if manhattan_distance(b.location, bot) <= radius
        ]

    def sense_own_bots(self) -> list[Bot]:
        """
        Get own bots excluding this bot.

        Returns:
            list[Bot]: Nearby friendly bots.
        """
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id]

    def sense_own_bots_in_radius(self, bot: Point, radius: int = 1) -> list[Bot]:
        """
        Detect own bots within a radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Bot]: Friendly bots within radius.
        """
        return [
            b
            for b in self.api.get_my_bots()
            if b.id != self.bot.id and manhattan_distance(b.location, bot) <= radius
        ]

    def sense_unknown_algae(self, bot: Point) -> list[tuple[int, Algae]]:
        """
        Detect algae within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Algae]: Algae within radius.
        """
        result = []

        for a in self.api.visible_algae():
            d = get_shortest_distance_between_points(bot, a.location)

            if d is not None and a.is_poison == "UNKNOWN":
                result.append((d, a))

        return sorted(result, key=lambda x: x[0])

    def sense_non_poisionous_algae(self, bot: Point) -> list[tuple[int, Algae]]:
        """
        Returns List of non_poisonous algae
        """
        result = []

        for a in self.api.visible_algae():
            d = get_shortest_distance_between_points(bot, a.location)

            if d is not None and a.is_poison == "FALSE":
                result.append((d, a))
        sorted_result = sorted(result, key=lambda x: x[0])
        return sorted_result

    def sense_scraps_in_radius(self, bot: Point, radius: int = 0) -> list[Scrap]:
        """
        Detect scraps within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Scrap]: Scraps within radius.
        """
        return [
            s
            for s in self.api.sense_bot_scraps()
            if manhattan_distance(s.location, bot) == radius
        ]

    def sense_objects(self) -> dict[str, list]:
        """
        Retrieve all static and resource objects visible to the player.

        Returns:
            dict: Mapping of object categories to entity lists.
        """
        return {
            "scraps": self.api.sense_bot_scraps(),
            "banks": self.api.banks(),
            "energypads": self.api.energypads(),
        }

    def sense_walls(self) -> list[Point]:
        """
        Get all visible walls.

        Returns:
            list[Wall]: Visible wall entities.
        """
        return self.api.visible_walls()

    def sense_walls_in_radius(self, bot: Point, radius: int = 1) -> list[Point]:
        """
        Detect walls within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Wall]: Walls within radius.
        """
        return [
            w for w in self.api.visible_walls() if manhattan_distance(w, bot) <= radius
        ]

    # ============= REACTING TO GAME STATE =============

    def get_depositing_banks_sorted(self):
        """
        Get depositing banks sorted by nearest distance from the bot.

        Returns:
            list[Bank]: Depositing banks sorted by distance.
        """
        pos = self.bot.location
        return sorted(
            (b for b in self.api.banks() if b.deposit_occuring),
            key=lambda b: manhattan_distance(b.location, pos),
        )

    # ==================== PATHING ====================

    def next_point(self, pos: Point, direction: Direction) -> Point | None:
        """
        Compute the next point for one step in `direction`.
        Returns None if the step would go out of bounds.
        """
        x, y = pos.x, pos.y
        if direction == Direction.NORTH:
            y -= 1
        elif direction == Direction.SOUTH:
            y += 1
        elif direction == Direction.EAST:
            x += 1
        elif direction == Direction.WEST:
            x -= 1

        if x < 0 or y < 0 or x >= self.api.view.width or y >= self.api.view.height:
            return None
        return Point(x, y)

    def next_point_speed(
        self, pos: Point, direction: Direction, step: int
    ) -> Point | None:
        """
        Compute the next point for a SPEED move in `direction` with `step` size.
        Returns None if any step would go out of bounds.
        """
        if step not in (1, 2):
            raise ValueError("Step size must be 1 or 2.")

        x, y = pos.x, pos.y
        if direction == Direction.NORTH:
            y -= step
        elif direction == Direction.SOUTH:
            y += step
        elif direction == Direction.EAST:
            x += step
        elif direction == Direction.WEST:
            x -= step

        if x < 0 or y < 0 or x >= self.api.view.width or y >= self.api.view.height:
            return None
        return Point(x, y)

    def can_move(self, direction: Direction) -> bool:
        """
        Check whether movement in a given direction stays within map bounds.

        Args:
            direction (Direction): Intended movement direction.

        Returns:
            bool: True if move is inside map bounds.
        """
        return self.next_point(self.bot.location, direction) is not None

    def check_blocked_point(self, pos: Point) -> bool:
        """
        Determine if a position is blocked by:
        - Out of bounds
        - Wall
        - Enemy
        - Own bot (optional, recommended for collision avoidance)

        Args:
            pos (Point): Position to check.

        Returns:
            bool: True if blocked.
        """

        if (
            pos.x < 0
            or pos.y < 0
            or pos.x >= self.api.view.width
            or pos.y >= self.api.view.height
        ):
            return True

        if any(w == pos for w in self.api.visible_walls()):
            return True

        if any(e.location == pos for e in self.api.visible_enemies()):
            return True

        if any(b.location == pos for b in self.api.get_my_bots()):
            return True

        return False

    def check_blocked_direction(self, direction: Direction) -> bool:
        """
        Determine if moving in a direction would result in a blocked position.

        Args:
            direction (Direction): Direction to check.

        Returns:
            bool: True if the position in that direction is blocked.
        """
        next_pos = self.next_point(self.bot.location, direction)
        if next_pos is None:
            return True
        return self.check_blocked_point(next_pos)

    def can_defend(self) -> bool:
        """
        Check if the bot has defensive capability.

        Returns:
            bool: True if SHIELD ability exists.
        """
        return Ability.SHIELD.value in self.bot.abilities

    def can_spawn(self, abilities: list[str]) -> bool:
        """
        Check whether spawning a bot with given abilities is possible.

        Args:
            abilities (list[str]): Ability list.

        Returns:
            bool: True if spawn is allowed.
        """
        if len(self.api.view.bots) >= self.api.view.max_bots:
            return False

        cost = self.spawn_cost(abilities)
        return self.api.get_scraps() >= cost

    # ==================== NEAREST OBJECT HELPERS ====================

    def get_nearest_bank(self) -> Bank:
        """
        Returns:
            Bank: Nearest bank.
        """
        pos = self.bot.location
        return min(
            self.api.banks(),
            key=lambda b: manhattan_distance(b.location, pos),
        )

    def get_energy_pads(self) -> list[EnergyPad]:
        """
        :return: List of energypafs
        :rtype: list[EnergyPad]
        """
        return self.api.energypads()

    def get_nearest_energy_pad(self) -> EnergyPad:
        """
        Return:
            EnergyPad: Nearest energy pad.
        """
        pos = self.bot.location
        return min(
            self.api.energypads(),
            key=lambda p: get_shortest_distance_between_points(p.location, pos),
        )

    def get_my_banks(self, bot: Point) -> list[Bank] | None:
        """
        Returns a list of my banks sorted in ascending order of distance
        (distance is min distance to any adjacent cell of the bank)
        """

        my_banks = [b for b in self.api.banks() if b.is_bank_owner]

        if not my_banks:
            return None

        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        def min_adjacent_distance(bank: Bank) -> int:
            distances = []
            for dx, dy in dirs:
                adj = Point(bank.location.x + dx, bank.location.y + dy)
                if not self.check_blocked_point(adj):
                    dist = get_shortest_distance_between_points(bot, adj)
                    if dist is not None:
                        distances.append(dist)
            return min(distances)

        # Sort banks by min adjacent distance
        my_banks.sort(key=min_adjacent_distance)
        return my_banks

    def get_opponent_banks(self, bot: Point) -> list[Bank] | None:
        """
        Returns a list of opponents banks sorted in ascending order of distance
        """
        opp_banks = [b for b in self.api.banks() if not b.is_bank_owner]
        if not opp_banks:
            return None
        dist1 = get_shortest_distance_between_points(bot, opp_banks[0].location)
        dist2 = get_shortest_distance_between_points(bot, opp_banks[1].location)

        if dist1 > dist2:
            return opp_banks.reverse()

        return opp_banks

    def get_nearest_scrap(self) -> Scrap:
        """
        Return:
            Scrap: Nearest scrap.
        """
        pos = self.bot.location
        return min(
            self.api.sense_bot_scraps(),
            key=lambda s: manhattan_distance(s.location, pos),
        )

    def get_nearest_algae(self) -> Algae:
        """
        Return:
            Algae: Nearest algae.
        """
        pos = self.bot.location
        return min(
            self.api.visible_algae(),
            key=lambda a: manhattan_distance(a.location, pos),
        )

    def get_nearest_enemy(self) -> Bot:
        """
        Return:
            Bot: Nearest enemy.
        """
        pos = self.bot.location
        return min(
            self.api.visible_enemies(),
            key=lambda e: manhattan_distance(e.location, pos),
        )

    # ==================== COLLISION AVOIDANCE ====================

    def move_target(self, bot: Point, target: Point) -> Direction | None:
        """
        High-performance movement with collision and edge protection.

        Args:
            bot (Point): Current bot position.
            target (Point): Target position.

        Returns:
            Direction | None: Preferred movement direction or None if blocked.
        """
        priority = get_optimal_next_hops(bot, target)
        if not priority:
            return None

        for direction in priority:
            if not self.check_blocked_direction(direction):
                return direction

        return None

    def move_target_speed(
        self, bot: Point, target: Point
    ) -> tuple[Direction | None, int]:
        if Ability.SPEED_BOOST.value not in self.bot.abilities:
            raise ValueError("Bot does not have SPEED ability equipped.")

        priority = get_optimal_next_hops(bot, target)
        if not priority:
            return None, 0

        one_step_fallback = None

        for direction in priority:
            # --- Check 1-step ---
            p1 = self.next_point_speed(bot, direction, 1)
            if p1 is None or self.check_blocked_point(p1):
                continue

            # store fallback if 2-step fails
            if one_step_fallback is None:
                one_step_fallback = direction

            # --- Check 2-step ---
            p2 = self.next_point_speed(bot, direction, 2)
            if p2 is not None and not self.check_blocked_point(p2):
                return direction, 2

        # If no valid 2-step, try 1-step
        if one_step_fallback is not None:
            return one_step_fallback, 1

        return None, 0
