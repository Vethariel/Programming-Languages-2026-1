#!/usr/bin/env python3
"""
Lexer EsJS — traducción directa del lexer.c
Uso: python3 lexer.py < input.esjs
     python3 lexer.py archivo.esjs
"""
import sys
import re

# ─── KEYWORDS ────────────────────────────────────────────────
KEYWORDS = set([
    # Control Keywords — quitando las ignoradas según enunciado
    "capturar", "caso", "con", "continuar", "crear",
    "elegir", "esperar", "hacer",
    "mientras", "para", "retornar", "sino", "si",
    "constructor", "eliminar", "extiende", "finalmente",
    "instanciaDe", "intentar", "lanzar", "longitud", "romper",
    "simbolo", "subcad", "tipoDe", "vacio",
    "ambiente", "super", "de", "en",
    "clase", "const", "var", "mut", "porDefecto", "funcion",
    # Language Constants — quitando ambienteGlobal
    "falso", "nulo", "verdadero", "indefinido",
    "Infinito", "NuN",
    # Support Functions — quitando depurador, establecerTemporizador, establecerIntervalo, Promesa
    "consola", "Fecha", "Numero", "Mate", "Matriz", "Arreglo",
    "Booleano", "Cadena", "Funcion",
    # Console Object — quitando las ignoradas
    "afirmar", "limpiar", "listar", "error",
    "agrupar", "info", "escribir", "tabla", "repetir",
])

# ─── TOKEN NAMES ─────────────────────────────────────────────
TOKEN_PRINT = {
    "PLUS":          "tkn_plus",
    "MINUS":         "tkn_minus",
    "TIMES":         "tkn_times",
    "DIV":           "tkn_div",
    "ASSIGN":        "tkn_assign",
    "EQ":            "tkn_equal",
    "EEQ":           "tkn_strict_equal",
    "ARROW":         "tkn_arrow",
    "LT":            "tkn_less",
    "LE":            "tkn_leq",
    "GT":            "tkn_greater",
    "GE":            "tkn_geq",
    "LPAREN":        "tkn_opening_par",
    "RPAREN":        "tkn_closing_par",
    "LBRACE":        "tkn_opening_key",
    "RBRACE":        "tkn_closing_key",
    "LBRACKET":      "tkn_opening_bra",
    "RBRACKET":      "tkn_closing_bra",
    "SEMI":          "tkn_semicolon",
    "COMMA":         "tkn_comma",
    "PERIOD":        "tkn_period",
    "COLON":         "tkn_colon",
    "IDENT":         "id",
    "NUMBER":        "tkn_num",
    "STR":           "tkn_str",
    "AND":           "tkn_and",
    "OR":            "tkn_or",
    "NOT":           "tkn_not",
    "NEQ":           "tkn_neq",
    "NEEQ":          "tkn_strict_neq",
    "TERNARY":       "tkn_ternary",
    "NULLISH":       "tkn_nulish",
    "INCREMENT":     "tkn_increment",
    "DECREMENT":     "tkn_decrement",
    "MOD":           "tkn_mod",
    "POWER":         "tkn_power",
    "MOD_ASSIGN":    "tkn_mod_assign",
    "POWER_ASSIGN":  "tkn_power_assign",
    "DIV_ASSIGN":    "tkn_div_assign",
    "PLUS_ASSIGN":   "tkn_plus_assign",
    "MINUS_ASSIGN":  "tkn_minus_assign",
    "TIMES_ASSIGN":  "tkn_times_assign",
    "SPREAD":        "tkn_spread",
    "REGEX":         "tkn_regex",   # <-- nuevo, por si acaso
}

