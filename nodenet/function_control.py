#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import division
from itertools import groupby
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

from .nodenet import Nodenet

def run(nodenet, target_output, function):
	output = _step_function(nodenet) # softmax output
	prediction = _get_symbol(output) # predicted symbol

	_pretty_print(prediction, target_output, function)

	_zero_gates(nodenet)

	return prediction
 
def _step_function(nodenet):

	for i, layer in enumerate(nodenet.layers):
		_net_function(nodenet)
		_link_function(nodenet)

		# fetch output from last layer
		if i == len(nodenet.layers)-1:
			output = [gate.activation for node in layer for gate in node.gate_vector]

	return _softmax(output) # apply softmax

# call node function for nodes that received activation
def _net_function(nodenet):
	node_dict = nodenet.node_dict

	for node in node_dict.values():
		for slot in node.slot_vector:
			if slot.activation != 0:
				node.node_function(slot.activation)
				slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function(nodenet):
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				if link.origin_gate.is_active():
					_send_activation_to_target_slot(link)

# HELPER FUNCTIONS

def _pretty_print(prediction, target_output, function):

	if str(prediction) == str(target_output):
		print target_output, ". ", "prediction: ", prediction, "✓"
	else:
		print target_output, ". ", "prediction: ", prediction, "⌧"

def _send_activation_to_target_slot(link):
	activation = link.origin_gate.activation * link.weight
	link.target_slot.activation = link.target_slot.activation + activation

def _softmax(output):
	exp_output = np.exp(output - np.max(output))
	return exp_output / exp_output.sum()

def _one_hot_to_int(one_hot):
	max_output = 0
	max_index = 0

	for node_index, node_output in enumerate(np.nditer(one_hot)):
		if node_output > max_output:
			max_output = node_output
			max_index = node_index

	return max_index

def _zero_gates(nodenet):
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				link.origin_gate.activation = 0

def _get_symbol(output):
	prediction = _one_hot_to_int(output) # integer output

	if prediction <=9:
		return prediction
	elif prediction == 10:
		return "+"
	elif prediction == 11:
		return "-"
	elif prediction == 12:
		return "*"
	elif prediction == 13:
		return "\\"
