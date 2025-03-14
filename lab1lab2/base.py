class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN  # Set of non-terminals
        self.VT = VT  # Set of terminals
        self.P = P    # Dictionary of production rules
        self.S = S