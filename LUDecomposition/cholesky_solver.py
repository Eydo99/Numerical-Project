import math

from GaussElimination.gauss_solver import round_sig


class cholesky_solver:
    def __init__(self,system,sig_figs=8):
        self.system=system
        self.sig_figs=sig_figs


    def decmpose(self):
        A=self.system.A
        sig_figs=self.system.sig_figs
        n=self.system.n
        symmetric= self.symmetryChecker(A)
        l=[[0 for j in range(n)] for i in range(n)]

        if(symmetric==0):
            return -1,-1

        for i in range(n):
            for j in range(n):
                if(i==j):
                    total=0
                    for k in range(i):
                        total+=round_sig(round_sig(l[i][k]*l[i][k],sig_figs),sig_figs)
                    temp=round_sig(A[i][j]-total,sig_figs)
                    if(temp>0):
                        l[i][j]=temp
                    else:return 0,0
                elif(i>j):
                    total=0
                    for k in range(j):
                        total+=round_sig(l[i][k]*l[j][k],sig_figs)
                    temp1=round_sig(A[i][j]-total,sig_figs)
                    temp2=round_sig(1/l[j][j],sig_figs)
                    l[i][j]=round_sig(temp1*temp2,sig_figs)
                else:continue
        lT=self.transpose(l)

        return l,lT


    def symmetryChecker(self,A):
        n=self.system.n
        for i in range(n):
            for j in range(n):
                if(i==j):
                    continue
                if(A[i][i]!=A[j][i]):
                    return False

        return True

    def transpose(self,A):
        n=self.system.n
        for i in range(n):
            for j in range(n):
                A[i][j]=A[j][i]
        return A