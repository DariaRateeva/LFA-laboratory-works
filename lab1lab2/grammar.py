# grammar.py
import random
from lab1lab2.base import Grammar
from lab1lab2.finite_automaton import FiniteAutomaton

  # Start symbol
class ExtendedGrammar(Grammar):
    def generate_string(self):
        #Generates a valid string by replacing non-terminals until only terminals remain. 
        current = self.S  
        steps = 0

        while any(char in self.VN for char in current) and steps < 50:  # Limit steps to prevent infinite loops
            nt_to_replace = random.choice([char for char in current if char in self.VN])  
            production = random.choice(self.P[nt_to_replace])  
            current = current.replace(nt_to_replace, production, 1)  
            steps += 1

        return current if all(char in self.VT for char in current) else None


    def toFiniteAutomaton(self):
       #Convert the grammar to a finite automaton
        states = set(self.VN)  # non-terminals -> statess
        transitions = {}
        final_states = set()

        # Process each production rule to create FA transitions
        for non_terminal in self.P:
            transitions[non_terminal] = {}  

            for production in self.P[non_terminal]:
                if len(production) == 1 and production in self.VT:
                    # Terminal-only production -> final state
                    if production not in transitions[non_terminal]:
                        transitions[non_terminal][production] = set()
                    transitions[non_terminal][production].add(non_terminal)  # Self-loop for terminal
                        
                    final_states.add(non_terminal)
                    
                else:
                    # Handle multi-symbol productions 
                    first_symbol = production[0]
                    next_state = production[1] if len(production) > 1 else None

                    if first_symbol not in transitions[non_terminal]:
                        transitions[non_terminal][first_symbol] = set()
                        
                    if next_state:
                        transitions[non_terminal][first_symbol].add(next_state)
                    else:
                        # If no next state, this state is final
                        final_states.add(non_terminal)

        fa = FiniteAutomaton(
            states=states,
            alphabet=self.VT,
            transitions=transitions,
            start_state=self.S,
            final_states=final_states
        )

        return fa

    def classify_chomsky_hierarchy(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # Type 2 (Context-Free) Check
                if len(lhs) > 1:
                    is_context_free = False

                # Type 1 (Context-Sensitive) Check
                if len(lhs) > len(rhs):
                    is_context_sensitive = False

                # Type 3 (Regular) Check
                if not (rhs.islower() or (rhs[:-1].islower() and rhs[-1].isupper())):
                    is_regular = False

        if is_regular:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"