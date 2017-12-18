#!/usr/bin/env python

from datetime import timedelta
import os
import numpy as np
import time
import sys

from data.process_data import *
from data.datasets.math_ops import math_ops_data_prep
from function_approximator import function_approximator
from nodenet import config, control
from nodenet.nodenet import Nodenet

def build_nodenet(nodenet):

	# enter nodes per layer
	network_dimensions = [784, 14]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

	return network_dimensions

def run_nodenet(nodenet, run_type, *data):
	start_time = time.time()

	images, labels = unpack_data(*data)

	# feed images into network
	for i, image in enumerate(images):

		config.set_activation(nodenet, image)
		control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


if __name__ == "__main__":

	nodenet = Nodenet()
	network_dimensions = build_nodenet(nodenet)

	# math_ops_data_prep.data_prep()

	# FUNCTION APPROXIMATOR
	function_approximator(nodenet, network_dimensions)

	# # TRAIN
	# MNIST_data = parse_data("MNIST", "training")
	# math_ops_data = parse_data("math_ops", "training")
	# data = (MNIST_data, math_ops_data)
	# run_nodenet(nodenet, "train", *data)
	# config.save_weights(nodenet, network_dimensions) # save trained network

	# # TEST
	# MNIST_data = parse_data("MNIST", "testing")
	# math_ops_data = parse_data("math_ops", "testing")
	# data = (MNIST_data, math_ops_data)
	# run_nodenet(nodenet, "test", *data)

	# PRETRAINED NET
	# MNIST_data = parse_data("MNIST", "testing")
	# math_ops_data = parse_data("math_ops", "testing")
	# data = (MNIST_data, math_ops_data)
	# config.initialize_net(nodenet, network_dimensions)
	# run_nodenet(nodenet, "test", *data)
