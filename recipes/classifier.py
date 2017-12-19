#!/usr/bin/env python
# -*- coding: utf-8 -*- 

""" CLASSIFIER

An n-layer perceptron classifier for images of handwritten digits and symbols

network_dimensions: 
	[784, ..., 10] will train or test on MNIST only
	[784, ..., 14] will train or test on a combination of MNIST and algebra operators
run_type: "train" or "test"
pretrain: if True, will run a saved net with the specified dimensions on test data
save_net: if True, will save a net (in config_specs) after it is finished running
"""

from datetime import timedelta
import os
import numpy as np
import time
import sys

from data.process_data import *
from nodenet import config, control

def classifier(nodenet, network_dimensions, run_type, pretrain=False, save_net=False):

	# MNIST data only
	# 60,000 training images, 10,000 testing images
	if network_dimensions[len(network_dimensions)-1] == 10 and network_dimensions[0] == 784:
		MNIST_data = parse_data("MNIST", run_type)
		images = MNIST_data["images"]
		labels = MNIST_data["labels"]
		data = (images, labels)

		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, "MNIST", *data)

	# Combination of MNIST data and mathematical operators (+, -, ×, ÷)
	# Adds 14,092 math ops images to train data and 4,697 math ops images to test data	
	elif network_dimensions[len(network_dimensions)-1] == 14 and network_dimensions[0] == 784:
		MNIST_data = parse_data("MNIST", run_type, math_ops=True)
		math_ops_data = parse_data("math_ops", run_type)
		data = (MNIST_data, math_ops_data)

		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, "math_ops", *data)
	
	else:
		raise ValueError("Incorrect network dimensions for available classifiers. " +
		"Please enter [784,...,10] for MNIST (0-9) or [784,...,14] to include +, -, ×, ÷.")

	if save_net == True:
		config.save_weights(nodenet, network_dimensions) # save trained network

def _run_classifier(nodenet, run_type, dataset, *data):
	start_time = time.time()

	if dataset == "math_ops":
		images, labels = unpack_data(*data)
	else:
		images = data[0]
		labels = data[1]

	# feed images into network
	for i, image in enumerate(images):

		config.set_activation(nodenet, image)
		control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))
