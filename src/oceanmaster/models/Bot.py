from typing import List
from oceanmaster.models.Point import Point
from oceanmaster.Constants import Ability, BotType

class Bot:
    id: int
    owner_id: int
    location: Point
    energy: int
    scraps: int
    abilities: List[Ability]
    algae_held: int