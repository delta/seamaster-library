"""
GameAPI module provides an interface to interact with the game state.
"""

from oceanmaster.models.player_view import PlayerView


class GameAPI:
    """
    GameAPI provides methods to interact with the game state.
    """

    def __init__(self, view: PlayerView):
        self.view = view

    # ---- GLOBAL ----
    def get_tick(self):
        """
        Returns the current tick of the game.
        returnType: int
        """
        return self.view.tick

    def get_scraps(self):
        """
        Returns the total scraps available in the game.
        returnType: int
        """
        return self.view.scraps

    def get_my_bots(self):
        """
        Returns a list of bots owned by the player.
        returnType: list[Bot]
        """
        return self.view.bots

    # ---- SENSING ----
    def visible_enemies(self):
        """
        Returns a list of visible enemy bots.
        returnType: list[Bot]
        """
        return self.view.visible_entities.enemies

    def visible_scraps(self):
        """
        Returns a list of visible scrap entities.
        returnType: list[VisibleScrap]
        """
        return self.view.visible_entities.scraps

    def banks(self):
        """
        Returns a list of visible banks.
        returnType: list[Bank]
        """
        return self.view.permanent_entities.banks

    def energypads(self):
        """
        Returns a list of visible energy pads.
        returnType: list[EnergyPad]
        """
        return self.view.permanent_entities.energypads

    def visible_walls(self):
        """
        Returns a list of visible walls.
        returnType: list[Point]
        """
        return self.view.permanent_entities.walls

    def visible_algae(self):
        """
        Returns a list of visible algae.
        returnType: list[Algae]
        """
        return self.view.permanent_entities.algae
