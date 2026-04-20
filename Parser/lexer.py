#!/usr/bin/env python3
"""
Lexer EsJS — traducción directa del lexer.c
Uso: python3 lexer.py < input.esjs
     python3 lexer.py archivo.esjs
"""
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
    ("STRICT_NEQ",  r"!=="),
    ("STRICT_EQUAL",r"==="),
    ("SPREAD",     r"\.\.\."),
    ("POWER_ASSIGN", r"\*\*="),

    # Operadores 2 chars
    ("EQUAL",      r"=="),
    ("NEQ",        r"!="),
    ("LEQ",        r"<="),
    ("GEQ",        r">="),
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
    ("POWER_ASSIGN", r"\*\*="),
    ("PERIOD2",    r"\.\."),   # dos puntos seguidos sin tercero

    # Operadores 1 char
    ("PLUS",       r"\+"),
    ("MINUS",      r"-"),
    ("TIMES",      r"\*"),
    ("DIV",        r"/"),
    ("ASSIGN",     r"="),
    ("LESS",       r"<"),
    ("GREATER",    r">"),
    ("MOD",        r"%"),
    ("NOT",        r"!"),
    ("TERNARY",    r"\?"),
    ("OPENING_PAR",r"\("),
    ("CLOSING_PAR",r"\)"),
    ("OPENING_KEY",r"\{"),
    ("CLOSING_KEY",r"\}"),
    ("OPENING_BRA",r"\["),
    ("CLOSING_BRA",r"\]"),
    ("SEMICOLON",  r";"),
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

DIVISION_CONTEXT = {
    "IDENT",
    "NUMBER",
    "INCREMENT",
    "DECREMENT",
    "CLOSING_PAR",
    "CLOSING_BRA",
}

ASI_TRIGGERS = {
    "IDENT", "NUMBER", "STR", "REGEX",
    "CLOSING_PAR",    # )
    "CLOSING_BRA",  # ]
    "INCREMENT", # ++
    "DECREMENT", # --
}

# Keywords que SIEMPRE insertan ';' después de newline
ASI_KEYWORD_TRIGGERS = {"retornar", "romper", "continuar", "lanzar"}

# Si el SIGUIENTE token es uno de estos, el newline NO es ';'
ASI_BLOCKERS = {"OPENING_PAR", "OPENING_BRA", "PLUS", "MINUS", "SLASH", "PERIOD"}

class Token:
    def __init__(self, kind: str, lexeme: str, line: int, col: int):
        self.kind   = kind
        self.lexeme = lexeme
        self.line   = line
        self.col    = col

    def __repr__(self):
        return f"Token({self.kind!r}, {self.lexeme!r}, line={self.line}, col={self.col})"


class LexerError(Exception):
    def __init__(self, line: int, col: int):
        super().__init__(f"Error lexico (linea: {line}, posicion: {col})")
        self.line = line
        self.col  = col


