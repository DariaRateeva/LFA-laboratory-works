class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states


    def belongs_to_language(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet or current_state not in self.transitions:
                return False
            if char in self.transitions[current_state]:
                current_state = list(self.transitions[current_state][char])[0]
            else:
                return False
                
        return current_state in self.final_states
