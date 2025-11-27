import math

from utils.models import LinearSystem
from utils.auxilary import round_sig
from utils.step_recorder import LUStepRecorder
from exceptions.singular import SingularMatrixException
from exceptions.asymmetric import AsymmetricMatrixException
from exceptions.positive_indefinite import PositiveIndefiniteException


class CholeskySolver:
    #Constructor to initizalize A,b
    def __init__(self,system : LinearSystem, single_step : bool = False):
        self.system=system
        self.recorder = LUStepRecorder(single_step)


    def solve(self, sig_figs = 8, tol = 1e-9) -> list[float]:
        
        A=self.system.A
        n=self.system.n
        b=self.system.b
        l,lt=self.decompose(sig_figs)
        x=self.solve_helper(l,list(range(n)),b,sig_figs, tol)
        return x

    # this was lu_solve_cholesky
    # No changes happened

    @staticmethod
    def solve_helper(A, o, b, sig_figs= 8, tol = 1e-9):

        n = len(A)
        y = [0] * n
        x = [0] * n

        # Forward Subst --> solving Ly=b
        #Algorithm using Formula: y_i = ( b_i - sum_{k=0}^{i-1} L[i][k] * y_k ) / L[i][i]
        if A[o[0]][0] < tol :
            raise SingularMatrixException()
        
        y[o[0]] = round_sig(b[o[0]] / A[o[0]][0], sig_figs)
        for i in range(1, n):
            s = b[o[i]]
            for j in range(i):
                s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
            
            if A[o[i]][i] < tol :
                raise SingularMatrixException()
            y[o[i]] = round_sig(s / A[o[i]][i], sig_figs)

        # Backward Subst --> solving Ux=y
        #Algorithm using Formula: x_i = ( y_i - sum_{k=i+1}^{n-1} L[k][i] * x_k ) / L[i][i]

        x[n - 1] = round_sig(y[o[n - 1]] / A[o[n - 1]][n - 1], sig_figs)
        for i in range(n - 2, -1, -1):
            s = 0
            for j in range(i + 1, n):
                s += round_sig(A[o[j]][i] * x[j], sig_figs)
            x[i] = round_sig((y[o[i]] - s) / A[o[i]][i], sig_figs)
        return x


    #Method to decompose A to l,lt
    def decompose(self, sig_figs= 8):
        A=self.system.A
        n=self.system.n

        #initialize empty l
        l=[[0 for j in range(n)] for i in range(n)]

        #Check for symmetric
        symmetric = self.symmetryChecker(A)
        if not symmetric:
            raise AsymmetricMatrixException()

        """
        Main Algorithm using formula:
        l_ii = sqrt( a_ii - sum_{k=0}^{i-1} l_ik^2 )
        l_ij = ( a_ij - sum_{k=0}^{j-1} l_ik * l_jk ) / l_jj , for i > j
        """
        for i in range(n):
            for j in range(n):
                if(i==j):
                    total=0
                    for k in range(i):
                        total+=round_sig(round_sig(l[i][k]*l[i][k],sig_figs),sig_figs)
                    temp=round_sig(A[i][j]-total,sig_figs)

                    #Check if Matrix is PD
                    if temp>0:
                        l[i][j]=round_sig(round_sig(math.sqrt(temp),sig_figs),sig_figs)
                    else:raise PositiveIndefiniteException()
                elif i>j:
                    total=0
                    for k in range(j):
                        total+=round_sig(l[i][k]*l[j][k],sig_figs)
                    temp1=round_sig(A[i][j]-total,sig_figs)
                    temp2=round_sig(1/l[j][j],sig_figs)
                    l[i][j]=round_sig(temp1*temp2,sig_figs)
                else:continue

        lt=self.transpose(l)

        return l,lt


    def symmetryChecker(self,A):
        n=self.system.n
        for i in range(n):
            for j in range(n):
                if i==j:
                    continue
                if A[i][j]!=A[j][i]:
                    return False

        return True


    def transpose(self,A):
        n=self.system.n
        At = [[0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                At[i][j]=A[j][i]
        return At