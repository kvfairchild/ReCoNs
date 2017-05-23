# !/usr/bin/env python

from nodenet2.nodenet import Nodenet
from random import random

"""
It is fine to do this directly in here, input statements are usually more awkward to use.
The correct way of doing this is a config file or a test file, of course.
"""
# set number of layers and nodes per layer
number_of_layers = 3
nodes_per_layer = 4

"""
Your definition implies that a nodenet will always be 2D array? It might be ok to have one of those for testing,
but in general, nodenets take an arbitrary shape.
"""
# construct nodenet
node_net = Nodenet("nodenet", number_of_layers, nodes_per_layer)  # usually this is not going to be the shape we want
node_net.build_nodenet()  # why not call this directly in the constructor?


def initialize_input_layer():  # rename "init" to something more descriptive, shift explanation into fn doc string
    """initialize first layer nodes to random value input"""
    initial_value = random()  # all to the same input value? why?
    print "initial value: ", initial_value
    for node in node_net.node_net[0]:  # how can you find the input layer if the nodenet is fully recurrent?
        for slot in node.slot_vector:
            slot.current_value = initial_value

"""
What are we going to do if the node has multiple slots? Since the slot cannot know or should not negotiate with the
other slots, this would need to happen in the node function, not in the slot or for every slot.

Per spec, slots don't have an activation threshold (gates might).
"""
def broadcast_input(layer):
    """if input exceeds slot activation threshold, push to node"""
    for node in layer:
        for slot in node.slot_vector:
            if slot.current_value >= slot.activation:
                node.current_value = slot.current_value
                print "node value: ", node.current_value


"""
This should not be called for each layer, but for each node, no? It will break if the net is not recurrent.
The function should probably be defined at the nodenet level, not here.
"""
def net_function(layer):
    """call node function and link function for active nodes"""
    for node in layer:
        if node.current_value is not None:  # comparisons with "None" are done with "is"
            node.node_function()
            node_net.link_function()
            node.current_value = None


"""
this ugly thing replaces "run" and is the idiomatic way to run a python file, can you guess why?
"""
if __name__ == "__main__":
    initialize_input_layer()
    for layer in node_net.node_net:  # this will break if the nodenet is recurrent
        print "layer"
        broadcast_input(layer)
        net_function(layer)

