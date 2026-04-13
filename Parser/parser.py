from grammar import Grammar
import sys
from lexer import Lexer

TOKEN_KIND_REPR = {
    # ── Literales ──────────────────────────────────────────
    "NUMBER":           "valor_numerico",
    "STR":              "cadena_de_caracteres",
    "REGEX":            "regex",

    # ── Operadores 3 chars ─────────────────────────────────
    "STRICT_NEQ":       "!==",
    "STRICT_EQUAL":     "===",
    "SPREAD":           "...",
    "POWER_ASSIGN":     "**=",

    # ── Operadores 2 chars ─────────────────────────────────
    "EQUAL":            "==",
    "NEQ":              "!=",
    "LEQ":              "<=",
    "GEQ":              ">=",
    "ARROW":            "=>",
    "AND":              "&&",
    "OR":               "||",
    "NULLISH":          "??",
    "INCREMENT":        "++",
    "DECREMENT":        "--",
    "POWER":            "**",
    "PLUS_ASSIGN":      "+=",
    "MINUS_ASSIGN":     "-=",
    "TIMES_ASSIGN":     "*=",
    "DIV_ASSIGN":       "/=",
    "MOD_ASSIGN":       "%=",
    "POWER_ASSIGN":     "**=",
    "PERIOD2":          "..",

    # ── Operadores 1 char ──────────────────────────────────
    "PLUS":             "+",
    "MINUS":            "-",
    "TIMES":            "*",
    "DIV":              "/",
    "ASSIGN":           "=",
    "LESS":             "<",
    "GREATER":          ">",
    "MOD":              "%",
    "NOT":              "!",
    "TERNARY":          "?",
    "OPENING_PAR":      "(",
    "CLOSING_PAR":      ")",
    "OPENING_KEY":      "{",
    "CLOSING_KEY":      "}",
    "OPENING_BRA":      "[",
    "CLOSING_BRA":      "]",
    "SEMICOLON":        ";",
    "COMMA":            ",",
    "COLON":            ":",
    "PERIOD":           ".",

    # ── Especiales ─────────────────────────────────────────
    "IDENT":            "id",
    "EOF":              "final de archivo",
    "COMMENT_SL":       "comment_sl",
    "COMMENT_ML":       "comment_ml",
    "COMMENT_ML_UNCLOSED": "comment_ml_unclosed",

    # ── Keywords de control ────────────────────────────────
    "capturar":         "capturar",
    "caso":             "caso",
    "con":              "con",
    "continuar":        "continuar",
    "crear":            "crear",
    "elegir":           "elegir",
    "esperar":          "esperar",
    "hacer":            "hacer",
    "mientras":         "mientras",
    "para":             "para",
    "retornar":         "retornar",
    "sino":             "sino",
    "si":               "si",
    "constructor":      "constructor",
    "eliminar":         "eliminar",
    "extiende":         "extiende",
    "finalmente":       "finalmente",
    "instanciaDe":      "instanciaDe",
    "intentar":         "intentar",
    "lanzar":           "lanzar",
    "longitud":         "longitud",
    "romper":           "romper",
    "simbolo":          "simbolo",
    "subcad":           "subcad",
    "tipoDe":           "tipoDe",
    "vacio":            "vacio",
    "ambiente":         "ambiente",
    "super":            "super",
    "de":               "de",
    "en":               "en",
    "clase":            "clase",
    "const":            "const",
    "var":              "var",
    "mut":              "mut",
    "porDefecto":       "porDefecto",
    "funcion":          "funcion",

    # ── Constantes del lenguaje ────────────────────────────
    "falso":            "falso",
    "nulo":             "nulo",
    "verdadero":        "verdadero",
    "indefinido":       "indefinido",
    "Infinito":         "Infinito",
    "NuN":              "NuN",

    # ── Funciones/objetos de soporte ───────────────────────
    "consola":          "consola",
    "Fecha":            "Fecha",
    "Numero":           "Numero",
    "Mate":             "Mate",
    "Matriz":           "Matriz",
    "Arreglo":          "Arreglo",
    "Booleano":         "Booleano",
    "Cadena":           "Cadena",
    "Funcion":          "Funcion",

    # ── Métodos de consola ─────────────────────────────────
    "afirmar":          "afirmar",
    "limpiar":          "limpiar",
    "listar":           "listar",
    "error":            "error",
    "agrupar":          "agrupar",
    "info":             "info",
    "escribir":         "escribir",
    "tabla":            "tabla",
    "repetir":          "repetir",
}

class SintaxError(Exception):
    pass

class ParseEOFError(Exception):
    pass

class Parser:
    def __init__(self, src):
        self.grammar = Grammar()
        self.lexer = Lexer(src)
        self.token = self.lexer.nextToken()
        
    def assign_symbol(self, symbol, follow=None):
        if symbol in self.grammar.grammar:
            self.parse_no_terminal(symbol, follow=follow)
        else:
            self.pair_terminals(symbol)
            
    def parse_no_terminal(self, no_terminal, follow=None):
        no_terminal_values = self.grammar.grammar[no_terminal]
        
        for rule in no_terminal_values["rules"]:
            if self.token.kind in rule["pred_set"]:
                symbols = [s for s in rule["rule"] if s != "epsylon"]
                
                for i, symbol in enumerate(symbols):
                    # Lo que viene después de este símbolo en esta regla
                    rest = symbols[i+1:]
                    first_rest = self.grammar.first_of_sequence(rest) if rest else {"epsylon"}
                    
                    if "epsylon" in first_rest:
                        # Si el resto puede ser vacío, el follow local incluye
                        # el follow que nos pasó el llamador
                        local_follow = (first_rest - {"epsylon"}) | (follow or set())
                    else:
                        local_follow = first_rest
                    
                    self.assign_symbol(symbol, follow=local_follow)
                return
        
        error_set = follow if follow is not None else no_terminal_values["total_pred_set"]
        self.sintax_error(list(error_set))
    
    def pair_terminals(self, expected_token):
        if self.token.kind == expected_token:
            if expected_token == "EOF":
                raise ParseEOFError("El analisis sintactico ha finalizado exitosamente.")
            self.token = self.lexer.nextToken()
        else:
            self.sintax_error(expected_token)
            
    def sintax_error(self, expected_token):
        if self.token.kind == "EOF": self.token.lexeme = "final de archivo"
        if isinstance(expected_token, list):
            expected_token.sort()
            expected_token = [TOKEN_KIND_REPR[e] if e in TOKEN_KIND_REPR else e for e in expected_token]
            expected_token = [f"\"{t}\"" for t in expected_token]
            expected_token = ", ".join(expected_token)
        else:
            expected_token = TOKEN_KIND_REPR[expected_token] if expected_token in TOKEN_KIND_REPR else expected_token
            expected_token = f"\"{expected_token}\""
        raise SintaxError(f"<{self.token.line}:{self.token.col}> Error sintactico: se encontro: \"{self.token.lexeme}\"; se esperaba: {expected_token}.")
        
def main():
    src = ""
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            src = f.read()
    else:
        src = sys.stdin.read()

    parser = Parser(src)
    try:
        parser.parse_no_terminal(parser.grammar.start_symbol)
    except (SintaxError, ParseEOFError) as e:
        print(e)

if __name__ == "__main__":
    main()