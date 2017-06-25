#!/usr/bin/env python

import os.path

f = open(os.path.join(os.pardir, "input_config.txt"), "r")

str = f.read()
print str
