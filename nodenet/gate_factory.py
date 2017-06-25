from gate import Gate

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

def gate_factory(gate_names):
    # return a list of gates, generated from gate types based on a list of names
    return [Gate(*GATE_TYPES.get(name)) for name in gate_names]
