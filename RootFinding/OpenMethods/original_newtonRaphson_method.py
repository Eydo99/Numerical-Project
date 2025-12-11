from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.step_recorder import openMethodStepRecorder
from RootFinding.utils.models import originalNewtonStep

class originalNewtonSolver:

    def __init__(self,func_lambda,diff_lambda,single_step:bool):
        self.func=func_lambda
        self.dydyx=diff_lambda
        self.recorder=openMethodStepRecorder(single_step)

    def solve(self, oldGuess: float, max_iter: int, tol: float, sig_figs: int)-> tuple[float, int] :

        for i in range(max_iter):
            oldGuess = round_sig(oldGuess,sig_figs)
            f_x = self.func(oldGuess)
            dydx = self.dydyx(oldGuess)
            newGuess =round_sig(oldGuess-(round_sig(f_x/dydx,sig_figs)),sig_figs)
            newGuess = round_sig(newGuess,sig_figs)
            diff=round_sig((round_sig(newGuess-oldGuess,sig_figs))/newGuess,sig_figs)

            self.recorder.record(originalNewtonStep(oldGuess,newGuess,self.func(newGuess)))

            if abs(diff) < tol:
                break

            oldGuess=newGuess

        return newGuess, i+1