# ─── REGEX PATTERNS (orden importa) ──────────────────────────
# Cada tupla: (tipo, patron)
TOKEN_PATTERNS = [
    # Comentarios — ignorar
    ("COMMENT_ML", r"/\*[\s\S]*?\*/"),
    ("COMMENT_ML_UNCLOSED", r"/\*[\s\S]*"),   # sin cerrar → error
    ("COMMENT_SL", r"//[^\n]*"),

    # Strings
    ("STR",        r'"[^"\n]*"'),
    ("STR",        r"'[^'\n]*'"),

    # Números
    ("NUMBER",     r"\d+\.\d+"),
    ("NUMBER",     r"\d+(?=\.)(?!\d*\.\d)"),  # 5. → solo "5", el punto queda fuera
    ("NUMBER",     r"\d+"),

    # Identificadores / keywords
    ("IDENT",      r"[a-zA-Z_$\u00C0-\uFFFF][a-zA-Z0-9_$\u00C0-\uFFFF]*"),

    # Operadores 3 chars
    ("NEEQ",       r"!=="),
    ("EEQ",        r"==="),
    ("SPREAD",     r"\.\.\."),
    ("POWER_ASSIGN", r"\*\*="),

    # Operadores 2 chars
    ("EQ",         r"=="),
    ("NEQ",        r"!="),
    ("LE",         r"<="),
    ("GE",         r">="),
    ("ARROW",      r"=>"),
    ("AND",        r"&&"),
    ("OR",         r"\|\|"),
    ("NULLISH",    r"\?\?"),
    ("INCREMENT",  r"\+\+"),
    ("DECREMENT",  r"--"),
    ("POWER",      r"\*\*"),
    ("PLUS_ASSIGN",  r"\+="),
    ("MINUS_ASSIGN", r"-="),
    ("TIMES_ASSIGN", r"\*="),
    ("DIV_ASSIGN",   r"/="),
    ("MOD_ASSIGN",   r"%="),
    ("PERIOD2",    r"\.\."),   # dos puntos seguidos sin tercero

    # Operadores 1 char
    ("PLUS",       r"\+"),
    ("MINUS",      r"-"),
    ("TIMES",      r"\*"),
    ("DIV",        r"/"),
    ("ASSIGN",     r"="),
    ("LT",         r"<"),
    ("GT",         r">"),
    ("MOD",        r"%"),
    ("NOT",        r"!"),
    ("TERNARY",    r"\?"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("LBRACE",     r"\{"),
    ("RBRACE",     r"\}"),
    ("LBRACKET",   r"\["),
    ("RBRACKET",   r"\]"),
    ("SEMI",       r";"),
    ("COMMA",      r","),
    ("COLON",      r":"),
    ("PERIOD",     r"\."),

    # Espacios — ignorar
    ("SPACE",      r"[ \t\r]+"),
    ("NEWLINE",    r"\n"),
]

MASTER_RE = re.compile(
    "|".join(f"(?P<T{i}_{t.replace('-','_')}>{p})"
             for i, (t, p) in enumerate(TOKEN_PATTERNS)),
    re.UNICODE
)

CAN_START_REGEX_AFTER = {
    None,
    "ASSIGN",
    "LPAREN",
    "LBRACE",
    "LBRACKET",
    "COMMA",
    "COLON",
    "TERNARY",
    "AND",
    "OR",
    "NOT",
    "EQ",
    "NEQ",
    "EEQ",
    "NEEQ",
    "LT",
    "LE",
    "GT",
    "GE",
}

DIVISION_CONTEXT = {
    "IDENT",
    "NUMBER",
    "INCREMENT",
    "DECREMENT",
    "RPAREN",
    "RBRACKET",
}

def lex(src: str):
    line = 1
    line_start = 0
    tokens = []
    pos = 0  # posición actual en src
    last_kind = None

    while pos < len(src):
        m = MASTER_RE.match(src, pos)
        # gap entre el fin del último match y el inicio de este → error léxico
        if m is None:
            for tk in tokens:
                print_token(*tk)
            tokens = []
            bad_col = len(src[line_start:pos]) + 1
            print(f">>> Error lexico (linea: {line}, posicion: {bad_col})")
            return None
        if m.start() > pos:
            for tk in tokens:
                print_token(*tk)
            tokens = []
            bad_col = len(src[line_start:pos]) + 1
            print(f">>> Error lexico (linea: {line}, posicion: {bad_col})")
            return None

        kind = None
        for k, v in m.groupdict().items():
            if v is not None:
                kind = "_".join(k.split("_")[1:])
                break

        col = len(src[line_start:m.start()]) + 1
        tok_line = line
        tok_col = col
        lexeme = m.group()
        nl_count = lexeme.count("\n")
        
        # 🔥 PRIORIDAD ABSOLUTA PARA '/'
        if src[pos] == '/':
            if pos + 1 < len(src) and src[pos + 1] in ('/', '*'):
                pass
            else:
                is_division = last_kind in DIVISION_CONTEXT
                if not is_division:
                    j = pos + 1
                    buf = []
                    found = False

                    while j < len(src) and src[j] != '\n':
                        if src[j] == '\\' and j + 1 < len(src):
                            buf.append(src[j])
                            buf.append(src[j + 1])
                            j += 2
                            continue

                        if src[j] == '/':
                            found = True
                            j += 1
                            break

                        buf.append(src[j])
                        j += 1

                    content = ''.join(buf)

                    if found and content:
                        tokens.append(("REGEX", content, tok_line, tok_col))
                        pos = j
                        last_kind = "REGEX"
                        continue
        
        if kind in ("COMMENT_ML", "SPACE", "COMMENT_SL" ):
            line += nl_count
            if nl_count:
                line_start = m.start() + lexeme.rfind("\n") + 1
            pos = m.end()
            continue

        if kind == "COMMENT_ML_UNCLOSED":
            for tk in tokens:
                print_token(*tk)
            tokens = []
            print(f">>> Error lexico (linea: {tok_line}, posicion: {col})")
            return None

        if kind == "NEWLINE":
            line += 1
            line_start = m.end()
            pos = m.end()
            continue

        if kind == "IDENT":
            if lexeme in KEYWORDS:
                kind = "KEYWORD"

        if kind == "PERIOD2":
            tokens.append(("PERIOD", ".", tok_line, col))
            tokens.append(("PERIOD", ".", tok_line, col + 1))
            pos = m.end()
            continue
        


        tokens.append((kind, lexeme, tok_line, col))
        last_kind = kind
        pos = m.end()

    # verificar si quedó texto sin procesar al final
    if pos < len(src):
        for tk in tokens:
            print_token(*tk)
        tokens = []
        bad_col = len(src[line_start:pos]) + 1
        print(f">>> Error lexico (linea: {line}, posicion: {bad_col})")
        return None

    return tokens

def print_token(kind, lexeme, line, col):
    if kind == "KEYWORD":
        print(f"<{lexeme},{line},{col}>")
    elif kind == "NUMBER":
        print(f"<{TOKEN_PRINT['NUMBER']},{lexeme},{line},{col}>")
    elif kind == "IDENT":
        print(f"<{TOKEN_PRINT['IDENT']},{lexeme},{line},{col}>")
    elif kind == "REGEX":
        inner = lexeme
        print(f"<tkn_reg,{inner},{line},{col}>")
    elif kind == "STR":
        # quitar comillas
        inner = lexeme[1:-1]
        print(f"<{TOKEN_PRINT['STR']},{inner},{line},{col}>")
    elif kind in TOKEN_PRINT:
        name = TOKEN_PRINT[kind]
        print(f"<{name},{line},{col}>")

def main():
    if len(sys.argv) > 1:
        src = open(sys.argv[1], encoding="utf-8").read()
    else:
        src = sys.stdin.read()

    tokens = lex(src)
    if tokens is None:
        return
    for kind, lexeme, line, col in tokens:
        print_token(kind, lexeme, line, col)

if __name__ == "__main__":
    main()