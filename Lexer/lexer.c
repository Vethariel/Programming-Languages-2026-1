/*
 * ============================================================
 *  LEXER con tablas de transición — sin copia de lexemas
 * ============================================================
 *  CÓMO AJUSTAR PARA LOS TEST OCULTOS:
 *  1. Edita transitions.csv y corre: python3 gen_table.py transitions.csv --patch lexer.c
 *  2. Añade/quita entradas en KEYWORDS[] y TOKEN_PRINT[].
 *  3. Cambia print_token() si el formato de salida varía.
 *  El motor (next_token / lex) NO necesita tocarse.
 * ============================================================
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>

/* ─── 1. CLASES DE CARACTERES (columnas de la tabla) ─────── */

typedef enum
{
    CL_LETTER = 0, /* a-z  A-Z  _           */
    CL_DIGIT,      /* 0-9                   */
    CL_DOT,        /* .  (decimal)          */
    CL_COLON,      /* :  (dos puntos)       */
    CL_PLUS,       /* +                     */
    CL_MINUS,      /* -                     */
    CL_STAR,       /* *                     */
    CL_SLASH,      /* /                     */
    CL_ASSIGN,     /* =                     */
    CL_LESS,       /* <                     */
    CL_GREATER,    /* >                     */
    CL_LPAREN,     /* (                     */
    CL_RPAREN,     /* )                     */
    CL_LBRACE,     /* {                     */
    CL_RBRACE,     /* }                     */
    CL_LBRACKET,   /* [                     */
    CL_RBRACKET,   /* ]                     */
    CL_SEMICOLON,  /* ;                     */
    CL_COMMA,      /* ,                     */
    CL_DQUOTE,     /* "                     */
    CL_SQUOTE,     /* '                     */
    CL_SPACE,      /* espacio / \t / \r     */
    CL_NEWLINE,    /* \n                    */
    CL_EOF,        /* \0                    */
    CL_OTHER,      /* cualquier otro        */
    ALPHA_SIZE
} CharClass;

typedef enum
{
    S_START = 0,
    S_IDENT,
    S_NUMBER,
    S_NUMBER_DOT,
    S_NUMBER_FRAC,
    S_STR_D,
    S_STR_S,
    S_ASSIGN,
    S_EQUAL,
    S_LESS,
    S_GREATER,
    S_SLASH,
    S_COMMENT,
    S_COMMENT_M,
    S_COMMENT_M_STAR,
    /* ── estados de aceptación ── */
    S_ACCEPT_ID,
    S_ACCEPT_NUM,
    S_ACCEPT_STR_D,
    S_ACCEPT_STR_S,
    S_ACCEPT_PLUS,
    S_ACCEPT_MINUS,
    S_ACCEPT_STAR,
    S_ACCEPT_DIV,
    S_ACCEPT_ASSIGN,
    S_ACCEPT_EQ,
    S_ACCEPT_EEQ,
    S_ACCEPT_ARROW,
    S_ACCEPT_LT,
    S_ACCEPT_LE,
    S_ACCEPT_GT,
    S_ACCEPT_GE,
    S_ACCEPT_LPAREN,
    S_ACCEPT_RPAREN,
    S_ACCEPT_LBRACE,
    S_ACCEPT_RBRACE,
    S_ACCEPT_LBRACKET,
    S_ACCEPT_RBRACKET,
    S_ACCEPT_SEMI,
    S_ACCEPT_COMMA,
    S_ACCEPT_DOT,
    S_ACCEPT_COLON,
    S_COMMENT_END,
    S_COMMENT_M_END,
    S_ERROR,
    STATE_COUNT
} State;

/* ─── 2. TABLA DE TRANSICIONES (generada por gen_table.py) ─── */
/*  Edita transitions.csv y ejecuta gen_table.py para regenerar.*/

