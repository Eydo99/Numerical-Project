from .diagonal_dominance_checker import check_diagonal_dominance
from utils.models import LinearSystem
from utils.auxilary import round_sig
from utils.step_recorder import IterativeStepRecorder
import time

class JacobiSolver :

    def __init__(self, system: LinearSystem, single_step : bool = False):
        self.system = system
        self.recorder = IterativeStepRecorder(single_step)
    
    def solve(self,initial : list,  sig_figs=6, tol=1e-12, max_itrs : int = 50, debug : bool = False) -> tuple[list, list[list], int, bool, bool] :
        A = self.system.A
        b = self.system.b
        n = self.system.n
        helper = initial.copy()
        start1=time.perf_counter()
        DD, newA,newb = check_diagonal_dominance(A,b)
        if DD:
            if debug : print("matrix is diagonally dominant => Jacobi will to converge.")
            A = newA
            b=newb
        else:
            if debug : print("matrix is not diagonally dominant => Jacobi may not converge.")


        X= [ "X"+str(i+1) for i in range(n) ]


        start2=time.perf_counter()


        if debug :
            print("\n Jacobi start \n")
            print("Initial Matrix A:")
            for row in A:
                print(row)
            print("\nVector B:", b)
            print("\nInitial Guess:", initial)
            print("\n---------------------------------------------\n")

        i = 0
        for i in range(max_itrs):
            if debug : print("Iteration no. ",i+1,"\n")

            for row in range(len(A)):
                computation=0
                for col in range (len(A[row])):
                    if row == col:
                        continue
                    else:
                        computation-=A[row][col]*initial[col]
                helper[row]=(b[row]+computation)*(1/A[row][row])
            print(type(A))    
        
            helper = [float(f"{val:.{sig_figs}g}") for val in helper]

            errors = []
            for j in range(n):
                if helper[j] != 0:
                    Ea=abs((helper[j]-initial[j])/helper[j])*100
                else:
                    Ea = 0
                errors.append(round_sig(Ea, sig_figs))

            if debug :
                for j in range(n):    
                    print(X[j]+"="+str(helper[j])+"   (error = "+str(errors[j])+"%)")
                    print()


            stop = True
            for e in errors:
                if e >= tol:
                    stop = False
                    break
                   
            if stop and (i+1)!=max_itrs:
                if debug : print("stopping early because all relative errors < margin\n")
                break
                    
            
            initial=helper.copy()
            self.recorder.record(initial,True)

        success = i < max_itrs
        if debug : print("Jacobi End")

        end =time.perf_counter()

        if debug : 
            print("execution time without diagoanlly dominant check:",round((end-start2)*1_000_000,3)," microsecond")
            print("execution time with diagoanlly dominant check:",round((end-start1)*1_000_000,3)," microsecond")
        return initial, i, newA, DD, success





