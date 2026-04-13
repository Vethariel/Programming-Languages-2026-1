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
    ],
    "code_block": [
        ["code_line", "code_block"],
        ["epsylon"]
    ],
    "declare_or_assign": [
        ["var_type", "IDENT", "assign"],
    ],
    "var_type": [
        ["mut"],
        ["var"],
        ["const"],
    ],
    "assign": [
        ["SEMI"],
        ["assign_type", "expr", "SEMI"]
    ],
    "assign_type": [
        ["ASSIGN"],
        ["PLUS_ASSIGN"],
        ["MINUS_ASSIGN"],
        ["TIMES_ASSIGN"],
        ["DIV_ASSIGN"],
        ["MOD_ASSIGN"],
    ],
    "expr": [
        ["expr_assign"],
    ],
    "expr_assign": [
        ["expr_or_nullish", "expr_assign_tail"],
    ],
    "expr_assign_tail": [
        ["assign_type", "expr_assign"],   # si hay operador, continúa
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
        ["EQ"],
        ["NEQ"],
        ["EEQ"],
        ["NEEQ"],
    ],
    "expr_rel": [
        ["expr_add", "expr_rel_tail"],
    ],
    "expr_rel_tail": [
        ["relational", "expr_add", "expr_rel_tail"],
        ["epsylon"]
    ],
    "relational": [
        ["LT"],
        ["LE"],
        ["GT"],
        ["GE"],
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
        ["tipoDe"],
        ["eliminar"],
        ["vacio"],
        ["esperar"],
    ],
    "expr_postfix": [
        ["expr_new", "expr_postfix_tail"],
    ],
    "expr_postfix_tail": [
        ["postfix", "expr_postfix_tail"],
        ["epsylon"]
    ],
    "postfix": [
        ["INCREMENT"],
        ["DECREMENT"],
    ],
    "expr_new": [
        ["crear", "expr_access_or_call"],
        ["expr_access_or_call"],
    ],
    "expr_access_or_call": [
        ["expr_group", "expr_access_or_call_tail"],
    ],
    "expr_access_or_call_tail": [
        ["PERIOD", "IDENT", "expr_access_or_call_tail"],
        ["LBRACKET", "expr", "RBRACKET", "expr_access_or_call_tail"],
        ["LPAREN", "call_args", "RPAREN", "expr_access_or_call_tail"],
        ["epsylon"]
    ],
    "call_args": [
        ["expr", "call_args_tail"],
        ["epsylon"]
    ],
    "call_args_tail": [
        ["COMMA", "expr", "call_args_tail"],
        ["epsylon"]
    ],
    "expr_group": [
        ["LPAREN", "expr_or_params", "RPAREN"],
        ["element"],
    ],
    "expr_or_params": [
        ["expr", "expr_or_params_tail"],
    ],
    "expr_or_params_tail": [
        ["COMMA", "expr", "expr_or_params_tail"],
        ["epsylon"]
    ],
    "element": [
        ["IDENT"],
        ["NUMBER"],
        ["STR"],
        ["REGEX"],
        ["arr_declare"],
        ["create_object"],
        ["verdadero"],
        ["falso"],
        ["nulo"],
        ["indefinido"],
    ],
    "arr_declare": [
        ["LBRACKET", "expr", "arr_declare_tail", "RBRACKET"],
    ],
    "arr_declare_tail": [
        ["COMMA", "expr", "arr_declare_tail"],
        ["epsylon"]
    ],
    "create_object": [
        ["LBRACE", "fields", "RBRACE"],
    ],
    "fields": [
        ["IDENT", "COLON", "expr", "fields_tail"],
        ["epsylon"]
    ],
    "fields_tail": [
        ["COMMA", "IDENT", "COLON", "expr", "fields_tail"],
        ["epsylon"]
    ],
   "conditional": [
        ["si", "LPAREN", "expr", "RPAREN", "simple_block", "conditional_alter"],
    ],
    "conditional_alter": [
        ["sino", "conditional_alter_tail"],
        ["epsylon"]
    ],
    "conditional_alter_tail": [
        ["si", "LPAREN", "expr", "RPAREN", "simple_block", "conditional_alter"],  # sino si ...
        ["simple_block"],  # sino { ... }
    ],
    "switch": [
        ["elegir", "LPAREN", "expr", "RPAREN", "LBRACE", "cases", "default_case", "RBRACE"],
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
        ["para", "LPAREN", "expr", "SEMI", "expr", "SEMI", "expr", "RPAREN", "simple_block_break_continue"],
    ],
    "while_loop": [
        ["mientras", "LPAREN", "expr", "RPAREN", "simple_block_break_continue"],
    ],
    "do_while_loop": [
        ["hacer", "simple_block_break_continue", "mientras", "LPAREN", "expr", "RPAREN", "SEMI"],
    ],
    "break": [
        ["romper", "SEMI"],
    ],
    "continue": [
        ["continuar", "SEMI"],
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
        ["LBRACE", "code_block_break_continue", "RBRACE"],
    ],
    "simple_block": [
        ["LBRACE", "code_block", "RBRACE"],
    ],
    "function": [
        ["funcion", "IDENT", "LPAREN", "params", "RPAREN", "simple_block", "return_stmt"],
    ],
    "return_stmt": [
        ["retornar", "return_stmt_tail"],
        ["epsylon"]
    ],
    "return_stmt_tail": [
        ["expr", "SEMI"],
        ["SEMI"]
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
        ["expr", "SEMI"],
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

def main():
    grammar = Grammar()
    for key, value in grammar.grammar.items():
        rules = value["rules"]
        for rule in rules:
            print(key," ->",rule["rule"], "-> ",rule["pred_set"])
    print("\nprediccion de no terminales\n")
    for key, value in grammar.grammar.items():
        pred = value["total_pred_set"]
        print(key, "->", pred)
    print("\nprimeros: ",grammar.first_set)
    print("\nsiguientes:", grammar.follow_set)
    print("\nconflictos:", grammar.conflicts)
    
if __name__ == "__main__":
    main()