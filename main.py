#!/usr/bin/env python

from random import random

from nodenet import nodenet
from nodenet import config
from nodenet.node_factory import node_factory

if __name__ == "__main__":
	nodes = node_factory(["sensor"])
