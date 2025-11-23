class LinearSystem:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.n = len(b)

class StepType :
    SWAP = "swap"
    ELIM = "elim"
    SOL = "sol"

class SolStep :
    stepType : StepType
    matrix : list[list[float]]
    answers : list[float]
    def __init__(self, matrix : list[list[float]], answers : list[float], stepType : StepType):
        import copy
        self.matrix = copy.deepcopy(matrix)
        self.answers = copy.deepcopy(answers)
        self.stepType = stepType


