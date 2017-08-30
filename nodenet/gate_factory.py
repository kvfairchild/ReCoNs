from gate import Gate

GATE_TYPES = {
    "gen": [
        "gen",
        0,
        {"threshold": 0}
    ],
    "por": [
        "por",
        0,
        {"threshold": 0.1}
    ],
    "ret": [
        "ret",
        0,
        {"threshold": 0.2}
    ],
    "sub": [
        "sub",
        0,
        {"threshold": 0.3}
    ],
    "sur": [
        "sur",
        0,
        {"threshold": 0.4}
    ],
    "cat": [
        "cat",
        0,
        {"threshold": 0.5}
    ],
    "exp": [
        "exp",
        0,
        {"threshold": 0.6}
    ],
    "sym": [
        "sym",
        0,
        {"threshold": 0.7}
    ],
    "ref": [
        "ref",
        0,
        {"threshold": 0.8}
    ]
}

def gate_factory(gate_names):
    # return a list of gates, generated from gate types based on a list of names
    return [Gate(*GATE_TYPES.get(name)) for name in gate_names]
