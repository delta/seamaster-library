# seamaster/context/bot_context.py
"""
BotContext module provides a read-only interface for bot strategies
to interact with the game engine state safely.
"""

from seamaster.api.game_api import GameAPI
from seamaster.constants import Direction, Ability, SCRAP_COSTS
from seamaster.models.algae import Algae
from seamaster.models.bank import Bank
from seamaster.models.bot import Bot
from seamaster.models.enemy_bot import EnemyBot
from seamaster.models.energy_pad import EnergyPad
from seamaster.models.point import Point
from seamaster.models.scrap import Scrap
from seamaster.utils import get_shortest_distance_between_points, get_optimal_next_hops


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

    def __init__(self, api: GameAPI, bot: Bot):
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

        Return Type: int
        """
        return self.bot.id

    def get_energy(self) -> float:
        """
        Get the current energy level of the bot.

        Returns Type: float
        """
        return self.bot.energy

    def get_location(self) -> Point:
        """
        Get the current grid position of the bot.

        Return Type: Point
        """
        return self.bot.location

    def get_abilities(self) -> list[Ability]:
        """
        Get the abilities currently equipped by the bot.

        Return Type: list[Ability]
        """
        return self.bot.abilities

    def get_algae_held(self) -> int:
        """
        Get the amount of algae currently carried by the bot.

        Return Type: int
        """
        return self.bot.algae_held

    def spawn_cost(self, abilities: list[Ability]) -> int:
        """
        Calculate the resource cost of spawning or upgrading abilities.

        Applies ability synergies where applicable.

        Args: List[Ability] - Abilities to be equipped on the new bot.

        Return Type: int - Total scrap cost for the given abilities.
        """
        total_scrap = 0

        for ability in abilities:
            if ability not in SCRAP_COSTS:
                continue
            total_scrap += SCRAP_COSTS[ability]

        return total_scrap

    def get_my_bot_ids(self) -> list[int]:
        """
        Get the IDs of all own bots excluding this bot.

        Returns:
            list[int]: IDs of all bots
        """
        return [b.id for b in self.api.get_my_bots() if b.id != self.bot.id]

    # ==================== SENSING ====================

    # Enemies -----------------
    def sense_enemies_in_radius(
        self, bot: Point, radius: int = 1
    ) -> list[tuple[int, EnemyBot]]:
        """
        Detects enemy bots within given radius of a point

        Return Type: list[tuple[int, EnemyBot]] - List of (distance, EnemyBot) tuples for enemies within radius, sorted by distance
        """
        result = []

        for e in self.api.visible_enemies():
            d = get_shortest_distance_between_points(bot, e.location)
            if d is not None and d <= radius:
                result.append((d, e))

        sorted_result = sorted(result, key=lambda x: x[0])
        return sorted_result

    def sense_all_enemies(self, bot: Point) -> list[tuple[int, EnemyBot]]:
        """
        Detects ALL visible enemy bots and their distances from a point

        Return Type: list[tuple[int, EnemyBot]] - List of (distance, EnemyBot) tuples for all visible enemies, sorted by distance
        """
        result = []

        for e in self.api.visible_enemies():
            d = get_shortest_distance_between_points(bot, e.location)
            if d is not None:
                result.append((d, e))

        sorted_result = sorted(result, key=lambda x: x[0])
        return sorted_result

    # Own Bots -----------------
    def sense_own_bots(self) -> list[Bot]:
        """
        Get own bots excluding current bot.

        Return Type: list[Bot]
        """
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id]

    def sense_own_bots_in_radius(self, bot: Point, radius: int = 1) -> list[Bot]:
        """
        Detect own bots within a radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Distance radius.

        Return Type: list[Bot] - List of own bots within given radius.
        """
        return [
            b
            for b in self.api.get_my_bots()
            if b.id != self.bot.id
            and get_shortest_distance_between_points(b.location, bot) <= radius
        ]

    # Algae -----------------
    def sense_unknown_algae(self, bot: Point) -> list[tuple[int, Algae]]:
        """
        Detect algae within a given radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Return Type: list[tuple[int, Algae]] - List of (distance, Algae) tuples for algae within radius, sorted by distance.
        """
        result = []

        for a in self.api.visible_algae():
            d = get_shortest_distance_between_points(bot, a.location)

            if d is not None and a.is_poison == "UNKNOWN":
                result.append((d, a))

        return sorted(result, key=lambda x: x[0])

    def sense_non_poisionous_algae(self, bot: Point) -> list[tuple[int, Algae]]:
        """
        Returns List of all non-poisonous algae sorted by distance from the bot.

        Args:
            bot (Point): Center position.

        Return Type: list[tuple[int, Algae]] - List of (distance, Algae) tuples for non-poisonous algae, sorted by distance.
        """
        result = []

        for a in self.api.visible_algae():
            d = get_shortest_distance_between_points(bot, a.location)

            if d is not None and a.is_poison == "FALSE":
                result.append((d, a))
        sorted_result = sorted(result, key=lambda x: x[0])
        return sorted_result

    # Scraps -----------------
    def sense_scraps_in_radius(self, bot: Point, radius: int = 0) -> list[Scrap]:
        """
        Detect scraps within a given radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Distance radius.

        Return Type: list[Scrap] - List of scraps within given radius.
        """
        return [
            s
            for s in self.api.visible_scraps()
            if get_shortest_distance_between_points(s.location, bot) == radius
        ]

    # Permanent Entities -----------------
    def sense_objects(self) -> dict[str, list]:
        """
        Returns a dictionary mapping object categories(scraps,banks and walls) to the objects

        Return Type: dict[str, list] - Mapping of object categories to entity lists.
        """
        return {
            "scraps": self.api.visible_scraps(),
            "banks": self.api.banks(),
            "energypads": self.api.energypads(),
        }

    def sense_walls(self) -> list[Point]:
        """
        Get all visible walls.

        Return Type: list[Wall] - Visible wall entities.
        """
        return self.api.visible_walls()

    def sense_walls_in_radius(self, bot: Point, radius: int = 1) -> list[Point]:
        """
        Detect walls within a given radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Distance radius.

        Return Type: list[Wall] - List of walls within given radius.
        """
        return [
            w
            for w in self.api.visible_walls()
            if get_shortest_distance_between_points(w, bot) <= radius
        ]

    def get_shortest_distance_in_four_directions(
        self, bot: Point, target: Point
    ) -> int:
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        not_blocked = []
        for dx, dy in dirs:
            adj = Point(target.x + dx, target.y + dy)
            if not self.check_blocked_point(adj):
                dist = get_shortest_distance_between_points(bot, adj)
                if dist is not None:
                    not_blocked.append(dist)
        return min(not_blocked) if not_blocked else 100_000_000

    def get_depositing_banks_sorted(self) -> list[Bank] | None:
        """
        Get depositing banks sorted by nearest distance from the bot.

        Return Type: list[Bank] - List of depositing banks sorted by distance.
        """
        pos = self.bot.location
        return sorted(
            (b for b in self.api.banks() if b.deposit_occuring),
            key=lambda b: self.get_shortest_distance_in_four_directions(
                b.location, pos
            ),
        )

    def get_opponent_banks(self) -> list[Bank] | None:
        """
        Returns a list of opponents banks sorted in ascending order of distance

        Return Type: list[Bank] - List of opponent banks sorted by distance.
        """
        bot = self.bot.location
        ans = sorted(
            (b for b in self.api.banks() if not b.is_bank_owner),
            key=lambda b: self.get_shortest_distance_in_four_directions(
                b.location, bot
            ),
        )
        return ans

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
        Return Type: Point | None
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
        - Own bot

        Args:
            pos (Point): Position to check.

        Return Type: bool - True if the position is blocked, False otherwise.
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

    def can_spawn(self, abilities: list[Ability]) -> bool:
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

    def get_nearest_energy_pad(self) -> EnergyPad:
        """
        Returns the nearest energy pad to the bot's current location.

        Return Type: EnergyPad
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

        Return Type: list[Bank] - List of own banks sorted by distance.
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

    def min_adjacent_distance_bank(
        self, bank: Bank, bot: Point
    ) -> tuple[float, Point | None]:
        """
        For the 4 adjacent cells of a bank, return:
        (minimum distance from bot, corresponding adjacent point)

        Return Type: tuple[float, Point | None] - (Minimum distance to an adjacent cell, the corresponding adjacent Point or None if unreachable)
        """

        min_dist = float("inf")
        min_point: Point | None = None

        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for dx, dy in dirs:
            adj = Point(bank.location.x + dx, bank.location.y + dy)

            if self.check_blocked_point(adj):
                continue

            dist = get_shortest_distance_between_points(bot, adj)

            if dist is not None and dist < min_dist:
                min_dist = dist
                min_point = adj

        return min_dist, min_point

    def get_nearest_scrap(self) -> Scrap:
        """
        Return Type: Scrap - Nearest Scrap.
        """
        pos = self.bot.location
        return min(
            self.api.visible_scraps(),
            key=lambda s: get_shortest_distance_between_points(s.location, pos),
        )

    def get_nearest_algae(self) -> Algae:
        """
        Return Type: Algae - Nearest Algae.
        """
        pos = self.bot.location
        return min(
            self.api.visible_algae(),
            key=lambda a: get_shortest_distance_between_points(a.location, pos),
        )

    def get_nearest_enemy(self) -> EnemyBot:
        """
        Return Type: EnemyBot - Nearest Enemy Bot.
        """
        pos = self.bot.location
        return min(
            self.api.visible_enemies(),
            key=lambda e: get_shortest_distance_between_points(e.location, pos),
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
