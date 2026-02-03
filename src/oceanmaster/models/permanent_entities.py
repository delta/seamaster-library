from oceanmaster.models.bank import Bank
from oceanmaster.models.energy_pad import EnergyPad
from typing import List
from oceanmaster.models.point import Point
from oceanmaster.models.algae import Algae


class PermanentEntities:
    banks: dict[int, Bank]
    energypads: dict[int, EnergyPad]
    walls: List[Point]
    
    @classmethod
    def from_dict(cls, data: dict):
        pe = cls()
        pe.banks = {int(k): Bank.from_dict(v) for k, v in data["banks"].items()}
        pe.energypads = {int(k): EnergyPad.from_dict(v) for k, v in data["energy_pads"].items()}
        pe.walls = [Point(**wall) for wall in data["walls"]]
        return pe