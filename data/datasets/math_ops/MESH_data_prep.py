""" 
Takes in a folder of test images depicting math operation symbols 
derived from https://www.kaggle.com/xainano/handwrittenmathsymbols 
and generates a MicroPsi MESH flownode-compatible numpy array of
testing data and one hot encoded labels. Labels are based on 
filename start character.

This math operators array is combined with MESH-compatible MNIST
data in the form of a npz file, which can be used as a dataset 
environment in MicroPsi.
"""

from __future__ import division
import matplotlib.image as img
import numpy as np
import os

from ...file_parsers import MNIST_micropsi_fp as fp

math_ops_folder = os.path.abspath("data/datasets/math_ops")
train_images = os.path.join(math_ops_folder, "ops_train_files")

old_MESH = os.path.join(math_ops_folder, "possible_mislabel_mathops_allinone.npz")
new_MESH = os.path.join(math_ops_folder, "mathops_allinone_onehot.npz")

# created files
allinone = os.path.join(math_ops_folder, "mathops_allinone_onehot.npz")

def data_prep():
	ops_images, ops_labels = _create_training_set(train_images)
	_join_sets(ops_images, ops_labels)
	
def _create_training_set(train_images):
	train_images_list = os.listdir(train_images)
	np.random.shuffle(train_images_list)

	train_label_array = _create_training_labels(train_images_list)

	train_images_array = []

	for image in train_images_list:
		image_path = os.path.join(train_images, image)
		image_data = img.imread(image_path)
		normalized_image = [(255 - pixel) * float(1/255)
		for column in image_data for pixel in column]
		train_images_array.append(normalized_image)

	return np.array(train_images_array), train_label_array

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

	return train_label_array

# combine MNIST data set with math operation symbols
def _join_sets(ops_images, ops_labels):

	MNIST_data = fp.read()
	MNIST_images = MNIST_data["images"]
	MNIST_labels = MNIST_data["labels"]
	MNIST = zip(MNIST_images, MNIST_labels)

	math_ops = zip(ops_images, ops_labels)

	combined_zip = np.append(MNIST, math_ops, axis=0)

	np.random.shuffle(combined_zip)

	combined_images = [image for image, label in combined_zip]
	combined_labels = [label for image, label in combined_zip]

	np.savez(new_MESH, x=combined_images, y=combined_labels)
