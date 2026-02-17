from seamaster.models.point import Point


class Bank:
    """
    Represents a bank in the game.
    """

    id: int
    location: Point
    deposit_occuring: bool
    deposit_amount: int
    is_deposit_owner: bool
    is_bank_owner: bool
    deposit_ticks_left: int
    lockpick_occuring: bool
    lockpick_ticks_left: int
    lockpick_botid: int

    @classmethod
    def from_dict(cls, data: dict):
        b = cls()
        b.id = data["id"]
        b.location = Point(**data["location"])
        b.deposit_occuring = data["deposit_occuring"]
        b.deposit_amount = data["deposit_amount"]
        b.is_deposit_owner = data["is_deposit_owner"]
        b.is_bank_owner = data["is_bank_owner"]
        b.deposit_ticks_left = data["deposit_ticks_left"]
        b.lockpick_occuring = data["lockpick_occuring"]
        b.lockpick_ticks_left = data["lockpick_ticks_left"]
        b.lockpick_botid = data["lockpick_botid"]
        return b
