from .gate import Gate

def gen():
	return Gate("gen", .1)
def por():
	return Gate("por", .2)
def ret():
	return Gate("ret", .3)

gate_transformer = {
	"gen": gen,
	"por": por,
	"ret": ret
}


def gate_factory(gates):
	gate_vector = []
	for gate in gates:
		gate_vector.append(gate_transformer.get(gate)())
	return gate_vector
