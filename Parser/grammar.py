GRAMMAR = {
    "start": [
        ["code_block", "EOF"],
    ],
    "code_line": [
        ["declare_or_assign"],
        ["conditional"],
        ["switch"],
        ["for_loop"],
        ["while_loop"],
        ["do_while_loop"],
        ["function"],
        ["simple_expr"],
        ["try_catch"],
        ["simple_block"],
    ],
    "code_block": [
        ["code_line", "code_block"],
        ["epsylon"]
    ],
    "declare_or_assign": [
        ["var_type", "IDENT", "more_declare","declare_or_assign_tail", "SEMICOLON"],
    ],
    "declare_or_assign_tail": [
        ["simple_assign", "expr_or_object"],
        ["epsylon"]
    ],
    "expr_or_object": [
        ["create_object"],
        ["expr"]
    ],
    "more_declare": [
        ["COMMA", "IDENT", "more_declare"],
        ["epsylon"]
    ],
    "var_type": [
        ["mut"],
        ["var"],
        ["const"],
    ],
    "simple_assign": [
        ["ASSIGN"],
    ],
    "assign_type": [
        ["ASSIGN"],
        ["PLUS_ASSIGN"],
        ["MINUS_ASSIGN"],
        ["TIMES_ASSIGN"],
        ["DIV_ASSIGN"],
        ["MOD_ASSIGN"],
        ["POWER_ASSIGN"],
        ["ARROW"],
    ],
    "expr": [
        ["expr_assign"],
    ],
    "expr_assign": [
        ["expr_or_nullish", "expr_assign_tail"],
        ["SPREAD", "expr_or_nullish", "expr_assign_tail"],  # spread
    ],
    "expr_assign_tail": [
        ["TERNARY", "expr_assign", "COLON", "expr_assign"],
        ["epsylon"]                        # si no, termina
    ],
    "expr_or_nullish": [
        ["expr_and", "expr_or_nullish_tail"],
    ],
    "expr_or_nullish_tail": [
        ["or_nullish", "expr_and", "expr_or_nullish_tail"],
        ["epsylon"]
    ],
    "or_nullish": [
        ["OR"],
        ["NULLISH"],
    ],
    "expr_and": [
        ["expr_equality", "expr_and_tail"],
    ],
    "expr_and_tail": [
        ["AND", "expr_equality", "expr_and_tail"],
        ["epsylon"]
    ],
    "expr_equality": [
        ["expr_rel", "expr_equality_tail"],
    ],
    "expr_equality_tail": [
        ["equality", "expr_rel", "expr_equality_tail"],
        ["epsylon"]
    ],
    "equality": [
        ["EQUAL"],
        ["NEQ"],
        ["STRICT_EQUAL"],
        ["STRICT_NEQ"],
    ],
    "expr_rel": [
        ["expr_add", "expr_rel_tail"],
    ],
    "expr_rel_tail": [
        ["relational", "expr_add", "expr_rel_tail"],
        ["epsylon"]
    ],
    "relational": [
        ["LESS"],
        ["LEQ"],
        ["GREATER"],
        ["GEQ"],
        ["en"],
        ["instanciaDe"],
    ],
    "expr_add": [
        ["expr_mul", "expr_add_tail"],
    ],
    "expr_add_tail": [
        ["additive", "expr_mul", "expr_add_tail"],
        ["epsylon"]
    ],
    "additive": [
        ["PLUS"],
        ["MINUS"],
    ],
    "expr_mul": [
        ["expr_power", "expr_mul_tail"],
    ],
    "expr_mul_tail": [
        ["multiplicative", "expr_power", "expr_mul_tail"],
        ["epsylon"]
    ],
    "multiplicative": [
        ["TIMES"],
        ["DIV"],
        ["MOD"],
    ],
    "expr_power": [
        ["expr_prefix", "expr_power_tail"],
    ],
    "expr_power_tail": [
        ["POWER", "expr_power"],   # right-associative → recursa en expr_power
        ["epsylon"]
    ],
    "expr_prefix": [
        ["prefix", "expr_prefix"],
        ["expr_postfix"],
    ],
    "prefix": [
        ["NOT"],
        ["MINUS"],
        ["PLUS"],
        ["INCREMENT"],
        ["DECREMENT"],
    ],
    "expr_postfix": [
        ["expr_group", "expr_postfix_tail"]
    ],
    "expr_postfix_tail": [
        ["postfix", "expr_postfix_tail"],
        ["epsylon"]
    ],
    "postfix": [
        ["INCREMENT"],
        ["DECREMENT"],
    ],
    "expr_group": [
        ["OPENING_PAR", "expr", "CLOSING_PAR"],
        ["element"],
    ],
    "call_args": [
        ["OPENING_PAR", "call_empty_args"],
    ],
    "call_empty_args": [
        ["CLOSING_PAR"],
        ["expr", "call_args_tail", "CLOSING_PAR"]
    ],
    "call_args_tail": [
        ["COMMA", "expr", "call_args_tail"],
        ["epsylon"]
    ],
    # Solo lo que puede recibir asignación (izquierda del =)
    "assignable": [
        ["IDENT", "assignable_tail"],
    ],
    "assignable_tail": [
        ["PERIOD", "IDENT", "assignable_tail"],                      # obj.prop
        ["OPENING_BRA", "expr", "CLOSING_BRA", "assignable_tail"],  # arr[0]
        ["epsylon"]
    ],

    # Todo lo que puede ser elemento (incluye llamadas)
    "element": [
        ["console_use"],
        ["IDENT", "element_access_tail"],   # cubre acceso, llamada y asignación
        ["NUMBER"],
        ["STR"],
        ["REGEX"],
        ["arr_declare"],
        ["verdadero"],
        ["falso"],
        ["nulo"],
        ["indefinido"],
    ],
    "element_access_tail": [
        ["PERIOD", "IDENT", "element_access_tail"],                      # obj.prop
        ["OPENING_BRA", "expr", "CLOSING_BRA", "element_access_tail"],  # arr[0]
        ["call_args", "element_access_tail"],  # func()
        ["assign_type", "assignment_or_expr"],                           # x = ...
        ["epsylon"]                                                      # solo ident
    ],
    # Lado derecho de una asignación
    "assignment_or_expr": [
        ["assignable", "assignment_or_expr_tail"],  # si hay assignable, puede asignar
        ["expr"],                                   # si no, expresión normal
        ["create_object"],
    ],
    "arr_declare": [
        ["OPENING_BRA", "expr", "arr_declare_tail", "CLOSING_BRA"],
    ],
    "arr_declare_tail": [
        ["COMMA", "expr", "arr_declare_tail"],
        ["epsylon"]
    ],
    "assignment_or_expr_tail": [
        ["assign_type", "assignment_or_expr"],  # encadena
        ["epsylon"]                             # termina
    ],
    "create_object": [
        ["OPENING_KEY", "fields", "CLOSING_KEY"],
    ],

    "fields": [
        ["IDENT", "field_body", "fields_tail"],
        ["epsylon"]
    ],

    "field_body": [
        # Propiedad normal:  key: value
        ["COLON", "expr"],
        # Método:  key(params) { ... }
        ["OPENING_PAR", "params", "CLOSING_PAR", "simple_block_return"],
    ],

    "fields_tail": [
        ["COMMA", "IDENT", "field_body", "fields_tail"],
        ["epsylon"]
    ],
    "console_use": [
        ["consola", "PERIOD", "console_method", "call_args"],
    ],
    "console_method": [
        ["escribir"],
        ["error"],
        ["afirmar"],
        ["limpiar"],
        ["agrupar"],
        ["info"],
        ["tabla"],
        # agrega los que necesites
    ],
   "conditional": [
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "simple_block", "conditional_alter"],
    ],
    "conditional_alter": [
        ["sino", "conditional_alter_tail"],
        ["epsylon"]
    ],
    "conditional_alter_tail": [
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "simple_block", "conditional_alter"],  # sino si ...
        ["simple_block"],  # sino { ... }
    ],
    "switch": [
        ["elegir", "OPENING_PAR", "expr", "CLOSING_PAR", "OPENING_KEY", "cases", "default_case", "CLOSING_KEY"],
    ],
    "cases": [
        ["caso", "expr", "simple_block_break_continue", "cases"],
        ["epsylon"]
    ],
    "default_case": [
        ["porDefecto", "simple_block_break_continue"],
        ["epsylon"]
    ],
    "for_loop": [
        ["para", "OPENING_PAR", "expr", "SEMICOLON", "expr", "SEMICOLON", "expr", "CLOSING_PAR", "simple_block_break_continue"],
    ],
    "while_loop": [
        ["mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "simple_block_break_continue"],
    ],
    "do_while_loop": [
        ["hacer", "simple_block_break_continue", "mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "SEMICOLON"],
    ],
    "break": [
        ["romper", "SEMICOLON"],
    ],
    "continue": [
        ["continuar", "SEMICOLON"],
    ],
    "code_line_break_continue": [
        ["code_line"],
        ["break"],
        ["continue"],
    ],
    "code_block_break_continue": [
        ["code_line_break_continue", "code_block_break_continue"],
        ["epsylon"]
    ],
    "simple_block_break_continue": [
        ["OPENING_KEY", "code_block_break_continue", "CLOSING_KEY"],
    ],
    "simple_block": [
        ["OPENING_KEY", "code_block", "CLOSING_KEY"],
    ],
    "function": [
        ["funcion", "IDENT", "OPENING_PAR", "params", "CLOSING_PAR", "simple_block_return"],
    ],
    "return_stmt": [
        ["retornar", "return_stmt_tail"],
        ["epsylon"]
    ],
    "return_stmt_tail": [
        ["expr", "SEMICOLON"],
        ["SEMICOLON"]
    ],
    "simple_block_return": [
        ["OPENING_KEY", "code_block","return_stmt", "CLOSING_KEY"],
    ],
    "params": [
        ["IDENT", "params_tail"],
        ["epsylon"]
    ],
    "params_tail": [
        ["COMMA", "IDENT", "params_tail"],
        ["epsylon"]
    ],
    "simple_expr": [
        ["expr", "SEMICOLON"],
    ],
    "try_catch": [
        ["intentar", "simple_block", "catch"],
    ],
    "catch": [
        ["capturar", "OPENING_PAR", "IDENT", "CLOSING_PAR", "simple_block"],
    ]
}

class Grammar:
    def __init__(self):
        self.grammar = self.construct_grammar(GRAMMAR)
        self.start_symbol = next(iter(self.grammar))
        self.first_set = {}
        self.first()
        self.follow_set = self.follow()
        self.conflicts = self.pred_sets()
        self.no_terminal_pred_set()
    
    def construct_grammar(self, grammar):
        for no_terminal, rules in grammar.items():
            for i, rule in enumerate(rules):
                rules[i] = {"rule":rule,"pred_set":set()}
            grammar[no_terminal] = {"rules":grammar[no_terminal],"total_pred_set":set()}
        return grammar
        
    def first_of_sequence(self, symbols):
        """Reutilizable por first() y follow()"""
        result = set()
        for symbol in symbols:
            if symbol == "epsylon":
                result.add("epsylon")
                break
            elif symbol not in self.first_set:  # Terminal
                result.add(symbol)
                break
            else:                               # No terminal
                result.update(self.first_set[symbol] - {"epsylon"})
                if "epsylon" not in self.first_set[symbol]:
                    break
        else:
            result.add("epsylon")
        return result
        
    def first(self):
        # Inicializar PRIMEROS con terminales directos y ε
        self.first_set = {nt: set() for nt in self.grammar}

        # Iterar hasta punto fijo
        changed = True
        while changed:
            changed = False
            for no_terminal, values in self.grammar.items():
                rules = values["rules"]
                for rule in rules:
                    new_firsts = self.first_of_sequence(rule["rule"])
                    if not new_firsts.issubset(self.first_set[no_terminal]):
                        self.first_set[no_terminal].update(new_firsts)
                        changed = True

        return self.first_set

    def follow(self):
        follow_set = {nt: set() for nt in self.grammar}
        follow_set[self.start_symbol].add("EOF")
        
        def follow_of_nt_in_rule(symbols, no_terminal, origin):
            result = set()
            for i, symbol in enumerate(symbols):
                if symbol != no_terminal:
                    continue
                
                # β = todo lo que viene después de la aparición de A
                beta = symbols[i+1:]

                if len(beta) == 0 or beta == ["epsylon"]:
                    # β = ε → Regla 2b: agregar SIGUIENTES(B)
                    result.update(follow_set[origin])
                else:
                    # Regla 2a: agregar PRIMEROS(β) - {ε}
                    first_beta = self.first_of_sequence(beta)
                    result.update(first_beta - {"epsylon"})

                    # Regla 2b: si ε ∈ PRIMEROS(β), agregar SIGUIENTES(B)
                    if "epsylon" in first_beta:
                        result.update(follow_set[origin])
            return result
        
        changed = True
        while changed:
            changed = False
            for origin, values in self.grammar.items():
                rules = values["rules"]
                for rule in rules:
                    for no_terminal in follow_set:
                        new_follows = follow_of_nt_in_rule(rule["rule"], no_terminal, origin)
                        if not new_follows.issubset(follow_set[no_terminal]):
                            follow_set[no_terminal].update(new_follows)
                            changed = True
                        
        
        return follow_set
    
    def pred_sets_of_rule(self, symbols, no_terminal):
        """
        PRED(A → α) = 
            si ε ∈ PRIMEROS(α): (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A)
            sino:                 PRIMEROS(α)
        """
        first_alpha = self.first_of_sequence(symbols)
        
        if "epsylon" in first_alpha:
            return (first_alpha - {"epsylon"}) | self.follow_set[no_terminal]
        else:
            return first_alpha

    def pred_sets(self):
        """
        Calcula PRED para cada regla y detecta conflictos (gramática no LL(1))
        """
        conflicts = {}
        
        for no_terminal, values in self.grammar.items():
            seen = set()  # Unión de todos los PRED de las reglas de este no terminal
            
            rules = values["rules"]
            
            for rule in rules:
                symbols = rule["rule"]
                rule["pred_set"] = self.pred_sets_of_rule(symbols, no_terminal)
                
                # Detectar conflicto: ¿el mismo terminal aparece en dos reglas de A?
                overlap = seen & rule["pred_set"]
                if overlap:
                    conflicts[no_terminal] = conflicts.get(no_terminal, set()) | overlap
                seen |= rule["pred_set"]
        
        return conflicts  # Vacío = gramática LL(1) ✓
    
    def no_terminal_pred_set(self):
        for values in self.grammar.values():
            total_pred_set = values["total_pred_set"]
            rules = values["rules"]
            for rule in rules:
                total_pred_set.update(rule["pred_set"])


from datetime import datetime


def write_grammar_report(grammar, filepath="grammar_report.txt"):
    """
    Escribe el reporte de la gramática en un archivo .txt,
    sobreescribiéndolo cada vez que se llame.
    """
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ─── Encabezado ───────────────────────────────────────────────
    lines.append("=" * 60)
    lines.append(f"  REPORTE DE GRAMÁTICA  —  {now}")
    lines.append("=" * 60)

    # ─── Reglas y conjuntos de predicción por producción ──────────
    lines.append("\n[1] REGLAS Y CONJUNTOS DE PREDICCIÓN\n")
    lines.append(f"  {'No terminal':<20} {'Producción':<30} {'Pred. Set'}")
    lines.append(f"  {'-'*20} {'-'*30} {'-'*20}")

    for key, value in grammar.grammar.items():
        for rule in value["rules"]:
            prod  = " ".join(rule["rule"]) if isinstance(rule["rule"], list) else str(rule["rule"])
            preds = str(rule["pred_set"])
            lines.append(f"  {key:<20} {prod:<30} {preds}")

    # ─── Predicción total por no terminal ─────────────────────────
    lines.append("\n[2] PREDICCIÓN TOTAL POR NO TERMINAL\n")
    lines.append(f"  {'No terminal':<20} {'Pred. Set total'}")
    lines.append(f"  {'-'*20} {'-'*30}")

    for key, value in grammar.grammar.items():
        lines.append(f"  {key:<20} {value['total_pred_set']}")

    # ─── Primeros ─────────────────────────────────────────────────
    lines.append("\n[3] CONJUNTOS PRIMEROS (FIRST)\n")
    for symbol, first in grammar.first_set.items():
        lines.append(f"  FIRST({symbol:<18}) = {first}")

    # ─── Siguientes ───────────────────────────────────────────────
    lines.append("\n[4] CONJUNTOS SIGUIENTES (FOLLOW)\n")
    for symbol, follow in grammar.follow_set.items():
        lines.append(f"  FOLLOW({symbol:<17}) = {follow}")

    # ─── Conflictos ───────────────────────────────────────────────
    lines.append("\n[5] CONFLICTOS\n")
    if grammar.conflicts:
        for conflict in grammar.conflicts:
            lines.append(f"  ⚠  {conflict}")
    else:
        lines.append("  ✔  Sin conflictos detectados.")

    lines.append("\n" + "=" * 60 + "\n")

    # ─── Escritura ────────────────────────────────────────────────
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    grammar = Grammar()
    write_grammar_report(grammar, filepath="grammar_report.txt")
    
if __name__ == "__main__":
    main()