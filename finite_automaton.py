from base import Grammar
import graphviz
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

    def to_regular_grammar(self):
        """
        Convert the finite automaton to a Regular Grammar (RG)
        and return a Grammar object.
        """
        non_terminals = self.Q  # FA states → Non-terminals
        terminals = self.Sigma  # FA alphabet → Terminals
        productions = {}  # Production rules

        for state in self.Q:
            productions[state] = []  # Initialize productions

            if state in self.delta:
                for symbol, next_states in self.delta[state].items():
                    for next_state in next_states:
                        productions[state].append(f"{symbol}{next_state}")

            # If state is final, add epsilon (ε) transition
            if state in self.F:
                productions[state].append("ε")

        # Return a Grammar object
        return Grammar(VN=non_terminals, VT=terminals, P=productions, S=self.q0)

    def is_deterministic(self):
        """Checks if the FA is deterministic (DFA)."""
        for state, transitions in self.delta.items():
            seen_symbols = set()
            for symbol, next_states in transitions.items():
                if symbol == "ε":  # If an ε-transition exists → NDFA
                    return False
                if len(next_states) > 1:  # If multiple destinations for a symbol → NDFA
                    return False
                if symbol in seen_symbols:
                    return False  # More than one transition for the same symbol
                seen_symbols.add(symbol)
        return True

    def convert_ndfa_to_dfa(self):
        """ Converts an NDFA to a DFA using the subset construction method. """
        from copy import deepcopy

        #dfa_states = {}  # Maps DFA state sets to names
        queue = [frozenset([self.q0])]  # Start DFA state as a set
        dfa_start = queue[0]  # DFA start state
        dfa_transitions = {}  # DFA transition table
        dfa_final_states = set()  # DFA final states

        seen_states = {}  # Dictionary to store unique state sets and map them to names

        while queue:
            current = queue.pop(0)  # Get current DFA state (set of NFA states)

            # Assign a unique state name if not already assigned
            if current not in seen_states:
                seen_states[current] = f"D{len(seen_states)}"

            current_name = seen_states[current]  # Get the assigned DFA state name

            # If any NFA final state is in this DFA state, mark DFA state as final
            if any(state in self.F for state in current):
                dfa_final_states.add(current_name)

            # Initialize transition table for this DFA state
            if current_name not in dfa_transitions:
                dfa_transitions[current_name] = {}

            for symbol in self.Sigma:  # Iterate over alphabet
                # Find the next DFA state (set of NFA states)
                next_state = frozenset(
                    sum([list(self.delta.get(s, {}).get(symbol, [])) for s in current], [])
                )

                if next_state:  # If the new state is non-empty
                    if next_state not in seen_states:
                        seen_states[next_state] = f"D{len(seen_states)}"
                        queue.append(next_state)  # Add new state to process

                    dfa_transitions[current_name][symbol] = seen_states[next_state]  # Set DFA transition

        return FiniteAutomaton(
            states=set(seen_states.values()),
            alphabet=self.Sigma,
            transitions=dfa_transitions,
            start_state=seen_states[dfa_start],
            final_states=dfa_final_states
        )

    def visualize(self, filename="finite_automaton"):
        """
        Generate a graphical representation of the finite automaton using Graphviz.
        """
        dot = graphviz.Digraph(format="png")

        # Ensure all states are correctly named
        state_labels = {state: state for state in self.Q}  # Ensures state names remain correct

        # Add states to the graph
        for state in self.Q:
            if state in self.F:
                dot.node(state_labels[state], shape="doublecircle")  # Final states: double circle
            elif state == self.q0:
                dot.node(state_labels[state], shape="circle", style="bold")  # Start state: bold circle
            else:
                dot.node(state_labels[state], shape="circle")

        # Add transitions
        for state, transitions in self.delta.items():
            for symbol, next_state in transitions.items():
                # Ensure next_state is correctly mapped
                next_state_label = state_labels.get(next_state, str(next_state))
                dot.edge(state_labels[state], next_state_label, label=symbol)

        # Add an invisible start node to indicate the start state
        dot.node("start", shape="none")  # Invisible starting point
        dot.edge("start", state_labels[self.q0])  # Arrow pointing to the start state

        # Render the graph
        dot.render(filename, view=True)
