#include <stdio.h>
#include <string.h>

#define TAM_BUFFER 1048576  // 1 MB

typedef struct {
    char *inicio;
    int   token_len;
    int   token_fila;
    int   token_col;
    int   fila;
    int   col;
    int   estado;
} Lexer;

void leer_input(char *fuente) {
    int len = 0;
    int c;
    while (len < TAM_BUFFER - 1 && (c = getchar()) != EOF) {
        fuente[len++] = (char)c;
    }
    fuente[len] = '\0';
}

void inicializar_lexer(Lexer *lx, char *fuente) {
    lx->inicio     = fuente;
    lx->token_len  = 0;
    lx->token_fila = 1;
    lx->token_col  = 1;
    lx->fila       = 1;
    lx->col        = 1;
    lx->estado     = 0;
}

void emitir_token(Lexer *lx) {
    if (lx->token_len > 0) {
        printf("<tkn,%.*s,%d,%d>\n", lx->token_len, lx->inicio, lx->token_fila, lx->token_col);
        lx->token_len = 0;
    }
}

void analizar(Lexer *lx, char *fuente) {
    char *actual = fuente;

    while (*actual != '\0') {

        if (*actual == ' ' || *actual == '\t' || *actual == '\r' || *actual == '\n') {
            emitir_token(lx);
            if (*actual == '\n') { lx->fila++; lx->col = 1; }
            else                 { lx->col++;               }
        } else {
            if (lx->token_len == 0) {
                lx->inicio     = actual;
                lx->token_fila = lx->fila;
                lx->token_col  = lx->col;
            }
            lx->token_len++;
            lx->col++;
        }

        actual++;
    }

    emitir_token(lx);
}

int main() {
    char  fuente[TAM_BUFFER];
    Lexer lexer;

    leer_input(fuente);
    inicializar_lexer(&lexer, fuente);
    analizar(&lexer, fuente);

    return 0;
}