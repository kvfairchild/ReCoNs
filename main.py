#!/usr/bin/env python

from nodenet import config

if __name__ == "__main__":
	config.add_nodes([["register1", "register"], ["register2", "register"]])
	config.link_nodes([
		{
			"origin": ["register1", "gen"],
			"target": ["register2", "gen"]
		}
	])