class Lexer:
    """
    Uso:
        lexer = Lexer(source_code)
        tok = lexer.nextToken()   # devuelve Token o None si llegó al EOF
    """

    def __init__(self, src: str):
        self.src        = src
        self.pos        = 0
        self.line       = 1
        self.line_start = 0
        self.last_token  = None          # para contexto regex vs división
        self._peeked: list[Token] = []  # buffer interno para tokens pre-calculados

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def nextToken(self) -> Token | None:
        """
        Devuelve el siguiente Token, o None al llegar al EOF.
        Lanza LexerError ante un token inválido.
        """
        if self._peeked:
            return self._peeked.pop(0)
        tok = self._scan()
        if tok is None:
            # ASI en EOF: si el último token puede cerrar sentencia, emitir ';'
            # antes de emitir EOF, igual que haría un salto de línea.
            if self.last_token is not None and (
                self.last_token.kind in ASI_TRIGGERS
                or self.last_token.kind in ASI_KEYWORD_TRIGGERS
            ):
                eof_line = self.line
                self._peeked.append(Token("EOF", "", eof_line, 1))
                self.last_token = None   # para no re-emitir ';' en la próxima llamada
                return Token("SEMICOLON", ";", eof_line+1, 1)
            return Token("EOF", "", self.line+1, 1)
        return tok

    def peek(self, offset: int = 1) -> Token | None:
        """
        Permite ver hasta `offset` tokens adelante sin consumirlos.
        peek(1) == el mismo token que devolvería nextToken().
        """
        while len(self._peeked) < offset:
            tok = self._scan()
            if tok is None:
                break
            self._peeked.append(tok)
        if offset <= len(self._peeked):
            return self._peeked[offset - 1]
        return None

    def tokenize(self) -> list[Token]:
        """Consume toda la entrada y devuelve la lista completa de tokens."""
        tokens = []
        tok = self.nextToken()
        while tok.kind != "EOF":
            tokens.append(tok)
            tok = self.nextToken()
        return tokens

    # ------------------------------------------------------------------
    # Lógica interna de escaneo
    # ------------------------------------------------------------------

    def _scan(self) -> Token | None:
        src = self.src

        while self.pos < len(src):
            pos        = self.pos
            line       = self.line
            line_start = self.line_start

            m = MASTER_RE.match(src, pos)

            # ── error léxico ──────────────────────────────────────────
            if m is None or m.start() > pos:
                bad_col = len(src[line_start:pos]) + 1
                raise LexerError(line, bad_col)

            # ── identificar grupo ────────────────────────────────────
            kind = None
            for k, v in m.groupdict().items():
                if v is not None:
                    kind = "_".join(k.split("_")[1:])
                    break

            col    = len(src[line_start:m.start()]) + 1
            lexeme = m.group()
            nl_count = lexeme.count("\n")

            # ── regex vs división (/) ─────────────────────────────────
            if src[pos] == "/":
                if pos + 1 < len(src) and src[pos + 1] in ("/", "*"):
                    pass  # es comentario → cae al manejo normal
                else:
                    if self.last_token.kind not in DIVISION_CONTEXT:
                        tok = self._try_scan_regex(pos, line, col)
                        if tok is not None:
                            self.last_token.kind = "REGEX"
                            return tok

            # ── tokens a ignorar (espacios / comentarios) ─────────────
            if kind in ("COMMENT_ML", "SPACE", "COMMENT_SL"):
                self.line += nl_count
                if nl_count:
                    self.line_start = m.start() + lexeme.rfind("\n") + 1
                self.pos = m.end()
                continue

            if kind == "COMMENT_ML_UNCLOSED":
                raise LexerError(line, col)

            if kind == "NEWLINE":
                self.line      += 1
                self.line_start = m.end()
                self.pos        = m.end()
                
                # ¿El token anterior puede cerrar sentencia?
                last_is_trigger = self.last_token is not None and (self.last_token.kind in ASI_TRIGGERS or 
                    self.last_token.kind in ASI_KEYWORD_TRIGGERS) and (self.last_token.line == line)
                
                if last_is_trigger:
                    # Mirar qué viene después para aplicar ASI_BLOCKERS
                    next_tok = self.peek() # escanea el siguiente real
                    
                    if next_tok is None:
                        # EOF tras trigger → sí aplica ASI
                        return Token("SEMICOLON", ";", line, col)

                    if next_tok.kind in ASI_BLOCKERS:
                        # El siguiente token bloquea ASI → no insertar ';'
                        return self._peeked.pop(0)
                    else:
                        # Sí aplica ASI → emitir ';' y guardar el siguiente
                        return Token("SEMICOLON", ";", line, col)
                continue

            # ── keyword vs identificador ──────────────────────────────
            if kind == "IDENT" and lexeme in KEYWORDS:
                kind = lexeme

            # ── PERIOD2 → dos tokens separados ───────────────────────
            if kind == "PERIOD2":
                self._peeked.append(Token("PERIOD", ".", line, col + 1))
                self.pos = m.end()
                tok = Token("PERIOD", ".", line, col)
                self.last_token = tok
                return tok

            # ── token normal ──────────────────────────────────────────
            self.pos       = m.end()
            tok = Token(kind, lexeme, line, col)
            self.last_token = tok
            return tok

        return None  # EOF

    def _try_scan_regex(self, pos: int, line: int, col: int) -> Token | None:
        """
        Intenta consumir una literal regex desde `pos`.
        Devuelve un Token REGEX si tiene éxito, o None si no es regex.
        """
        src = self.src
        j   = pos + 1
        buf = []

        while j < len(src) and src[j] != "\n":
            if src[j] == "\\" and j + 1 < len(src):
                buf.append(src[j])
                buf.append(src[j + 1])
                j += 2
                continue
            if src[j] == "/":
                content = "".join(buf)
                if content:                     # regex vacía //, no aplica
                    self.pos = j + 1
                    return Token("REGEX", content, line, col)
                return None
            buf.append(src[j])
            j += 1

        return None  # no se cerró → no es regex

