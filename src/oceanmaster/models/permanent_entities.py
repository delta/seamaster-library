from oceanmaster.models.bank import Bank
from oceanmaster.models.energy_pad import EnergyPad
from typing import List
from oceanmaster.models.point import Point
from oceanmaster.models.algae import Algae


class PermanentEntities:
    banks: List[Bank]
    energypads: List[EnergyPad]
    walls: List[Point]
    algae: List[Algae]
