from grammar import Grammar

def main():
    grammar = Grammar()
    generated_strings = set()  
    while len(generated_strings) < 5:
        new_string = grammar.generate_string()
        generated_strings.add(new_string)

    for string in generated_strings:
        print(string)
    
    # Convert to finite automaton
    fa = grammar.toFiniteAutomaton()
    
    # Testing strings
    test_strings = ["ababadaaba", "abababadbbdaaabbbabababababadbbdaba", "abd", "ba", "dba"]
    print("\nTesting strings:")
    for test_str in test_strings:
        belongs = fa.stringBelongToLanguage(test_str)
        print(f"String '{test_str}' belongs to language: {belongs}")

    classification = grammar.classify_chomsky_hierarchy()
    print(f"Grammar classification: {classification}")

if __name__ == "__main__":
    main()