# Generated from D:/Projekty/learningPytest/Kompilatorki/Synth\synth.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .synthParser import synthParser
else:
    from synthParser import synthParser

# This class defines a complete generic visitor for a parse tree produced by synthParser.

class synthVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by synthParser#program.
    def visitProgram(self, ctx:synthParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#function.
    def visitFunction(self, ctx:synthParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#return_block.
    def visitReturn_block(self, ctx:synthParser.Return_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#function_final.
    def visitFunction_final(self, ctx:synthParser.Function_finalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#nchannel_definition.
    def visitNchannel_definition(self, ctx:synthParser.Nchannel_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#duration_definition.
    def visitDuration_definition(self, ctx:synthParser.Duration_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#block.
    def visitBlock(self, ctx:synthParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#line.
    def visitLine(self, ctx:synthParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#statement.
    def visitStatement(self, ctx:synthParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#if_statement.
    def visitIf_statement(self, ctx:synthParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#while_statement.
    def visitWhile_statement(self, ctx:synthParser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#for_statement.
    def visitFor_statement(self, ctx:synthParser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#range_statement.
    def visitRange_statement(self, ctx:synthParser.Range_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#print_statement.
    def visitPrint_statement(self, ctx:synthParser.Print_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#function_call.
    def visitFunction_call(self, ctx:synthParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#parameters.
    def visitParameters(self, ctx:synthParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#expression.
    def visitExpression(self, ctx:synthParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#logic_expression.
    def visitLogic_expression(self, ctx:synthParser.Logic_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#math_expression.
    def visitMath_expression(self, ctx:synthParser.Math_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#sound_expression.
    def visitSound_expression(self, ctx:synthParser.Sound_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#sequence_expression.
    def visitSequence_expression(self, ctx:synthParser.Sequence_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#bool_op.
    def visitBool_op(self, ctx:synthParser.Bool_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#compare_op.
    def visitCompare_op(self, ctx:synthParser.Compare_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#add_op.
    def visitAdd_op(self, ctx:synthParser.Add_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#mult_op.
    def visitMult_op(self, ctx:synthParser.Mult_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#var_definition.
    def visitVar_definition(self, ctx:synthParser.Var_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#var_definition_assignment.
    def visitVar_definition_assignment(self, ctx:synthParser.Var_definition_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#channel_addition.
    def visitChannel_addition(self, ctx:synthParser.Channel_additionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#synth_name.
    def visitSynth_name(self, ctx:synthParser.Synth_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#synth_params.
    def visitSynth_params(self, ctx:synthParser.Synth_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#synth_constructor.
    def visitSynth_constructor(self, ctx:synthParser.Synth_constructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#sound_constructor.
    def visitSound_constructor(self, ctx:synthParser.Sound_constructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#sequence_constructor.
    def visitSequence_constructor(self, ctx:synthParser.Sequence_constructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by synthParser#type.
    def visitType(self, ctx:synthParser.TypeContext):
        return self.visitChildren(ctx)



del synthParser