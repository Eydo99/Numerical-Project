from GaussElimination.linear_system import LinearSystem
from LUDecomposition.cholesky_solver import cholesky_solver
from LUDecomposition.crout_solver import crout_solver
from doolittle_solver import doolittle


def print_matrix(M, name):
    print(f"\n{name}:")
    for row in M:
        print(["{:8.4f}".format(x) for x in row])


def extract_LU(A):
    """Given the combined LU matrix A, return L and U separately."""
    n = len(A)
    L = [[0]*n for _ in range(n)]
    U = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i > j:
                L[i][j] = A[i][j]
            elif i == j:
                L[i][j] = 1.0
                U[i][j] = A[i][j]
            else:
                U[i][j] = A[i][j]

    return L, U


def main():
    # Test system
    A=[[4, 12, -16],
    [12, 37, -43],
    [-16, -43, 98]]
    b = [-20, -43, 192]


    print("========= DOOLITTLE WITH SCALED PIVOTING =========")
    
    A_scaled = [row[:] for row in A]  # deep copy
    LUmatrix_scaled, x_scaled = doolittle(A_scaled, b, scaled=True)

    L_scaled, U_scaled = extract_LU(LUmatrix_scaled)

    print_matrix(L_scaled, "L (scaled)")
    print_matrix(U_scaled, "U (scaled)")

    print("\nSolution x (scaled):", x_scaled)

    # ---------------------------------------------------------

    print("\n\n========= DOOLITTLE WITHOUT SCALING (NORMAL PIVOTING) =========")

    A_unscaled = [row[:] for row in A]  # deep copy
    LUmatrix_unscaled, x_unscaled = doolittle(A_unscaled, b, scaled=False)

    L_un, U_un = extract_LU(LUmatrix_unscaled)

    print_matrix(L_un, "L (unscaled)")
    print_matrix(U_un, "U (unscaled)")

    print("\nSolution x (unscaled):", x_unscaled)


    print("\n========================Example on Crout Decomposition==========================")
    system=LinearSystem(A,b)
    croutSolver=crout_solver(system)
    x_crout = croutSolver.solve()
    l,u=croutSolver.decompose()
    merge=croutSolver.merge()
    print(l)
    print(u)
    print(merge)
    print("\nSolution x (Crout):", x_crout)


    print("\n===============================Example on Cholesky Decomposition=============================")

    mysystem=LinearSystem(A,b)

    solver = cholesky_solver(mysystem)
    l,u = solver.decompose()
    if l==0 and u==0:
        print("Matrix ins't PD")
        exit()
    if l==-1 and u==-1:
        print("Matrix ins't symmetric")
        exit()
    x_cholesky,exec_time=solver.solve()
    print("\nSolution x (Cholesky):", x_cholesky,"Execution time:",exec_time*1e6,"us")



if __name__ == "__main__":
    main()



