from RootFinding.utils.auxilary import round_sig
from RootFinding.utils.models import bisectionStep
from RootFinding.utils.step_recorder import openMethodStepRecorder


class falsePositionSolver:

    def __init__(self, func_lambda, single_step: bool):
        self.func = func_lambda
        self.recorder = openMethodStepRecorder(single_step)

    def solve(
        self,
        xl: float,
        xu: float,
        max_itrs: int,
        tol: float,
        sig_figs: int
    ) -> tuple[float, int] :

        absoluteDiff = float('inf')
        temp = 0
        xl = round_sig(xl, sig_figs)
        xu = round_sig(xu, sig_figs)
        xr = 0
        i = 0
        
        for i in range(max_itrs):
            
            f_xl = round_sig(self.func(xl), sig_figs)
            f_xu = round_sig(self.func(xu), sig_figs)

            # zero division
            denominator = round_sig(f_xl - f_xu, sig_figs)
            if denominator == 0:
                print(f"Error: Division by zero (f(xl)=f(xu)) at iteration {i}. Stopping.")
                return xl, i

            numerator = round_sig(f_xu * (xl - xu), sig_figs)
            xr = round_sig(xu - (numerator / denominator), sig_figs)
            f_xr = round_sig(self.func(xr), sig_figs)

            # current step
            self.recorder.record(bisectionStep(xl, xu, xr, f_xr))

            
            if i != 0:
                absoluteDiff = round_sig(abs(xr - temp), sig_figs)
            temp = xr

            
            if f_xr * f_xl < 0:
                xu = xr
            elif f_xr * f_xl > 0:
                xl = xr
            else:
                absoluteDiff = 0

            # stopping condition
            if absoluteDiff < tol:
                break

        
        return xr, i + 1






    # @staticmethod
    # def test():

    #     f = lambda x: x**3 - 4*x - 10  # Root between 2 and 3

    #     solver = falsePositionSolver(f, single_step=False)
    #     root, iterations = solver.solve(2, 3, 100, 1e-6, 6)

    #     print(f"Test:, root={root}, iterations={iterations}")
        