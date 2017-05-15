#!/usr/bin/env python

from nodenet import nodenet

nodenet = nodenet.Nodenet("katherine")

nodenet.node_factory()
N2 = nodenet.node_factory()

for node in nodenet.node_dict:
	print nodenet.node_dict[node].name

nodenet.remove_node(N2.name)

for node in nodenet.node_dict:
	print nodenet.node_dict[node].name