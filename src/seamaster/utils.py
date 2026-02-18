"""
Provides utility functions and classes for the SeaWars game.
"""

from seamaster.models.point import Point
from seamaster.constants import Direction
from seamaster.shortest_distances import GUIDE, DIST


def manhattan_distance(p1: Point, p2: Point) -> int:
    """
    Calculate the Manhattan distance between two points.
    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.
    Returns:
        int: The Manhattan distance between p1 and p2.
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def next_point(p: Point, d: Direction):
    """
    Get the next point in the specified direction.
    Args:
        p (Point): The current point.
        d (Direction): The direction to move.
    Returns:
        Point: The next point in the specified direction.
    """
    if d == Direction.NORTH and p.y + 1 >= 0 and p.y + 1 < 20:
        return Point(p.x, p.y + 1)
    if d == Direction.SOUTH and p.y - 1 >= 0 and p.y - 1 < 20:
        return Point(p.x, p.y - 1)
    if d == Direction.EAST and p.x + 1 >= 0 and p.x + 1 < 20:
        return Point(p.x + 1, p.y)
    if d == Direction.WEST and p.x - 1 >= 0 and p.x - 1 < 20:
        return Point(p.x - 1, p.y)


def direction_from_point(p1: Point, p2: Point) -> Direction:
    """
    Get the primary cardinal direction from p1 to p2.
    Args:
        p1 (Point): The starting point.
        p2 (Point): The target point.
    Returns:
        Direction: The primary cardinal direction from p1 to p2.
    Raises:
        ValueError: If either point is out of bounds.
    """
    if (
        p1.x > 20
        or p1.x < 0
        or p1.y > 20
        or p1.y < 0
        or p2.x > 20
        or p2.x < 0
        or p2.y > 20
        or p2.y < 0
    ):
        raise ValueError(
            "Points must be within the grid bounds (0-19 for both x and y)"
        )
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if abs(dx) >= abs(dy):
        return Direction.EAST if dx > 0 else Direction.WEST
    return Direction.NORTH if dy > 0 else Direction.SOUTH


def get_direction_in_one_radius(src: Point, trg: Point) -> Direction | None:
    """

    The function checks all four cardinal neighbors (north, east, south, west)
    of the source point and returns the corresponding Direction if the target
    lies in one of those adjacent cells.

    Args:
        src (Point): Current position.
        trg (Point): Target position (must be at Manhattan distance 1).

    Returns:
        Direction | None: The direction needed to move from src to trg if the
        target is adjacent; otherwise, None.
    """
    drow = [-1, 0, 1, 0]
    dcol = [0, 1, 0, -1]
    dir = [Direction.WEST, Direction.SOUTH, Direction.EAST, Direction.NORTH]
    for i in range(4):
        nx = src.x + drow[i]
        ny = src.y + dcol[i]
        if nx == trg.x and ny == trg.y:
            return dir[i]
    return None


def get_optimal_next_hops(start: Point, end: Point) -> list[Direction]:
    """
    The function looks up a precomputed GUIDE table that maps a source coordinate to a
    target coordinate and returns one or more optimal directions that lie on a shortest
    path between them.

    Args:
        start (Point): Current position of the agent.
        end (Point): Target position to move toward.

    Returns:
        list[Direction]: A list of directions representing optimal next hops along a
        shortest path. Returns an empty list if no path information is available.
    """
    src = f"{start.x},{start.y}"
    trg = f"{end.x},{end.y}"
    priority = GUIDE.get(src, {}).get(trg)
    if not priority:
        return []
    directions = []
    for d in priority.split(","):
        direction = Direction[d]
        directions.append(direction)
    return directions


def get_shortest_distance_between_points(start: Point, end: Point) -> int:
    """
    The distance is obtained from a precomputed DIST lookup table that
    stores shortest distances between all reachable grid coordinates,
    ignoring walls, banks, and other dynamic obstacles.

    Args:
        start (Point): Starting coordinate.
        end (Point): Ending coordinate.

    Returns:
        int: The shortest distance between start and end.
            Returns None if no distance information is available.
    """
    src = f"{start.x},{start.y}"
    trg = f"{end.x},{end.y}"
    distance = DIST.get(src, {}).get(trg)
    return distance


class BotIDAllocator:
    """
    bot ID generator.
    """

    def __init__(self, start: int = 1):
        self._next_id = start

    def allocate(self) -> int:
        """
        Allocate and return the next available bot ID.
        """
        bot_id = self._next_id
        self._next_id += 1
        return bot_id
