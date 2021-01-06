from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ArrayT:
    dims: int
    eltype: any
    size: any

    def __hash__(self):
        return hash((self.dims, self.eltype, self.size))


result_types = defaultdict(lambda a, b: None)

result_types['+'] = lambda a, b: a + b
result_types['-'] = lambda a, b: a - b
result_types['*'] = lambda a, b: a * b
result_types['/'] = lambda a, b: a / b

result_types['<'] = lambda a, b: a < b
result_types['>'] = lambda a, b: a > b
result_types['=='] = lambda a, b: a == b
result_types['!='] = lambda a, b: a != b
result_types['<='] = lambda a, b: a <= b
result_types['>='] = lambda a, b: a >= b


class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent is None:
            return None
        return self.parent.get(name)
