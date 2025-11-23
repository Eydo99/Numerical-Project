from LUDecomposition.cholesky_solver import cholesky_solver
from GaussElimination.linear_system import LinearSystem

A=[[4,12,-16],
   [12,37,-43],
   [-16,-43,98]]
b=[-20,-43,192]
sigFigures=8
mysystem=LinearSystem(A,b)

solver=cholesky_solver(mysystem,sigFigures)
l,u=solver.decmpose()
if(l==0 and u==0):
    print("Matrix isn't PD")
    exit()
if(l==-1 and u==-1):
    print("Matrix isn't symmetric")
    exit()
print(l,u)
