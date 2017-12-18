#!/usr/bin/env python

""" 
Uses pretrained perceptron to identify the individual symbols in handwritten 
algebra functions, then feeds them to Request Confirmation Networks (ReCoNs),
which execute the functions as scripts and return the numeric value as output.
"""

import cv2
from nodenet import config, function_config, function_control, recon
from nodenet.nodenet import Nodenet
from data.datasets.functions import symbols_image_prep
import numpy as np
import os
from PIL import Image

def function_approximator(nodenet, network_dimensions):

	# create individual symbol images from function images
	# symbols_image_prep.function_parser()

	symbols = os.path.abspath("data/datasets/functions/symbols")

	# initialize pretrained net to classify symbols
	config.initialize_net(nodenet, network_dimensions)

	for s, subfolder in enumerate(os.listdir(symbols)):
		function = subfolder
		subfolder = os.path.normpath(os.path.join(symbols, subfolder))
		if s == 2:
			if os.path.isdir(subfolder):
				print "Function: ", function
				symbol_array = _classify_symbols(nodenet, subfolder)

				# build ReCoN to execute function
				recon = Nodenet()
				_build_recon(recon, symbol_array)
				_execute_function(recon, symbol_array)

def _classify_symbols(nodenet, subfolder):

	# collect symbol predictions in an array for each function
	symbol_array = []

	for filename in os.listdir(subfolder):
		filepath = os.path.join(subfolder, filename)

		image_index = _classify_symbols.counter
		target_output = filename[-5:-4] # get label from filename (@ len(filename)-5)

		image = np.array(Image.open(filepath))

		# convert uint16 to uint8
		cvuint8 = cv2.convertScaleAbs(image, alpha=(255.0/65535.0))
		# invert pixel values to match training data (0 <-> 255)
		inverse_image = np.invert(cvuint8)

		config.set_activation(nodenet, inverse_image)
		symbol = function_control.run(nodenet, target_output, subfolder, image_index)
		symbol_array.append(symbol)

		_classify_symbols.counter += 1

	return symbol_array

_classify_symbols.counter = 0

def _build_recon(recon, symbol_array):

	node_data = function_config.generate_node_data(symbol_array)
	function_config.add_nodes(recon, node_data)

	link_data = function_config.generate_link_data(recon, symbol_array)
	function_config.link_nodes(recon, link_data)

def _execute_function(recon, symbol_array):

	recon.run_recon(recon)


