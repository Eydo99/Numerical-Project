import copy
from .models import GaussStep,LUStep, StepType

class GaussStepRecorder:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps = []

    def record(self, A, b, step_type):
        if self.enabled:
            self.steps.append(GaussStep(copy.deepcopy(A),copy.deepcopy(b), step_type))

class LUStepRecorder:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps = []

    def record(self, L, U, step_type):
        if self.enabled:
            self.steps.append(LUStep(copy.deepcopy(L),copy.deepcopy(U), step_type))
    
    
    def record_dolittle(self, A, o, i, j, step_type):
        """ o : order array
            i : index of eliminating row
            j : index of row on which the elimination takes place"""
        L = list[list]
        U = list[list]
        n = len(A)
        if self.enabled:
            k : int 
            for k in range(j + 1):
                u_start = min(k, i + 1)
                # Handling U
                U.append([0]*u_start + copy.deepcopy(A[o[k]][u_start:]))
                # Handling L
                L.append(copy.deepcopy(A[o[k]][:u_start]) + [0]*(k-u_start) + [1] + [0]*[n-1 - k])
            for k in range(j + 1, n):
                # Handling U
                U.append([0]*(i) + copy.deepcopy(A[o[k]][i:]))
                # Handling L
                L.append(copy.deepcopy(A[o[k]][:i]) + [0]*(k-i) + [1] + [0]*[n-1 - k])

            self.steps.append(LUStep(L,U,step_type))