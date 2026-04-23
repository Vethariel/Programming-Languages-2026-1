import subprocess
import sys
import os
from datetime import datetime

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
    # ── Casos oficiales ───────────────────────────────────────────────────────────
    {
"name": "Test 1",
"input": """\
n1=125%(2/3)*5+2**2
n2=50+22 / (14-7) % 2
// imprimimos los valores
consola.escribir( n1+ ' '+n2)""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 2",
"input": """\
funcion my_function()[
   consola.info("asi no era *smile in full pain")
]""",
"expected": '<1:22> Error sintactico: se encontro: "["; se esperaba: "{".',
    },
    {
"name": "Test 3",
"input": """\
/* I forgot what was the
main purpose of the commas over there */
mut mistake,""",
"expected": '<4:1> Error sintactico: se encontro: "final de archivo"; se esperaba: "id".',
    },
    {
"name": "Test 4",
"input": """\
// un try catch latinizado
intentar{

} // no faltará algo?""",
"expected": '<5:1> Error sintactico: se encontro: "final de archivo"; se esperaba: "capturar".',
    },
    {
"name": "Test 5",
"input": """\
funcion(random){
   consola.escribir("función bien definida")
}
/* así no se definian las funciones anónimas*/""",
"expected": '<1:8> Error sintactico: se encontro: "("; se esperaba: "id".',
    },
    {
"name": "Test 6",
"input": """\
funcion cuadrado(numero) {
  retornar numero * numero;
}

consola.escribir(cuadrado(3));

funcion afuera() {
  mut x = 5;
  funcion adentro(x) {
    retornar x * 2;
  }
  retornar adentro;
}

afuera()(10);""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 7",
"input": """\
mut miMatriz = [1, 2, 3];

consola.escribir(miMatriz[0]); // 1
consola.escribir(miMatriz[1]); // 2
consola.escribir(miMatriz[2]); // 3
/* :v */
// (ups, tengo que indicar el comentario :v)""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 8",
"input": """\
consola.invento()""",
"expected": '<1:9> Error sintactico: se encontro: "invento"; se esperaba: "afirmar", "agrupar", "error", "escribir", "info", "limpiar", "tabla".',
    },
    {
"name": "Test 12",
"input": """\
mut entrada;

si (entrada === indefinido) {
  consola.error('Valor indefinido');
} sino {
  consola.escribir('Valor definido');
}""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 13",
"input": """\
1>2 ? ? consola.escribir("a") : 1;""",
"expected": '<1:7> Error sintactico: se encontro: "?"; se esperaba: "Arreglo", "Booleano", "Cadena", "cadena_de_caracteres", "consola", "falso", "id", "indefinido", "Infinito", "Mate", "Matriz", "NuN", "nulo", "Numero", "-", "!", "[", "{", "(", "+", "valor_numérico", "verdadero".',
    },
    {
"name": "Test 14",
"input": """\
mut i = 0;

hacer {
    consola.escribir(i);
    i = i + 1;
} mientras i < 5;""",
"expected": '<6:12> Error sintactico: se encontro: "i"; se esperaba: "(".',
    },
    {
"name": "Test 17",
"input": """\
consola.escribir(45"this")""",
"expected": '<1:20> Error sintactico: se encontro: "this"; se esperaba: "&&", ")", ",", "/", "==", ">=", ">", "<=", "<", "-", "%", "!=", "||", "+", "**", "===", "!==", "?", "*".',
    },
    {
"name": "Test 18",
"input": """\
mut i = 0;

mientras (i < 5) {
    consola escribir(i);
    i = i + 1;
}""",
"expected": '<4:13> Error sintactico: se encontro: "escribir"; se esperaba: ".".',
    },
    {
"name": "Test 21",
"input": """\
mut miObjeto = {
    metodo() {
        consola.escribir('Hola mundo');
    }
};

miObjeto.metodo(); // 'Hola mundo'

miObjeto['metodo'](); // 'Hola mundo'

mut miObjeto = {
    propiedad: 'valor'
};

consola.escribir(miObjeto.propiedad); // 'valor'

consola.escribir(miObjeto['propiedad']); // 'valor'""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 22",
"input": """\
{
  consola.escribir(x);
  x = x + 1; // Aumenta el valor de "x" para la siguiente iteración
}""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
    {
"name": "Test 23",
"input": """\
var 1;""",
"expected": '<1:5> Error sintactico: se encontro: "1"; se esperaba: "id".',
    },
    {
"name": "Test 24",
"input": """\
si (condicion) {
    // código
} sino mientras {
    // código
}
""",
"expected": '<3:8> Error sintactico: se encontro: "mientras"; se esperaba: "si", "{".',
    },
    {
"name": "Test 25",
"input": """\
// No es lo mismo declarar que actualizar
const variable += 70;""",
"expected": '<2:16> Error sintactico: se encontro: "+="; se esperaba: "Arreglo", "Booleano", "Cadena", "cadena_de_caracteres", "consola", "const", "continuar", "elegir", "falso", "final de archivo", "funcion", "hacer", "id", "indefinido", "Infinito", "intentar", "Mate", "Matriz", "mientras", "mut", "NuN", "nulo", "Numero", "para", "retornar", "romper", "si", "=", ",", "-", "!", "[", "{", "(", "+", ";", "valor_numérico", "var", "verdadero".',
    },
    {
"name": "Test 26",
"input": """\
si(){}""",
"expected": '<1:4> Error sintactico: se encontro: ")"; se esperaba: "Arreglo", "Booleano", "Cadena", "cadena_de_caracteres", "falso", "id", "indefinido", "Infinito", "Mate", "Matriz", "NuN", "nulo", "Numero", "-", "!", "[", "{", "(", "+", "valor_numérico", "verdadero".',
    },
    {
"name": "Test 28",
"input": """\
const operaciones = {
  suma: (a, b) => a + b,
  resta: (a, b) => a - b,
  mult: (a, b) => a * b
};

const tipo = "suma";

funcion_.inventada(operaciones[tipo](10, 5));""",
"expected": 'El analisis sintactico ha finalizado exitosamente.',
    },
]

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
        ok = "exitosamente" not in output.lower()
        note = "(se espera cualquier error sintáctico)"
    else:
        ok = output == expected
        note = ""
    return ok, note

# ── Clase para escribir en consola y archivo simultáneamente ──────────────────
class DualWriter:
    def __init__(self, filepath):
        self.file = open(filepath, "w", encoding="utf-8")

    def write(self, text_plain, text_console=None):
        """
        text_plain  → versión sin colores ANSI (va al archivo)
        text_console → versión con colores  (va a consola); si None usa text_plain
        """
        print(text_console if text_console is not None else text_plain)
        self.file.write(text_plain + "\n")

    def close(self):
        self.file.close()

# ── Runner principal ──────────────────────────────────────────────────────────
def main():
    passed = 0
    failed = 0
    errors = 0

    # Nombre del reporte con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"parser_report_{timestamp}.txt"
    dw = DualWriter(report_path)

    sep  = "═" * 64
    sep2 = "─" * 64

    dw.write(sep, f"{BOLD}{CYAN}{sep}{RESET}")
    dw.write("  Tester — Analizador Sintáctico EsJs",
             f"{BOLD}{CYAN}  Tester — Analizador Sintáctico EsJs{RESET}")
    dw.write(sep + "\n", f"{BOLD}{CYAN}{sep}{RESET}\n")

    for i, tc in enumerate(TEST_CASES, 1):
        output = run_case(tc)

        if output.startswith("__"):
            status_plain   = "ERROR"
            status_console = f"{RED}ERROR{RESET}"
            errors += 1
        else:
            ok, note = check(tc, output)
            if ok:
                status_plain   = "PASS"
                status_console = f"{GREEN}PASS{RESET}"
                passed += 1
            else:
                status_plain   = "FAIL"
                status_console = f"{RED}FAIL{RESET}"
                failed += 1

        dw.write(
            f"[{i:02d}] {status_plain:<6} {tc['name']}",
            f"[{i:02d}] {status_console}  {tc['name']}"
        )

        if not output.startswith("__"):
            ok, note = check(tc, output)
            if not ok:
                exp = tc["expected"] if tc["expected"] is not None else "(cualquier error)"
                dw.write(f"       Esperado: {exp}",
                         f"       {YELLOW}Esperado:{RESET} {exp}")
                dw.write(f"       Obtenido: {output}",
                         f"       {YELLOW}Obtenido:{RESET} {output}")
            elif note:
                dw.write(f"       {note}",
                         f"       {CYAN}{note}{RESET}")
        else:
            dw.write(f"       {output}",
                     f"       {RED}{output}{RESET}")

    total = len(TEST_CASES)
    summary_plain = (
        f"\n{sep2}\n"
        f"  Total: {total}  |  Pasaron: {passed}  |  "
        f"Fallaron: {failed}  |  Errores de ejecución: {errors}\n"
        f"{sep2}\n"
    )
    summary_console = (
        f"\n{BOLD}{sep2}{RESET}\n"
        f"  Total: {total}  |  "
        f"{GREEN}Pasaron: {passed}{RESET}  |  "
        f"{RED}Fallaron: {failed}{RESET}  |  "
        f"{YELLOW}Errores de ejecución: {errors}{RESET}\n"
        f"{BOLD}{sep2}{RESET}\n"
    )
    # write() agrega \n propio, así que usamos print/file directo para el bloque
    print(summary_console)
    dw.file.write(summary_plain)

    dw.write(f"Reporte guardado en: {report_path}",
             f"{CYAN}Reporte guardado en: {report_path}{RESET}")
    dw.close()

    sys.exit(0 if failed == 0 and errors == 0 else 1)

if __name__ == "__main__":
    main()