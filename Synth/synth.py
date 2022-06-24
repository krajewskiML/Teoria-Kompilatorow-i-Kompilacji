from Tools.synthLexer import synthLexer
from Tools.synthParser import synthParser
from Synth.utils.CustomSynthVisitor import CustomSynthVisitor

import argparse

from antlr4 import InputStream, CommonTokenStream


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", "-g", type=str)
    parser.add_argument("--destination", "-d", type=str)
    args = parser.parse_args()
    input_file = args.generate
    output_file = args.destination
    with open(input_file) as fin:
        data_str = "".join(fin)
        data_str = data_str.replace('\n', '')

    input_stream = InputStream(data_str)
    lexer = synthLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = synthParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        exit(-1000)
    visitor = CustomSynthVisitor(output_file)
    visitor.visit(tree)


if __name__ == "__main__":
    main()
