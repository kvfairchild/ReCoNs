#!/usr/bin/env python

""" 
Takes in a folder of images depicting algebra functions and splits them into
individual images of their component symbols. Images are prepared MNIST-style:
20x20 digits centered on a 28x28 canvas.
"""

import numpy as np
import ntpath
import os
from PIL import Image, ImageChops
from pylab import *
from skimage import data, io, filters, segmentation
from skimage.measure import label
from skimage.color import rgb2gray, label2rgb
from skimage.measure import regionprops
import warnings

def function_parser():

	functions = os.path.abspath("data/datasets/functions/function_data")

	symbols = os.path.abspath("data/datasets/functions/symbols")
	if not os.path.exists(symbols):
		os.makedirs(symbols)

	# split function into images of individual symbols
	for filename in os.listdir(functions):
		filepath = os.path.join(functions, filename)
		_split_function(filename, filepath, symbols)

	# clean and resize symbol images
	for subfolder in os.listdir(symbols):
		subfolder = os.path.normpath(os.path.join(symbols, subfolder))
		if os.path.isdir(subfolder):
			for filename in os.listdir(subfolder):
				filepath = os.path.join(subfolder, filename)
				_trim_whitespace(filepath)
				_make_square(filepath)
				_center_image(filepath)

def _split_function(filename, filepath, symbols):
	warnings.filterwarnings("ignore") # silence precision loss warnings

	# Adapted from Yale Digital Humanities Lab utilities for image segmentation tasks  
	# https://github.com/YaleDHLab/image-segmentation/blob/master/british_library_periodicals/segment_periodicals.py#L86

	image = rgb2gray(io.imread(filepath))

	# use Otsu's method to find dividing line between 0 and 255
	val = filters.threshold_otsu(image)
	mask = image < val

	# apply mask to image object
	clean_border = segmentation.clear_border(mask)

	labeled = label(clean_border)

	cropped_images = []
	image_dims = []
	pad = 3
	extra_pad = 10

	for index, region in enumerate(regionprops(labeled)):

		# draw a bounding box and use coordinates to crop
		minr, minc, maxr, maxc = region.bbox

		if maxc - minc > 10 or maxr - minr > 10:

			if minr > extra_pad and maxr < (len(image)-pad):
				cropped_images.append(image[minr-extra_pad:maxr+extra_pad, minc:maxc])
				image_dims.append(minc) # save symbols in left-right order
			else:
				cropped_images.append(image[minr-pad:maxr+pad, minc:maxc])
				image_dims.append(minc) # save symbols in left-right order

	cropped_images = [image for _,image in sorted(zip(image_dims,cropped_images))]

	for index, cropped_image in enumerate(cropped_images):

		function_folder = os.path.join(symbols, os.path.splitext(filename)[0])
		if not os.path.exists(function_folder):
			os.makedirs(function_folder)

		cropped_filename = str(index) + " | " + filename[index] + ".png"
		cropped_filepath = os.path.join(function_folder, cropped_filename)
		io.imsave(cropped_filepath, cropped_image)

def _trim_whitespace(filepath):
	image = Image.open(filepath)
	image_data = np.asarray(image)

	idx = np.where(image_data-65535)[0:2]
	box = map(min,idx)[::-1] + map(max,idx)[::-1]

	trimmed_image = image.crop(box)
	trimmed_image.save(filepath)

def _make_square(filepath):
	image = Image.open(filepath)
	width, height = image.size

	# if image width > height, add vertical whitespace
	# if image height > width, add horizontal whitespace
	if width > height:
		new_size = (width, width)
	elif width < height:
		new_size = (height, height)
	else:
		new_size = (width, height)
	
	canvas = Image.new("I", new_size, 65535) # uint-8 "white" 
	canvas.paste(image, ((new_size[0]-image.size[0])/2, (new_size[1]-image.size[1])/2))
	canvas.save(filepath)

def _center_image(filepath):
	image = Image.open(filepath)

	interim_image = image.resize((20, 20), Image.ANTIALIAS)
	interim_size = interim_image.size

	new_size = (28, 28)
	canvas = Image.new("I", new_size, 65535) 
	canvas.paste(interim_image, ((new_size[0]-interim_size[0])/2, (new_size[1]-interim_size[1])/2))
	canvas.save(filepath)

