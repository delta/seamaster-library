"""
Initialization of Action model.
"""

from typing import Dict, Any
from seamaster.constants import Ability


class Action:
    """
    Represents an action taken by a bot.
    """

    def __init__(self, action_type: Ability, payload: Dict[str, Any]):
        self.action_type = action_type
        self.payload = payload

    def to_dict(self):
        """
        Converts the Action to a dictionary format.
        """
        out = {"action": self.action_type.value}
        out.update(self.payload)
        return out
