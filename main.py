#!/usr/bin/env python

from nodenet import nodenet

nodenet = nodenet.Nodenet("nodenet")

N1 = nodenet.node_factory("n1")
N2 = nodenet.node_factory()

for node in nodenet.node_dict:
	print nodenet.node_dict[node].name
	print nodenet.node_dict[node].slot_vector

nodenet.remove_node("n1")

for node in nodenet.node_dict:
	print nodenet.node_dict[node].name