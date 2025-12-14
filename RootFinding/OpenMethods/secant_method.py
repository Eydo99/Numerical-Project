from sympy import *
from RootFinding.utils.step_recorder import openMethodStepRecorder
from RootFinding.utils.models import SecantStep
from RootFinding.utils.auxilary import round_sig, get_lambda_func
from RootFinding.Exceptions.zero_division import ZeroDivision
import math




class SecantSolver :
    
    def __init__ (self, func_lambda, single_step : bool) :
        self.func = func_lambda   
        self.recorder =openMethodStepRecorder(single_step)
    

    def solve(self,
              first : float, second : float,  
              max_itrs : int, tol : float, sig_figs : int) -> tuple[float, int] :
        
        for i in range(max_itrs) :
            if(abs(round_sig(self.func(second) - self.func(first), sig_figs)) == 0):
                raise ZeroDivision("division by zero encountered at itr " + str(i + 1) + " f(xi) - f(xi-1) = 0")

            diff = round_sig(
                self.func(second) * round_sig(
                    (second - first) / round_sig(
                        self.func(second) - self.func(first)
                        , sig_figs)
                    , sig_figs)
                , sig_figs)
            third = round_sig(second - diff, sig_figs)

            self.recorder.record(SecantStep(first, second, third, round_sig(self.func(third), sig_figs)))

            if(abs(diff) < tol) :
                break
            first = second
            second = third
        
        return third, i + 1

