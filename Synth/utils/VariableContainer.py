from collections import namedtuple
from typing import Dict

Variable = namedtuple("Variable", ["type", "value"])


class VariableContainer:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}

    def declare_variable(self, name, dtype: type, value=None):
        if name not in self.variables:
            self.variables[name] = Variable(dtype, value)
        else:
            raise Exception(f"{name} is already defined in this scope")

    def assign_value(self, name, value):
        if name not in self.variables:
            raise Exception(f"{name} is not defined in this scope")

        type_of_var = self.variables[name].type
        self.variables[name] = Variable(type_of_var, value)

    def get_value(self, name):
        if name not in self.variables:
            raise Exception(f"{name} is not defined in this scope")

        return self.variables[name].value

    def get_type(self, name):
        if name not in self.variables:
            raise Exception(f"{name} is not defined in this scope")
        return self.variables[name].type

    def remove_variable(self, name):
        self.variables.pop(name)


