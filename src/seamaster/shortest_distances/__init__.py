import json
import importlib.resources as resources
import sys

_pkg = sys.modules[__name__]


def _load_json(name: str):
    with resources.files(_pkg).joinpath(name).open("r") as f:
        return json.load(f)


GUIDE = _load_json("directions.json")
DIST = _load_json("dist.json")
