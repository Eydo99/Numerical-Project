from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.models import fixedPointStep
from RootFinding.utils.step_recorder import openMethodStepRecorder


class fixedPointSolver:

    #initialize f(x),g(x) and step recorder
    def __init__(self,func_lambda,gx_lambda,single_step:bool):
        self.func=func_lambda
        self.recorder=openMethodStepRecorder(single_step)
        self.gx=gx_lambda

    def solve(self, oldGuess : float, max_itrs : int, tol : float, sig_figs : int) ->tuple[float,int]:
        # rounding the x0 and making ea=infinity at first
        oldGuess = round_sig(oldGuess, sig_figs)
        absoluteDiff=float('inf')

        for i in range(max_itrs):
            #x(i+1)=g(xi)
            newGuess=round_sig(self.gx(oldGuess),sig_figs)

            #record current loop
            print(newGuess)
            self.recorder.record(fixedPointStep(oldGuess,newGuess,round_sig(self.func(newGuess), sig_figs)))

            # ea cannot be determined in first loop
            if i!=0:
                absoluteDiff=round_sig(abs(newGuess-oldGuess),sig_figs)

            # if ea<es break
            if absoluteDiff<tol:
                break

            oldGuess=newGuess

        # return the approximate root and no. of iterations
        return newGuess, i+1
