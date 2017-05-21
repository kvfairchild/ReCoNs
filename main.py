#!/usr/bin/env python

from nodenet import nodenet
from random import random

# get number of layers and nodes per layer from user
num_layers = input("Number of layers: ")
num_nodes = input("Number of nodes per layer: ")

# construct nodenet
node_net = nodenet.Nodenet("nodenet", num_layers, num_nodes)
node_net.build_nodenet()

def run():
	init()
	for layer in node_net.node_net:
		print "layer"
		broadcast_input(layer)
		net_function(layer)

# initialize first layer nodes to random value input
def init():
	initial_value = random()
	print "initial value: ", initial_value
	for node in node_net.node_net[0]:
		for slot in node.slot_vector:
			slot.current_value = initial_value

# if input exceeds slot activation threshold, push to node
def broadcast_input(layer):
	for node in layer:
		for slot in node.slot_vector:
			if slot.current_value >= slot.activation:
				node.current_value = slot.current_value
				print "node value: ", node.current_value

# call node function and link function for active nodes
def net_function(layer):
	for node in layer:
		if node.current_value != None:
			node.node_function()
			node_net.link_function()
			node.current_value = None

run()
