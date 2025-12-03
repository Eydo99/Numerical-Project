class LinearSystem:
    def __init__(self, A, b):
        import copy
        self.A = copy.deepcopy(A)
        self.b = copy.deepcopy(b)
        self.n = len(b)

class StepType :
    SWAP = "swap"
    ELIM = "elim"
    SOL = "sol"
    ITR_ROW = "itr_row"
    ITR_ELE = "itr_ele"

class GaussStep :
    stepType : StepType
    matrix : list[list[float]]
    answers : list[float]
    def __init__(self, matrix : list[list[float]], answers : list[float], stepType : StepType):
        self.matrix = matrix
        self.answers = answers
        self.stepType = stepType



class LUStep :
    stepType : StepType
    L : list[list[float]]
    U : list[list[float]]
    def __init__(self, L : list[list[float]], U : list[list[float]], stepType : StepType):
        self.L = L
        self.U = U
        self.stepType = stepType

class IterativeStep :
    answers : list[float]
    def __init__(self, answers: list, stepType : StepType):
        self.answers = answers
        self.stepType = stepType
