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

	MNIST_data = parse_data("MNIST", run_type)

	if network_dimensions[len(network_dimensions)-1] == 10 and network_dimensions[0] == 784:
		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, MNIST_data)
	
	elif network_dimensions[len(network_dimensions)-1] == 14 and network_dimensions[0] == 784:
		math_ops_data = parse_data("math_ops", run_type)
		data = (MNIST_data, math_ops_data)

		if pretrain == True:
			config.initialize_net(nodenet, network_dimensions)
		_run_classifier(nodenet, run_type, *data)
	
	else:
		raise ValueError("Incorrect network dimensions for available classifiers. " +
		"Please enter [784, ... , 10] for MNIST or [784, ... , 14] to include +, -, ×, ÷.")

	if save_net == True:
		config.save_weights(nodenet, network_dimensions) # save trained network

def _run_classifier(nodenet, run_type, *data):
	start_time = time.time()

	images, labels = unpack_data(*data)

	# feed images into network
	for i, image in enumerate(images):

		config.set_activation(nodenet, image)
		control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


	# # TRAIN
	# MNIST_data = parse_data("MNIST", "training")
	# math_ops_data = parse_data("math_ops", "training")
	# data = (MNIST_data, math_ops_data)
	# run_nodenet(nodenet, "train", *data)


	# # TEST
	# MNIST_data = parse_data("MNIST", "testing")
	# math_ops_data = parse_data("math_ops", "testing")
	# data = (MNIST_data, math_ops_data)
	# run_nodenet(nodenet, "test", *data)

	# # PRETRAINED NET
	# MNIST_data = parse_data("MNIST", "testing")
	# math_ops_data = parse_data("math_ops", "testing")
	# data = (MNIST_data, math_ops_data)
	# config.initialize_net(nodenet, network_dimensions)
	# run_nodenet(nodenet, "test", *data)
