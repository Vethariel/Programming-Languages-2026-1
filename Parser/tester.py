import subprocess
import sys
import os

# ── Colores ANSI ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ── Ruta al parser (ajusta si es necesario) ───────────────────────────────────
PARSER_CMD = [sys.executable, "Parser/parser.py"]   # cambia a ["java", "Parser"] si usas Java

# ── Casos de prueba ───────────────────────────────────────────────────────────
TEST_CASES = [
    # ── Del enunciado ─────────────────────────────────────────────────────────
    {
"name": "Función iniciar con Fecha (OK)",
"input": """\
//Ejemplo Fecha
funcion iniciar() {
    const fecha = crear Fecha()
    consola.escribir(fecha)
}

iniciar()
""",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "var seguido de literal numérico",
"input": "var 1;",
"expected": '<1:5> Error sintactico: se encontro: "1"; se esperaba: "id".',
    },
    {
"name": "consola.escribir con dos argumentos sin coma",
"input": 'consola.escribir(45"this")',
"expected": (
'<1:20> Error sintactico: se encontro: "this"; '
'se esperaba: "&&", ")", "/", "==", ">=", ">", "<=", "<", "-", "%", '
'"!=", "??", "||", "+", "**", "===", "!==", "?", "*".'
        ),
    },
    {
"name": "mut con si/sino (OK)",
"input": """\
mut entrada;

si (entrada === indefinido) {
  consola.error('Valor indefinido');
} sino {
  consola.escribir('Valor definido');
}
""",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "mientras con punto faltante",
"input": """\
mut i = 0;

mientras (i < 5) {
    consola escribir(i);
    i = i + 1;
}
""",
"expected": '<4:13> Error sintactico: se encontro: "escribir"; se esperaba: ".".',
    },

    # ── Casos extra ───────────────────────────────────────────────────────────
    {
"name": "Programa vacío (OK)",
"input": "",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Declaración var simple (OK)",
"input": "var x = 42;",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Declaración mut sin inicialización (OK)",
"input": "mut y;",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Función con parámetros y retorno (OK)",
"input": """\
funcion suma(a, b) {
    retornar a + b;
}
""",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Llamada encadenada consola.escribir (OK)",
"input": 'consola.escribir("hola mundo");',
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Expresión aritmética compleja (OK)",
"input": 'var r = "n" + a - verdadero * (vari[3] % 70);',
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Múltiples vars en una línea (OK)",
"input": "var a = 4; var b = 5;",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Llave de cierre faltante",
"input": """\
funcion foo() {
    var x = 1;
""",
"expected": None,   # None = no comprobamos texto exacto, solo que hay error
    },
    {
"name": "Paréntesis de cierre faltante en mientras",
"input": """\
mientras (i < 10 {
    i = i + 1;
}
""",
"expected": None,
    },
    {
"name": "Operador == en condición si (OK)",
"input": """\
si (x == 5) {
    consola.escribir(x);
}
""",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Operador === en condición si (OK)",
"input": """\
si (x === nulo) {
    consola.escribir(x);
}
""",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "Acceso a índice de arreglo (OK)",
"input": "var v = arr[i + 1];",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
    {
"name": "nuevo objeto con new/crear (OK)",
"input": "const obj = crear MiClase(1, 2);",
"expected": "El analisis sintactico ha finalizado exitosamente.",
    },
]

# ── Ejecutar un caso ──────────────────────────────────────────────────────────
def run_case(tc):
    try:
        result = subprocess.run(
            PARSER_CMD,
            input=tc["input"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        output = "__TIMEOUT__"
    except FileNotFoundError as e:
        output = f"__ERROR__: {e}"
    return output

# ── Comparar resultado ────────────────────────────────────────────────────────
def check(tc, output):
    expected = tc["expected"]
    if expected is None:
        # Solo verificamos que NO diga que finalizó exitosamente
        ok = "exitosamente" not in output.lower()
        note = "(se espera cualquier error sintáctico)"
    else:
        ok = output == expected
        note = ""
    return ok, note

# ── Runner principal ──────────────────────────────────────────────────────────
def main():
    passed = 0
    failed = 0
    errors = 0

    print(f"\n{BOLD}{CYAN}{'═'*64}{RESET}")
    print(f"{BOLD}{CYAN}  Tester — Analizador Sintáctico EsJs{RESET}")
    print(f"{BOLD}{CYAN}{'═'*64}{RESET}\n")

    for i, tc in enumerate(TEST_CASES, 1):
        output = run_case(tc)

        if output.startswith("__"):
            status = f"{RED}ERROR{RESET}"
            errors += 1
        else:
            ok, note = check(tc, output)
            if ok:
                status = f"{GREEN}PASS{RESET}"
                passed += 1
            else:
                status = f"{RED}FAIL{RESET}"
                failed += 1

        print(f"[{i:02d}] {status}  {tc['name']}")

        if not output.startswith("__"):
            ok, note = check(tc, output)
            if not ok:
                exp = tc["expected"] if tc["expected"] is not None else "(cualquier error)"
                print(f"       {YELLOW}Esperado:{RESET} {exp}")
                print(f"       {YELLOW}Obtenido:{RESET} {output}")
            elif note:
                print(f"       {CYAN}{note}{RESET}")
        else:
            print(f"       {RED}{output}{RESET}")

    total = len(TEST_CASES)
    print(f"\n{BOLD}{'─'*64}{RESET}")
    print(f"  Total: {total}  |  "
          f"{GREEN}Pasaron: {passed}{RESET}  |  "
          f"{RED}Fallaron: {failed}{RESET}  |  "
          f"{YELLOW}Errores de ejecución: {errors}{RESET}")
    print(f"{BOLD}{'─'*64}{RESET}\n")

    sys.exit(0 if failed == 0 and errors == 0 else 1)

if __name__ == "__main__":
    main()
