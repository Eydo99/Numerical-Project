from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.models import fixedPointStep
from RootFinding.utils.step_recorder import openMethodStepRecorder
from .checks import convergence_status, ConvStatus
import math

class fixedPointSolver:

    #initialize f(x),g(x) and step recorder
    def __init__(self,func_lambda,gx_lambda,single_step:bool):
        self.func=func_lambda
        self.recorder=openMethodStepRecorder(single_step)
        self.gx=gx_lambda

    def solve(self, oldGuess : float, max_itrs : int, tol : float, sig_figs : int) ->tuple[float,int, int, float | None, int]:
        # rounding the x0 and making ea=infinity at first
        oldGuessUnrounded = oldGuess
        oldGuess = round_sig(oldGuessUnrounded, sig_figs)
        absoluteDiff=float('inf')
        errors = []
        newGuess = 0
        i = 0
        err = None
        
        for i in range(max_itrs):
            #x(i+1)=g(xi)
            newGuessUnrounded = self.gx(oldGuess)
            newGuess=round_sig(newGuessUnrounded,sig_figs)

            #record current loop
            
            
            
            self.recorder.record(fixedPointStep(oldGuess,newGuess,round_sig(self.func(newGuess), sig_figs)))
            
            if math.isnan(newGuess) or math.isinf(newGuess) or newGuess > 9e15 :
                return oldGuess, i + 1, ConvStatus.DIVERGENT, err, 0

            # ea cannot be determined in first loop
            if i!=0:
                absoluteDiff=round_sig(abs(newGuess-oldGuess),sig_figs)

            
            # if ea<es break
            
            err = abs(newGuessUnrounded - oldGuessUnrounded)/max(1, abs(newGuessUnrounded))*100

            if err < tol or abs(self.func(newGuess)) < tol:
                if(i == 0) :
                    err = None
                break
            
            errors.append(absoluteDiff)
            oldGuess=newGuess
            oldGuessUnrounded = newGuessUnrounded

        # print(oldGuessUnrounded)
        # print(newGuessUnrounded)
        # rel_err = abs((newGuessUnrounded - oldGuessUnrounded)/newGuessUnrounded) * 100
        
        if(err == 0 or err is None):
            corr_sig_figs = sig_figs
        elif(err) :
            corr_sig_figs = math.floor(2-math.log(err/0.5, 10)) 
        status = convergence_status(error_history=errors,iterations=i + 1,max_iterations=max_itrs)  
        
    
    
        # return the approximate root and no. of iterations
        return newGuess, i+1, status, err, corr_sig_figs
