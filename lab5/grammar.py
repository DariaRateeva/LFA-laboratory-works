from collections import defaultdict
import itertools


class CFGtoCNFConverter:
    def __init__(self, grammar, start_symbol):
        self.grammar = defaultdict(list)
        for head, bodies in grammar.items():
            for body in bodies:
                self.grammar[head].append(tuple(body))
        self.start_symbol = start_symbol
        self.counter = 1
        self.term_map = {}

    def print_grammar(self, title):
        print(f"\n=== {title} ===")
        for head in sorted(self.grammar.keys()):
            bodies = [" ".join(body) for body in self.grammar[head]]
            print(f"{head} → {' | '.join(bodies)}")

    def eliminate_epsilon(self):
        nullable = set()
        for head, prods in self.grammar.items():
            for prod in prods:
                if prod == ('ε',):
                    nullable.add(head)

        # Remove ε-productions
        for head in self.grammar:
            self.grammar[head] = [p for p in self.grammar[head] if p != ('ε',)]

        changed = True
        while changed:
            changed = False
            for head, prods in self.grammar.items():
                for prod in prods:
                    if all(sym in nullable for sym in prod):
                        if head not in nullable:
                            nullable.add(head)
                            changed = True

        new_grammar = defaultdict(list)
        for head, prods in self.grammar.items():
            for prod in prods:
                indices = [i for i, sym in enumerate(prod) if sym in nullable]
                for mask in itertools.product([True, False], repeat=len(indices)):
                    new_prod = list(prod)
                    for i, remove in zip(indices, mask):
                        if remove:
                            new_prod[i] = None
                    new_prod = tuple(sym for sym in new_prod if sym)
                    if new_prod and new_prod not in new_grammar[head]:
                        new_grammar[head].append(new_prod)

        self.grammar = new_grammar
        self.print_grammar("After Eliminating ε-productions")

    def eliminate_unit_productions(self):
        unit_pairs = set()
        for head in self.grammar:
            for prod in self.grammar[head]:
                if len(prod) == 1 and prod[0].isupper():
                    unit_pairs.add((head, prod[0]))

        while True:
            new_pairs = unit_pairs.copy()
            for (A, B) in unit_pairs:
                for prod in self.grammar.get(B, []):
                    if len(prod) == 1 and prod[0].isupper():
                        new_pairs.add((A, prod[0]))
            if new_pairs == unit_pairs:
                break
            unit_pairs = new_pairs

        new_grammar = defaultdict(list)
        for head, prods in self.grammar.items():
            for prod in prods:
                if not (len(prod) == 1 and prod[0].isupper()):
                    new_grammar[head].append(prod)

        for (A, B) in unit_pairs:
            for prod in self.grammar[B]:
                if not (len(prod) == 1 and prod[0].isupper()) and prod not in new_grammar[A]:
                    new_grammar[A].append(prod)

        self.grammar = new_grammar
        self.print_grammar("After Eliminating Unit Productions")

    def replace_terminals_in_long_productions(self):
        updated_grammar = defaultdict(list)
        for head, prods in self.grammar.items():
            for prod in prods:
                if len(prod) > 1:
                    new_prod = []
                    for sym in prod:
                        if not sym.isupper():
                            if sym not in self.term_map:
                                new_nonterminal = f"X_{sym}"
                                self.term_map[sym] = new_nonterminal
                                updated_grammar[new_nonterminal].append((sym,))
                            new_prod.append(self.term_map[sym])
                        else:
                            new_prod.append(sym)
                    updated_grammar[head].append(tuple(new_prod))
                else:
                    updated_grammar[head].append(prod)
        self.grammar = updated_grammar
        self.print_grammar("After Replacing Terminals in Long Productions")

    def convert_to_binary_rules(self):
        def create_new_symbol():
            sym = f"Y{self.counter}"
            self.counter += 1
            return sym

        bin_cache = {}  # (A, B) → New symbol
        updated_grammar = defaultdict(list)

        for head, prods in self.grammar.items():
            for prod in prods:
                symbols = list(prod)
                while len(symbols) > 2:
                    pair = (symbols[0], symbols[1])
                    if pair not in bin_cache:
                        new_sym = create_new_symbol()
                        bin_cache[pair] = new_sym
                        updated_grammar[new_sym].append(pair)
                    new_nt = bin_cache[pair]
                    symbols = [new_nt] + symbols[2:]
                updated_grammar[head].append(tuple(symbols))

        self.grammar = updated_grammar
        self.print_grammar("After Converting to Binary Rules")

    def convert(self):
        self.print_grammar("Initial Grammar")
        self.eliminate_epsilon()
        self.eliminate_unit_productions()
        self.replace_terminals_in_long_productions()
        self.convert_to_binary_rules()
        self.print_grammar("Final CNF Grammar")
        return dict(self.grammar)


# === Example input ===

cfg = {
    "S": [["d", "B"], ["A"]],
    "A": [["d"], ["d", "S"], ["a", "B", "d", "A", "B"]],
    "B": [["a"], ["d", "A"], ["A"], ["ε"]],
    "C": [["A", "a"]]
}

converter = CFGtoCNFConverter(cfg, start_symbol="S")
cnf = converter.convert()