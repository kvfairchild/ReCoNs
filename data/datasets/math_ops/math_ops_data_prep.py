""" 
Takes in two folders (train/test) of images depicting math operation symbols 
derived from https://www.kaggle.com/xainano/handwrittenmathsymbols and generates 
two sets of numpy arrays: testing and training data and their respective one hot 
encoded labels. Labels are based on filename start character.
"""

from __future__ import division
import matplotlib.image as img
import numpy as np
import os

images_folder = os.path.abspath("data/datasets/math_ops")
train_images = os.path.join(images_folder, "ops_train_files")
test_images = os.path.join(images_folder, "ops_test_files")

# created files
train_data = os.path.join(images_folder, "ops_train_data")
test_data = os.path.join(images_folder, "ops_test_data")
train_labels = os.path.join(images_folder, "ops_train_labels")
test_labels = os.path.join(images_folder, "ops_test_labels")

def data_prep():
	_create_training_set(train_images, train_labels)
	_create_testing_set(test_images, test_labels)

def _create_training_set(train_images, train_labels):
	train_images_list = os.listdir(train_images)
	np.random.shuffle(train_images_list)

	_create_training_labels(train_images_list)

	train_array = []

	for image in train_images_list:
		image_path = os.path.join(train_images, image)
		image_data = img.imread(image_path)
		normalized_image = [(255 - pixel)
		for column in image_data for pixel in column] # add * float(1/255) for micropsi
		train_array.append(normalized_image)
	
	train_array = np.array(train_array)
	np.save(train_data, train_array)


def _create_testing_set(test_images, test_labels):
	test_images_list = os.listdir(test_images)
	np.random.shuffle(test_images_list)

	_create_testing_labels(test_images_list)

	test_array = []

	for image in test_images_list:
		image_path = os.path.join(test_images, image)
		image_data = img.imread(image_path)
		normalized_image = [(255 - pixel) 
		for column in image_data for pixel in column] # add * float(1/255) for micropsi
		test_array.append(normalized_image)
	
	test_array = np.array(test_array)
	np.save(test_data, test_array)

def _create_training_labels(train_images_list):

	train_label_array = []

	for filename in train_images_list:
		if filename.startswith("+"):
			label = np.zeros(14)
			np.put(label, 10, 1)
		elif filename.startswith("-"):
			label = np.zeros(14)
			np.put(label, 11, 1)
		elif filename.startswith("times"):
			label = np.zeros(14)
			np.put(label, 12, 1)
		elif filename.startswith("div"):
			label = np.zeros(14)
			np.put(label, 13, 1)
		else:
			print filename
			raise ValueError("label prefix not recognized")
		train_label_array.append(label)

	np.save(train_labels, train_label_array)

def _create_testing_labels(test_images_list):
	test_label_array = []

	for filename in test_images_list:
		if filename.startswith("+"):
			label = np.zeros(14)
			np.put(label, 10, 1)
		elif filename.startswith("-"):
			label = np.zeros(14)
			np.put(label, 11, 1)
		elif filename.startswith("times"):
			label = np.zeros(14)
			np.put(label, 12, 1)
		elif filename.startswith("div"):
			label = np.zeros(14)
			np.put(label, 13, 1)
		else:
			raise ValueError("label prefix not recognized")
		test_label_array.append(label)

	np.save(test_labels, test_label_array)
