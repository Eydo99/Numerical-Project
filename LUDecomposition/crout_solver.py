from GaussElimination import linear_system
from GaussElimination.back_substitution import round_sig
from lu_common import lu_solve


class crout_solver:

    #Constuctor for initializing system(A,B) and no of signifacant figures
    def __init__(self,system:linear_system,noOfSig):
        self.system = system
        self.noOfSig = noOfSig



    def decompose(self):
        A = self.system.A
        n = self.system.n
        noOfSig =self.noOfSig
        l=[[0 for j in range(n)] for i in range(n)]
        u=[[0 for j in range(n)] for i in range(n)]
        for i in range(n):
            u[i][i] = 1
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
                u[j][k]=round_sig(temp/l[j][j],noOfSig)
        return l,u

    def merge(self):
        l,u=self.decompose()
        n=self.system.n
        merged=u
        for i in range(n):
            for j in range(n):
                if(i>=j):
                    merged[i][j]=l[i][j]
        return merged


    def solve(self):
         merged=self.merge()
         b=self.system.b
         n=self.system.n
         x=lu_solve(merged,list(range(n)),b)
         return x








