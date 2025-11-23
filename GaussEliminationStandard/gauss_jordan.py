from typing import Optional
from .models import SolStep, StepType, LinearSystem
from .step_recorder import GaussStepRecorder
from .auxilary import round_sig, pivot
import copy

class GaussJordanSolver :
    def __init__(self, system:LinearSystem, single_step : bool = False) :
        self.system = system
        self.step_recorder = GaussStepRecorder(single_step)

    
    def solve(self, sig_figs=6, tol=1e-12,
               scaling : bool = True) -> tuple[list[SolStep], list[float]] :
        
        
        matrix = self.system.A
        answers = self.system.b

        # Forward Elimination
        length = self.system.n
        scales = [1] * length

        # Only apply scaling if required
        if(scaling):
            for i, row in enumerate(matrix) :
                scales[i] = row[0]
                for j in range(1,length):
                    scales[i] = max(scales[i], abs(row[j]))
                # Now we enforce rounding
                scales[i] = round_sig(scales[i], sig_figs)
        
        # Forward + Back Elimination
        for i in range(length) :
            # Here we need to ensure that the pivot is large as possible to not divide by an infinitesmal value
            # By pivoting
            err = pivot(matrix, answers, i, scaling, scales, tol)
            if err == -1 :
                return None

            self.step_recorder.record(matrix, answers, StepType.SWAP)

            # i : the index of eliminating pivot 
            for j in range(length):
                # j : the index of the row having element to eliminate
                # unlike in the normal Gauss elimination here we eliminate above and below the pivot 
                # so we must ignore the element itself
                if(j == i) : continue

                factor = round_sig(matrix[j][i] / matrix[i][i], sig_figs)

                for k in range(i, length):
                    # k : the index of the column having element to eliminate
                    matrix[j][k] = round_sig(matrix[j][k] - round_sig(factor * matrix[i][k], sig_figs), sig_figs)
                
                answers[j] = round_sig(answers[j] - round_sig(factor * answers[i], sig_figs), sig_figs)

                self.step_recorder.record(matrix, answers, StepType.ELIM)
            
            
        for i in range(length):
            answers[i] /= matrix[i][i]
            matrix[i][i] = 1
        

        self.step_recorder.record(matrix, answers, StepType.SOL)

        return self.step_recorder.steps, answers



        # Enforcing precision
        # precision = Decimal("0." + "0" * (digits - 1) + "1")
        
        # def round_val(value : float): # since we want to enforce n-digit precision everywhere
        #     # rounded : float = Decimal(value).quantize(precision, rounding= ROUND_HALF_UP)
        #     return round(value, digits)
        

