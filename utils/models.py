class LinearSystem:
    def __init__(self, A, b):
        self.A = A
        self.b = b
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
        import copy
        self.matrix = copy.deepcopy(matrix)
        self.answers = copy.deepcopy(answers)
        self.stepType = stepType



class LUStep :
    stepType : StepType
    L : list[list[float]]
    U : list[list[float]]
    answers : list[float]
    def __init__(self, L : list[list[float]], U : list[list[float]], stepType : StepType):
        import copy
        self.L = copy.deepcopy(L)
        self.U = copy.deepcopy(U)
        self.stepType = stepType

class IterativeStep :
    answers : list[float]
    def __init__(self, answers: list, stepType : StepType):
        import copy
        self.answers = copy.deepcopy(answers)
        self.stepType = stepType
