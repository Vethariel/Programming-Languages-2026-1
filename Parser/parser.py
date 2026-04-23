import sys
from grammar import Grammar
from lexer import Lexer

TOKEN_KIND_REPR = {
    # ── Literales ──────────────────────────────────────────
    "NUMBER":           "valor_numérico",
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

# Diccionario inverso: repr -> sort_key
TOKEN_REPR_SORT_KEY = {}
for kind, repr_ in TOKEN_KIND_REPR.items():
    if kind.isupper() and not repr_[0].isalpha():
        TOKEN_REPR_SORT_KEY[repr_] = f"tkn_{kind.lower()}"
    elif kind == "NuN":
        TOKEN_REPR_SORT_KEY[repr_] = "nu"  # "NuN" se ordena literalmente
    else:
        TOKEN_REPR_SORT_KEY[repr_] = repr_.lower()

class SintaxError(Exception):
    pass

class ParseEOFError(Exception):
    pass

class Parser:
    def __init__(self, src):
        self.grammar = Grammar()
        self.lexer = Lexer(src)
        self.token = self.lexer.nextToken()
        
    def assign_symbol(self, symbol):
        if symbol in self.grammar.grammar:
            self.parse_no_terminal(symbol)
        else:
            self.pair_terminals(symbol)
            
    def parse_no_terminal(self, no_terminal):
        
        no_terminal_values = self.grammar.grammar[no_terminal]
        
        for rule in no_terminal_values["rules"]:
            if self.token.kind in rule["pred_set"]:
                symbols = [s for s in rule["rule"] if s != "epsylon"]
                for symbol in symbols:
                    self.assign_symbol(symbol)  # ← sin propagar follow dinámico
                return
        
        # Ninguna regla matchea
        has_epsilon = any("epsylon" in rule["rule"] for rule in no_terminal_values["rules"])
        
        if has_epsilon:
            # Verificar con el FOLLOW formal calculado
            formal_follow = self.grammar.follow_set[no_terminal]
            if self.token.kind in formal_follow:
                return  # epsilon válido
            else:
                #print(f"DEBUG epsilon: no_terminal={no_terminal}, token={self.token.kind}")
                self.sintax_error(list(no_terminal_values["total_pred_set"]))
        else:
            #print(f"DEBUG no-epsilon: no_terminal={no_terminal}, token={self.token.kind}")
            self.sintax_error(list(no_terminal_values["total_pred_set"]))
        
    def pair_terminals(self, expected_token):
        if self.token.kind == expected_token:
            if expected_token == "EOF":
                raise ParseEOFError("El analisis sintactico ha finalizado exitosamente.")
            self.token = self.lexer.nextToken()
        else:
            self.sintax_error(expected_token)
            
    def sintax_error(self, expected_token):
        if self.token.kind == "EOF": self.token.lexeme = "final de archivo"
        if self.token.kind == "STR": self.token.lexeme = self.token.lexeme[1:-1]
        if isinstance(expected_token, list):
            expected_token = [TOKEN_KIND_REPR[e] if e in TOKEN_KIND_REPR else e for e in expected_token]
            expected_token.sort(key=lambda s: TOKEN_REPR_SORT_KEY.get(s, s.lower()))
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