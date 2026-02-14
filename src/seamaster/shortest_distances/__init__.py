import json
from importlib import resources

with (
    resources.files("seamaster.shortest_distances")
    .joinpath("directions.json")
    .open("r") as f
):
    GUIDE = json.load(f)
