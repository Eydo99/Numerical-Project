from LSE.utils.models import GaussStep, StepType, LinearSystem
from LSE.utils.step_recorder import GaussStepRecorder
from LSE.utils.auxilary import round_sig, pivot, back_sub, scaling_factors
from LSE.exceptions.singular import SingularMatrixException
import time
import math


class GaussSolver:
    def __init__(self, system:LinearSystem, single_step=False):
        self.system = system
        self.step_recorder = GaussStepRecorder(single_step)

    def solve(self, sig_figs=6, tol=1e-12, scaling : bool = True) -> tuple[list, list[list]] :
        
        A, b, n = self.system.A , self.system.b, self.system.n
        scales = scaling_factors(A) if scaling else [1]*n
        # start_time = time.perf_counter()
        for col in range(n):
            er = pivot(A, b, col, scaling, scales, tol=tol)
            if er == -1:
                raise SingularMatrixException()
            self.step_recorder.record(A, b, StepType.SWAP)

            for row in range(col+1, n):
                factor = round_sig(A[row][col] / A[col][col],sig_figs)
                for i in range(col+1, n):
                    A[row][i] = round_sig(A[row][i] - round_sig(factor * A[col][i], sig_figs), sig_figs)

                A[row][col] = 0
                b[row] = round_sig(b[row] - round_sig(factor*b[col], sig_figs), sig_figs)
                self.step_recorder.record(A, b, StepType.ELIM)
        
        x = back_sub(A,b,sig_figs)
        self.step_recorder.record(A, b, StepType.SOL)
        # end_time = time.perf_counter()
        return x, A
