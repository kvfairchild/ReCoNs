#!/usr/bin/env python

""" 
Feeds handwritten algebra functions to pretrained perceptron to identify their 
subcomponent symbols and output the final value using Request Confirmation Networks
(ReCoNs) to execute the relevant scripts.
"""

import cv2
from nodenet import config, function_control
from data.datasets.functions import symbols_image_prep
import numpy as np
import os
from PIL import Image
from skimage import img_as_ubyte

def function_approximator(nodenet, network_dimensions):
	symbols = os.path.abspath("data/datasets/functions/symbols")

	config.initialize_net(nodenet, network_dimensions)

	# create symbols from functions
	# symbols_image_prep.function_parser()

	for s, subfolder in enumerate(os.listdir(symbols)):
		subfolder = os.path.normpath(os.path.join(symbols, subfolder))
		if s == 2:
			if os.path.isdir(subfolder):
				function = subfolder
				symbol_array = _run_approximator(nodenet, subfolder, function)

def _run_approximator(nodenet, subfolder, function):

	symbol_array = []

	for filename in os.listdir(subfolder):
		filepath = os.path.join(subfolder, filename)

		image_index = _run_approximator.counter
		target_output = filename[-5:-4]

		image = np.array(Image.open(filepath))
		cvuint8 = cv2.convertScaleAbs(image, alpha=(255.0/65535.0))
		inverse_image = np.invert(cvuint8)

		config.set_activation(nodenet, inverse_image)
		symbol = function_control.run(nodenet, target_output, function, image_index)
		symbol_array.append(symbol)

		_run_approximator.counter += 1

_run_approximator.counter = 0


