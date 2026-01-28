from oceanmaster.models.Bank import Bank
from oceanmaster.models.energy_pad import EnergyPad
from typing import List
from oceanmaster.models.Point import Point
from oceanmaster.models.Algae import Algae

class PermanentEntities:
    banks: List[Bank]
    energypads: List[EnergyPad]
    walls: List[Point]
    algae: List[Algae]
