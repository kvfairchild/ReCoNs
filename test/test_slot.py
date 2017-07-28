import unittest

from nodenet.slot import Slot

class TestSlot(unittest.TestCase):

	def test_constructor(self):
		slot = Slot("test")
		self.assertEqual(slot.name, "test")
		self.assertEqual(slot.activation, 0)

	def test_activation(self):
		slot = Slot("test", 1)
		self.assertEqual(slot.activation, 1)

if __name__ == '__main__':
    unittest.main()
