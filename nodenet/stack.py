class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
    	self.items.append(item)

    	if item in ("+", "-", "*", "/"):
    		self._calculate()

    def pop(self):
    	return self.items.pop()

    def _calculate(self):
    	op, digit2, digit1 = self.pop(), self.pop(), self.pop()
    	
    	if op == "+":
    		result = digit1 + digit2
    	elif op == "-":
    		result = digit1 - digit2
    	elif op == "*":
    		result = digit1 * digit2
    	else:
    		result = digit1 / digit2

    	self.items.append(result)
