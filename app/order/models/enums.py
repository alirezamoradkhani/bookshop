from enum import Enum

class OrderState(str, Enum):
    WAITING = "waiting"
    IN_PROCCESE = "in_proccese"
    DONE = "done"
    CANCELED = "canceled"

class OrderItemState(str, Enum):
    WAITING = "waiting"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    FORCEREJECTED = "forcerejected"
    PREPARING = "preparing"
    DONE = "done"
    CANCELED = "canceled"