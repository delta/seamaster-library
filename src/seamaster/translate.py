"""
Provides functions to create various game actions.
"""

from seamaster.models.point import Point
from seamaster.models.action import Action
from seamaster.constants import Direction, Ability
from seamaster.utils import BotIDAllocator

BOT_ID_ALLOCATOR = BotIDAllocator()


def move(direction: Direction):
    """
    Creates a move action in the specified direction.
    """
    return Action(Ability.MOVE, {"direction": direction.value})


def move_speed(direction: Direction, step: int):
    """
    Creates a move action in the specified direction with a given step size.
    """
    return Action(Ability.MOVE, {"direction": direction.value, "step": step})


def harvest(direction: Direction):
    """ "
    Creates a harvest action in the specified direction.
    """
    return Action(Ability.HARVEST, {"direction": direction.value})


def self_destruct():
    """
    Creates a self-destruct action.
    """
    return Action(Ability.SELF_DESTRUCT, {"direction": "NULL"})


def spawn(Ability: list[str], location: int):
    """
    Creates a spawn action with specified Ability at a given location.
    """
    bot_id = BOT_ID_ALLOCATOR.allocate()
    return bot_id, {"Ability": Ability, "location": {"x": location, "y": 0}}


def lockpick(location: Point):
    """
    Creates a lockpick action.
    """
    return Action(Ability.LOCKPICK, {"location": location})


def poison(direction: Direction):
    """
    Creates a poison action in the specified direction.
    """
    return Action(Ability.POISON, {"direction": direction.value})
