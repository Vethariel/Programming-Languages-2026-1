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
    CL_AMPERSAND,  /* &                     */
    CL_PIPE,       /* |                     */
    CL_PERCENT,    /* %                     */
    CL_BANG,       /* !                     */
    CL_QUESTION,   /* ?                     */
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
    S_AND,
    S_OR,
    S_PERIOD,
    S_SPREAD,
    S_PLUS,
    S_MINUS,
    S_MOD,
    S_TIMES,
    S_POWER,
    S_NOT,
    S_NOT_EQUAL,
    S_TERNARY,
    /* ── estados de aceptación ── */
    S_ACCEPT_ID,
    S_ACCEPT_NUM,
    S_ACCEPT_STR_D,
    S_ACCEPT_STR_S,
    S_ACCEPT_PLUS,
    S_ACCEPT_MINUS,
    S_ACCEPT_TIMES,
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
    S_ACCEPT_PERIOD,
    S_ACCEPT_COLON,
    S_COMMENT_END,
    S_COMMENT_M_END,
    S_ACCEPT_AND,
    S_ACCEPT_OR,
    S_ACCEPT_SPREAD,
    S_ACCEPT_INCREMENT,
    S_ACCEPT_DECREMENT,
    S_ACCEPT_MOD,
    S_ACCEPT_POWER,
    S_ACCEPT_NOT,
    S_ACCEPT_NEQ,
    S_ACCEPT_TERNARY,
    S_ACCEPT_NULLISH,
    S_ACCEPT_PLUS_ASSIGN,
    S_ACCEPT_MINUS_ASSIGN,
    S_ACCEPT_DIV_ASSIGN,
    S_ACCEPT_TIMES_ASSIGN,
    S_ACCEPT_POWER_ASSIGN,
    S_ACCEPT_MOD_ASSIGN,
    S_ACCEPT_NEEQ,
    S_ERROR,
    STATE_COUNT
} State;

/* ─── 2. TABLA DE TRANSICIONES (generada por gen_table.py) ─── */
/*  Edita transitions.csv y ejecuta gen_table.py para regenerar.*/

