"""
OceanMaster AI SDK

High-level imports for common usage.
"""

#API
from oceanmaster.api.game_api import GameAPI

#Context
from oceanmaster.context.bot_context import BotContext

# Base classes
from oceanmaster.botbase import BotController

# templates
from oceanmaster.templates.forager import Forager
from oceanmaster.templates.flash_scout import FlashScout
from oceanmaster.templates.lurker import Lurker
from oceanmaster.templates.saboteur import Saboteur

#models
from oceanmaster.models.point import Point
from oceanmaster.models.bot import Bot
from oceanmaster.models.player_view import PlayerView
from oceanmaster.models.visible_entities import VisibleEntities
from oceanmaster.models.permanent_entities import PermanentEntities
from oceanmaster.models.scrap import Scrap
from oceanmaster.models.bank import Bank
from oceanmaster.models.energy_pad import EnergyPad
from oceanmaster.models.algae import Algae
from oceanmaster.models.action import Action

# constants
from oceanmaster.constants import (
    Ability, 
    Direction,
    ABILITY_COSTS
)


# Actions
# src/oceanmaster/__init__.py

from oceanmaster.translate import (
    move,
    move_speed,
    harvest,
    self_destruct,
    spawn,
    lockpick,
    poison
)

#Utils
from oceanmaster.utils import manhattan_distance, next_point, direction_from_point


__all__ = [
    "GameAPI",
    "BotContext",
    "BotController",
    "Forager",
    "FlashScout",
    "Lurker",
    "Saboteur",
    "Point",
    "Bot",
    "PlayerView",
    "VisibleEntities",
    "PermanentEntities",
    "Scrap",
    "Bank",
    "EnergyPad",
    "Algae",
    "Action",
    "Ability",
    "Direction",
    "ABILITY_COSTS",
    "move",
    "move_speed",
    "harvest",
    "self_destruct",
    "lockpick",
    "poison",
    "spawn",
    "manhattan_distance",
    "next_point",
    "direction_from_point"
]
