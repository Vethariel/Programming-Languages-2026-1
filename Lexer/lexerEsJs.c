#include <stdio.h>
#include <string.h>

#define TAM_BUFFER 1048576 // 1 MB

typedef enum
{
    EST_INICIO,
    EST_IDENTIFICADOR,
    EST_NUMERO,
    EST_STRING,
    EST_OPERADOR,
    EST_ERROR
} Estado;

typedef struct
{
    char *inicio;
    int token_len;
    int token_fila;
    int token_col;
    int fila;
    int col;
    Estado estado;
} Lexer;

/* ── clasificadores de carácter ─────────────────── */

int es_espacio(unsigned char c)
{
    return c == ' ' || c == '\t' || c == '\r';
}

int es_salto_linea(unsigned char c)
{
    return c == '\n';
}

int es_letra(unsigned char c)
{
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
           c == '_' || c == '$' ||
           c > 127;
}

int es_digito(unsigned char c)
{
    return c >= '0' && c <= '9';
}

int es_comilla(unsigned char c)
{
    return c == '"' || c == '\'';
}

int es_operador(unsigned char c)
{
    return c == '+' || c == '-' || c == '*' || c == '/' ||
           c == '=' || c == '!' || c == '<' || c == '>' ||
           c == '&' || c == '|' || c == '?' || c == '.' ||
           c == ',' || c == ';' || c == ':' || c == '%' ||
           c == '(' || c == ')' || c == '{' || c == '}' ||
           c == '[' || c == ']';
}

Estado clasificar_caracter(unsigned char c)
{
    if (es_letra(c))
        return EST_IDENTIFICADOR;
    if (es_digito(c))
        return EST_NUMERO;
    if (es_comilla(c))
        return EST_STRING;
    if (es_operador(c))
        return EST_OPERADOR;
    return EST_ERROR;
}

/* ── gestión del lexer ──────────────────────────── */

void leer_input(char *fuente)
{
    int len = 0;
    int c;
    while (len < TAM_BUFFER - 1 && (c = getchar()) != EOF)
    {
        fuente[len++] = (char)c;
    }
    fuente[len] = '\0';
}

void inicializar_lexer(Lexer *lx, char *fuente)
{
    lx->inicio = fuente;
    lx->token_len = 0;
    lx->token_fila = 1;
    lx->token_col = 1;
    lx->fila = 1;
    lx->col = 1;
    lx->estado = EST_INICIO;
}

void emitir_token(Lexer *lx)
{
    if (lx->token_len > 0)
    {
        printf("<tkn,%.*s,%d,%d>\n", lx->token_len, lx->inicio,
               lx->token_fila, lx->token_col);
        lx->token_len = 0;
        lx->estado = EST_INICIO;
    }
}

void iniciar_token(Lexer *lx, char *actual, Estado estado)
{
    lx->inicio = actual;
    lx->token_fila = lx->fila;
    lx->token_col = lx->col;
    lx->estado = estado;
    lx->token_len = 1;
}

void analizar(Lexer *lx, char *fuente)
{
    char *actual = fuente;

    while (*actual != '\0')
    {
        unsigned char c = (unsigned char)*actual;

        if (es_salto_linea(c))
        {
            emitir_token(lx);
            lx->fila++;
            lx->col = 1;
        }
        else if (es_espacio(c))
        {
            emitir_token(lx);
            lx->col++;
        }

        else
        {
            Estado nuevo = clasificar_caracter(c);

            if (nuevo == EST_ERROR)
            {
                printf(">>> Error lexico (linea: %d, posicion: %d)\n",
                       lx->fila, lx->col);
                return;
            }

            if (lx->estado == EST_INICIO)
            {
                iniciar_token(lx, actual, nuevo);
            }
            else if (nuevo == lx->estado)
            {
                lx->token_len++;
            }
            else
            {
                emitir_token(lx);
                iniciar_token(lx, actual, nuevo);
            }

            lx->col++;
        }

        actual++;
    }

    emitir_token(lx);
}

/* ── main ───────────────────────────────────────── */

int main()
{
    char fuente[TAM_BUFFER];
    Lexer lexer;

    leer_input(fuente);
    inicializar_lexer(&lexer, fuente);
    analizar(&lexer, fuente);

    return 0;
}