#!/usr/bin/env python

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser

from datetime import timedelta
import time
import numpy as np

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
	start_time = time.time()
	error_count = 0

	images = data["images"]
	labels = data["labels"]

	# for i, image in enumerate(images):
	i = 0
	while i < 50:

		config.set_activation(nodenet, images[i])

		target_output = labels[i] # one hot encoded label
		target_int = _one_hot_to_int(target_output) # integer label

		output = control.run(nodenet) # one hot encoded output
		predicted_int = _one_hot_to_int(output) # integer output

		error_array = target_output - output

		if predicted_int == target_int:
			print i, "prediction: ", predicted_int, " target: ", target_int, "HIT"
		else:
			print i, "prediction: ", predicted_int, " target: ", target_int
			error_count += 1

		config.update_weights(nodenet, error_array, images[i])

	success_rate = (error_count / len(images)) * 100
	print "success rate: ", success_rate
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

	data = parse_data()
	train(nodenet, data)
