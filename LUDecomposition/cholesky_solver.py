import math
import time

from GaussElimination.gauss_solver import round_sig
from LUDecomposition.lu_common import lu_solve_cholesky


class cholesky_solver:
    #Constructor to initizalize A,b
    def __init__(self,system,sig_figs=8):
        self.system=system
        self.sig_figs=sig_figs


    #Method to decompose A to l,lt
    def decompose(self):
        A=self.system.A
        sig_figs=self.sig_figs
        n=self.system.n

        #initialize empty l
        l=[[0 for j in range(n)] for i in range(n)]

        #Check for symmetric
        symmetric = self.symmetryChecker(A)
        if not symmetric:
            return -1,-1

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
                    else:return 0,0
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


    def solve(self):
        start_time=time.perf_counter()
        A=self.system.A
        n=self.system.n
        sig_figs=self.sig_figs
        b=self.system.b
        l,lt=self.decompose()
        x=lu_solve_cholesky(l,list(range(n)),b,sig_figs)
        exec_time=time.perf_counter()-start_time
        return x , exec_time


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