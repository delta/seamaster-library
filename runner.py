# runner.py

import json
import sys
import types

from oceanmaster.models.player_view import PlayerView
from oceanmaster.models.bot import Bot
from oceanmaster.models.point import Point
from oceanmaster.models.visible_entities import VisibleEntities
from oceanmaster.models.permanent_entities import PermanentEntities
from oceanmaster.api.game_api import GameAPI

print("RUNNER STARTED")


def load_user():
    user = types.ModuleType("user")
    with open("tests/test1.py") as f:
        exec(f.read(), user.__dict__)
    sys.modules["user"] = user


def load_player_view(path: str) -> PlayerView:
    with open(path) as f:
        data = json.load(f)

    view = PlayerView()
    view.tick = data["tick"]
    view.scraps = data["scraps"]
    view.algae = data["algae"]
    view.bot_count = data["bot_count"]
    view.max_bots = data["max_bots"]
    view.width = data["width"]
    view.height = data["height"]

    view.bots = []
    for b in data["bots"]:
        bot = Bot()
        bot.id = b["id"]
        bot.owner_id = b["owner_id"]
        bot.location = Point(**b["location"])
        bot.energy = b["energy"]
        bot.scraps = b["scraps"]
        bot.abilities = b["abilities"]
        bot.algae_held = b["algae_held"]
        view.bots.append(bot)

    view.visible_entities = VisibleEntities()
    view.visible_entities.enemies = []
    view.visible_entities.scraps = []

    view.permanent_entities = PermanentEntities()
    view.permanent_entities.banks = []
    view.permanent_entities.energypads = []
    view.permanent_entities.walls = []
    view.permanent_entities.algae = []

    return view


def main():
    print("MAIN CALLED")
    load_user()

    from oceanmaster.wrapper import play

    for tick_file in [
        "tick0.json",
        "tick1.json",
        "tick2.json",
        "tick3.json",
        "tick4.json",
    ]:
        print(f"\n===== RUNNING {tick_file} =====")

        view = load_player_view(tick_file)
        api = GameAPI(view)

        output = play(api)
        print(json.dumps(output, indent=2))



if __name__ == "__main__":
    main()
