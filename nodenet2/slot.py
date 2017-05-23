from uuid import uuid4


class Slot:
    def __init__(self, name, activation=0):
        self.uid = uuid4()
        self.name = name
        self.activation = activation
        self.current_value = 0

"""
Original version had   self.activation = activation if activation is not None else slots.get(name, default=None)
where slots is not defined!
"""