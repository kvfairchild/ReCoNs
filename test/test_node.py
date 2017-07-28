import unittest

from nodenet.node import Node

class MockVector:
	def __init__(self, name):
		self.name = name

test_slot_vector = [MockVector(name="SLOT")]
test_gate_vector = [MockVector(name="GATE")]
test_node = Node("test", test_slot_vector, test_gate_vector, None)

class TestNode(unittest.TestCase):

	def test_constructor(self):
		self.assertEqual(test_node.name, "test")

	def test_get_vectors(self):
		self.assertEqual(test_node.get_slot("SLOT").name, "SLOT")
		self.assertEqual(test_node.get_gate("GATE").name, "GATE")

if __name__ == '__main__':
    unittest.main()
