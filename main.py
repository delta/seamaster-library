# main.py
import json
import sys
import types

from oceanmaster.api.game_api import GameAPI
from oceanmaster.models.player_view import PlayerView


def load_user():
    user = types.ModuleType("user")
    with open("tests/test3.py") as f:
        exec(f.read(), user.__dict__)
    sys.modules["user"] = user


def main():
    load_user()
    from oceanmaster.wrapper import play

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        data = json.loads(line)

        view = PlayerView.from_dict(data)

        api = GameAPI(view)
        out = play(api)

        print(json.dumps(out))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
