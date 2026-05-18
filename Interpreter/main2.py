import sys
sys.path.insert(0, './TestCases')

from antlr4 import CommonTokenStream, FileStream
from EsJSLexer import EsJSLexer
from EsJSParser import EsJSParser
from interpreter import Interpreter


def run(filepath):
    input_stream = FileStream(filepath, encoding='utf-8')
    lexer = EsJSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EsJSParser(stream)
    tree = parser.programa()
    interpreter = Interpreter()
    interpreter.visit(tree)


if __name__ == '__main__':
    for i in range(1, 7):
        filepath = f'./TestCases/{i:02d}.in'
        print(f'\n--- Test {i:02d} ---')
        try:
            run(filepath)
        except Exception as e:
            print(f'Error: {e}')