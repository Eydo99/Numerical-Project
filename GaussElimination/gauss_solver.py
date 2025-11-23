from .step_recorder import StepRecorder
from .linear_system import LinearSystem
from .pivot_manager import pivot_manager
from .back_substitution import back_substitution
import time
import math

def round_sig(x, sig=6):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)



class GaussSolver:
    def __init__(self, system:LinearSystem, single_step=False, sig_figs=6, tol=1e-12):
        self.system = system
        self.step_recorder = StepRecorder(single_step)
        self.sig_figs = sig_figs
        self.tol = tol

    def solve(self):
        A, b, n = self.system.A , self.system.b, self.system.n

        start_time = time.perf_counter()
        for col in range(n):
            A, b, er = pivot_manager.pivot(A, b, col, tol=self.tol)
            if er == -1:
                return None, self.step_recorder.steps, time.perf_counter() - start_time, "singular"
            self.step_recorder.record(A, b, f"Pivoted on column {col}")

            for row in range(col+1, n):
                factor = round_sig(A[row][col] / A[col][col],self.sig_figs)
                for i in range(col+1, n):
                    A[row][i] -= round_sig(factor * A[col][i], self.sig_figs)
                A[row][col] = 0
                b[row] -= round_sig(factor*b[col], self.sig_figs)
                self.step_recorder.record(A, b, f"Eliminate row {row} using row {col}")
        
        x = back_substitution.solve(A,b,self.sig_figs)
        self.step_recorder.record(A, b, f"Solution: {x}")
        end_time = time.perf_counter()
        return x, self.step_recorder.steps, end_time-start_time, ""
