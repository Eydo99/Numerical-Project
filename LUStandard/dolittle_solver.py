
from utils.auxilary import scaling_factors, round_sig, pivot_lu
from utils.models import LinearSystem
from utils.step_recorder import LUStepRecorder
from utils.models import StepType


class DolittleSolver :
        #Constructor to initizalize A,b
    def __init__(self,system : LinearSystem, single_step : bool = False):
        self.system=system
        self.recorder = LUStepRecorder(single_step)

    def solve(self, sig_figs=8,tol=1e-12, scaled=True) -> tuple[list, list[list]]:
        A = self.system.A
        n = self.system.n
        o = list(range(n))
        s = scaling_factors(A) if scaled else [1]*n

        for k in range(n-1):

            pivot_lu(A, k, o, scaled, s, sig_figs)
            pivot_ratio = round_sig(abs(A[o[k]][k] / s[o[k]]), sig_figs)
            self.recorder.record_dolittle(A,o,StepType.SWAP)

            if pivot_ratio < tol:
                raise ValueError("Matrix is singular.")
            
            #Elimination
            for i in range(k+1, n):
                factor = round_sig(A[o[i]][k] / A[o[k]][k], sig_figs)
                A[o[i]][k] = factor

                for j in range(k+1, n):
                    A[o[i]][j] -= round_sig(factor * A[o[k]][j], sig_figs)
                
                self.recorder.record_dolittle(A,o,StepType.ELIM)
                
        #Last pivot check
        last = A[o[n-1]][n-1]
        pivot_ratio = round_sig(abs(last) / s[o[n-1]], sig_figs)
        if pivot_ratio < tol:
            raise ValueError("Matrix is singular")
        
        self.recorder.record_dolittle(A, o, StepType.SOL)
                
        x = self.solve_helper(A, o, self.system.b, sig_figs)

        return x, A
    

    def solve_helper(A, o, b, sig_figs=8):
        n = len(A)
        y = [0]*n
        x = [0]*n

        # Forward Subst --> solving Ly=b
        y[o[0]] = b[o[0]]
        for i in range(1, n):
            s = b[o[i]]
            for j in range(i):
                s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
            y[o[i]] = s

        # Backward Subst --> solving Ux=y
        x[n-1] = round_sig(y[o[n-1]] / A[o[n-1]][n-1], sig_figs)
        for i in range(n-2, -1, -1):
            s=0
            for j in range(i+1, n):
                s += round_sig(A[o[i]][j] * x[j], sig_figs)
            x[i] = round_sig((y[o[i]] - s) / A[o[i]][i], sig_figs)

        return x
