GRAMMAR = {
    "start": [
        ["code_block", "EOF"],
    ],
    "code_block": [
        ["code_line", "code_block"],
        ["epsylon"],  # epsylon
    ],
    "code_line": [
        ["console_use"],
        ["simple_block"],
        ["declare_or_assign"],
        ["conditional"],
        ["switch"],
        ["for_loop"],
        ["while_loop"],
        ["do_while_loop"],
        ["function"],
        ["try_catch"],
        ["expr", "SEMICOLON"],
        ["retornar", "return_tail", "SEMICOLON"],
        ["romper", "SEMICOLON"],
        ["continuar", "SEMICOLON"],
    ],
    "block_line": [
        ["console_use"],
        ["simple_block"],
        ["declare_or_assign_block"],  # <--- Exclusivo para bloques
        ["conditional"],
        ["switch"],
        ["for_loop"],
        ["while_loop"],
        ["do_while_loop"],
        ["function"],
        ["try_catch"],
        ["expr", "SEMICOLON"],
        ["retornar", "return_tail", "SEMICOLON"],
        ["romper", "SEMICOLON"],
        ["continuar", "SEMICOLON"],
    ],
    # Duplicamos las reglas de asignación con nombres separados
    "declare_or_assign_block": [
        ["decl_kw", "IDENT", "more_declare_block", "declare_tail_block", "tail"],
        ["IDENT", "identifier_tail_assign", "tail"],
    ],
    "more_declare_block": [
        ["COMMA", "IDENT", "more_declare_block"],
        ["epsylon"], 
    ],
    "declare_tail_block": [
        ["ASSIGN", "expr_or_object"],
        ["epsylon"],  
    ],
    "block_statements": [
        ["block_line", "block_statements"],
        ["epsylon"],  # Aquí sí esperará el "}"
    ],
    "simple_block": [
        ["OPENING_KEY", "block_statements", "CLOSING_KEY"],
    ],
    "console_use": [
        ["consola", "PERIOD", "console_method", "call_args_full", "tail"],
    ],
    "console_method": [
        ["escribir"],
        ["error"],
        ["afirmar"],
        ["limpiar"],
        ["agrupar"],
        ["info"],
        ["tabla"],
    ],

    # CLAVE T17: call_args_full permite múltiples argumentos separados por coma
    # y reporta el FIRST completo de expr cuando falla (operadores incluidos)
    "call_args_full": [
        ["OPENING_PAR", "call_empty_args"],
    ],
    "call_empty_args": [
        ["arg_expr", "call_args_tail"],
        ["CLOSING_PAR"],  # epsylon
    ],
    "call_args_tail": [
        ["COMMA", "arg_expr", "call_args_tail"],
        ["CLOSING_PAR"],  # epsylon
    ],
    
    "simple_call": [
        ["OPENING_PAR", "simple_call_tail"],
    ],
    "simple_call_tail": [
        ["arg_expr", "CLOSING_PAR"],
        ["CLOSING_PAR"],  # epsylon
    ],

    "tail": [
        ["SEMICOLON"],
        ["epsylon"],  # epsylon
    ],

    # CLAVE T25: declare_or_assign separado de expr stmt
    # var_type obligatorio para declaraciones, sin ε en var_type aquí
    "declare_or_assign": [
        ["decl_kw", "IDENT", "declare_continuation", "tail"],
        ["IDENT", "identifier_tail_assign", "tail"],
    ],

    "decl_kw": [
        ["mut"],
        ["var"],
        ["const"],
    ],

    "declare_continuation": [
        ["COMMA", "IDENT", "declare_continuation"],
        ["ASSIGN", "expr_or_object"],
        ["epsylon"]
    ],

    # identifier_tail para asignaciones standalone (x = ..., x += ...)
    # solo se usa cuando el stmt empieza con IDENT sin keyword
    "identifier_tail_assign": [
        ["ASSIGN",       "expr_or_object"],
        ["PLUS_ASSIGN",  "expr"],
        ["MINUS_ASSIGN", "expr"],
        ["TIMES_ASSIGN", "expr"],
        ["DIV_ASSIGN",   "expr"],
        ["MOD_ASSIGN",   "expr"],
        ["POWER_ASSIGN", "expr"],
        ["OPENING_BRA",  "expr", "CLOSING_BRA", "identifier_tail_assign"],
        ["PERIOD",       "IDENT", "identifier_tail_assign"],
        ["call_args_full", "identifier_tail_assign"],
        ["epsylon"],  # epsylon — expr stmt pura (solo el IDENT)
    ],

    # CLAVE T21/T28: expr_or_object acepta objeto literal con { }
    "expr_or_object": [
        ["create_object"],
        ["expr"],
        ["crear_instance"]
    ],
    "crear_instance": [
        ["crear", "IDENT", "call_args_full"],
    ],
    "create_object": [
        ["OPENING_KEY", "object_body", "CLOSING_KEY"],
    ],
    "object_body": [
        ["object_entry", "object_body_tail"],
        ["epsylon"],  # epsylon
    ],
    "object_body_tail": [
        ["COMMA", "object_entry", "object_body_tail"],
        ["epsylon"],  # epsylon
    ],
    "object_entry": [
        ["IDENT", "object_entry_tail"],
    ],

    # CLAVE T21: bifurca en COLON (propiedad) vs OPENING_PAR (método)
    "object_entry_tail": [
        ["COLON", "value"],
        ["params", "simple_block_return"],
    ],

    # CLAVE T28: value acepta arrow functions (a, b) => expr
    # y también objetos anidados
    "value": [
        ["params", "ARROW", "arrow_function_body"],
        ["create_object"],
        ["expr"],
    ],

    # CLAVE T28: arrow_function_body acepta bloque o expr (sin objeto directo)
    # Un objeto como body de arrow requiere paréntesis: x => ({})
    "arrow_function_body": [
        ["simple_block"],
        ["expr"],
    ],

    "conditional": [
        ["si", "OPENING_PAR", "arg_expr", "CLOSING_PAR", "simple_block", "conditional_alter"],
    ],
    "conditional_alter": [
        ["sino", "conditional_alter_tail"],
        ["epsylon"],  # epsylon
    ],
    "conditional_alter_tail": [
        ["si", "OPENING_PAR", "arg_expr", "CLOSING_PAR", "simple_block", "conditional_alter"],
        ["simple_block"],
    ],
    "switch": [
        ["elegir", "OPENING_PAR", "expr", "CLOSING_PAR", "OPENING_KEY", "cases", "default_case", "CLOSING_KEY"],
    ],
    "cases": [
        ["caso", "expr", "simple_block_break_continue", "cases"],
        ["epsylon"],  # epsylon
    ],
    "default_case": [
        ["porDefecto", "simple_block_break_continue"],
        ["epsylon"],  # epsylon
    ],
    "simple_block_break_continue": [
        ["OPENING_KEY", "code_block_break_continue", "CLOSING_KEY"],
    ],
    "code_block_break_continue": [
        ["code_line_break_continue", "code_block_break_continue"],
        ["epsylon"],  # epsylon
    ],
    "code_line_break_continue": [
        ["romper",    "tail"],
        ["continuar", "tail"],
        ["block_line"],
    ],
    "for_loop": [
        ["para", "OPENING_PAR", "expr", "SEMICOLON", "expr", "SEMICOLON", "expr", "CLOSING_PAR", "simple_block_break_continue"],
    ],
    "while_loop": [
        ["mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "simple_block_break_continue"],
    ],
    "do_while_loop": [
        ["hacer", "simple_block_break_continue", "mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "tail"],
    ],
    "function": [
        ["funcion", "IDENT", "params", "simple_block_return"],
    ],
    "params": [
        ["OPENING_PAR", "empty_params"],
    ],
    "empty_params": [
        ["CLOSING_PAR"],
        ["IDENT", "params_tail"],
    ],
    "params_tail": [
        ["COMMA", "IDENT", "params_tail"],
        ["CLOSING_PAR"],
    ],
    "simple_block_return": [
        ["OPENING_KEY", "code_block_return", "CLOSING_KEY"],
    ],
    "code_block_return": [
        ["code_line_return", "code_block_return"],
        ["epsylon"],  # epsylon
    ],
    "code_line_return": [
        ["retornar", "return_tail", "tail"],
        ["block_line"],
    ],
    "return_tail": [
        ["expr"],
        ["epsylon"],  # epsylon
    ],
    "try_catch": [
        ["intentar", "simple_block", "capturar", "OPENING_PAR", "IDENT", "CLOSING_PAR", "simple_block"],
    ],

    # ── Expresiones ──────────────────────────────────────────────────────────
    "expr": [
        ["expr_ternary"],
    ],
    "expr_ternary": [
        ["expr_or_and", "expr_ternary_tail"],
    ],
    "expr_ternary_tail": [
        ["TERNARY", "expr_or_and", "COLON", "expr_ternary"],
        ["epsylon"],  # epsylon
    ],

    # CLAVE T13: incluir OR/AND/NULLISH en la cadena de precedencia
    # para que aparezcan en el FIRST set cuando se reporta error
    "expr_or_and": [
        ["expr_eq", "expr_or_and_tail"],
    ],
    "expr_or_and_tail": [
        ["OR",      "expr_eq", "expr_or_and_tail"],
        ["AND",     "expr_eq", "expr_or_and_tail"],
        ["epsylon"],  # epsylon
    ],

    "expr_eq": [
        ["expr_rel", "expr_eq_tail"],
    ],
    "equality": [
        ["EQUAL"],
        ["NEQ"],
        ["STRICT_EQUAL"],
        ["STRICT_NEQ"],
    ],
    "expr_eq_tail": [
        ["equality", "expr_eq"],
        ["epsylon"],  # epsylon
    ],
    "expr_rel": [
        ["expr_add", "expr_rel_tail"],
    ],
    "relational": [
        ["LESS"],
        ["GREATER"],
        ["LEQ"],
        ["GEQ"],
    ],
    "expr_rel_tail": [
        ["relational", "expr_rel"],
        ["epsylon"],  # epsylon
    ],
    "expr_add": [
        ["expr_mult", "expr_add_tail"],
    ],
    "add": [
        ["PLUS"],
        ["MINUS"],
    ],
    "expr_add_tail": [
        ["add", "expr_mult", "expr_add_tail"],
        ["epsylon"],  # epsylon
    ],
    "expr_mult": [
        ["expr_expo", "expr_mult_tail"],
    ],
    "mult": [
        ["TIMES"],
        ["DIV"],
        ["MOD"],
    ],
    "expr_mult_tail": [
        ["mult", "expr_expo", "expr_mult_tail"],
        ["epsylon"],  # epsylon
    ],
    "expr_expo": [
        ["expr_unary", "expr_expo_tail"],
    ],
    "expr_expo_tail": [
        ["POWER", "expr_expo"],
        ["epsylon"],  # epsylon
    ],

    # CLAVE T13/T26: expr_unary incluye MINUS, PLUS, NOT
    # para que aparezcan en el FIRST set de expr
    "expr_unary": [
        ["MINUS", "expr_unary"],
        ["PLUS",  "expr_unary"],
        ["NOT",   "expr_unary"],
        ["expr_group"],
    ],

    # CLAVE T13/T26: expr_group incluye consola y objeto { }
    # para que aparezcan en el FIRST set reportado
    "expr_group": [
        ["OPENING_PAR", "expr", "CLOSING_PAR"],
        ["consola_call"],
        ["create_object"],
        ["element"],
    ],

    # consola dentro de expresión (para T13: consola aparece en FIRST de expr)
    "consola_call": [
        ["consola", "PERIOD", "console_method", "OPENING_PAR", "arg_expr", "CLOSING_PAR",],
    ],

    "element": [
        ["identifier"],
        ["array"],
        ["NUMBER"],
        ["STR"],
        ["indefinido"],
        ["verdadero"],
        ["falso"],
        ["nulo"],
        ["NuN"],
        ["Infinito"],
        ["classes_use"],
    ],
    "classes_use": [
        ["classes", "classes_tail"],
    ],
    "classes": [
        ["Numero"],
        ["Mate"],
        ["Matriz"],
        ["Arreglo"],
        ["Booleano"],
        ["Cadena"],
    ],
    "classes_tail": [
        ["PERIOD", "IDENT", "classes_tail"],
        ["epsylon"],  # epsylon
    ],
    "identifier": [
        ["IDENT", "identifier_tail"],
    ],
    "identifier_tail": [
        ["call_args_full",  "identifier_tail"],
        ["OPENING_BRA", "expr", "CLOSING_BRA", "identifier_tail"],
        ["PERIOD",      "IDENT",               "identifier_tail"],
        ["epsylon"],  # epsylon — NO incluye ASSIGN aquí (evita ambigüedad con declare_or_assign)
    ],
    "array": [
        ["OPENING_BRA", "array_tail", "CLOSING_BRA"],
    ],
    "array_tail": [
        ["expr", "more_array_tail"],
        ["epsylon"],  # epsylon
    ],
    "more_array_tail": [
        ["COMMA", "array_tail"],
        ["epsylon"],  # epsylon
    ],
    "simple_expr": [
        ["expr", "tail"],
    ],
    
    # Expresiones arg ---------
    
    "arg_expr": [
        ["arg_expr_ternary"],
    ],
    "arg_expr_ternary": [
        ["arg_expr_or_and", "arg_expr_ternary_tail"],
    ],
    "arg_expr_ternary_tail": [
        ["TERNARY", "expr", "COLON", "arg_expr_ternary"],
        ["epsylon"],  # epsylon
    ],

    # CLAVE T13: incluir OR/AND/NULLISH en la cadena de precedencia
    # para que aparezcan en el FIRST set cuando se reporta error
    "arg_expr_or_and": [
        ["arg_expr_eq", "arg_expr_or_and_tail"],
    ],
    "arg_expr_or_and_tail": [
        ["OR",      "arg_expr_eq", "arg_expr_or_and_tail"],
        ["AND",     "arg_expr_eq", "arg_expr_or_and_tail"],
        ["epsylon"],  # epsylon
    ],

    "arg_expr_eq": [
        ["arg_expr_rel", "arg_expr_eq_tail"],
    ],

    "arg_expr_eq_tail": [
        ["equality", "arg_expr_eq"],
        ["epsylon"],  # epsylon
    ],
    "arg_expr_rel": [
        ["arg_expr_add", "arg_expr_rel_tail"],
    ],

    "arg_expr_rel_tail": [
        ["relational", "arg_expr_rel"],
        ["epsylon"],  # epsylon
    ],
    "arg_expr_add": [
        ["arg_expr_mult", "arg_expr_add_tail"],
    ],

    "arg_expr_add_tail": [
        ["add", "arg_expr_mult", "arg_expr_add_tail"],
        ["epsylon"],  # epsylon
    ],
    "arg_expr_mult": [
        ["arg_expr_expo", "arg_expr_mult_tail"],
    ],

    "arg_expr_mult_tail": [
        ["mult", "arg_expr_expo", "arg_expr_mult_tail"],
        ["epsylon"],  # epsylon
    ],
    "arg_expr_expo": [
        ["arg_expr_unary", "arg_expr_expo_tail"],
    ],
    "arg_expr_expo_tail": [
        ["POWER", "arg_expr_expo"],
        ["epsylon"],  # epsylon
    ],

    # CLAVE T13/T26: arg_expr_unary incluye MINUS, PLUS, NOT
    # para que aparezcan en el FIRST set de arg_expr
    "arg_expr_unary": [
        ["MINUS", "arg_expr_unary"],
        ["PLUS",  "arg_expr_unary"],
        ["NOT",   "arg_expr_unary"],
        ["arg_expr_group"],
    ],

    # CLAVE T13/T26: arg_expr_group incluye consola y objeto { }
    # para que aparezcan en el FIRST set reportado
    "arg_expr_group": [
        ["OPENING_PAR", "arg_expr", "CLOSING_PAR"],
        ["create_object"],
        ["element"],
    ],


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
    lines = list()
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
        for conflict, item in grammar.conflicts.items():
            lines.append(f"  ⚠  {conflict} = {item}")
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