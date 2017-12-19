#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from datetime import timedelta
import os
import numpy as np
import time
import sys

from data.process_data import *
from nodenet import config, control


def classifier(nodenet, network_dimensions, run_type, pretrain=False, save_net=False):

	if network_dimensions[len(network_dimensions)-1] == 10 and network_dimensions[0] == 784:
		MNIST_data = parse_data("MNIST", run_type)
		images = MNIST_data["images"]
		labels = MNIST_data["labels"]
		data = (images, labels)

		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, "MNIST", *data)
	
	elif network_dimensions[len(network_dimensions)-1] == 14 and network_dimensions[0] == 784:
		MNIST_data = parse_data("MNIST", run_type, math_ops=True)
		math_ops_data = parse_data("math_ops", run_type)
		data = (MNIST_data, math_ops_data)

		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, "math_ops", *data)
	
	else:
		raise ValueError("Incorrect network dimensions for available classifiers. " +
		"Please enter [784, ... , 10] for MNIST or [784, ... , 14] to include +, -, ×, ÷.")

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
