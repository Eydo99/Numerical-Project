from typing import Optional
from utils.models import GaussStep, StepType, LinearSystem
from utils.step_recorder import GaussStepRecorder
from utils.auxilary import round_sig, pivot, scaling_factors
from exceptions.singular import SingularMatrixException


class GaussJordanSolver :
    def __init__(self, system:LinearSystem, single_step : bool = False) :
        self.system = system
        self.step_recorder = GaussStepRecorder(single_step)

    
    def solve(self, sig_figs=6, tol=1e-12, scaling : bool = True)-> tuple[list,list[list]]:
        
        
        matrix = self.system.A
        answers = self.system.b

        # Forward Elimination
        length = self.system.n
        scales = scaling_factors(matrix) if scaling else [1] * length
        
        # Forward + Back Elimination
        for i in range(length) :
            # Here we need to ensure that the pivot is large as possible to not divide by an infinitesmal value
            # By pivoting
            err = pivot(matrix, answers, i, scaling, scales, tol)
            if err == -1 :
                raise SingularMatrixException()

            self.step_recorder.record(matrix, answers, StepType.SWAP)

            # i : the index of eliminating pivot 
            for j in range(length):
                # j : the index of the row having element to eliminate
                # unlike in the normal Gauss elimination here we eliminate above and below the pivot 
                # so we must ignore the element itself
                if(j == i) : continue

                # no need to check again since if pivot was 0 i would have known
                factor = round_sig(matrix[j][i] / matrix[i][i], sig_figs)

                for k in range(i, length):
                    # k : the index of the column having element to eliminate
                    matrix[j][k] = round_sig(matrix[j][k] - round_sig(factor * matrix[i][k], sig_figs), sig_figs)
                
                answers[j] = round_sig(answers[j] - round_sig(factor * answers[i], sig_figs), sig_figs)

                print(f"{matrix}" + "\n\n\n")
                self.step_recorder.record(matrix, answers, StepType.ELIM)
            
            
        for i in range(length):
            answers[i] = round_sig(answers[i] / matrix[i][i], sig_figs) 
            matrix[i][i] = 1
        

        self.step_recorder.record(matrix, answers, StepType.SOL)

        return answers, matrix


