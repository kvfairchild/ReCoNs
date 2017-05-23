from gate import Gate

"""
Good idea to introduce a way to handle similar gate types.
I was planning to introduce node types as the next step, and each node type has a default set of gates and slots.
The only thing that should differ for node instances are individual values, so we can minimize the memory overhead.

"""


"""
Instead of creating a function for every node type, it may be better to just use a dict or so.
"""

GATE_TYPES = {
    "gen": [
        "gen",
        0,
        {"threshold": 0.1}
    ],
    "por": [
        "por",
        0,
        {"threshold": 0.2}
    ],
    "ret": [
        "ret",
        0,
        {"threshold": 0.3}
    ]
}


"""
Instead of an explicit iteration over the names and append to array in each step, I use a list comprehension.
Python also has dict comprehensions.
GATE_TYPES.get("por") returns ["por", 0, {"threshold": 0.2}], and the * unpacks the list so I can feed it directly into
the Gate constructor.
"""


def gate_factory(gate_names):
    """return a list of gates, which are generated from gate types based on a list of names"""
    return [Gate(*GATE_TYPES.get(name)) for name in gate_names]

