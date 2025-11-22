from lu_common import pivot_with_scaling, scaling_factors, pivot_no_scaling, lu_solve 
import math

def round_sig(x, sig=8):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def doolittle(A, b, tol=1e-12, scaled=True, sig_figs=8):
    n = len(A)
    o = list(range(n))
    s = scaling_factors(A) if scaled else None

    for k in range(n-1):
        if scaled:
            pivot_with_scaling(A, o, s, k)
            pivot_ratio = round_sig(abs(A[o[k]][k] / s[o[k]]), sig_figs)
        else:
            pivot_no_scaling(A, o, k)
            pivot_ratio = abs(A[o[k]][k])
        if pivot_ratio < tol:
            raise ValueError("Matrix is singular.")
        
        #Elimination
        for i in range(k+1, n):
            factor = round_sig(A[o[i]][k] / A[o[k]][k], sig_figs)
            A[o[i]][k] = factor

            for j in range(k+1, n):
                A[o[i]][j] -= round_sig(factor * A[o[k]][j], sig_figs)
            
    #Last pivot check
    last = A[o[n-1]][n-1]
    pivot_ratio = round_sig(abs(last) / s[o[n-1]], sig_figs) if scaled else round_sig(abs(last), sig_figs)
    if pivot_ratio < tol:
        raise ValueError("Matrix is singular")
        
    x = lu_solve(A, o, b)
    return A, x