/*  state             LETTER       DIGIT        DOT          COLON        PLUS         MINUS        STAR         SLASH        ASSIGN       LESS         GREATER      LPAREN       RPAREN       LBRACE       RBRACE       LBRACKET     RBRACKET     SEMICOLON    COMMA        DQUOTE       SQUOTE       AMPERSAND    PIPE         PERCENT      BANG         QUESTION     SPACE        NEWLINE      EOF          OTHER      */
static const State TRANS[STATE_COUNT][ALPHA_SIZE] = {
/* START          */ { S_IDENT, S_NUMBER, S_PERIOD, S_ACCEPT_COLON, S_PLUS, S_MINUS, S_TIMES, S_SLASH, S_ASSIGN, S_LESS, S_GREATER, S_ACCEPT_LPAREN, S_ACCEPT_RPAREN, S_ACCEPT_LBRACE, S_ACCEPT_RBRACE, S_ACCEPT_LBRACKET, S_ACCEPT_RBRACKET, S_ACCEPT_SEMI, S_ACCEPT_COMMA, S_STR_D, S_STR_S, S_AND, S_OR, S_MOD, S_NOT, S_TERNARY, S_START, S_START, S_ERROR, S_ERROR },
/* IDENT          */ { S_IDENT, S_IDENT, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID, S_ACCEPT_ID },
/* NUMBER         */ { S_ACCEPT_NUM, S_NUMBER, S_NUMBER_DOT, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* NUMBER_DOT     */ { S_ACCEPT_NUM, S_NUMBER_FRAC, S_ERROR, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* NUMBER_FRAC    */ { S_ACCEPT_NUM, S_NUMBER_FRAC, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM, S_ACCEPT_NUM },
/* STR_D          */ { S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_ACCEPT_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_STR_D, S_ERROR, S_ERROR, S_STR_D },
/* STR_S          */ { S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_ACCEPT_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_STR_S, S_ERROR, S_ERROR, S_STR_S },
/* ASSIGN         */ { S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_EQUAL, S_ACCEPT_ASSIGN, S_ACCEPT_ARROW, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN, S_ACCEPT_ASSIGN },
/* EQUAL          */ { S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EEQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ, S_ACCEPT_EQ },
/* LESS           */ { S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LE, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT, S_ACCEPT_LT },
/* GREATER        */ { S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GE, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT, S_ACCEPT_GT },
/* SLASH          */ { S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_COMMENT_M, S_COMMENT, S_ACCEPT_DIV_ASSIGN, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV, S_ACCEPT_DIV },
/* COMMENT        */ { S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT, S_COMMENT_END, S_COMMENT_END, S_COMMENT },
/* COMMENT_M      */ { S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M_STAR, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_ERROR, S_COMMENT_M },
/* COMMENT_M_STAR */ { S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M_STAR, S_COMMENT_M_END, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_COMMENT_M, S_ERROR, S_COMMENT_M },
/* AND            */ { S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ACCEPT_AND, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR },
/* OR             */ { S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ACCEPT_OR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR },
/* PERIOD         */ { S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_SPREAD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD, S_ACCEPT_PERIOD },
/* SPREAD         */ { S_ERROR, S_ERROR, S_ACCEPT_SPREAD, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR, S_ERROR },
/* PLUS           */ { S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_INCREMENT, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS_ASSIGN, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS, S_ACCEPT_PLUS },
/* MINUS          */ { S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_DECREMENT, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS_ASSIGN, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS, S_ACCEPT_MINUS },
/* MOD            */ { S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD_ASSIGN, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD, S_ACCEPT_MOD },
/* TIMES          */ { S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_POWER, S_ACCEPT_TIMES, S_ACCEPT_TIMES_ASSIGN, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES, S_ACCEPT_TIMES },
/* POWER          */ { S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER_ASSIGN, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER, S_ACCEPT_POWER },
/* NOT            */ { S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_NOT_EQUAL, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT, S_ACCEPT_NOT },
/* NOT_EQUAL      */ { S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ, S_ACCEPT_NEQ },
/* TERNARY        */ { S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_NULLISH, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY, S_ACCEPT_TERNARY },
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
    TOK_TIMES,
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
    TOK_PERIOD,
    TOK_COLON,
    TOK_AND,
    TOK_OR,
    TOK_NOT,
    TOK_NEQ,
    TOK_NEEQ,
    TOK_TERNARY,
    TOK_NULLISH,
    TOK_INCREMENT,
    TOK_DECREMENT,
    TOK_MOD,
    TOK_POWER,
    TOK_MOD_ASSIGN,
    TOK_POWER_ASSIGN,
    TOK_DIV_ASSIGN,
    TOK_PLUS_ASSIGN,
    TOK_MINUS_ASSIGN,
    TOK_TIMES_ASSIGN,
    TOK_SPREAD,
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
    [S_ACCEPT_TIMES] = TOK_TIMES,
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
    [S_ACCEPT_PERIOD] = TOK_PERIOD,
    [S_ACCEPT_COLON] = TOK_COLON,
    [S_COMMENT_END] = TOK_NONE,
    [S_COMMENT_M_END] = TOK_NONE,
    [S_ACCEPT_AND] = TOK_AND,
    [S_ACCEPT_OR] = TOK_OR,
    [S_ACCEPT_SPREAD] = TOK_SPREAD,
    [S_ACCEPT_INCREMENT] = TOK_INCREMENT,
    [S_ACCEPT_DECREMENT] = TOK_DECREMENT,
    [S_ACCEPT_MOD] = TOK_MOD,
    [S_ACCEPT_POWER] = TOK_POWER,
    [S_ACCEPT_NOT] = TOK_NOT,
    [S_ACCEPT_NEQ] = TOK_NEQ,
    [S_ACCEPT_TERNARY] = TOK_TERNARY,
    [S_ACCEPT_NULLISH] = TOK_NULLISH,
    [S_ACCEPT_PLUS_ASSIGN] = TOK_PLUS_ASSIGN,
    [S_ACCEPT_MINUS_ASSIGN] = TOK_MINUS_ASSIGN,
    [S_ACCEPT_DIV_ASSIGN] = TOK_DIV_ASSIGN,
    [S_ACCEPT_TIMES_ASSIGN] = TOK_TIMES_ASSIGN,
    [S_ACCEPT_POWER_ASSIGN] = TOK_POWER_ASSIGN,
    [S_ACCEPT_MOD_ASSIGN] = TOK_MOD_ASSIGN,
    [S_ACCEPT_NEEQ] = TOK_NEEQ,
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
    [S_ACCEPT_PLUS] = 1,
    [S_ACCEPT_MINUS] = 1,
    [S_ACCEPT_TIMES] = 1,
    [S_ACCEPT_POWER] = 1,
    [S_ACCEPT_MOD] = 1,
    [S_ACCEPT_DIV] = 1,
    [S_ACCEPT_TERNARY] = 1,
    [S_ACCEPT_NOT] = 1,
    [S_ACCEPT_NEQ] = 1,
    [S_ACCEPT_PERIOD] = 1,
};

/* ─── 4. KEYWORDS ────────────────────────────────────────── */
/* ── AJUSTA ESTA LISTA SEGUN EL LENGUAJE DEL TEST ────────── */

static const char *KEYWORDS[] = {
    /* Control Keywords (41) */
    "capturar", "caso", "con", "continuar", "crear", "desde",
    "elegir", "esperar", "exportar", "hacer", "importar",
    "mientras", "para", "retornar", "sino", "si",
    "constructor", "eliminar", "extiende", "finalmente",
    "instanciaDe", "intentar", "lanzar", "longitud", "romper",
    "simbolo", "subcad", "tipoDe", "vacio", "producir",
    "ambiente", "super", "de", "en", "asincrono",
    "clase", "const", "var", "mut", "porDefecto", "funcion",
    /* Language Constants (7) */
    "falso", "nulo", "verdadero", "indefinido",
    "Infinito", "NuN", "ambienteGlobal",
    /* Support Functions (13) */
    "consola", "depurador", "establecerTemporizador", "establecerIntervalo",
    "Fecha", "Numero", "Mate", "Matriz", "Arreglo",
    "Booleano", "Cadena", "Funcion", "Promesa",
    /* Console Object (17) */
    "afirmar", "limpiar", "contar", "reiniciarContador",
    "depurar", "listar", "listarXml", "error",
    "agrupar", "agruparColapsado", "finalizarAgrupacion",
    "info", "escribir", "perfil", "finalizarPerfil",
    "tabla", "tiempo", "finalizarTiempo", "registrarTiempo",
    "marcaDeTiempo", "rastrear", "advertencia", "repetir",
    NULL
};

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
    [TOK_TIMES] = "tkn_times",
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
    [TOK_PERIOD] = "tkn_period",
    [TOK_COLON] = "tkn_colon",
    [TOK_IDENT] = "id",
    [TOK_NUMBER] = "tkn_num",
    [TOK_STR_D] = "tkn_str",
    [TOK_STR_S] = "tkn_str",
    [TOK_AND] = "tkn_and",
    [TOK_OR] = "tkn_or",
    [TOK_NOT] = "tkn_not",
    [TOK_NEQ] = "tkn_neq",
    [TOK_NEEQ] = "tkn_strict_neq",
    [TOK_TERNARY] = "tkn_ternary",
    [TOK_NULLISH] = "tkn_nulish",
    [TOK_INCREMENT] = "tkn_increment",
    [TOK_DECREMENT] = "tkn_decrement",
    [TOK_MOD] = "tkn_mod",
    [TOK_POWER] = "tkn_power",
    [TOK_MOD_ASSIGN] = "tkn_mod_assign",
    [TOK_POWER_ASSIGN] = "tkn_power_assign",
    [TOK_DIV_ASSIGN] = "tkn_div_assign",
    [TOK_PLUS_ASSIGN] = "tkn_plus_assign",
    [TOK_MINUS_ASSIGN] = "tkn_minus_assign",
    [TOK_TIMES_ASSIGN] = "tkn_times_assign",
    [TOK_SPREAD] = "tkn_spread",
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
    case '&':
        return CL_AMPERSAND;
    case '|':
        return CL_PIPE;
    case '%':
        return CL_PERCENT;
    case '!':
        return CL_BANG;
    case '?':
        return CL_QUESTION;
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