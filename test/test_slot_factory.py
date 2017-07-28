import unittest
from testfixtures import Comparison

from nodenet.slot_factory import slot_factory
from nodenet.slot import Slot

class TestSlotFactory(unittest.TestCase):

	def test_factory(self):
		slot_list = slot_factory(["gen", "por", "ret"])
		self.assertTrue(Comparison(Slot, name="gen", activation=0) == slot_list[0])
		self.assertTrue(Comparison(Slot, name="por", activation=0) == slot_list[1])
		self.assertTrue(Comparison(Slot, name="ret", activation=0) == slot_list[2])

	def test_faulty_name(self):
		with self.assertRaises(TypeError):
			slot_factory(["fail"])
			slot_factory(["gen", "fail"])

	def test_empty_list(self):
		slot_list = slot_factory([])
		self.assertEquals(slot_list, [])

if __name__ == '__main__':
    unittest.main()
