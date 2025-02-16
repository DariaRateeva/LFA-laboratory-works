
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states             
        self.Sigma = alphabet        
        self.delta = transitions    
        self.q0 = start_state      
        self.F = final_states      

    def stringBelongToLanguage(self, input_string):
        #Check if the input string belongs to the language
        current_states = set([self.q0])
        
        for char in input_string:
            if char not in self.Sigma:
                return False
                
            next_states = set()
            # For each current state, find all possible next states
            for state in current_states:
                if state in self.delta and char in self.delta[state]:
                    for next_state in self.delta[state][char]:
                        next_states.add(next_state)
                    
            if not next_states:
                return False
                
            current_states = next_states
            
        # Check if any current state is a final state
        return bool(current_states.intersection(self.F))