"""
OceanMaster AI SDK

High-level imports for common usage.
"""

# Core interfaces
from oceanmaster.api.game_api import GameAPI
from oceanmaster.context.bot_context import BotContext

# Base classes
from oceanmaster.botbase import BotController

# templates
from oceanmaster.templates import Forager, FlashScout, HeatSeeker, Lurker, Saboteur

# Constants
from oceanmaster.Constants import Ability, Direction, ABILITY_COSTS


# Actions
from oceanmaster.Translate import move, moveSpeed, harvest, self_destruct, defend, spawn

__all__ = [
    "GameAPI",
    "BotContext",
    "BotController",
    "Forager",
    "FlashScout",
    "HeatSeeker",
    "Lurker",
    "Saboteur",
    "Ability",
    "Direction",
    "ABILITY_COSTS",
    "spawn",
    "moveSpeed",
    "move",
    "harvest",
    "self_destruct",
    "defend",
]
