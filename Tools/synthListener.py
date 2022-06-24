# Generated from D:/Projekty/learningPytest/Kompilatorki/Synth\synth.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .synthParser import synthParser
else:
    from synthParser import synthParser

# This class defines a complete listener for a parse tree produced by synthParser.
class synthListener(ParseTreeListener):

    # Enter a parse tree produced by synthParser#program.
    def enterProgram(self, ctx:synthParser.ProgramContext):
        pass

    # Exit a parse tree produced by synthParser#program.
    def exitProgram(self, ctx:synthParser.ProgramContext):
        pass


    # Enter a parse tree produced by synthParser#function.
    def enterFunction(self, ctx:synthParser.FunctionContext):
        pass

    # Exit a parse tree produced by synthParser#function.
    def exitFunction(self, ctx:synthParser.FunctionContext):
        pass


    # Enter a parse tree produced by synthParser#return_block.
    def enterReturn_block(self, ctx:synthParser.Return_blockContext):
        pass

    # Exit a parse tree produced by synthParser#return_block.
    def exitReturn_block(self, ctx:synthParser.Return_blockContext):
        pass


    # Enter a parse tree produced by synthParser#function_final.
    def enterFunction_final(self, ctx:synthParser.Function_finalContext):
        pass

    # Exit a parse tree produced by synthParser#function_final.
    def exitFunction_final(self, ctx:synthParser.Function_finalContext):
        pass


    # Enter a parse tree produced by synthParser#nchannel_definition.
    def enterNchannel_definition(self, ctx:synthParser.Nchannel_definitionContext):
        pass

    # Exit a parse tree produced by synthParser#nchannel_definition.
    def exitNchannel_definition(self, ctx:synthParser.Nchannel_definitionContext):
        pass


    # Enter a parse tree produced by synthParser#duration_definition.
    def enterDuration_definition(self, ctx:synthParser.Duration_definitionContext):
        pass

    # Exit a parse tree produced by synthParser#duration_definition.
    def exitDuration_definition(self, ctx:synthParser.Duration_definitionContext):
        pass


    # Enter a parse tree produced by synthParser#block.
    def enterBlock(self, ctx:synthParser.BlockContext):
        pass

    # Exit a parse tree produced by synthParser#block.
    def exitBlock(self, ctx:synthParser.BlockContext):
        pass


    # Enter a parse tree produced by synthParser#line.
    def enterLine(self, ctx:synthParser.LineContext):
        pass

    # Exit a parse tree produced by synthParser#line.
    def exitLine(self, ctx:synthParser.LineContext):
        pass


    # Enter a parse tree produced by synthParser#statement.
    def enterStatement(self, ctx:synthParser.StatementContext):
        pass

    # Exit a parse tree produced by synthParser#statement.
    def exitStatement(self, ctx:synthParser.StatementContext):
        pass


    # Enter a parse tree produced by synthParser#if_statement.
    def enterIf_statement(self, ctx:synthParser.If_statementContext):
        pass

    # Exit a parse tree produced by synthParser#if_statement.
    def exitIf_statement(self, ctx:synthParser.If_statementContext):
        pass


    # Enter a parse tree produced by synthParser#while_statement.
    def enterWhile_statement(self, ctx:synthParser.While_statementContext):
        pass

    # Exit a parse tree produced by synthParser#while_statement.
    def exitWhile_statement(self, ctx:synthParser.While_statementContext):
        pass


    # Enter a parse tree produced by synthParser#for_statement.
    def enterFor_statement(self, ctx:synthParser.For_statementContext):
        pass

    # Exit a parse tree produced by synthParser#for_statement.
    def exitFor_statement(self, ctx:synthParser.For_statementContext):
        pass


    # Enter a parse tree produced by synthParser#range_statement.
    def enterRange_statement(self, ctx:synthParser.Range_statementContext):
        pass

    # Exit a parse tree produced by synthParser#range_statement.
    def exitRange_statement(self, ctx:synthParser.Range_statementContext):
        pass


    # Enter a parse tree produced by synthParser#print_statement.
    def enterPrint_statement(self, ctx:synthParser.Print_statementContext):
        pass

    # Exit a parse tree produced by synthParser#print_statement.
    def exitPrint_statement(self, ctx:synthParser.Print_statementContext):
        pass


    # Enter a parse tree produced by synthParser#function_call.
    def enterFunction_call(self, ctx:synthParser.Function_callContext):
        pass

    # Exit a parse tree produced by synthParser#function_call.
    def exitFunction_call(self, ctx:synthParser.Function_callContext):
        pass


    # Enter a parse tree produced by synthParser#parameters.
    def enterParameters(self, ctx:synthParser.ParametersContext):
        pass

    # Exit a parse tree produced by synthParser#parameters.
    def exitParameters(self, ctx:synthParser.ParametersContext):
        pass


    # Enter a parse tree produced by synthParser#expression.
    def enterExpression(self, ctx:synthParser.ExpressionContext):
        pass

    # Exit a parse tree produced by synthParser#expression.
    def exitExpression(self, ctx:synthParser.ExpressionContext):
        pass


    # Enter a parse tree produced by synthParser#logic_expression.
    def enterLogic_expression(self, ctx:synthParser.Logic_expressionContext):
        pass

    # Exit a parse tree produced by synthParser#logic_expression.
    def exitLogic_expression(self, ctx:synthParser.Logic_expressionContext):
        pass


    # Enter a parse tree produced by synthParser#math_expression.
    def enterMath_expression(self, ctx:synthParser.Math_expressionContext):
        pass

    # Exit a parse tree produced by synthParser#math_expression.
    def exitMath_expression(self, ctx:synthParser.Math_expressionContext):
        pass


    # Enter a parse tree produced by synthParser#sound_expression.
    def enterSound_expression(self, ctx:synthParser.Sound_expressionContext):
        pass

    # Exit a parse tree produced by synthParser#sound_expression.
    def exitSound_expression(self, ctx:synthParser.Sound_expressionContext):
        pass


    # Enter a parse tree produced by synthParser#sequence_expression.
    def enterSequence_expression(self, ctx:synthParser.Sequence_expressionContext):
        pass

    # Exit a parse tree produced by synthParser#sequence_expression.
    def exitSequence_expression(self, ctx:synthParser.Sequence_expressionContext):
        pass


    # Enter a parse tree produced by synthParser#bool_op.
    def enterBool_op(self, ctx:synthParser.Bool_opContext):
        pass

    # Exit a parse tree produced by synthParser#bool_op.
    def exitBool_op(self, ctx:synthParser.Bool_opContext):
        pass


    # Enter a parse tree produced by synthParser#compare_op.
    def enterCompare_op(self, ctx:synthParser.Compare_opContext):
        pass

    # Exit a parse tree produced by synthParser#compare_op.
    def exitCompare_op(self, ctx:synthParser.Compare_opContext):
        pass


    # Enter a parse tree produced by synthParser#add_op.
    def enterAdd_op(self, ctx:synthParser.Add_opContext):
        pass

    # Exit a parse tree produced by synthParser#add_op.
    def exitAdd_op(self, ctx:synthParser.Add_opContext):
        pass


    # Enter a parse tree produced by synthParser#mult_op.
    def enterMult_op(self, ctx:synthParser.Mult_opContext):
        pass

    # Exit a parse tree produced by synthParser#mult_op.
    def exitMult_op(self, ctx:synthParser.Mult_opContext):
        pass


    # Enter a parse tree produced by synthParser#var_definition.
    def enterVar_definition(self, ctx:synthParser.Var_definitionContext):
        pass

    # Exit a parse tree produced by synthParser#var_definition.
    def exitVar_definition(self, ctx:synthParser.Var_definitionContext):
        pass


    # Enter a parse tree produced by synthParser#var_definition_assignment.
    def enterVar_definition_assignment(self, ctx:synthParser.Var_definition_assignmentContext):
        pass

    # Exit a parse tree produced by synthParser#var_definition_assignment.
    def exitVar_definition_assignment(self, ctx:synthParser.Var_definition_assignmentContext):
        pass


    # Enter a parse tree produced by synthParser#channel_addition.
    def enterChannel_addition(self, ctx:synthParser.Channel_additionContext):
        pass

    # Exit a parse tree produced by synthParser#channel_addition.
    def exitChannel_addition(self, ctx:synthParser.Channel_additionContext):
        pass


    # Enter a parse tree produced by synthParser#synth_name.
    def enterSynth_name(self, ctx:synthParser.Synth_nameContext):
        pass

    # Exit a parse tree produced by synthParser#synth_name.
    def exitSynth_name(self, ctx:synthParser.Synth_nameContext):
        pass


    # Enter a parse tree produced by synthParser#synth_params.
    def enterSynth_params(self, ctx:synthParser.Synth_paramsContext):
        pass

    # Exit a parse tree produced by synthParser#synth_params.
    def exitSynth_params(self, ctx:synthParser.Synth_paramsContext):
        pass


    # Enter a parse tree produced by synthParser#synth_constructor.
    def enterSynth_constructor(self, ctx:synthParser.Synth_constructorContext):
        pass

    # Exit a parse tree produced by synthParser#synth_constructor.
    def exitSynth_constructor(self, ctx:synthParser.Synth_constructorContext):
        pass


    # Enter a parse tree produced by synthParser#sound_constructor.
    def enterSound_constructor(self, ctx:synthParser.Sound_constructorContext):
        pass

    # Exit a parse tree produced by synthParser#sound_constructor.
    def exitSound_constructor(self, ctx:synthParser.Sound_constructorContext):
        pass


    # Enter a parse tree produced by synthParser#sequence_constructor.
    def enterSequence_constructor(self, ctx:synthParser.Sequence_constructorContext):
        pass

    # Exit a parse tree produced by synthParser#sequence_constructor.
    def exitSequence_constructor(self, ctx:synthParser.Sequence_constructorContext):
        pass


    # Enter a parse tree produced by synthParser#type.
    def enterType(self, ctx:synthParser.TypeContext):
        pass

    # Exit a parse tree produced by synthParser#type.
    def exitType(self, ctx:synthParser.TypeContext):
        pass



del synthParser