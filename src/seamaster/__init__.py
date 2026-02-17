"""
OceanMaster AI SDK

High-level imports for common usage.
"""

# API
from seamaster.api.game_api import GameAPI

# Context
from seamaster.context.bot_context import BotContext

# Base classes
from seamaster.botbase import BotController

# templates
from seamaster.templates.forager import Forager
from seamaster.templates.flash_scout import FlashScout
from seamaster.templates.lurker import Lurker
from seamaster.templates.saboteur import Saboteur

# models
from seamaster.models.point import Point
from seamaster.models.bot import Bot
from seamaster.models.player_view import PlayerView
from seamaster.models.visible_entities import VisibleEntities
from seamaster.models.permanent_entities import PermanentEntities
from seamaster.models.scrap import Scrap
from seamaster.models.bank import Bank
from seamaster.models.energy_pad import EnergyPad
from seamaster.models.algae import Algae
from seamaster.models.action import Action

# constants
from seamaster.constants import Ability, Direction, ABILITY_COSTS


# Actions
# src/seamaster/__init__.py

from seamaster.translate import (
    move,
    move_speed,
    harvest,
    self_destruct,
    spawn,
    lockpick,
    poison,
)

# Utils
from seamaster.utils import manhattan_distance, next_point, direction_from_point


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
    "direction_from_point",
]
