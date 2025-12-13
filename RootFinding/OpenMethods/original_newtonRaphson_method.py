from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.step_recorder import openMethodStepRecorder
from RootFinding.utils.models import originalNewtonStep
from RootFinding.Exceptions.zero_division import ZeroDivision
class originalNewtonSolver:

    #initialize f(x),f'(x),and step recorder
    def __init__(self,func_lambda,diff_lambda,single_step:bool):
        self.func=func_lambda
        self.dydyx=diff_lambda
        self.recorder=openMethodStepRecorder(single_step)

    def solve(self, oldGuess: float, max_iter: int, tol: float, sig_figs: int)-> tuple[float, int] :
        #rounding the x0 and making ea=infinity at first
        oldGuess = round_sig(oldGuess, sig_figs)
        absoluteDiff=float('inf')

        for i in range(max_iter):
            #calculate f(x) and f'(x)
            f_x = round_sig(self.func(oldGuess), sig_figs)
            dydx = round_sig(self.dydyx(oldGuess), sig_figs)
            if dydx == 0:
                raise ZeroDivision(f"Error: Division by zero (f'(x)=0) at iteration {i+1}")
            # x(i+1)=x(i)-f(xi)/f'(xi)
            newGuess =round_sig(oldGuess-(round_sig(f_x/dydx,sig_figs)),sig_figs)

            #ea cannot be determined in first loop
            if i!=0:
                absoluteDiff=round_sig(abs(newGuess-oldGuess),sig_figs)

            #record the current loop
            self.recorder.record(originalNewtonStep(oldGuess,newGuess,round_sig(self.func(newGuess),sig_figs)))

            #if ea<es break
            if absoluteDiff < tol:
                break

            oldGuess=newGuess

        #return the approximate root and no. of iterations
        return newGuess, i+1


print()        
print(round_sig(122, 2))