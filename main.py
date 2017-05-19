#!/usr/bin/env python

from nodenet import nodenet

num_layers = input("Number of layers: ")
num_nodes = input("Number of nodes per layer: ")

nodenet = nodenet.Nodenet("nodenet", num_layers, num_nodes)

nodenet.build_nodenet()

#N1 = nodenet.node_factory("n1")
# N2 = nodenet.node_factory()


#print N1.slot_vector
#print N1.gate_vector

# for node in nodenet.node_dict:
# 	print nodenet.node_dict[node].name
# 	print nodenet.node_dict[node].slot_vector

# nodenet.remove_node("n1")

# for node in nodenet.node_dict:
# 	print nodenet.node_dict[node].name