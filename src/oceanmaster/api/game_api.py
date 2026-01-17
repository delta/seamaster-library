from oceanmaster.models.PlayerView import PlayerView


class GameAPI:
    def __init__(self, view: PlayerView):
        self.view = view

    # ---- GLOBAL ----
    def get_tick(self):
        return self.view.tick

    def get_scraps(self):
        return self.view.scraps

    def get_my_bots(self):
        return self.view.bots

    # ---- SENSING ----
    def visible_enemies(self):
        return self.view.visible_entities.enemies

    def visible_algae(self):
        return self.view.visible_entities.algae
        
    def visible_scraps(self):
        return self.view.visible_entities.scraps

    def banks(self):
        return self.view.permanent_entities.banks

    def energypads(self):
        return self.view.permanent_entities.energypads
    
    def visible_walls(self):
        return self.view.visible_entities.walls
    
    def visible_algae(self):
        return self.view.permanent_entities.algae
