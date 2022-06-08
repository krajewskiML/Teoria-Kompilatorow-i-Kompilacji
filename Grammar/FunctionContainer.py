from collections import namedtuple
from typing import Dict
from VariableContainer import Variable

VariablePlaceholder = namedtuple("VariablePlaceHolder", ["name", "type"])

class Function:
    def __init__(self, variables, return_type, run_node):
        self.variables = variables
        self.return_type = return_type
        self.run_node = run_node


class FunctionContainer:
    def __init__(self):
        self.functions: Dict[str, Function] = {}

    def declare_function(self, name, function):
        if name not in self.functions:
            self.functions[name] = function
        else:
            raise Exception(f"{name} is already defined")

    def get_function(self, name):
        if name not in self.functions:
            raise Exception(f"{name} is not defined")

        return self.functions[name]



