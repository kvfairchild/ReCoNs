#!/usr/bin/env python

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser

#from test.input_config import *

def build_nodenet(nodenet):
	# enter number of nodes to create in each layer
	network_dimensions = [784, 10]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(node_data)
	config.link_nodes(nodenet, link_data)
		
def parse_data():
	return MNIST_file_parser.read()

def train(nodenet, data):
	# for image in data["images"]:
	config.set_activation(nodenet, data["images"][0])
	output = control.run(nodenet)
	print output


if __name__ == "__main__":
	nodenet = Nodenet()
	build_nodenet(nodenet)

	data = parse_data()
	train(nodenet, data)
