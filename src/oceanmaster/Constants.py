"""
constants used in the OceanMaster game.
"""

from enum import Enum


class Ability(str, Enum):
    """
    Abilities that bots can have.
    """

    HARVEST = "HARVEST"
    SCOUT = "SCOUT"
    POISON = "POISON"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    SPEED = "SPEED"
    SHIELD = "SHIELD"
    LOCKPICK = "LOCKPICK"


class ActionType(str, Enum):
    """
    Types of actions that bots can perform.
    """

    MOVE = "MOVE"
    HARVEST = "HARVEST"
    POISON = "POISON"
    DEFEND = "DEFEND"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    LOCKPICK = "LOCKPICK"
    SPAWN = "SPAWN"


class Direction(str, Enum):
    """
    Possible movement directions.
    """

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class BotType(str, Enum):
    """
    Types of bots in the game.
    """

    FORAGER = "Forager"
    HOARDER = "Hoarder"
    MULE = "Mule"
    LURKER = "Lurker"
    SABOTEUR = "Saboteur"
    HEATSEEKER = "HeatSeeker"
    CUSTOMBOT = "CustomBot"


class AlgaeType(str, Enum):
    """
    Types of algae in the game.
    """

    UNKNOWN = "UNKNOWN"
    TRUE = "TRUE"


ABILITY_COSTS = {
    "HARVEST": {"scrap": 10, "energy": 0},
    "SCOUT": {"scrap": 10, "energy": 1.5},
    "SELF_DESTRUCT": {"scrap": 5, "energy": 0.5},
    "SPEED": {"scrap": 10, "energy": 1},
    "SHIELD": {"scrap": 5, "energy": 0.25},
    "POISON": {"scrap": 5, "energy": 0.5},
    "LOCKPICK": {"scrap": 10, "energy": 1.5},
}
