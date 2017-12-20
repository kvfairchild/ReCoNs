#!/usr/bin/env python

from recipes.classifier import classifier
from recipes.function_approximator import function_approximator
from nodenet import config
from nodenet.nodenet import Nodenet

def build_nodenet(nodenet):

	# enter nodes per layer
	network_dimensions = [784, 60, 14]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

	return network_dimensions


if __name__ == "__main__":

	nodenet = Nodenet()
	network_dimensions = build_nodenet(nodenet)

	""" CLASSIFIER
	classifier(nodenet, network_dimensions, run_type, pretrain=False, save_net=False)

	An n-layer perceptron classifier for images of handwritten digits and symbols

	network_dimensions (set above in `build_nodenet()`): 
		[784, ..., 10] will train or test on MNIST only
		[784, ..., 14] will train or test on a combination of MNIST and algebra operators
	run_type: "train" or "test"
	pretrain: if True, will run a saved net with the specified dimensions on test data
	save_net: if True, will save a net (in config_specs) after it is finished running
	"""
	# classifier(nodenet, network_dimensions, "test", pretrain=True)

	""" FUNCTION APPROXIMATOR
	function_approximator(nodenet, network_dimensions)

	Takes images of handwritten algebra functions as input and outputs the numeric value 
	of the evaluated function.

	Parses functions into component symbols, then feeds them into a pretrained perceptron
	classifier, which outputs a prediction array for each function.  This array is used 
	to build a Request Confirmation Network (ReCoN), which executes the function. The
	final output is the numeric value of the evaluated function.
	"""
	function_approximator(nodenet, network_dimensions)
