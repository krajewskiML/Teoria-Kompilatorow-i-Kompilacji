from Tools.synthVisitor import synthVisitor
from Tools.synthParser import synthParser
from Tools.synthLexer import synthLexer
from VariableContainer import VariableContainer
from antlr4 import *


class CustomSynthVisitor(synthVisitor):
    def __init__(self, ):
        super().__init__()
        self.variables = VariableContainer()

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
        children = ctx.children
        children_number = len(children)
        if children_number == 1:
            # IDENTIFIER
            if isinstance(children[0], TerminalNode):
                var_name = children[0].symbol.text
                return self.variables.get_value(var_name)
            # function call
            # value
            if children[0].getRuleIndex() == synthParser.RULE_value:
                return self.visitValue(children[0])
            pass
        elif children_number == 3:
            # parenthesis
            if children[1].getRuleIndex() == synthParser.RULE_expression:
                return self.visitExpression(children[1])
            # multiplication
            if children[1].getRuleIndex() == synthParser.RULE_mult_op:
                sign = self.visitMult_op(children[1])
                if sign == synthParser.MULTIPLICATION:
                    return self.visitExpression(children[0]) * self.visitExpression(children[2])
                if sign == synthParser.DIVISION:
                    return self.visitExpression(children[0]) / self.visitExpression(children[2])
                if sign == synthParser.MODULO:
                    return self.visitExpression(children[0]) % self.visitExpression(children[2])
            # addition
            if children[1].getRuleIndex() == synthParser.RULE_add_op:
                sign = self.visitAdd_op(children[1])
                if sign == synthParser.ADDITION:
                    return self.visitExpression(children[0]) + self.visitExpression(children[2])
                if sign == synthParser.SUBTRACTION:
                    return self.visitExpression(children[0]) - self.visitExpression(children[2])
            # compare
            if children[1].getRuleIndex() == synthParser.RULE_compare_op:
                sign = self.visitCompare_op(children[1])
                if sign == synthParser.EQUALS:
                    return self.visitExpression(children[0]) == self.visitExpression(children[2])
                if sign == synthParser.NOT_EQUALS:
                    return self.visitExpression(children[0]) != self.visitExpression(children[2])
                if sign == synthParser.GT:
                    return self.visitExpression(children[0]) > self.visitExpression(children[2])
                if sign == synthParser.GOET:
                    return self.visitExpression(children[0]) >= self.visitExpression(children[2])
                if sign == synthParser.LT:
                    return self.visitExpression(children[0]) < self.visitExpression(children[2])
                if sign == synthParser.LOET:
                    return self.visitExpression(children[0]) <= self.visitExpression(children[2])
            # bool
            if children[1].getRuleIndex() == synthParser.RULE_bool_op:
                sign = self.visitBool_op(children[1])
                if sign == synthParser.AND:
                    return self.visitExpression(children[0]) and self.visitExpression(children[2])
                if sign == synthParser.OR:
                    return self.visitExpression(children[0]) or self.visitExpression(children[2])

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
        if isinstance(ctx.children[0], TerminalNode):
            var_name = ctx.children[0].symbol.text
            var_value = self.visitExpression(ctx.children[2])
            self.variables.assign_value(var_name, var_value)
        else:
            var_name = self.visitVar_definition(ctx.children[0])
            var_value = self.visitExpression(ctx.children[2])
            self.variables.assign_value(var_name, var_value)

    def visitPrint_statement(self, ctx:synthParser.Print_statementContext):
        value = self.visitExpression(ctx.children[2])
        print(value)

    def visitFunction_call(self, ctx:synthParser.Function_callContext):
        # deepcopy main variables
        # clear variables
        # run function block
        pass

