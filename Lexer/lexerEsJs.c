#include <stdio.h>
#include <stdlib.h>

#define TAM_BUFFER 1048576  // 1MB, suficiente para cualquier caso de prueba

int main() {
    char *fuente = malloc(TAM_BUFFER);
    int  len     = 0;
    int  c;

    while ((c = getchar()) != EOF) {
        fuente[len++] = (char)c;
    }
    fuente[len] = '\0';

    // aquí arranca el lexer
    // ...

    free(fuente);
    return 0;
}