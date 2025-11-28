import time

from utils.models import LinearSystem
from utils.auxilary import round_sig
from utils.step_recorder import LUStepRecorder
from exceptions.singular import SingularMatrixException

class CroutSolver:

    #Constuctor for initializing system(A,B) and no of signifacant figures
    def __init__(self,system: LinearSystem, single_step : bool = False):
        self.system = system
        self.recorder = LUStepRecorder(single_step)


    #Method to get x
    def solve(self, sig_figs=8, tol = 1e-9):

        start_time=time.perf_counter()
        merged=self.merge()
        b=self.system.b
        n=self.system.n
        noOfSig=sig_figs
        x= self.solve_helper(merged,list(range(n)),b,noOfSig, tol)
        exec_time=time.perf_counter()-start_time
        return x, exec_time


    @staticmethod
    def solve_helper(A, o, b, sig_figs=8, tol = 1e-6):

            n = len(A)
            y = [0] * n
            x = [0] * n

            # Forward Subst --> solving Ly=b
            #Algorithm using Formula: y_i = b_i - sum_{j=0}^{i-1} L[i][j] * y_j
            if abs(A[o[0]][0]) < tol :
                raise SingularMatrixException()
            y[o[0]] = b[o[0]] / A[o[0]][0]
            
            for i in range(1, n):
                s = b[o[i]]
                for j in range(i):
                    s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
                if abs(A[o[i]][i]) < tol :
                    raise SingularMatrixException()
                y[o[i]] = round_sig(s / A[o[i]][i], sig_figs)

            # Backward Subst --> solving Ux=y
            #Algorithm using Formula:  x_i = ( y_i - sum_{j=i+1}^{n-1} U[i][j] * x_j ) / U[i][i]
            x[n - 1] = y[o[n - 1]]
            for i in range(n - 2, -1, -1):
                s = 0
                for j in range(i + 1, n):
                    s += round_sig(A[o[i]][j] * x[j], sig_figs)
                x[i] = round_sig(y[o[i]] - s, sig_figs)
            return x

        #decompose A into L and U
    def decompose(self, sig_figs = 6, tol = 1e-6):

            A = self.system.A
            n = self.system.n
            noOfSig = sig_figs

            #Initialize l and u
            l=[[0 for j in range(n)] for i in range(n)]
            u=[[0 for j in range(n)] for i in range(n)]

            #make diagonal of u=1
            for i in range(n):
                u[i][i] = 1

            """
            main Algorithm using Formula:
            Compute L (i >= j)
            L_ij = A_ij - sum_{k=0}^{j-1} L_ik * U_kj

            Compute U (i < j)
            U_ij = ( A_ij - sum_{k=0}^{i-1} L_ik * U_kj ) / L_ii
            """
            for j in range(n):
                for i in range(j,n):
                    total=0
                    for v in range(j):
                        total+=round_sig(l[i][v]*u[v][j],noOfSig)
                    l[i][j]=round_sig(A[i][j]-total,noOfSig)
                for k in range(j+1,n):
                    total=0
                    for v in range(j):
                        total+=round_sig(l[j][v]*u[v][k],noOfSig)
                    temp=round_sig(A[j][k]-total,noOfSig)
                    if abs(l[j][j]) < tol : 
                        raise SingularMatrixException()
                    u[j][k]=round_sig(temp/l[j][j],noOfSig)
            return l,u


    #Method for merging l and u
    def merge(self):
        l,u=self.decompose()
        n=self.system.n
        merged=u
        for i in range(n):
            for j in range(n):
                if(i>=j):
                    merged[i][j]=l[i][j]
        return merged










