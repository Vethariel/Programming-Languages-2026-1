#!/usr/bin/env python3
"""
gen_table.py — genera el bloque TRANS[][] para lexer.c a partir de transitions.csv

Uso:
    python gen_table.py                        # imprime en stdout
    python gen_table.py -o tabla_generada.c    # escribe a archivo
    python gen_table.py --patch lexer.c        # reemplaza la sección en lexer.c

El script también valida:
  - que todos los estados destino existan como filas o sean estados de aceptación/error conocidos
  - que todas las filas tengan el mismo número de columnas
"""

import csv
import sys
import re
import argparse
from pathlib import Path

# ── Estados de aceptación y especiales que NO aparecen como filas en el CSV
# (son manejados por el motor del lexer, no tienen transiciones propias)
ACCEPT_STATES = {
    "ACCEPT_STR_D", "ACCEPT_STR_S",
    "ACCEPT_LBRACKET", "ACCEPT_RBRACKET",
    "ACCEPT_ID", "ACCEPT_NUM", "ACCEPT_STR",
    "ACCEPT_PLUS", "ACCEPT_MINUS", "ACCEPT_TIMES", "ACCEPT_DIV",
    "ACCEPT_ASSIGN", "ACCEPT_EQ", "ACCEPT_EEQ",
    "ACCEPT_LT", "ACCEPT_LE", "ACCEPT_GT", "ACCEPT_GE",
    "ACCEPT_LPAREN", "ACCEPT_RPAREN",
    "ACCEPT_LBRACE", "ACCEPT_RBRACE", "ACCEPT_ARROW",
    "ACCEPT_SEMI", "ACCEPT_COMMA", "ACCEPT_PERIOD",
    "COMMENT_END", "COMMENT_M_END","ERROR", "ACCEPT_COLON",
    "ACCEPT_AND", "ACCEPT_OR", "ACCEPT_NOT",
    "ACCEPT_DIV_ASSIGN", "ACCEPT_MOD_ASSIGN",
    "ACCEPT_PLUS_ASSIGN", "ACCEPT_MINUS_ASSIGN",
    "ACCEPT_TERNARY", "ACCEPT_NEQ", "ACCEPT_NEEQ", "ACCEPT_NULLISH",
    "ACCEPT_POWER", "ACCEPT_POWER_ASSIGN", "ACCEPT_MOD",
    "ACCEPT_MOD_ASSIGN", "ACCEPT_SPREAD", "ACCEPT_INCREMENT", "ACCEPT_DECREMENT",
    "ACCEPT_TIMES_ASSIGN"
}

# Prefijo que usa el enum State en el .c
STATE_PREFIX = "S_"


def load_csv(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        sys.exit("ERROR: el CSV está vacío")
    classes = [k for k in rows[0].keys() if k != "state"]
    return rows, classes


def validate(rows, classes):
    defined_states = {r["state"] for r in rows} | ACCEPT_STATES
    errors = []
    for row in rows:
        if len(row) - 1 != len(classes):   # -1 por la columna "state"
            errors.append(f"Fila '{row['state']}' tiene {len(row)-1} columnas, se esperan {len(classes)}")
        for cl in classes:
            dest = row[cl]
            if dest not in defined_states:
                errors.append(f"  [{row['state']}][{cl}] → '{dest}' no está definido")
    if errors:
        print("ERRORES DE VALIDACIÓN:", file=sys.stderr)
        for e in errors:
            print(" ", e, file=sys.stderr)
        sys.exit(1)


def generate_block(rows, classes) -> str:
    col_w   = max(len(c) for c in classes) + 2   # ancho columna header
    state_w = max(len(r["state"]) for r in rows) + 2

    lines = []
    lines.append("/* ─── 2. TABLA DE TRANSICIONES (generada por gen_table.py) ─── */")
    lines.append("/*  Edita transitions.csv y ejecuta gen_table.py para regenerar.*/")
    lines.append("")

    # Cabecera de columnas como comentario
    header_cols = "  ".join(f"{c:<{col_w}}" for c in classes)
    lines.append(f"/*  {'state':<{state_w}}  {header_cols}*/")

    lines.append("static const State TRANS[STATE_COUNT][ALPHA_SIZE] = {")
    for row in rows:
        state = row["state"]
        entries = []
        for cl in classes:
            dest = row[cl]
            entries.append(f"{STATE_PREFIX}{dest}")
        # Alinear entradas
        body = ", ".join(entries)
        lines.append(f"/* {state:<{state_w-2}} */ {{ {body} }},")
    lines.append("};")
    return "\n".join(lines)


def patch_file(c_path: str, block: str):
    """Reemplaza la sección TRANS en el archivo .c usando marcadores de sección."""
    src = Path(c_path).read_text(encoding="utf-8")

    # Buscamos desde el comentario de sección 2 hasta el cierre de la tabla
    pattern = re.compile(
        r"/\* ─── 2\..*?^};\n",
        re.DOTALL | re.MULTILINE
    )
    if not pattern.search(src):
        sys.exit(f"ERROR: no se encontró la sección 2 en '{c_path}'.\n"
                 "Asegúrate de que el comentario '/* ─── 2.' exista en el archivo.")

    new_src = pattern.sub(block + "\n", src, count=1)
    Path(c_path).write_text(new_src, encoding="utf-8")
    print(f"✓ '{c_path}' actualizado.")


def main():
    parser = argparse.ArgumentParser(description="Genera TRANS[][] desde transitions.csv")
    parser.add_argument("csv", nargs="?", default="transitions.csv",
                        help="Ruta al CSV (default: transitions.csv)")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Escribir bloque generado a FILE en vez de stdout")
    parser.add_argument("--patch", metavar="LEXER_C",
                        help="Reemplazar la sección TRANS en LEXER_C directamente")
    parser.add_argument("--no-validate", action="store_true",
                        help="Saltar validación de estados destino")
    args = parser.parse_args()

    rows, classes = load_csv(args.csv)

    if not args.no_validate:
        validate(rows, classes)

    block = generate_block(rows, classes)

    if args.patch:
        patch_file(args.patch, block)
    elif args.output:
        Path(args.output).write_text(block + "\n", encoding="utf-8")
        print(f"✓ Bloque escrito en '{args.output}'.")
    else:
        print(block)


if __name__ == "__main__":
    main()