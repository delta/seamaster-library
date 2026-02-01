from oceanmaster.models.point import Point


class Bank:
    id: int
    location: Point
    deposit_occuring: bool
    deposit_amount: int
    deposit_owner: int
    depositticksleft: int
