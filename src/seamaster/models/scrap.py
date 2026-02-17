"""
Represents a scrap that is visible to the bot.
"""

from seamaster.models.point import Point


class Scrap:
    """
    Represents a scrap that is visible to the bot.
    """

    location: Point
    amount: int

    @classmethod
    def from_dict(cls, data: dict):
        s = cls()
        s.location = Point(**data["location"])
        s.amount = data["amount"]
        return s
