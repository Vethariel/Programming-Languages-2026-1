from grammar import Grammar
import sys
import os

# Añade la carpeta padre al "camino" de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Lexer.lexer import Lexer

class SintaxError(Exception):
    pass

class ParseEOFError(Exception):
    pass

class Parser:
    def __init__(self, src, grammar=None):
        self.grammar = grammar
        self.lexer = Lexer(src)
        self.token = self.lexer.nextToken()
        
    def assign_symbol(self, symbol):
        if symbol in self.grammar:
            self.parse_no_terminal(symbol)
        else:
            self.pair_terminals(symbol)
            
    def parse_no_terminal(self, no_terminal):
        if self.token.kind == "EOF" and no_terminal == "EOF":
            raise ParseEOFError("El analisis sintactico ha finalizado exitosamente.")
        
        no_terminal_values = self.grammar.grammar[no_terminal]
        
        for rule in no_terminal_values["rules"]:
            if self.token.kind in rule["pred_set"]:
                for symbol in rule["rule"]:
                    self.assign_symbol(symbol)
                return  # ← importante salir tras aplicar la regla
        
        # Solo si ninguna regla coincidió
        self.sintax_error(list(no_terminal_values["total_pred_set"]))
    
    def pair_terminals(self, expected_token):
        if self.token.kind == expected_token:
            self.token = self.lexer.nextToken()
        else:
            self.sintax_error(expected_token)
            
    def sintax_error(self, expected_token):
        if isinstance(expected_token, list):
            expected_token = [f"\"{t}\"" for t in expected_token]
            expected_token = ", ".join(expected_token)
        else:
            expected_token = f"\"{expected_token}\""
        raise SintaxError(f"<{self.token.line}:{self.token.col}> Error sintactico: se encontro: \"{self.token.lexeme}\"; se esperaba: {expected_token}.")
        
def main():
    src = ""
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            src = f.read()
    else:
        src = sys.stdin.read()

    parser = Parser(src, Grammar())
    try:
        parser.parse_no_terminal(parser.grammar.start_symbol)
    except (SintaxError, ParseEOFError) as e:
        print(e)

if __name__ == "__main__":
    main()