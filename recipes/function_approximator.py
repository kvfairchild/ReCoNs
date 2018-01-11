#!/usr/bin/env python

""" FUNCTION APPROXIMATOR

Takes images of handwritten algebra functions as input and outputs the numeric value 
of the evaluated function.

Parses functions into component symbols, then feeds them into a pretrained perceptron
classifier, which outputs a prediction array for each function.  This array is used 
to build a Request Confirmation Network (ReCoN), which executes the function. The
final output is the numeric value of the evaluated function.
"""

import cv2
from nodenet import config, function_control, recon_config, recon_control
from nodenet.nodenet import Nodenet
from data.datasets.functions import symbols_image_prep
import numpy as np
import os
from PIL import Image

def function_approximator(nodenet, network_dimensions):

	# create individual symbol images from function images
	# symbols_image_prep.function_parser()

	symbols = os.path.abspath("data/datasets/functions/symbols")

	# initialize pretrained classifier net
	config.initialize_net(nodenet, network_dimensions)

	# classify all symbol images in function folder
	for s, subfolder in enumerate(os.listdir(symbols)):
		function = subfolder
		subfolder = os.path.normpath(os.path.join(symbols, subfolder))
		if s == 3:
			if os.path.isdir(subfolder):
				print "\nFunction: ", function
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

		target_output = filename[-5:-4] # get label from filename (@ len(filename)-5)

		image = np.array(Image.open(filepath))

		# convert uint16 to uint8
		cvuint8 = cv2.convertScaleAbs(image, alpha=(255.0/65535.0))
		# invert pixel values to match training data (0 <-> 255)
		inverse_image = np.invert(cvuint8)

		config.set_activation(nodenet, inverse_image)
		symbol = function_control.run(nodenet, target_output, subfolder)
		symbol_array.append(symbol)

	return symbol_array

def _build_recon(recon, symbol_array):

	node_data = recon_config.generate_node_data(symbol_array)
	recon_config.add_nodes(recon, node_data)

	link_data = recon_config.generate_link_data(recon, symbol_array)
	recon_config.link_nodes(recon, link_data)

def _execute_function(recon, symbol_array):

	recon_control.run(recon, symbol_array)


