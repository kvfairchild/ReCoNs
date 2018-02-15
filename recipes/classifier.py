# -*- coding: utf-8 -*- 

""" CLASSIFIER

An n-layer perceptron classifier for images of handwritten digits and symbols

network_dimensions: [784, ..., 14] 
run_type: "train" or "test"
	"train" will train a new network of the specified dimensions on training data
	"test" will run a saved pretrained net with the specified dimensions on test data
save_net: if True, will save a net (in config_specs) after it is finished running
"""

from datetime import timedelta
import os
import numpy as np
import time
import sys

from data.process_data import *
from nodenet import classifier_config, classifier_control

# Combination of MNIST data and mathematical operators (+, -, ×, ÷)
# Adds 14,220 math ops images to MNIST train data
# Adds 4,696 math ops images to test data	
def classifier(nodenet, network_dimensions, run_type, save_net=False):

	if network_dimensions[0] == 784 and network_dimensions[len(network_dimensions)-1] == 14:
		MNIST_data = parse_data("MNIST", run_type)
		math_ops_data = parse_data("math_ops", run_type)
		data = (MNIST_data, math_ops_data)

		if run_type == "test":
			classifier_config.initialize_net(nodenet, network_dimensions)
			
		_run_classifier(nodenet, run_type, *data)
	
	else:
		raise ValueError("Please enter network dimensions in the form of [784, ..., 14] for classifier.")

	if save_net == True:
		classifier_config.save_weights(nodenet, network_dimensions) # save trained network

def _run_classifier(nodenet, run_type, *data):
	start_time = time.time()

	images, labels = unpack_data(*data)

	# feed images into network
	for i, image in enumerate(images):

		classifier_config.set_activation(nodenet, image)
		classifier_control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))
