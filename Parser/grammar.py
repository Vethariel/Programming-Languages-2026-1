GRAMMAR = {
    "S": [
        { "rule": ["A", "uno", "B", "C"] },
        { "rule": ["S", "dos"] }
    ],
    "A": [
        { "rule": ["B", "C", "D"] },
        { "rule": ["A", "tres"] },
        { "rule": ["epsylon"] }
    ],
    "B": [
        { "rule": ["D", "cuatro", "C", "tres"] },
        { "rule": ["epsylon"] }
    ],
    "C": [
        { "rule": ["cinco", "D", "B"] },
        { "rule": ["epsylon"] }
    ],
    "D": [
        { "rule": ["seis"] },
        { "rule": ["epsylon"] }
    ]
}

import time

class Grammar:
    def __init__(self):
        self.grammar = GRAMMAR
        self.start_symbol = "S"
        self.first_set = {}
        self.first()
        self.follow_set = self.follow()
        self.conflicts = self.pred_sets()
        
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
            for no_terminal, rules in self.grammar.items():
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
            for origin, rules in self.grammar.items():
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
        
        for no_terminal, rules in self.grammar.items():
            seen = set()  # Unión de todos los PRED de las reglas de este no terminal
            
            for rule in rules:
                symbols = rule["rule"]
                rule["pred_set"] = self.pred_sets_of_rule(symbols, no_terminal)
                
                # Detectar conflicto: ¿el mismo terminal aparece en dos reglas de A?
                overlap = seen & rule["pred_set"]
                if overlap:
                    conflicts[no_terminal] = conflicts.get(no_terminal, set()) | overlap
                seen |= rule["pred_set"]
        
        return conflicts  # Vacío = gramática LL(1) ✓

def main():
    grammar = Grammar()
    for key, value in grammar.grammar.items():
        for rule in value:
            print(key," ->",rule["rule"], "-> ",rule["pred_set"])
    print("primeros: ",grammar.first_set)
    print("siguientes:", grammar.follow_set)
    print("conflictos:", grammar.conflicts)
    
if __name__ == "__main__":
    main()