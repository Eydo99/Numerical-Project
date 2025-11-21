class LinearSystem:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.n = len(b)