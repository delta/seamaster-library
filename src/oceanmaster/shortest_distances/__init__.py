import json
from importlib import resources

with (
    resources.files("oceanmaster.shortest_distances")
    .joinpath("directions.json")
    .open("r") as f
):
    GUIDE = json.load(f)
