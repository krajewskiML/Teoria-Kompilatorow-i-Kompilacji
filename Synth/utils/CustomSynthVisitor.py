from typing import Union, List

from Synth.utils.MusicHandler import MusicHandler
from Tools.synthVisitor import synthVisitor
from Tools.synthParser import synthParser
from Tools.synthLexer import synthLexer
from Synth.utils.VariableContainer import VariableContainer
from Synth.utils.FunctionContainer import FunctionContainer, Function, VariablePlaceholder
from Synth.utils.SoundObject import SoundObject, SOUND_TYPES
from antlr4 import *

import numpy as np
from copy import deepcopy


class CustomSynthVisitor(synthVisitor):
    def __init__(self, filename: str):
        super().__init__()
        self.variables = VariableContainer()
        self.functions = FunctionContainer()
        self.filename = filename
        self.music_handler = None

    def visitFunction_final(self, ctx:synthParser.Function_finalContext):
        children = ctx.children
        nchannel = self.visitNchannel_definition(children[1])
        duration = self.visitDuration_definition(children[3])

        self.music_handler = MusicHandler(nchannel, duration, self.filename)

        self.visitBlock(children[4])

        self.music_handler.compile()

    def visitNchannel_definition(self, ctx:synthParser.Nchannel_definitionContext):
        child = ctx.children[2]
        return int(child.symbol.text)

    def visitDuration_definition(self, ctx:synthParser.Duration_definitionContext):
        child = ctx.children[2]
        return int(child.symbol.text)

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
        if child.getRuleIndex() == synthParser.RULE_function_call:
            return self.visitFunction_call(child)
        if child.getRuleIndex() == synthParser.RULE_sound_expression:
            return self.visitSound_expression(child)
        if child.getRuleIndex() == synthParser.RULE_sequence_expression:
            return self.visitSequence_expression(child)

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
                func_name = children[0].symbol.text
                if self.functions.get_type(func_name) == bool:
                    return self.visitFunction_call(children[0])
                else:
                    raise Exception("Wrong type of return variable")
        elif children_number == 3:
            # parenthesis
            if children[1].getRuleIndex() == synthParser.RULE_logic_expression:
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
                func_name = children[0].symbol.text
                if self.functions.get_type(func_name) in (float, int):
                    return self.visitFunction_call(children[0])
                else:
                    raise Exception("Wrong type of return variable")
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
        if ctx.children[0].symbol.text in ["sound", "synth"]:
            return SoundObject
        if ctx.children[0].symbol.text == "seq":
            return list
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
            var_name = ctx.children[1].symbol.text
            type_name = ctx.children[0].symbol.text
            if type_name in SOUND_TYPES:
                value = self.visitSound_expression(ctx.children[3])
                self.variables.declare_variable(var_name, SoundObject, value)
                return
            if type_name == "seq":
                value = self.visitSequence_expression(ctx.children[3])
                self.variables.declare_variable(var_name, list, value)
                return
            dtype = eval(type_name)
            if dtype == bool:
                value = self.visitLogic_expression(ctx.children[3])
                self.variables.declare_variable(var_name, dtype, value)
            elif dtype == float:
                value = self.visitMath_expression(ctx.children[3])
                self.variables.declare_variable(var_name, dtype, value)
            elif dtype == int:
                value = self.visitMath_expression(ctx.children[3])
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
        return expressions

    def visitSound_expression(self, ctx:synthParser.Sound_expressionContext):
        children = ctx.children
        if len(children) == 3:
            return self.visitSound_expression(children[1])
        else:
            child = children[0]
            if isinstance(child, TerminalNode):
                var_name = child.symbol.text

                # file name
                if child.symbol.type == synthParser.SOUND:
                    file_dict = {"filename": var_name}
                    a = SoundObject(**file_dict)
                    return a
                # variable
                if self.variables.get_type(var_name) == SoundObject:
                    return self.variables.get_value(var_name)
                else:
                    raise Exception("Wrong type of variable")
            # function call
            if child.getRuleIndex() == synthParser.RULE_function_call:
                func_name = child.symbol.text
                if self.functions.get_type(func_name) == SoundObject:
                    return self.visitFunction_call(child)
                else:
                    raise Exception("Wrong type of return variable")
            #
            if child.getRuleIndex() == synthParser.RULE_synth_constructor:
                a = self.visitSynth_constructor(child)
                return a
            if child.getRuleIndex() == synthParser.RULE_sound_constructor:
                a = self.visitSound_constructor(child)
                return a

    def visitSynth_constructor(self, ctx:synthParser.Synth_constructorContext):
        children = ctx.children
        params = [self.visitSynth_params(child) for child in children if not isinstance(child, TerminalNode) and child.getRuleIndex() == synthParser.RULE_synth_params]
        synth_type = self.visitSynth_name(children[0])
        duration = self.visitMath_expression(children[-1])
        synth_dict = {
            "type": synth_type,
            "properties": {
                prop[0]: prop[1]
                for prop in params
            },
            "duration": duration
        }
        return SoundObject(**synth_dict)

    def visitSound_constructor(self, ctx:synthParser.Sound_constructorContext):
        children = ctx.children
        filename = children[0].symbol.text
        duration = self.visitMath_expression(children[2])
        sound_dict = {
            "filename": filename,
            "duration": duration
        }
        return SoundObject(**sound_dict)

    def visitSynth_params(self, ctx:synthParser.Synth_paramsContext):
        children = ctx.children
        return children[0].symbol.text, float(children[2].symbol.text)

    def visitSynth_name(self, ctx:synthParser.Synth_nameContext):
        child = ctx.children[0]
        return child.symbol.text

    def visitSequence_expression(self, ctx:synthParser.Sequence_expressionContext):
        children = ctx.children
        # length 1
        if len(children) == 1:
            child = children[0]
            # IDENTIFIER
            if isinstance(child, TerminalNode):
                var_name = child.symbol.text
                if self.variables.get_type(var_name) in (SoundObject, list):
                    return self.variables.get_value(var_name)
                else:
                    raise Exception("Wrong type of variable")
            # sequence constructor
            if child.getRuleIndex() == synthParser.RULE_sequence_constructor:
                return self.visitSequence_constructor(child)
            # function call
            if child.getRuleIndex() == synthParser.RULE_function_call:
                func_name = child.children[0].symbol.text
                if self.functions.get_type(func_name) in (SoundObject, list):
                    return self.visitFunction_call(child)
                else:
                    raise Exception("Wrong type of return variable")
        # length 3
        # sequence in parenthesis
        if isinstance(children[0], TerminalNode) and children[0].symbol.type == synthParser.LP:
            return self.visitSequence_expression(children[1])
        # operations on two things

        # underlying is identifier
        if isinstance(children[0].children[0], TerminalNode) and len(children[0].children) == 1:
            first_arg = self.variables.get_value(children[0].children[0].symbol.text)
        elif children[0].getRuleIndex() == synthParser.RULE_sound_expression:
            first_arg = self.visitSound_expression(children[0])
        elif children[0].getRuleIndex() == synthParser.RULE_sequence_expression:
            first_arg = self.visitSequence_expression(children[0])
        else:
            first_arg = self.visitMath_expression(children[0])

        # underlying is identifier
        if isinstance(children[2].children[0], TerminalNode) and len(children[2].children) == 1:
            try:
                second_arg = self.visitMath_expression(children[2])
            except:
                second_arg = self.variables.get_value(children[2].children[0].symbol.text)
        elif children[0].getRuleIndex() == synthParser.RULE_sound_expression:
            second_arg = self.visitSound_expression(children[2])
        elif children[0].getRuleIndex() == synthParser.RULE_sequence_expression:
            second_arg = self.visitSequence_expression(children[2])


        if isinstance(children[1], TerminalNode) and children[1].symbol.type == synthParser.ADDITION:
            if isinstance(first_arg, SoundObject) and isinstance(second_arg, SoundObject):
                return [first_arg, second_arg]
            if isinstance(first_arg, list) and isinstance(second_arg, list):
                return first_arg + second_arg
        if isinstance(children[1], TerminalNode) and children[1].symbol.type == synthParser.MULTIPLICATION:
            if isinstance(first_arg, SoundObject) and isinstance(second_arg, (int, float)):
                return first_arg * second_arg
            if isinstance(second_arg, SoundObject) and isinstance(first_arg, (int, float)):
                return second_arg * first_arg
            if isinstance(first_arg, list) and isinstance(second_arg, (int, float)):
                return self.seq_multiplication(first_arg, second_arg)
            if isinstance(second_arg, list) and isinstance(first_arg, (int, float)):
                return self.seq_multiplication(second_arg, first_arg)

        raise Exception("Wrong parameters for creating a sequence")

    def seq_multiplication(self, seq: List, multiplier: Union[float, int]):
        if multiplier < 0:
            raise ValueError("Sequence must be multiplied by number greater than zero")

        if isinstance(multiplier, int):
            return seq * multiplier
        else:
            whole = int(multiplier)
            partial = multiplier - whole
            seq_len = sum(sound.duration for sound in seq)
            required_len = partial * seq_len
            sounds = []
            for sound in seq:
                current_len = sum(soundy.duration for soundy in sounds)
                if current_len + sound.duration < required_len:
                    sounds.append(sound)
                else:
                    missing = required_len - current_len
                    fraction = missing / sound.duration
                    sounds.append((sound * fraction)[0])

                if current_len == required_len:
                    break
            return self.seq_multiplication(seq, whole) + sounds

    def visitChannel_addition(self, ctx:synthParser.Channel_additionContext):
        children = ctx.children
        channel = int(children[0].symbol.text[1:])

        if isinstance(children[2], TerminalNode):
            var_name = children[2].symbol.text
            if self.variables.get_type(var_name) in (SoundObject, list):
                sound = self.variables.get_value(var_name)
                self.music_handler.add_to_channel(channel, sound)
                return
            else:
                raise Exception("Wrong type of variable")

        if children[2].getRuleIndex() == synthParser.RULE_sequence_expression:
            sound = self.visitSequence_expression(children[2])
        if children[2].getRuleIndex() == synthParser.RULE_sound_expression:
            sound = self.visitSound_expression(children[2])

        self.music_handler.add_to_channel(channel, sound)
