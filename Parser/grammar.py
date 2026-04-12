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
        self.first_set = self.first()
        self.follow_set = self.follow()
        
    def first(self):
        first_set = {}
        pending_no_terminal = []
        for no_terminal in self.grammar.keys():
            first_set[no_terminal] = set()
            pending_no_terminal.append((no_terminal,"all",0,0))
        MAX_ITER = 1000
        iterations = 0
        while pending_no_terminal and iterations < MAX_ITER:
            iterations += 1
            no_terminal, pending, index, rule_index = pending_no_terminal.pop(0)
            if pending == "all":
                for rules in self.grammar[no_terminal]:
                    rule = rules["rule"]
                    first_symbol = rule[index]
                    if first_symbol == "epsylon":
                        first_set[no_terminal].add("epsylon")
                    else:
                        if first_symbol not in first_set.keys():
                            first_set[no_terminal].add(first_symbol)
                        else:
                            pending_no_terminal.append((no_terminal,first_symbol, 0, self.grammar[no_terminal].index(rules)))
            elif pending not in first_set.keys():
                first_set[no_terminal].add(pending)
            elif no_terminal == pending:
                if "epsylon" in first_set[pending]:
                    rule = self.grammar[no_terminal][rule_index]
                    rule_arr = rule["rule"]
                    if index+1 < len(rule_arr):
                        new_pending = rule_arr[index+1]
                        pending_no_terminal.append((no_terminal,new_pending,index+1,rule_index))
            else:
                incomplete_no_terminal = [x for x in pending_no_terminal if x[0] == pending]
                if len(incomplete_no_terminal) == 0:
                    first_pending = first_set[pending].copy()
                    epsylon = "epsylon" in first_pending
                    if epsylon: first_pending.remove("epsylon")
                    if len(first_pending) == 0: first_set[no_terminal].add("epsylon")
                    else:
                        rule = self.grammar[no_terminal][rule_index]
                        rule_arr = rule["rule"]
                        if index+1 < len(rule_arr):
                            new_pending = rule_arr[index+1]
                            pending_no_terminal.append((no_terminal,new_pending,index+1,rule_index))
                    first_set[no_terminal].update(first_pending)
                else:
                    pending_no_terminal.append((no_terminal, pending, index, rule_index))
        return first_set

    def follow(self):
        pass

    def pred_sets(self):
        self.first()
        self.follow()

def main():
    grammar = Grammar()
    for key, value in grammar.grammar.items():
        for rule in value:
            print(key," ->",rule["rule"])
    print(grammar.first_set)
    
if __name__ == "__main__":
    main()