import math
from utils.auxilary import round_sig


def lu_solve_crout(A, o, b, sig_figs=8):
    n = len(A)
    y = [0] * n
    x = [0] * n

    # Forward Subst --> solving Ly=b
    #Algorithm using Formula: y_i = b_i - sum_{j=0}^{i-1} L[i][j] * y_j
    y[o[0]] = b[o[0]] / A[o[0]][0]
    for i in range(1, n):
        s = b[o[i]]
        for j in range(i):
            s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
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





