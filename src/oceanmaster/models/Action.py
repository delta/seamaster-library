import json
from typing import Dict, Any
from oceanmaster.Constants import ActionType

class Action:
    def __init__(self, action_type: ActionType, payload: Dict[str, Any]):
        self.action_type = action_type
        self.payload = payload

    def to_dict(self):
        out = {"action": self.action_type.value}
        out.update(self.payload)
        return out
