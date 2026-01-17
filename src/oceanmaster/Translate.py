from oceanmaster.models.Action import Action
from oceanmaster.Constants import ActionType, Direction
from oceanmaster.Utils import BotIDAllocator

BOT_ID_ALLOCATOR = BotIDAllocator()


def move(direction: Direction):
    return Action(ActionType.MOVE, {
        "direction": direction.value
    })

def moveSpeed(direction: Direction, step: int):
    return Action(ActionType.MOVE, {
        "direction": direction.value,
        "step": step
    })

def harvest(direction: Direction):
    return Action(ActionType.HARVEST, {
        "direction": direction.value
    })

def self_destruct():
    return Action(ActionType.SELF_DESTRUCT, {
        "direction": "NULL"
    })

def defend():
    return Action(ActionType.DEFEND, {
        "direction": "NULL"
    })

def spawn(abilities: list[str], location:int):
    bot_id= BOT_ID_ALLOCATOR.allocate()
    return bot_id, {
        "abilities": abilities,
        "location": {"x": location, "y": 0}
    }