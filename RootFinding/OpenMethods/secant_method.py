import math

from sympy import *

from RootFinding.Exceptions.zero_division import ZeroDivision
from RootFinding.utils.auxilary import get_lambda_func, round_sig
from RootFinding.utils.models import SecantStep
from RootFinding.utils.step_recorder import openMethodStepRecorder

from .checks import convergence_status, ConvStatus


class SecantSolver:
    def __init__(self, func_lambda, single_step: bool):
        self.func = func_lambda
        self.recorder = openMethodStepRecorder(single_step)

    def solve(
        self, first: float, second: float, max_itrs: int, tol: float, sig_figs: int
    ) -> tuple[float, int, int, float | None, int]:
        errors = []
        err = None
        thirdUnrounded = second
        secondUnrounded = second
        for i in range(max_itrs):
            if abs(round_sig(self.func(second) - self.func(first), sig_figs)) == 0:
                raise ZeroDivision(
                    "division by zero encountered at itr "
                    + str(i + 1)
                    + " f(xi) - f(xi-1) = 0"
                )

            diff = round_sig(
                self.func(second)
                * round_sig(
                    (second - first)
                    / round_sig(self.func(second) - self.func(first), sig_figs),
                    sig_figs,
                ),
                sig_figs,
            )

            thirdUnrounded = second - diff
            third = round_sig(thirdUnrounded, sig_figs)
            
            if math.isnan(third) or math.isinf(third) :
                return second, i + 1, ConvStatus.DIVERGENT, err, 0

            errors.append(abs(diff))

            self.recorder.record(
                SecantStep(first, second, third, round_sig(self.func(third), sig_figs))
            )

            err = abs((thirdUnrounded - secondUnrounded) / max(1, abs(thirdUnrounded)))

            if err < tol or abs(self.func(third)) < tol:
                if(i == 0):
                    err = None
                break
            first = second
            second = third
            secondUnrounded = thirdUnrounded

        rel_err = abs((thirdUnrounded - secondUnrounded)/thirdUnrounded) * 100    
        if(rel_err == 0 or  rel_err is None ):
             corr_sig_figs = sig_figs
        elif(rel_err) :
             corr_sig_figs = math.floor(2-math.log(rel_err/0.5, 10))  

        status = convergence_status(
            error_history=errors, iterations=i + 1, max_iterations=max_itrs
        )

        return third, i + 1, status, err, corr_sig_figs
