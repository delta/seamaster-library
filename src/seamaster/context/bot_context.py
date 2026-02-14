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
from seamaster.utils import manhattan_distance, next_point
from seamaster.shortest_distances import GUIDE


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

    def sense_algae(self, radius: int = 1) -> list[Algae]:
        """
        Detect visible algae within a radius of the bot.

        Args:
            radius (int): Manhattan distance radius.

        Returns:
            list[Algae]: Algae entities within radius.
        """
        pos = self.bot.location
        return [
            a
            for a in self.api.visible_algae()
            if manhattan_distance(a.location, pos) <= radius
        ]

    def sense_algae_in_radius(self, bot: Point, radius: int = 1) -> list[Algae]:
        """
        Detect algae within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Algae]: Algae within radius.
        """
        return [
            a
            for a in self.api.visible_algae()
            if manhattan_distance(a.location, bot) <= radius
        ]

    def sense_scraps_in_radius(self, radius: int = 1) -> list[Scrap]:
        """
        Detect visible scrap resources within a radius of the bot.

        Args:
            radius (int): Manhattan distance radius.

        Returns:
            list[Scrap]: Scrap entities within radius.
        """
        pos = self.bot.location
        return [
            a
            for a in self.api.visible_scraps()
            if manhattan_distance(a.location, pos) <= radius
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

    def can_move(self, direction: Direction) -> bool:
        """
        Check whether movement in a given direction stays within map bounds.

        Args:
            direction (Direction): Intended movement direction.

        Returns:
            bool: True if move is inside map bounds.
        """
        x, y = self.bot.location.x, self.bot.location.y

        if direction == Direction.NORTH:
            y += 1
        elif direction == Direction.SOUTH:
            y -= 1
        elif direction == Direction.EAST:
            x += 1
        elif direction == Direction.WEST:
            x -= 1

        return 0 <= x < self.api.view.width and 0 <= y < self.api.view.height

    def shortest_path(self, target: Point) -> int:
        """
        Compute Manhattan distance to a target point.

        Args:
            target (Point): Target location.

        Returns:
            int: Manhattan distance.
        """
        bx, by = self.bot.location.x, self.bot.location.y
        return abs(bx - target.x) + abs(by - target.y)

    def check_blocked_point(self, pos: Point) -> bool:
        """
        Determine if a position is blocked by any obstacle.

        Args:
            pos (Point): Position to check.

        Returns:
            bool: True if blocked.
        """
        return (
            len(self.sense_walls_in_radius(pos)) > 0
            or len(self.sense_enemies_in_radius(pos)) > 0
        )

    def check_blocked_direction(self, direction: Direction) -> bool:
        """
        Determine if moving in a direction would result in a blocked position.

        Args:
            direction (Direction): Direction to check.

        Returns:
            bool: True if the position in that direction is blocked.
        """
        pos = self.bot.location
        x, y = pos.x, pos.y

        if direction == Direction.NORTH:
            y += 1
        elif direction == Direction.SOUTH:
            y -= 1
        elif direction == Direction.EAST:
            x += 1
        elif direction == Direction.WEST:
            x -= 1

        return self.check_blocked_point(Point(x, y))

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
            key=lambda p: manhattan_distance(p.location, pos),
        )

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
        src = f"{bot.x},{bot.y}"
        trg = f"{target.x},{target.y}"

        priority = GUIDE.get(src, {}).get(trg)
        if not priority:
            return None

        for d in priority.split(","):
            direction = Direction[d]
            if not self.check_blocked_direction(direction):
                return direction

        return None

    def move_target_speed(
        self, bot: Point, target: Point
    ) -> tuple[Direction | None, int]:
        """
        High-performance SPEED movement with collision detection and edge protection.

        Args:
            bot (Point): Current bot position.
            target (Point): Target position.

        Returns:
            tuple[Direction | None, int]: Preferred movement direction and step size (1 or 2), or (None, 0) if blocked.
        """
        if Ability.SPEED_BOOST.value not in self.bot.abilities:
            raise ValueError("Bot does not have SPEED ability equipped.")

        src = f"{bot.x},{bot.y}"
        trg = f"{target.x},{target.y}"

        priority = GUIDE.get(src, {}).get(trg)
        if not priority:
            return None, 0

        for d in priority.split(","):
            direction = Direction[d]

            p1 = next_point(bot, direction)
            if p1 is None or self.check_blocked_point(p1):
                continue

            p2 = next_point(p1, direction)
            if p2 is not None and not self.check_blocked_point(p2):
                return direction, 2

            return direction, 1

        return None, 0
