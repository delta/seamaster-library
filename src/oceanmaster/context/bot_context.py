"""
BotContext module provides a read-only interface for bot strategies
to interact with the game engine state safely.
"""

from oceanmaster.constants import Direction, Ability, ABILITY_COSTS
from oceanmaster.models.point import Point
from oceanmaster.Utils import manhattan_distance, next_point


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

    def __init__(self, api, bot):
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

    def cost(self, abilities: list[str]) -> dict:
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
        total_energy = 0.0

        for ability in abilities:
            if ability not in ABILITY_COSTS:
                continue
            total_scrap += ABILITY_COSTS[ability]["scrap"]
            total_energy += ABILITY_COSTS[ability]["energy"]

        # HeatSeeker synergy discount
        if "SPEED" in abilities and "SELF_DESTRUCT" in abilities:
            total_scrap -= 5

        return {"scrap": total_scrap, "energy": total_energy}

    # ==================== SENSING ====================

    def sense_enemies(self):
        """
        Get all visible enemy bots.

        Returns:
            list[Bot]: Visible enemy bots.
        """
        return self.api.visible_enemies()

    def sense_enemies_in_radius(self, bot: Point, radius: int = 1):
        """
        Detect enemies within a Manhattan radius of a given point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Bot]: Enemies within radius.
        """
        return [
            b
            for b in self.api.visible_enemies()
            if manhattan_distance(b.location, bot) <= radius
        ]

    def sense_own_bots(self):
        """
        Get own bots excluding this bot.

        Returns:
            list[Bot]: Nearby friendly bots.
        """
        return [
            b for b in self.api.get_my_bots() if b.id != self.bot.id
        ]

    def sense_own_bots_in_radius(self, bot: Point, radius: int = 1):
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
            if b.id != self.bot.id
            and manhattan_distance(b.location, bot) <= radius
        ]

    def sense_algae(self, radius: int = 1):
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

    def sense_scraps_in_radius(self, radius: int = 1):
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

    def sense_objects(self):
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

    def sense_walls(self):
        """
        Get all visible walls.

        Returns:
            list[Wall]: Visible wall entities.
        """
        return self.api.visible_walls()

    def sense_walls_in_radius(self, bot: Point, radius: int = 1):
        """
        Detect walls within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Wall]: Walls within radius.
        """
        return [
            w
            for w in self.api.visible_walls()
            if manhattan_distance(w, bot) <= radius
        ]

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

        return (
            0 <= x < self.api.view.width
            and 0 <= y < self.api.view.height
        )

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

    def check_blocked(self, pos: Point) -> bool:
        """
        Determine if a position is blocked by any obstacle.

        Args:
            pos (Point): Position to check.

        Returns:
            bool: True if blocked.
        """
        return (
            self.sense_walls_in_radius(pos)
            or self.sense_enemies_in_radius(pos)
            or self.sense_own_bots_in_radius(pos)
        )

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
        if self.api.view.bot_count >= self.api.view.max_bots:
            return False

        cost = self.cost(abilities)
        return (
            self.api.get_scraps() >= cost["scrap"]
            and self.api.get_energy() >= cost["energy"]
        )

    # ==================== NEAREST OBJECT HELPERS ====================

    def get_nearest_bank(self) -> Point:
        """Return nearest bank location."""
        pos = self.bot.location
        return min(
            self.api.banks(),
            key=lambda b: manhattan_distance(b.location, pos),
        ).location

    def get_nearest_energy_pad(self) -> Point:
        """Return nearest energy pad location."""
        pos = self.bot.location
        return min(
            self.api.energypads(),
            key=lambda p: manhattan_distance(p.location, pos),
        ).location

    def get_nearest_scrap(self) -> Point:
        """Return nearest scrap location."""
        pos = self.bot.location
        return min(
            self.api.sense_bot_scraps(),
            key=lambda s: manhattan_distance(s.location, pos),
        ).location

    def get_nearest_algae(self) -> Point:
        """Return nearest algae location."""
        pos = self.bot.location
        return min(
            self.api.visible_algae(),
            key=lambda a: manhattan_distance(a.location, pos),
        ).location

    def get_nearest_enemy(self) -> Point:
        """Return nearest enemy location."""
        pos = self.bot.location
        return min(
            self.api.visible_enemies(),
            key=lambda e: manhattan_distance(e.location, pos),
        ).location


# ==================== COLLISION AVOIDANCE ====================

def move_target(self, bot: Point, target: Point):
    """
    Fast, edge-safe movement toward target.
    O(1) time, no allocations.
    """
    x, y = bot.x, bot.y
    at_left = x == 0
    at_right = x == 19
    at_bottom = y == 0
    at_top = y == 19

    dx = target.x - x
    dy = target.y - y

    if abs(dx) >= abs(dy):
        preferred = Direction.EAST if dx > 0 else Direction.WEST
    else:
        preferred = Direction.NORTH if dy > 0 else Direction.SOUTH

    def try_dir(d: Direction):
        np = next_point(bot, d)
        return np is not None and not self.check_blocked(np)

    if (
        (preferred == Direction.EAST and not at_right)
        or (preferred == Direction.WEST and not at_left)
        or (preferred == Direction.NORTH and not at_top)
        or (preferred == Direction.SOUTH and not at_bottom)
    ):
        if try_dir(preferred):
            return preferred

    if at_left and try_dir(Direction.EAST):
        return Direction.EAST
    if at_right and try_dir(Direction.WEST):
        return Direction.WEST
    if at_bottom and try_dir(Direction.NORTH):
        return Direction.NORTH
    if at_top and try_dir(Direction.SOUTH):
        return Direction.SOUTH

    if not at_top and try_dir(Direction.NORTH):
        return Direction.NORTH
    if not at_right and try_dir(Direction.EAST):
        return Direction.EAST
    if not at_bottom and try_dir(Direction.SOUTH):
        return Direction.SOUTH
    if not at_left and try_dir(Direction.WEST):
        return Direction.WEST

    return None


def move_target_speed(self, bot: Point, target: Point):
    """
    High-performance SPEED movement with edge protection.
    """
    if Ability.SPEED.value not in self.bot.abilities:
        raise ValueError(
            "Bot does not have SPEED ability equipped."
        )

    x, y = bot.x, bot.y
    at_left = x == 0
    at_right = x == 19
    at_bottom = y == 0
    at_top = y == 19

    dx = target.x - x
    dy = target.y - y

    if abs(dx) >= abs(dy):
        preferred = Direction.EAST if dx > 0 else Direction.WEST
    else:
        preferred = Direction.NORTH if dy > 0 else Direction.SOUTH

    def speed_try(d: Direction):
        p1 = next_point(bot, d)
        if p1 is None or self.check_blocked(p1):
            return None

        p2 = next_point(p1, d)
        if p2 is not None and not self.check_blocked(p2):
            return d, 2

        return d, 1

    if (
        (preferred == Direction.EAST and not at_right)
        or (preferred == Direction.WEST and not at_left)
        or (preferred == Direction.NORTH and not at_top)
        or (preferred == Direction.SOUTH and not at_bottom)
    ):
        res = speed_try(preferred)
        if res:
            return res

    if at_left:
        res = speed_try(Direction.EAST)
        if res:
            return res
    if at_right:
        res = speed_try(Direction.WEST)
        if res:
            return res
    if at_bottom:
        res = speed_try(Direction.NORTH)
        if res:
            return res
    if at_top:
        res = speed_try(Direction.SOUTH)
        if res:
            return res

    for d in (
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ):
        res = speed_try(d)
        if res:
            return res

    return None, 0
