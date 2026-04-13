import sys
import os

# Añade la carpeta padre al "camino" de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Parser.lexer import Lexer, LexerError, Token

src = """
// Código ESJS
// Caso 1: ASI básico con retornar
funcion suma(a, b) {
    retornar
    a + b
}

// Caso 2: ASI bloqueado por (
funcion llamada() {
    var x = obtener()
    (x + 1).toString()
}

// Caso 3: ASI bloqueado por [
funcion acceso() {
    var arr = [1, 2, 3]
    [0, 1].forEach(funcion(i) {})
}

// Caso 4: ++ y -- como triggers
funcion contadores() {
    var i = 0
    
    ;
    i++
    i--
    ++i
}

// Caso 5: break y continue
funcion bucle() {
    mientras (verdadero) {
        si (x > 10) {
            romper
        }
        continuar
    }
}

// Caso 6: encadenamiento de métodos (NO debe insertar ';')
funcion cadena() {
    var resultado = [1, 2, 3]
        .filter(funcion(x) { retornar x > 1 })
        .map(funcion(x) { retornar x * 2 })
}

// Caso 7: operadores al inicio de línea (NO debe insertar ';')
funcion operadores() {
    var total = 1
        + 2
        + 3
}

// Caso 8: lanzar error
funcion validar(x) {
    si (x < 0) {
        lanzar
        nuevo Error("negativo")
    }
}

// Caso 9: múltiples asignaciones
funcion asignaciones() {
    var a = 1
    var b = 2
    var c = a + b
    var d = c * 2
}

// Caso 10: regex después de operadores (no debe confundirse con división)
funcion regex() {
    var patron = /hola mundo/
    var resultado = texto.replace(/\d+/, "numero")
    var division = 10 / 2
    var otro = total / cantidad
}
"""

lexer = Lexer(src)

# Opción 1 — token a token
while True:
    tok = lexer.nextToken()
    if tok.kind == "EOF": break
    print(tok)