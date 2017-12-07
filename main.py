#!/usr/bin/env python
from datetime import timedelta
import os
import numpy as np
import time
import sys

from datasets import join_sets
from datasets.math_ops.data_prep import data_prep
from datasets.math_ops import image_prep

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser, MNIST_micropsi_file_parser, math_ops_file_parser

def build_nodenet(nodenet):

	# enter nodes per layer
	network_dimensions = [784, 14]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

	return network_dimensions

def parse_data(data_type, run_type):
	if data_type == "MNIST":
		return MNIST_file_parser.read(run_type)
	elif data_type == "MNIST_micropsi":
		return MNIST_micropsi_file_parser.read(run_type)
	else:
		return math_ops_file_parser.read(run_type)

def run_nodenet(nodenet, MNIST_data, math_ops_data, run_type):
	start_time = time.time()

	MNIST_images = MNIST_data["images"]
	MNIST_labels = MNIST_data["labels"]

	math_ops_images = math_ops_data["images"]
	math_ops_labels = math_ops_data["labels"]

	combined_set = join_sets.combine(MNIST_images, MNIST_labels, 
		math_ops_images, math_ops_labels)

	images = combined_set[0]
	labels = combined_set[1]

	# feed images into network
	for i, image in enumerate(images):

	  config.set_activation(nodenet, image)
	  control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


if __name__ == "__main__":

	nodenet = Nodenet()
	network_dimensions = build_nodenet(nodenet)

	image_prep.read()

	# TRAIN
	# MNIST_data = parse_data("MNIST", "training")
	# math_ops_data = parse_data("math_ops", "training")
	# run_nodenet(nodenet, MNIST_data, math_ops_data, "train")
	# config.save_weights(nodenet, network_dimensions) # save trained network

	# TEST
	# MNIST_data = parse_data("MNIST", "testing")
	# math_ops_data = parse_data("math_ops", "testing")
	# run_nodenet(nodenet, MNIST_data, math_ops_data, "test")

	# PRETRAINED NET FOR FUNCTIONS
	# functions = 
	# config.initialize_net(nodenet, network_dimensions)
	# run_nodenet(nodenet, functions, "test")
