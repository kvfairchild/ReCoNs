import numbers

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
    	self.items.append(item)

    	if item in ("+", "-", "*", "\\") and len(self.items) >= 3:
    		self._calculate()

    def pop(self):
    	return self.items.pop()

    def _calculate(self):
    	op, digit2, digit1 = self.pop(), self.pop(), self.pop()
        print "op: ", op, "digit2: ", digit2, "digit1: ", digit1

        if not all((isinstance(digit1, numbers.Number), isinstance(digit2, numbers.Number))):
            raise ValueError("incorrect values on stack for function calculation")
            return
    	
    	if op == "+":
    		result = digit1 + digit2
    	elif op == "-":
    		result = digit1 - digit2
    	elif op == "*":
    		result = digit1 * digit2
    	else:
    		result = digit1 / digit2

        if not isinstance(result, numbers.Number):
            raise ValueError("incorrect values on stack for function calculation")
            return

    	self.items.append(result)
