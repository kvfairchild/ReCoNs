#!/usr/bin/env python
from __future__ import division
from datetime import timedelta
import time
import numpy as np

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
		
def parse_data(data_type):
	return MNIST_file_parser.read(data_type)

def run_nodenet(nodenet, data):
	start_time = time.time()
	error_count = 0

	images = data["images"]
	labels = data["labels"]

	# feed images into network
	for i, image in enumerate(images):

		config.set_activation(nodenet, images[i])

		target_output = labels[i] # one hot label
		target_int = _one_hot_to_int(target_output) # integer label

		output = control.run(nodenet) # one hot output
		predicted_int = _one_hot_to_int(output) # integer output

		error_array = target_output - output

		if predicted_int == target_int:
			print "#", i+1, "prediction: ", predicted_int, " target: ", target_int, "HIT"
		else:
			print "#", i+1, "prediction: ", predicted_int, " target: ", target_int
			error_count += 1
		
		success_rate = "{:.2f}".format((((i+1) - error_count) / (i+1)) * 100)
		print "success rate: ", success_rate, "%"

		config.update_weights(nodenet, error_array, images[i], i)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))

def _one_hot_to_int(one_hot):
	max_output = 0
	max_index = 0

	for node_index, node_output in enumerate(np.nditer(one_hot)):
		if node_output > max_output:
			max_output = node_output
			max_index = node_index

	return max_index


if __name__ == "__main__":
	nodenet = Nodenet()
	build_nodenet(nodenet)

	# TRAIN
	data = parse_data("training")
	run_nodenet(nodenet, data)

	# TEST
	data = parse_data("testing")
	run_nodenet(nodenet, data)
