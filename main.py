#!/usr/bin/env python
from datetime import timedelta
import time
import numpy as np

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser

#from test.input_config import *

def build_nodenet(nodenet):
	# enter nodes per layer
	network_dimensions = [784, 10]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

def parse_data(data_type):
	return MNIST_file_parser.read(data_type)

def run_nodenet(nodenet, data):
	start_time = time.time()

	images = data["images"]
	labels = data["labels"]

	# feed images into network
	for i, image in enumerate(images):

		activation = config.set_activation(nodenet, images[i])
		error_array = control.run(nodenet, labels[i], i)
		config.update_weights(nodenet, activation, error_array, i)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


if __name__ == "__main__":
	nodenet = Nodenet()
	build_nodenet(nodenet)

	# TRAIN
	data = parse_data("training")
	run_nodenet(nodenet, data)

	# TEST
	data = parse_data("testing")
	run_nodenet(nodenet, data)
