from LUDecomposition.crout_solver import crout_solver
from GaussElimination.linear_system import LinearSystem

A=[[2,-1,1],
   [4,5,6],
   [-2,3,8]]
b=[1,2,3]
sigFigures=6
mysystem=LinearSystem(A,b)

solver=crout_solver(mysystem,sigFigures)
l,u=solver.decompose()
merge=solver.merge()
x=solver.solve()
print("l=",l)
print("u=",u)
print("merge=",merge)
print("x=",x)