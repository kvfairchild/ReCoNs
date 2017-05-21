from .slot import Slot

def gen():
	return Slot("gen", .1)
def por():
	return Slot("por", .2)
def ret():
	return Slot("ret", .3)

slot_transformer = {
	"gen": gen,
	"por": por,
	"ret": ret
}


def slot_factory(slot_name_list):
	slot_vector = []
	for slot in slot_name_list:
		slot_vector.append(slot_transformer.get(slot)())
	return slot_vector
