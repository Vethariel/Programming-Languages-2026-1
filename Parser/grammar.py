GRAMMAR = {
    "start": [
        ["global_code", "EOF"],
    ],
    
    "global_code": [
        ["g_stmt", "global_code"],
        ["epsylon"]
    ],
    "block_code": [
        ["b_stmt", "block_code"],
        ["epsylon"]
    ],
    
    # Usamos expr (expresión general) en las estructuras para no contaminar arg_expr
    "g_stmt": [
        ["decl_keyword", "g_decl_list", "g_semicolon_opt"], 
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt", "g_sino_opt"],                    
        ["mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt"],              
        ["hacer", "block_stmt", "mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "g_semicolon_opt"],        
        ["para", "OPENING_PAR", "para_init", "SEMICOLON", "expr_opt", "SEMICOLON", "expr_opt", "CLOSING_PAR", "block_stmt"],
        ["elegir", "OPENING_PAR", "expr", "CLOSING_PAR", "OPENING_KEY", "casos_list", "CLOSING_KEY"],
        ["romper", "g_semicolon_opt"],
        ["continuar", "g_semicolon_opt"],
        ["intentar", "block_stmt", "capturar", "block_stmt"],              
        ["funcion", "IDENT", "OPENING_PAR", "params_opt", "CLOSING_PAR", "block_stmt"],               
        ["block_stmt"],                 
        ["retornar", "expr_opt", "g_semicolon_opt"], 
        ["consola_call", "g_semicolon_opt"],              
        ["expr", "g_semicolon_opt"],             
        ["SEMICOLON"]                           
    ],
    "g_decl_list": [
        ["IDENT", "g_decl_init", "g_decl_list_prime"] 
    ],
    "g_decl_init": [
        ["ASSIGN", "expr_or_crear"],
        ["epsylon"]
    ],
    "g_decl_list_prime": [
        ["COMMA", "g_decl_list"], 
        ["epsylon"]
    ],
    "g_semicolon_opt": [
        ["SEMICOLON"],
        ["epsylon"]
    ],
    "g_sino_opt": [
        ["sino", "g_sino_tail"],
        ["epsylon"]
    ],
    "g_sino_tail": [
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt", "g_sino_opt"],
        ["block_stmt"] 
    ],

    "b_stmt": [
        ["decl_keyword", "b_decl_list", "b_semicolon_opt"], 
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt", "b_sino_opt"],                    
        ["mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt"],              
        ["hacer", "block_stmt", "mientras", "OPENING_PAR", "expr", "CLOSING_PAR", "b_semicolon_opt"],        
        ["para", "OPENING_PAR", "para_init", "SEMICOLON", "expr_opt", "SEMICOLON", "expr_opt", "CLOSING_PAR", "block_stmt"],
        ["elegir", "OPENING_PAR", "expr", "CLOSING_PAR", "OPENING_KEY", "casos_list", "CLOSING_KEY"],
        ["romper", "b_semicolon_opt"],
        ["continuar", "b_semicolon_opt"],
        ["intentar", "block_stmt", "capturar", "block_stmt"],              
        ["funcion", "IDENT", "OPENING_PAR", "params_opt", "CLOSING_PAR", "block_stmt"],               
        ["block_stmt"],                 
        ["retornar", "expr_opt", "b_semicolon_opt"], 
        ["consola_call", "b_semicolon_opt"],              
        ["expr", "b_semicolon_opt"],             
        ["SEMICOLON"]                           
    ],
    "b_decl_list": [
        ["IDENT", "b_decl_init", "b_decl_list_prime"] 
    ],
    "b_decl_init": [
        ["ASSIGN", "expr_or_crear"],
        ["epsylon"]
    ],
    "b_decl_list_prime": [
        ["COMMA", "b_decl_list"], 
        ["epsylon"]
    ],
    "b_semicolon_opt": [
        ["SEMICOLON"],
        ["epsylon"]
    ],
    "b_sino_opt": [
        ["sino", "b_sino_tail"],
        ["epsylon"]
    ],
    "b_sino_tail": [
        ["si", "OPENING_PAR", "expr", "CLOSING_PAR", "block_stmt", "b_sino_opt"],
        ["block_stmt"] 
    ],

    "decl_keyword": [
        ["var"], ["mut"], ["const"]
    ],
    
    "expr_or_crear": [
        ["crear", "crear_type", "crear_args_opt"],
        ["expr"]
    ],
    "crear_args_opt": [
        ["OPENING_PAR", "args_opt", "CLOSING_PAR"],
        ["epsylon"]
    ],
    "crear_type": [
        ["IDENT"], ["Arreglo"], ["Cadena"], ["Matriz"]
    ],

    "para_init": [
        ["decl_keyword", "b_decl_list"],
        ["expr_opt"]
    ],
    "casos_list": [
        ["caso", "expr", "COLON", "block_code", "casos_list"],
        ["porDefecto", "COLON", "block_code"],
        ["epsylon"]
    ],
    "block_stmt": [
        ["OPENING_KEY", "block_code", "CLOSING_KEY"]
    ],

    # ── Expresiones Globales ────────────────────────────────────────────────────
    "expr_opt": [
        ["expr"],
        ["epsylon"]
    ],
    "expr": [
        ["factor", "expr_prime"]
    ],
    "expr_prime": [
        ["PLUS", "factor", "expr_prime"],
        ["MINUS", "factor", "expr_prime"],
        ["TIMES", "factor", "expr_prime"],
        ["DIV", "factor", "expr_prime"],
        ["MOD", "factor", "expr_prime"],
        ["POWER", "factor", "expr_prime"],
        ["EQUAL", "factor", "expr_prime"],
        ["STRICT_EQUAL", "factor", "expr_prime"],
        ["NEQ", "factor", "expr_prime"],
        ["STRICT_NEQ", "factor", "expr_prime"],
        ["LESS", "factor", "expr_prime"],
        ["GREATER", "factor", "expr_prime"],
        ["LEQ", "factor", "expr_prime"],
        ["GEQ", "factor", "expr_prime"],
        ["AND", "factor", "expr_prime"],
        ["OR", "factor", "expr_prime"],
        ["TERNARY", "ternary_mid_expr", "COLON", "expr_or_consola"], 
        ["epsylon"]
    ],
    "expr_or_consola": [
        ["expr"],
        ["consola_call"]
    ],

    # ── Expresiones Internas Estrictas (EXCLUSIVAS para los argumentos) ─────────
    "arg_expr": [
        ["factor", "arg_expr_prime"]
    ],
    "arg_expr_prime": [
        ["PLUS", "factor", "arg_expr_prime"],
        ["MINUS", "factor", "arg_expr_prime"],
        ["TIMES", "factor", "arg_expr_prime"],
        ["DIV", "factor", "arg_expr_prime"],
        ["MOD", "factor", "arg_expr_prime"],
        ["POWER", "factor", "arg_expr_prime"],
        ["EQUAL", "factor", "arg_expr_prime"],
        ["STRICT_EQUAL", "factor", "arg_expr_prime"],
        ["NEQ", "factor", "arg_expr_prime"],
        ["STRICT_NEQ", "factor", "arg_expr_prime"],
        ["LESS", "factor", "arg_expr_prime"],
        ["GREATER", "factor", "arg_expr_prime"],
        ["LEQ", "factor", "arg_expr_prime"],
        ["GEQ", "factor", "arg_expr_prime"],
        ["AND", "factor", "arg_expr_prime"],
        ["OR", "factor", "arg_expr_prime"],
        ["TERNARY", "ternary_mid_expr", "COLON", "arg_expr_or_consola"], 
        ["epsylon"]
    ],
    "arg_expr_or_consola": [
        ["arg_expr"],
        ["consola_call"]
    ],

    # ── Expresiones Medias de Ternario (Atrapan el COLON) ───────────────────────
    "ternary_mid_expr": [
        ["factor", "ternary_mid_expr_prime"],
        ["consola_call"]
    ],
    "ternary_mid_expr_prime": [
        ["PLUS", "factor", "ternary_mid_expr_prime"],
        ["MINUS", "factor", "ternary_mid_expr_prime"],
        ["TIMES", "factor", "ternary_mid_expr_prime"],
        ["DIV", "factor", "ternary_mid_expr_prime"],
        ["MOD", "factor", "ternary_mid_expr_prime"],
        ["POWER", "factor", "ternary_mid_expr_prime"],
        ["EQUAL", "factor", "ternary_mid_expr_prime"],
        ["STRICT_EQUAL", "factor", "ternary_mid_expr_prime"],
        ["NEQ", "factor", "ternary_mid_expr_prime"],
        ["STRICT_NEQ", "factor", "ternary_mid_expr_prime"],
        ["LESS", "factor", "ternary_mid_expr_prime"],
        ["GREATER", "factor", "ternary_mid_expr_prime"],
        ["LEQ", "factor", "ternary_mid_expr_prime"],
        ["GEQ", "factor", "ternary_mid_expr_prime"],
        ["AND", "factor", "ternary_mid_expr_prime"],
        ["OR", "factor", "ternary_mid_expr_prime"],
        ["TERNARY", "ternary_mid_expr", "COLON", "ternary_mid_expr"], 
        ["epsylon"]
    ],

    "consola_call": [
        ["consola", "PERIOD", "consola_method", "OPENING_PAR", "args_opt", "CLOSING_PAR"]
    ],
    "consola_method": [
        ["afirmar"], ["agrupar"], ["error"], ["escribir"], 
        ["info"], ["limpiar"], ["tabla"]
    ],

    # ── Factores Limpios (Sin crear, ++, ni --) ─────────────────────────────────
    "factor": [
        ["IDENT", "factor_tail"],
        ["Mate", "factor_tail"], ["Numero", "factor_tail"], 
        ["Arreglo", "factor_tail"], ["Cadena", "factor_tail"], 
        ["Matriz", "factor_tail"], ["Booleano", "factor_tail"], 
        ["OPENING_PAR", "args_opt", "CLOSING_PAR", "factor_tail"],
        ["OPENING_BRA", "array_args_opt", "CLOSING_BRA", "factor_tail"], 
        ["OPENING_KEY", "obj_elements", "CLOSING_KEY"],
        
        ["NUMBER"],
        ["STR"],
        ["verdadero"], ["falso"], ["nulo"], ["indefinido"], 
        ["Infinito"], ["NuN"], 

        ["MINUS", "factor"],
        ["PLUS", "factor"],
        ["NOT", "factor"]
    ],
    "factor_tail": [
        ["OPENING_PAR", "args_opt", "CLOSING_PAR", "factor_tail"],
        ["OPENING_BRA", "expr", "CLOSING_BRA", "factor_tail"],
        ["PERIOD", "IDENT", "factor_tail"],
        ["ASSIGN", "expr_or_crear"],
        ["PLUS_ASSIGN", "expr"],
        ["MINUS_ASSIGN", "expr"],
        ["TIMES_ASSIGN", "expr"],
        ["DIV_ASSIGN", "expr"],
        ["MOD_ASSIGN", "expr"],
        ["POWER_ASSIGN", "expr"],
        ["ARROW", "arrow_body"],
        
        # Test 19 solucionado: i++ y i-- admitidos como sufijos válidos de identificadores
        ["INCREMENT", "factor_tail"],
        ["DECREMENT", "factor_tail"],
        
        ["epsylon"]
    ],
    "arrow_body": [
        ["block_stmt"],
        ["expr"]
    ],

    # ── Estructuras con Siguientes Protegidos ───────────────────────────────────
    "params_opt": [
        ["IDENT", "params_prime"],
        ["epsylon"]
    ],
    "params_prime": [
        ["COMMA", "IDENT", "params_prime"],
        ["epsylon"]
    ],
    
    "args_opt": [
        ["arg_expr", "args_prime"],
        ["epsylon"]
    ],
    "args_prime": [
        ["COMMA", "arg_expr", "args_prime"],
        ["epsylon"]
    ],
    
    "array_args_opt": [
        ["expr", "array_args_prime"],
        ["epsylon"]
    ],
    "array_args_prime": [
        ["COMMA", "expr", "array_args_prime"],
        ["epsylon"]
    ],
    
    "obj_elements": [
        ["IDENT", "obj_tail", "obj_prime"],
        ["epsylon"]
    ],
    "obj_tail": [
        ["COLON", "expr"],
        ["OPENING_PAR", "params_opt", "CLOSING_PAR", "block_stmt"]
    ],
    "obj_prime": [
        ["COMMA", "IDENT", "obj_tail", "obj_prime"],
        ["epsylon"]
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