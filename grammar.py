import random
from finite_automaton import FiniteAutomaton


class Grammar:
    def __init__(self, non_terminals, terminals, production_rules, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.production_rules = production_rules
        self.start_symbol = start_symbol

    def generate_string(self):
        current = self.start_symbol
        result = ""

        while any(char in self.production_rules for char in current):
            new_string = ""
            for char in current:
                if char in self.production_rules:
                    new_string += random.choice(self.production_rules[char])
                else:
                    new_string += char
            current = new_string
        return current
    

    def to_finite_automaton(self):
        states = set(self.non_terminals)
        alphabet = set(self.terminals)
        transitions = {}

        for non_terminals, replacements in self.production_rules.items():
            for replacement in replacements:
                first_char = replacements[0]
                if first_char in self.terminals:
                    transitions.setdefault(non_terminals, {}).setdefault(first_char, set()).add(replacement)
                else:
                    transitions.setdefault(non_terminals, {}).setdefault(first_char, set()).add(first_char)

        return FiniteAutomaton(states, alphabet, transitions, self.start_symbol, {"C", "D"})
    

    def generate_multiple_strings(self, n=5):
        return [self.generate_string() for _ in range(n)]
