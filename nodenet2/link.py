import uuid


class Link:
    def __init__(self, origin_node, origin_gate, target_node, target_slot, weight=1.0):  # added opt weight parameter
        self.uid = uuid.uuid4()
        self.origin_node = origin_node
        self.origin_gate = origin_gate
        self.target_node = target_node
        self.target_slot = target_slot
        self.weight = weight


"""
giving the link a random weight should not be hidden in the default constructor, because it is a hard to find
source of unpredictable behavior. Let us shift it to the test function that builds our nodenet later, ok?
"""