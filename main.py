from grammar import Grammar
from finite_automaton import FiniteAutomaton

if __name__ == "__main__":
    grammar = Grammar(
        non_terminals={"S", "A", "C", "D"},
        terminals={"a", "b"},
        production_rules={
            "S" : ["aA"],
            "A" : ["bS", "dD"],
            "D" : ["bC", "aD"],
            "C": ["a", "bA"]
        },
        start_symbol="S"
    )

    print("Generated strings: ")
    generated_strings = grammar.generate_multiple_strings(5)
    for s in generated_strings:
        print(s)

    automaton = grammar.to_finite_automaton()

    print("\nString Validation in Finite Automaton: ")
    test_string = ["aab", "abb", "abd", "ba", "dba"]
    for string in test_string:
        result = automaton.belongs_to_language(string)
        print(f"'{string}' -> {result}")