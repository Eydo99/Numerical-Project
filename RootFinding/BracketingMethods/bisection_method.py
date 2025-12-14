
from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.models import bisectionStep
from RootFinding.utils.step_recorder import openMethodStepRecorder
import math

class bisectionSolver :

    #initialize function and recorder
    def __init__(self,func_lambda,single_step:bool):
        self.func = func_lambda
        self.recorder=openMethodStepRecorder(single_step)

    def solve(self, xl : float, xu :float, max_itrs : int, tol : float, sig_figs : int) -> tuple[float, int, float, int] | None :

            #if f(xl)*f(xu)>0 -> no root exists in this interval
            if self.func(xl)*self.func(xu) > 0:
                return None
                
            #round xl,xr,initialize ea=infinity
            absoluteDiff=float('inf')
            temp=None
            xl = round_sig(xl, sig_figs)
            xu = round_sig(xu, sig_figs)
            old = round_sig((xl+xu)/2,sig_figs)
            xr = 0
            i = 0

            for i in range(max_itrs):

                #xr=(xl+xu)/2
                xr= round_sig((xl+xu)/2,sig_figs)
                f_xr=round_sig(self.func(xr),sig_figs)

                #record current loop
                self.recorder.record(bisectionStep(xl,xu,xr,f_xr))

                #ea cannot be determined in first loop
                if i!=0:
                    absoluteDiff = round_sig(abs(xr - temp),sig_figs)

                temp = xr

                #f(xl)*f(xr)<0 -> xu=xr , f(xl)*f(xr)>0 -> xl=xr , f(xl)*f(xr)=0 -> xr is the root so ea=0
                if f_xr*self.func(xl)<0: xu=xr
                elif f_xr*self.func(xl)>0: xl=xr
                else: absoluteDiff=0
                
                

                #if ea<es:break
                if absoluteDiff<tol:
                    break
                    
                old = xr    
                
            rel_err = abs((xr - old)/xr) * 100
            if(rel_err == 0):
                corr_sig_figs = 6
            else :
                corr_sig_figs = math.floor(2-math.log(rel_err/0.5, 10)) 
            #             
            # return the approximate root and no. of iterations
            return xr, i+1 , rel_err,corr_sig_figs

