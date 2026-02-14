"""
GameAPI module provides an interface to interact with the game state.
"""

from seamaster.constants import Ability, SCRAP_COSTS
from seamaster.models.algae import Algae
from seamaster.models.bank import Bank
from seamaster.models.enemy_bot import EnemyBot
from seamaster.models.energy_pad import EnergyPad
from seamaster.models.player_view import PlayerView
from seamaster.models.bot import Bot
from seamaster.models.point import Point


class GameAPI:
    """
    GameAPI provides methods to interact with the game state.
    """

    def __init__(self, view: PlayerView):
        self.view = view

    # ---- GLOBAL ----
    def get_tick(self) -> int:
        """
        Returns the current tick of the game.
        returnType: int
        """
        return self.view.tick

    def get_scraps(self) -> int:
        """
        Returns the total scraps available in the game.
        returnType: int
        """
        return self.view.scraps

    def get_my_bots(self) -> list[Bot]:
        """
        Returns a list of bots owned by the player.
        returnType: list[Bot]
        """
        return list(self.view.bots.values())

    # ---- SENSING ----
    def visible_enemies(self) -> list[EnemyBot]:
        """
        Returns a list of visible enemy bots.
        returnType: list[EnemyBot]
        """
        return self.view.visible_entities.enemies

    def visible_scraps(self):
        """
        Returns a list of visible scrap entities.
        returnType: list[Scrap]
        """
        return self.view.visible_entities.scraps

    def banks(self) -> list[Bank]:
        """
        Returns a list of visible banks.
        returnType: list[Bank]
        """
        return list(self.view.permanent_entities.banks.values())

    def energypads(self) -> list[EnergyPad]:
        """
        Returns a list of visible energy pads.
        returnType: list[EnergyPad]
        """
        return list(self.view.permanent_entities.energypads.values())

    def visible_walls(self) -> list[Point]:
        """
        Returns a list of visible walls.
        returnType: list[Point]
        """
        return self.view.permanent_entities.walls

    def visible_algae(self) -> list[Algae]:
        """
        Returns a list of visible algae.
        returnType: list[Algae]
        """
        return self.view.visible_entities.algae

    def can_spawn(self, abilities: list[Ability]) -> bool:
        """
        Returns whether a bot can be spawned
        returnType: bool
        """
        cost = 0
        for ability in abilities:
            if ability not in SCRAP_COSTS:
                continue
            cost += SCRAP_COSTS[ability.value]

        return cost <= self.view.scraps
