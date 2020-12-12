from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ArrayT:
    dims: int
    eltype: any
    size: any

    def __hash__(self):
        return hash((self.dims, self.eltype, self.size))


AnyT = 'any'
IntT = 'int'
FloatT = 'float'
StringT = 'string'
RangeT = 'range'
BoolT = 'bool'


result_types = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: AnyT
        ))
)

for op in '+-*/':
    result_types[op][IntT][IntT] = IntT
    result_types[op][IntT][FloatT] = FloatT
    result_types[op][FloatT][IntT] = FloatT
    result_types[op][FloatT][FloatT] = FloatT

for op in ['<', '<=', '>', '>=', '!=', '==']:
    result_types[op][IntT][IntT] = BoolT
    result_types[op][IntT][FloatT] = BoolT
    result_types[op][FloatT][FloatT] = BoolT
    result_types[op][FloatT][FloatT] = BoolT

for op in ['==', '!=']:
    result_types[op][StringT][StringT] = BoolT


class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)