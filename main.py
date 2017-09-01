#!/usr/bin/env python

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser

from test.input_config import *

def build_nodenet(nodenet):
	# enter number of nodes to create in each layer
	network_dimensions = [5, 2]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(node_data)
	config.link_nodes(nodenet, link_data)

	# read in MNIST data
	# data = MNIST_file_parser.read()
	# print data.images[0]

	# config.initialize_root_node(nodenet, *root_node_data)
	# config.set_exit_node(nodenet, *exit_node_data)

	# control.run(nodenet)

if __name__ == "__main__":
	build_nodenet(Nodenet())
