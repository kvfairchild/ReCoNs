SLOT_TYPES = {
    "gen": [
        "gen",
        0
    ],
    "por": [
        "por",
        0
    ],
    "ret": [
        "ret",
        0
    ],
    "sub": [
        "sub",
        0
    ],
    "sur": [
        "sur",
        0
    ]
}

def slot_factory(slot_names):
        # return a list of slots, generated from slot types based on a list of names
        return [Slot(*SLOT_TYPES.get(name)) for name in slot_names]

class Slot:
    def __init__(self, name=None, activation=0):
        self.name = name
        self.activation = activation
