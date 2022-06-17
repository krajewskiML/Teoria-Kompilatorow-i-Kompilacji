from Tools.synthVisitor import synthVisitor
from Tools.synthParser import synthParser
from Tools.synthLexer import synthLexer
from VariableContainer import VariableContainer, Variable
from FunctionContainer import FunctionContainer, Function, VariablePlaceholder
from SoundObject import SoundObject
from antlr4 import *

import numpy as np
from copy import deepcopy


class CustomSynthVisitor(synthVisitor):
    def __init__(self, ):
        super().__init__()
        self.variables = VariableContainer()
        self.functions = FunctionContainer()

    def visitValue(self, ctx:synthParser.ValueContext):
        child = ctx.children[0]
        child_type = child.symbol.type
        if child_type == synthLexer.INT:
            return int(child.symbol.text)
        elif synthLexer.FLOAT:
            return float(child.symbol.text)
        elif synthLexer.BOOL:
            return child.symbol.text == 'true'
        else:
            return self.visitChildren(ctx)

    def visitAdd_op(self, ctx:synthParser.Add_opContext):
        child = ctx.children[0]
        return child.symbol.type

    def visitMult_op(self, ctx:synthParser.Mult_opContext):
        child = ctx.children[0]
        return child.symbol.type

    def visitBool_op(self, ctx:synthParser.Bool_opContext):
        child = ctx.children[0]
        return child.symbol.type

    def visitCompare_op(self, ctx:synthParser.Compare_opContext):
        child = ctx.children[0]
        return child.symbol.type

    def visitExpression(self, ctx:synthParser.ExpressionContext):
        # children = ctx.children
        # children_number = len(children)
        # 1 child expected
        child = ctx.children[0]
        # IDENTIFIER
        if isinstance(child, TerminalNode):
            var_name = child.symbol.text
            return self.variables.get_value(var_name)
        if child.getRuleIndex() == synthParser.RULE_logic_expression:
            return self.visitLogic_expression(child)
        if child.getRuleIndex() == synthParser.RULE_math_expression:
            return self.visitMath_expression(child)

    def visitLogic_expression(self, ctx: synthParser.Logic_expressionContext):
        children = ctx.children
        children_number = len(children)
        if children_number == 1:
            if isinstance(children[0], TerminalNode):
                # bool
                if children[0].symbol.type == synthLexer.BOOL:
                    child = ctx.children[0]
                    return child.symbol.text == "true"
                # IDENTIFIER
                var_name = children[0].symbol.text
                if self.variables.get_type(var_name) == bool:
                    return self.variables.get_value(var_name)
                else:
                    raise Exception("Wrong type of variable")
            # function call
            if children[0].getRuleIndex() == synthParser.RULE_function_call:
                return self.visitFunction_call(children[0])
        elif children_number == 3:
            # parenthesis
            if children[1].getRuleIndex() == synthParser.RULE_expression:
                return self.visitExpression(children[1])
            # compare
            if children[1].getRuleIndex() == synthParser.RULE_compare_op:
                sign = self.visitCompare_op(children[1])
                if sign == synthParser.EQUALS:
                    return self.visitMath_expression(children[0]) == self.visitMath_expression(children[2])
                if sign == synthParser.NOT_EQUALS:
                    return self.visitMath_expression(children[0]) != self.visitMath_expression(children[2])
                if sign == synthParser.GT:
                    return self.visitMath_expression(children[0]) > self.visitMath_expression(children[2])
                if sign == synthParser.GOET:
                    return self.visitMath_expression(children[0]) >= self.visitMath_expression(children[2])
                if sign == synthParser.LT:
                    return self.visitMath_expression(children[0]) < self.visitMath_expression(children[2])
                if sign == synthParser.LOET:
                    return self.visitMath_expression(children[0]) <= self.visitMath_expression(children[2])
            # bool
            if children[1].getRuleIndex() == synthParser.RULE_bool_op:
                sign = self.visitBool_op(children[1])
                if sign == synthParser.AND:
                    return self.visitLogic_expression(children[0]) and self.visitLogic_expression(children[2])
                if sign == synthParser.OR:
                    return self.visitLogic_expression(children[0]) or self.visitLogic_expression(children[2])

    def visitMath_expression(self, ctx:synthParser.Math_expressionContext):
        children = ctx.children
        children_number = len(children)
        if children_number == 1:
            if isinstance(children[0], TerminalNode):
                # int
                if children[0].symbol.type == synthLexer.INT:
                    child = ctx.children[0]
                    return int(child.symbol.text)
                # float
                if children[0].symbol.type == synthLexer.FLOAT:
                    child = ctx.children[0]
                    return float(child.symbol.text)
                # IDENTIFIER
                var_name = children[0].symbol.text
                if self.variables.get_type(var_name) in (float, int):
                    return self.variables.get_value(var_name)
                else:
                    raise Exception("Wrong type of variable")
            # function call
            if children[0].getRuleIndex() == synthParser.RULE_function_call:
                return self.visitFunction_call(children[0])
        elif children_number == 3:
            # parenthesis
            if children[1].getRuleIndex() == synthParser.RULE_math_expression:
                return self.visitMath_expression(children[1])
            # multiplication
            if children[1].getRuleIndex() == synthParser.RULE_mult_op:
                sign = self.visitMult_op(children[1])
                if sign == synthParser.MULTIPLICATION:
                    return self.visitMath_expression(children[0]) * self.visitMath_expression(children[2])
                if sign == synthParser.DIVISION:
                    return self.visitMath_expression(children[0]) / self.visitMath_expression(children[2])
                if sign == synthParser.MODULO:
                    return self.visitMath_expression(children[0]) % self.visitMath_expression(children[2])
            # addition
            if children[1].getRuleIndex() == synthParser.RULE_add_op:
                sign = self.visitAdd_op(children[1])
                if sign == synthParser.ADDITION:
                    return self.visitMath_expression(children[0]) + self.visitMath_expression(children[2])
                if sign == synthParser.SUBTRACTION:
                    return self.visitMath_expression(children[0]) - self.visitMath_expression(children[2])

    def visitType(self, ctx:synthParser.TypeContext):
        variable_type = eval(ctx.children[0].symbol.text)
        return variable_type

    def visitVar_definition(self, ctx:synthParser.Var_definitionContext):
        variable_type = self.visitType(ctx.children[0])
        variable_name = ctx.children[1].symbol.text
        self.variables.declare_variable(variable_name, variable_type)
        return variable_name

    def visitVar_definition_assignment(self, ctx:synthParser.Var_definition_assignmentContext):
        # pre declared variable
        if len(ctx.children) == 3:
            var_name = ctx.children[0].symbol.text
            var_value = self.visitExpression(ctx.children[2])
            self.variables.assign_value(var_name, var_value)
        else:
            dtype = eval(ctx.children[0].symbol.text)
            if dtype == bool:
                value = self.visitLogic_expression(ctx.children[3])
                var_name = ctx.children[1].symbol.text
                self.variables.declare_variable(var_name, dtype, value)
            elif dtype == float:
                value = self.visitMath_expression(ctx.children[3])
                var_name = ctx.children[1].symbol.text
                self.variables.declare_variable(var_name, dtype, value)
            elif dtype == int:
                value = self.visitMath_expression(ctx.children[3])
                var_name = ctx.children[1].symbol.text
                self.variables.declare_variable(var_name, dtype, value)

    def visitPrint_statement(self, ctx: synthParser.Print_statementContext):
        value = self.visitExpression(ctx.children[2])
        print(value)

    def visitWhile_statement(self, ctx: synthParser.While_statementContext):
        children = ctx.children
        condition = self.visitLogic_expression(children[2])
        while condition:
            self.visitBlock(children[4])
            condition = self.visitLogic_expression(children[2])

    def visitIf_statement(self, ctx: synthParser.If_statementContext):
        children = ctx.children
        # does it contain else
        else_present = children[-2].symbol.text == "else"
        # 5 + n * 5 + 2?
        first_condition = self.visitLogic_expression(children[2])
        if first_condition:
            self.visitBlock(children[4])
            return
        elifs_number = (len(children) - 5 - 2) // 5 if else_present else (len(children) - 5) // 5
        indices_of_other_conditions = [7 + i * 5 for i in range(elifs_number)]
        for idx_logic_condition in indices_of_other_conditions:
            condition = self.visitLogic_expression(children[idx_logic_condition])
            if condition:
                self.visitBlock(children[idx_logic_condition + 2])
                return
        if else_present:
            self.visitBlock(children[-1])

    def visitFor_statement(self, ctx: synthParser.For_statementContext):
        children = ctx.children
        var_name = children[2].symbol.text
        self.variables.declare_variable(var_name, float)
        for n in self.visitRange_statement(children[4]):
            self.variables.assign_value(var_name, n)
            self.visitBlock(children[6])
        self.variables.remove_variable(var_name)

    def visitRange_statement(self, ctx: synthParser.Range_statementContext):
        children = ctx.children

        if len(children) == 4:
            return np.arange(0.0,
                             float(self.visitMath_expression(children[2])),
                             1.0)
        if len(children) == 6:
            return np.arange(float(self.visitMath_expression(children[2])),
                             float(self.visitMath_expression(children[4])),
                             1.0)
        if len(children) == 8:
            return np.arange(float(self.visitMath_expression(children[2])),
                             float(self.visitMath_expression(children[4])),
                             float(self.visitMath_expression(children[6])))

    def visitParameters(self, ctx:synthParser.ParametersContext):
        children = ctx.children
        num_of_expressions = len(children) // 2 + 1 if children else 0
        return [self.visitExpression(children[i*2]) for i in range(num_of_expressions)]

    def visitFunction_call(self, ctx: synthParser.Function_callContext):
        children = ctx.children
        # deepcopy main variables
        outer_scope_variables = deepcopy(self.variables)
        parameters = self.visitParameters(children[2])
        # clear variables
        self.variables = VariableContainer()
        # replace variables by those provided as parameters
        func_to_run = self.functions.get_function(children[0].symbol.text)
        for var_place_holder, param in zip(func_to_run.variables, parameters):
            if not var_place_holder.type == type(param):
                raise ValueError("Wrong type of expression")
            self.variables.declare_variable(var_place_holder.name, var_place_holder.type, param)
        # run function block
        return_val = self.visitReturn_block(func_to_run.run_node)
        self.variables = outer_scope_variables
        return return_val

    def visitFunction(self, ctx:synthParser.FunctionContext):
        children = ctx.children
        variable_type = self.visitType(children[0])
        variable_name = children[1].symbol.text
        return_block = children[-1]
        # 0 1 2 (3) 4 (5) 6 7
        num_of_variables = (len(children) - 5) // 2 + 1 if len(children) > 5 else 0
        variables = [
            VariablePlaceholder(children[3+i*2].children[1].symbol.text, self.visitType(children[3+i*2].children[0]))
            for i in range(num_of_variables)
        ]
        func = Function(variables, variable_type, return_block)
        self.functions.declare_function(variable_name, func)

    def visitReturn_block(self, ctx:synthParser.Return_blockContext):
        children = ctx.children
        num_of_lines = len(children) - 5
        for i in range(num_of_lines):
            self.visitLine(children[i + 1])

        return self.visitExpression(children[-3])

    def visitSequence_constructor(self, ctx:synthParser.Sequence_constructorContext):
        children = ctx.children
        num_of_expressions = (len(children) - 2) // 2 + 1 if (len(children) - 2) > 0 else 0
        # [ a , b, c ]
        expressions_indices = [1 + i * 2 for i in range(num_of_expressions)]
        expressions = [self.visitSound_expression(children[idx]) for idx in expressions_indices]

    def visitSound_expression(self, ctx:synthParser.Sound_expressionContext):
        children = ctx.children
        if len(children):
            return self.visitSound_expression(children[1])
        else:
            child = children[0]
            if isinstance(child, TerminalNode):
                var_name = child.symbol.text
                return self.variables.get_value(var_name)
            if child.getRuleIndex() == synthParser.RULE_synth_constructor:
                a = 0