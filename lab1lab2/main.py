from lab1lab2.grammar import ExtendedGrammar
from lab1lab2.finite_automaton import FiniteAutomaton

def main():
    # Define Grammar
    grammar = ExtendedGrammar(
        VN={'S', 'A', 'B'},
        VT={'a', 'b'},
        P={
            'S': ['aA', 'bB'],
            'A': ['a', 'aS'],
            'B': ['b', 'bB']
        },
        S='S'
    )

    # Check and print Grammar classification
    classification = grammar.classify_chomsky_hierarchy()
    print(f"\nGrammar Classification: {classification}")

    # Define FA (Variant 24)
    states = {"q0", "q1", "q2"}
    alphabet = {"a", "b"}
    transitions = {
        "q0": {"b": {"q0", "q1"}, "a": {"q0"}},
        "q1": {"b": {"q2"}, "a": {"q1"}},
        "q2": {"a": {"q2"}}
    }
    start_state = "q0"
    final_states = {"q2"}

    # Create FA object
    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    # Check if FA is Deterministic
    print(f"\nIs the FA deterministic? {fa.is_deterministic()}")

    # Convert NDFA → DFA (if necessary)
    if not fa.is_deterministic():
        dfa = fa.convert_ndfa_to_dfa()

        print("\nConverted DFA:")
        print(f"States: {dfa.Q}")
        print(f"Alphabet: {dfa.Sigma}")
        print(f"Start State: {dfa.q0}")
        print(f"Final States: {dfa.F}")

        print("Transitions:")
        for state, transitions in dfa.delta.items():
            for symbol, next_states in transitions.items():
                print(f"  {state} → {symbol} → {next_states}")
        print("\nGenerating DFA visualization...")
        dfa.visualize("dfa_graph")

        # Convert FA to Regular Grammar
    rg = fa.to_regular_grammar()

    # Print Regular Grammar
    print("\nConverted Regular Grammar:")
    print(f"Non-terminals (VN): {rg.VN}")
    print(f"Terminals (VT): {rg.VT}")
    print(f"Start Symbol: {rg.S}")
    print("Production Rules:")
    for lhs, rhs in rg.P.items():
        print(f"{lhs} → {' | '.join(rhs)}")

if __name__ == "__main__":
    main()
