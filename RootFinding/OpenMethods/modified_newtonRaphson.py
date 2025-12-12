from RootFinding.Exceptions.ZeroDivsion import ZeroDivision
from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.step_recorder import openMethodStepRecorder
from RootFinding.utils.models import modifiedNewtonStep
from typing import Tuple, Optional


class modifiedNewtonSolver:
    
    
    def __init__(self, func_lambda, diff_lambda, d2ydx2_lambda, single_step: bool):
     
        
        self.func = func_lambda
        self.dydx = diff_lambda
        self.d2ydx2 = d2ydx2_lambda
        self.recorder = openMethodStepRecorder(single_step)

    def solve(
        self,
        oldGuess: float,
        max_iter: int,
        tol: float,
        sig_figs: int,
        multiplicity: Optional[float] = None
    ) -> Tuple[float, int]:
       
        
        oldGuess = round_sig(oldGuess, sig_figs)
        newGuess = oldGuess  
        absoluteDiff = float('inf')
        i = 0  

        for i in range(max_iter):
            #  f(x) , f'(x)
            f_x = round_sig(self.func(oldGuess), sig_figs)
            dydx = round_sig(self.dydx(oldGuess), sig_figs)


            if multiplicity is not None:
                #Modified 1
                if dydx == 0:
                    raise ZeroDivision(f"Error: Division by zero (f'(x)=0) at iteration {i}")
                term = round_sig(f_x / dydx, sig_figs)
                newGuess = round_sig(oldGuess - (multiplicity * term), sig_figs)

            else:
               # Modified 2
                d2ydx2 = round_sig(self.d2ydx2(oldGuess), sig_figs)
                
                numerator = round_sig(f_x * dydx, sig_figs)
                denominator = round_sig((dydx ** 2) - (f_x * d2ydx2), sig_figs)

                # zero division
                if denominator == 0:
                    raise ZeroDivision(f"Error: Division by zero in denominator at iteration {i}. Stopping.")
                    return oldGuess, i

                term = round_sig(numerator / denominator, sig_figs)
                newGuess = round_sig(oldGuess - term, sig_figs)

            # ea
            if i != 0:
                absoluteDiff = round_sig(abs(newGuess - oldGuess), sig_figs)

            # step recorder
            f_newGuess = round_sig(self.func(newGuess), sig_figs)
            self.recorder.record(modifiedNewtonStep(oldGuess, newGuess, f_newGuess , absoluteDiff))
            
            
            #print(modifiedNewtonStep(oldGuess, newGuess, f_newGuess , absoluteDiff))
            
            # stopping conditions 
            if absoluteDiff < tol or f_newGuess == 0:
                break

            oldGuess = newGuess

        return newGuess, i + 1
        
    # @staticmethod
    # def test():
        
    #     f = lambda x: 3*x**2+5*x-10
    #     df = lambda x: 6*x+5
    #     d2f = lambda x: 6
            
    #     solver = modifiedNewtonSolver(f, df, d2f, single_step=False)
    #     root, iterations = solver.solve(1, 100, 1e-6, 6  )
            
    #     print(f"Test:, root={root}, iterations={iterations}")
                      