/*  state             LETTER       DIGIT        DOT          COLON        PLUS         MINUS        STAR         SLASH        ASSIGN       LESS         GREATER      LPAREN       RPAREN       LBRACE       RBRACE       LBRACKET     RBRACKET     SEMICOLON    COMMA        DQUOTE       SQUOTE       SPACE        NEWLINE      EOF          OTHER      */
static const State TRANS[STATE_COUNT][ALPHA_SIZE] = {
/* START          */ { S_IDENT, S_NUMBER, S_ACCEPT_DOT, S_ACCEPT_COLON, S_ACCEPT_PLUS, S_ACCEPT_MINUS, S_ACCEPT_STAR, S_SLASH, S_ASSIGN, S_LESS, S_GREATER, S_ACCEPT_LPAREN, S_ACCEPT_RPAREN, S_ACCEPT_LBRACE, S_ACCEPT_RBRACE, S_ACCEPT_LBRACKET, S_ACCEPT_RBRACKET, S_ACCEPT_SEMI, S_ACCEPT_COMMA, S_STR_D, S_STR_S, S_START, S_START, S_ERROR, S_ERROR },
/* IDENT          */ { S_IDENT, S_IDENT, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID },
/* NUMBER         */ { S_ACCEPT_NUM, S_NUMBER, S_NUMBER_DOT, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* NUMBER_DOT     */ { S_ACCEPT_NUM, S_NUMBER_FRAC, S_ERROR, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* NUMBER_FRAC    */ { S_ACCEPT_NUM, S_NUMBER_FRAC, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* STR_D          */ { S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_ACCEPT_STR_D, S_STR_D, S_STR_D, S_ERROR, S_ERROR, S_STR_D },
/* STR_S          */ { S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_ACCEPT_STR_S, S_STR_S, S_ERROR, S_ERROR, S_STR_S },
/* ASSIGN         */ { S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_EQUAL, S_ACCEPT_ASSIGN, S_ACCEPT_ARROW, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN },
/* EQUAL          */ { S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EEQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ },
/* LESS           */ { S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LE, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT },
/* GREATER        */ { S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GE, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT },
/* SLASH          */ { S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_COMMENT_M, S_COMMENT, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV },
/* COMMENT        */ { S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT_END, S_COMMENT_END, S_COMMENT },
/* COMMENT_M      */ { S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M_STAR, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_ERROR, S_COMMENT_M },
/* COMMENT_M_STAR */ { S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M_STAR, S_COMMENT_M_END, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_ERROR, S_COMMENT_M },
};

/* ─── 3. PROPIEDADES DE ESTADOS ──────────────────────────── */

typedef enum
{
    TOK_IDENT = 0,
    TOK_KEYWORD,
    TOK_NUMBER,
    TOK_STR_D,
    TOK_STR_S,
    TOK_PLUS,
    TOK_MINUS,
    TOK_STAR,
    TOK_DIV,
    TOK_ASSIGN,
    TOK_EQ,
    TOK_EEQ,
    TOK_ARROW,
    TOK_LT,
    TOK_LE,
    TOK_GT,
    TOK_GE,
    TOK_LPAREN,
    TOK_RPAREN,
    TOK_LBRACE,
    TOK_RBRACE,
    TOK_LBRACKET,
    TOK_RBRACKET,
    TOK_SEMI,
    TOK_COMMA,
    TOK_DOT,
    TOK_COLON,
    TOK_EOF,
    TOK_ERROR,
    TOK_NONE,
    TOK_COUNT
} TokenType;

static const TokenType ACCEPT_TOKEN[STATE_COUNT] = {
    [S_ACCEPT_ID] = TOK_NONE,
    [S_ACCEPT_NUM] = TOK_NUMBER,
    [S_ACCEPT_STR_D] = TOK_STR_D,
    [S_ACCEPT_STR_S] = TOK_STR_S,
    [S_ACCEPT_PLUS] = TOK_PLUS,
    [S_ACCEPT_MINUS] = TOK_MINUS,
    [S_ACCEPT_STAR] = TOK_STAR,
    [S_ACCEPT_DIV] = TOK_DIV,
    [S_ACCEPT_ASSIGN] = TOK_ASSIGN,
    [S_ACCEPT_EQ] = TOK_EQ,
    [S_ACCEPT_EEQ] = TOK_EEQ,
    [S_ACCEPT_ARROW] = TOK_ARROW,
    [S_ACCEPT_LT] = TOK_LT,
    [S_ACCEPT_LE] = TOK_LE,
    [S_ACCEPT_GT] = TOK_GT,
    [S_ACCEPT_GE] = TOK_GE,
    [S_ACCEPT_LPAREN] = TOK_LPAREN,
    [S_ACCEPT_RPAREN] = TOK_RPAREN,
    [S_ACCEPT_LBRACE] = TOK_LBRACE,
    [S_ACCEPT_RBRACE] = TOK_RBRACE,
    [S_ACCEPT_LBRACKET] = TOK_LBRACKET,
    [S_ACCEPT_RBRACKET] = TOK_RBRACKET,
    [S_ACCEPT_SEMI] = TOK_SEMI,
    [S_ACCEPT_COMMA] = TOK_COMMA,
    [S_ACCEPT_DOT] = TOK_DOT,
    [S_ACCEPT_COLON] = TOK_COLON,
    [S_COMMENT_END] = TOK_NONE,
    [S_COMMENT_M_END] = TOK_NONE,
    [S_ERROR] = TOK_ERROR,
};

/* 1 → ultimo char avanzado era lookahead, hay que retroceder */
static const int NEEDS_UNGET[STATE_COUNT] = {
    [S_ACCEPT_ID] = 1,
    [S_ACCEPT_NUM] = 1,
    [S_ACCEPT_ASSIGN] = 1,
    [S_ACCEPT_EQ] = 1,
    [S_ACCEPT_LT] = 1,
    [S_ACCEPT_GT] = 1,
    [S_ACCEPT_DIV] = 1,
    [S_COMMENT_END] = 1,
};

/* ─── 4. KEYWORDS ────────────────────────────────────────── */
/* ── AJUSTA ESTA LISTA SEGUN EL LENGUAJE DEL TEST ────────── */

static const char *KEYWORDS[] = {
    "mut", "const", "var", "caso", "consola", "capturar",
    "si", "sino", "mientras", "para", "repetir", "en",
    "retornar", "romper", "continuar", "Booleano",
    "verdadero", "falso", "nulo", "simbolo", "longitud", "de",
    "funcion", "clase", "importar", "escribir",
    NULL};

static int is_keyword(const char *start, int len)
{
    for (int i = 0; KEYWORDS[i]; i++)
        if ((int)strlen(KEYWORDS[i]) == len &&
            strncmp(start, KEYWORDS[i], len) == 0)
            return 1;
    return 0;
}

/* ─── 5. NOMBRES DE OPERADORES PARA IMPRESION ────────────── */
/* ── AJUSTA AQUI SI EL JUEZ ESPERA OTRO NOMBRE ───────────── */

static const char *TOKEN_PRINT[TOK_COUNT] = {
    [TOK_PLUS] = "tkn_plus",
    [TOK_MINUS] = "tkn_minus",
    [TOK_STAR] = "tkn_times",
    [TOK_DIV] = "tkn_div",
    [TOK_ASSIGN] = "tkn_assign",
    [TOK_EQ] = "tkn_equal",
    [TOK_EEQ] = "tkn_strict_equal",
    [TOK_ARROW] = "tkn_arrow",
    [TOK_LT] = "tkn_less",
    [TOK_LE] = "tkn_leq",
    [TOK_GT] = "tkn_greater",
    [TOK_GE] = "tkn_geq",
    [TOK_LPAREN] = "tkn_opening_par",
    [TOK_RPAREN] = "tkn_closing_par",
    [TOK_LBRACE] = "tkn_opening_key",
    [TOK_RBRACE] = "tkn_closing_key",
    [TOK_LBRACKET] = "tkn_opening_bra",
    [TOK_RBRACKET] = "tkn_closing_bra",
    [TOK_SEMI] = "tkn_semicolon",
    [TOK_COMMA] = "tkn_comma",
    [TOK_DOT] = "tkn_period",
    [TOK_COLON] = "tkn_colon",
    [TOK_IDENT] = "id",
    [TOK_NUMBER] = "tkn_num",
    [TOK_STR_D] = "tkn_str",
    [TOK_STR_S] = "tkn_str",
};

/* ─── 6. CLASIFICADOR DE CARACTERES ─────────────────────── */

static CharClass char_class(char c)
{
    unsigned char u = (unsigned char)c;
    // UTF-8 multibyte: byte inicial de secuencia de 2, 3 o 4 bytes
    // 110xxxxx (0xC0-0xDF), 1110xxxx (0xE0-0xEF), 11110xxx (0xF0-0xF7)
    if (u >= 0xC0 && u <= 0xF7)
        return CL_LETTER;

    // byte de continuación 10xxxxxx (0x80-0xBF) — parte del mismo carácter
    if (u >= 0x80 && u <= 0xBF)
        return CL_LETTER;
    if (isalpha(u) || c == '_' || c == '$')
        return CL_LETTER;
    if (isdigit(u))
        return CL_DIGIT;
    switch (c)
    {
    case '.':
        return CL_DOT;
    case ':':
        return CL_COLON;
    case '+':
        return CL_PLUS;
    case '-':
        return CL_MINUS;
    case '*':
        return CL_STAR;
    case '/':
        return CL_SLASH;
    case '=':
        return CL_ASSIGN;
    case '<':
        return CL_LESS;
    case '>':
        return CL_GREATER;
    case '(':
        return CL_LPAREN;
    case ')':
        return CL_RPAREN;
    case '{':
        return CL_LBRACE;
    case '}':
        return CL_RBRACE;
    case '[':
        return CL_LBRACKET;
    case ']':
        return CL_RBRACKET;
    case ';':
        return CL_SEMICOLON;
    case ',':
        return CL_COMMA;
    case '"':
        return CL_DQUOTE;
    case '\'':
        return CL_SQUOTE;
    case ' ':
    case '\t':
    case '\r':
        return CL_SPACE;
    case '\n':
        return CL_NEWLINE;
    case '\0':
        return CL_EOF;
    default:
        return CL_OTHER;
    }
}

/* ─── 7. ESTRUCTURA DEL TOKEN ────────────────────────────── */

typedef struct
{
    TokenType type;
    const char *start;
    int length;
    int line;
    int col;
} Token;

/* ─── 8. MOTOR DEL LEXER ─────────────────────────────────── */

static Token next_token(const char **p, int *line, int *col)
{
    Token tok;
    State state = S_START;
    const char *start = *p;
    int tok_line = *line;
    int tok_col = *col;

    while (1)
    {
        char c = **p;
        CharClass cl = char_class(c);

        /* EOF desde START */
        if (state == S_START && cl == CL_EOF)
        {
            tok.type = TOK_EOF;
            tok.start = *p;
            tok.length = 0;
            tok.line = *line;
            tok.col = *col;
            return tok;
        }

        State ns = TRANS[state][cl];

        /* fijar inicio del token al salir de START */
        if (state == S_START && ns != S_START)
        {
            start = *p;
            tok_line = *line;
            tok_col = *col;
        }

        /* avanzar puntero y contadores de posición */
        (*p)++;
        if (c == '\n')
        {
            (*line)++;
            *col = 1;
        }
        else
        {
            unsigned char u = (unsigned char)c;
            // solo contar si es byte inicial (ASCII o inicio de multibyte)
            // los bytes de continuación 10xxxxxx no suman columna
            if (u < 0x80 || u > 0xBF)
                (*col)++;
        }
        state = ns;

        /* estado de aceptación */
        if (state >= S_ACCEPT_ID)
        {
            if (NEEDS_UNGET[state])
            {
                (*p)--;
                unsigned char u = (unsigned char)**p;
                if (**p == '\n')
                {
                    (*line)--;
                }
                else if (u < 0x80 || u > 0xBF)
                {
                    (*col)--;
                }
            }

            tok.start = start;
            tok.line = tok_line;
            tok.col = tok_col;
            tok.type = ACCEPT_TOKEN[state];
            tok.length = (int)(*p - tok.start);

            if (state == S_ACCEPT_ID)
                tok.type = is_keyword(tok.start, tok.length)
                               ? TOK_KEYWORD
                               : TOK_IDENT;

            /* comentario: ignorar y reiniciar */
            if (tok.type == TOK_NONE)
            {
                state = S_START;
                start = *p;
                tok_line = *line;
                tok_col = *col;
                continue;
            }
            return tok;
        }
    }
}

/* ─── 9. IMPRESION ───────────────────────────────────────── */
/* ── CAMBIA SOLO ESTE BLOQUE SI EL FORMATO VARIA ─────────── */

static void print_token(const Token *t)
{
    switch (t->type)
    {
    case TOK_KEYWORD:
        /* <lexema,fila,col> */
        printf("<%.*s,%d,%d>\n", t->length, t->start, t->line, t->col);
        break;
    case TOK_NUMBER:
    case TOK_IDENT:
        printf("<%s,%.*s,%d,%d>\n", TOKEN_PRINT[t->type], t->length, t->start, t->line, t->col);
        break;
    case TOK_STR_D:
    case TOK_STR_S:
        printf("<%s,%.*s,%d,%d>\n", TOKEN_PRINT[t->type], t->length - 2, t->start + 1, t->line, t->col);
        break;
    default:
        /* operadores y simbolos: <tkn_nombre,fila,col> */
        if (TOKEN_PRINT[t->type])
            printf("<%s,%d,%d>\n", TOKEN_PRINT[t->type], t->line, t->col);
        break;
    }
}

/* ─── 10. BUCLE PRINCIPAL ────────────────────────────────── */

static void lex(const char *src)
{
    const char *p = src;
    int line = 1, col = 1;

    while (1)
    {
        Token t = next_token(&p, &line, &col);
        if (t.type == TOK_EOF)
            break;
        if (t.type == TOK_ERROR)
        {
            printf(">>> Error lexico (linea: %d, posicion: %d)\n",
                   t.line, t.col);
            break;
        }
        print_token(&t);
    }
}

/* ─── 11. ENTRADA ────────────────────────────────────────── */

#define MAX_SRC 65536

int main(void)
{
    static char src[MAX_SRC];
    int c, i = 0;
    while ((c = getchar()) != EOF && i < MAX_SRC - 1)
        src[i++] = (char)c;
    src[i] = '\0';
    lex(src);
    return 0;
}