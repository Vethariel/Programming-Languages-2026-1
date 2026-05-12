import sys
sys.path.insert(0, './TestCases')

from antlr4 import CommonTokenStream, FileStream
from antlr4.error.ErrorListener import ErrorListener
from EsJSLexer import EsJSLexer
from EsJSParser import EsJSParser

class MiErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append(f"  Error sintactico (linea {line}, col {column}): {msg}")

def test_parser(filepath):
    print(f"\n{'='*50}")
    print(f"Archivo: {filepath}")
    print('='*50)

    input_stream = FileStream(filepath, encoding='utf-8')
    lexer = EsJSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EsJSParser(stream)

    parser.removeErrorListeners()
    error_listener = MiErrorListener()
    parser.addErrorListener(error_listener)

    tree = parser.programa()

    if error_listener.errores:
        for e in error_listener.errores:
            print(e)
    else:
        print("  OK - Sin errores sintacticos")
        # Imprimir el árbol
        print(tree.toStringTree(recog=parser))

test_parser('./TestCases/05.in')  # empieza solo con el primero