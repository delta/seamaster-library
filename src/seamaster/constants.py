"""
constants used in the Seawars game.
"""

from enum import Enum


class Ability(str, Enum):
    """
    Abilities that bots can have.
    """

    HARVEST = "HARVEST"
    SCOUT = "SCOUT"
    POISON = "POISON"
    SELF_DESTRUCT = "SELFDESTRUCT"
    SPEED_BOOST = "SPEEDBOOST"
    SHIELD = "SHIELD"
    LOCKPICK = "LOCKPICK"
    MOVE = "MOVE"
    DEPOSIT = "DEPOSIT"


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
    LURKER = "Lurker"
    SABOTEUR = "Saboteur"
    CUSTOM = "Custom"


class AlgaeType(str, Enum):
    """
    Types of algae in the game.
    """

    UNKNOWN = "UNKNOWN"
    TRUE = "TRUE"
    FALSE = "FALSE"


class BotStatus(str, Enum):
    """
    Gives Bot's Status
    """

    ACTIVE = "ACTIVE"
    DEPOSITING = "DEPOSITING"
    CHARGING = "CHARGING"


ABILITY_COSTS = {
    "HARVEST": {"traversal": 0, "action": 1},
    "SCOUT": {"traversal": 3, "action": 0},
    "SELF_DESTRUCT": {"traversal": 0.5, "action": 0},
    "SPEED_BOOST": {"traversal": 0.5, "action": 1},
    "SHIELD": {"traversal": 0.25, "action": 0},
    "POISON": {"traversal": 0.5, "action": 2},
    "LOCKPICK": {"traversal": 1.5, "action": 0},
    "DEPOSIT": {"traversal": 0, "action": 1},
    "MOVE": {"traversal": 0, "action": 0},
}

SCRAP_COSTS = {
    "HARVEST": 8,
    "SCOUT": 8,
    "SELF_DESTRUCT": 6,
    "SPEED_BOOST": 8,
    "SHIELD": 7,
    "POISON": 7,
    "LOCKPICK": 6,
}
