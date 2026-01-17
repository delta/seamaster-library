from enum import Enum

class Ability(str, Enum):
    HARVEST = "HARVEST"
    SCOUT = "SCOUT"
    POISON = "POISON"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    SPEED = "SPEED"
    SHIELD = "SHIELD"
    LOCKPICK = "LOCKPICK"
    

class ActionType(str, Enum):
    MOVE = "MOVE"
    HARVEST = "HARVEST"
    POISON = "POISON"
    DEFEND = "DEFEND"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    LOCKPICK = "LOCKPICK"
    SPAWN = "SPAWN"
    
class Direction(str, Enum):
		NORTH = "NORTH"
		EAST = "EAST"
		SOUTH = "SOUTH"
		WEST = "WEST"
	
ABILITY_COSTS = {
    "HARVEST":   {"scrap": 10, "energy": 0},
    "SCOUT":     {"scrap": 10, "energy": 1.5},
    "SELF_DESTRUCT": {"scrap": 5, "energy": 0.5},
    "SPEED":     {"scrap": 10, "energy": 1},
    "SHIELD":    {"scrap": 5, "energy": 0.25},
    "POISON":    {"scrap": 5, "energy": 0.5},
    "LOCKPICK":  {"scrap": 10, "energy": 1.5},
}

class BotType(str, Enum):
    FORAGER = "Forager"
    HOARDER = "Hoarder"
    MULE = "Mule"
    LURKER = "Lurker"
    SABOTEUR = "Saboteur"
    HEATSEEKER = "HeatSeeker"
    CUSTOMBOT = "CustomBot"
    
class AlgaeType(str, Enum):
    UNKNOWN = "UNKNOWN"
    TRUE = "TRUE"