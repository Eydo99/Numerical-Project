
from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.models import bisectionStep
from RootFinding.utils.step_recorder import openMethodStepRecorder


class bisectionSolver :

    def __init__(self,func_lambda,single_step:bool):
        self.func = func_lambda
        self.recorder=openMethodStepRecorder(single_step)

    def solve(self, xl : float, xu :float, max_itrs : int, tol : float, sig_figs : int) -> tuple[float, int] | None :

            if self.func(xl)*self.func(xu) > 0:
                return None

            diff=0
            temp=None
            for i in range(max_itrs):
                xl=round_sig(xl,sig_figs)
                xu=round_sig(xu,sig_figs)
                xr= round_sig((xl+xu)/2,sig_figs)
                f_xr=round_sig(self.func(xr),sig_figs)
                self.recorder.record(bisectionStep(xl,xu,xr,f_xr))

                if temp is not None:
                    diff = round_sig(round_sig(xr - temp,sig_figs)/xr,sig_figs)

                temp = xr

                if f_xr*self.func(xl)<0: xu=xr
                elif f_xr*self.func(xl)>0: xl=xr
                else: diff=0

                if abs(diff)<tol:
                    break
            return xr, i+1

