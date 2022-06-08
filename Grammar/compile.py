from Tools.synthLexer import synthLexer
from Tools.synthParser import synthParser
from Tools.synthVisitor import synthVisitor
from Tools.synthListener import synthListener
from CustomSynthVisitor import CustomSynthVisitor

from antlr4 import InputStream, CommonTokenStream


def main():
    with open("test.synth") as fin:
        data_str = "".join(fin)
        data_str = data_str.replace('\n', '')

    input_stream = InputStream(data_str)
    lexer = synthLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = synthParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        exit(-1000)
    visitor = CustomSynthVisitor()
    visitor.visit(tree)


if __name__ == "__main__":
    main()
