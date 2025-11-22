import math

def round_sig(x, sig=8):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def scaling_factors(A):
    n = len(A)
    s=[0]*n
    for i in range(n):
        s[i] = max(abs(val) for val in A[i])
    return s


def pivot_with_scaling(A, o, s, k, sig_figs=8):
    n=len(A)
    p = k
    big = round_sig(abs(A[o[k]][k] / s[o[k]]), sig_figs)

    for i in range(k+1, n):
        dummy = round_sig(abs(A[o[i]][k] /s[o[i]]), sig_figs)
        if dummy > big:
            big = dummy
            p = i
    
    o[k], o[p] = o[p], o[k]

def pivot_no_scaling(A, o, k, sig_figs=8):
    n = len(A)
    p = k
    big = abs(A[o[k]][k])

    for i in range(k+1, n):
        dummy = abs(A[o[i]][k])
        if dummy > big:
            big = dummy
            p = i
    
    o[k], o[p] = o[p], o[k]


def lu_solve(A, o, b, sig_figs=8,type="crout"):
    n = len(A)
    y = [0]*n
    x = [0]*n

    if type == "doolittle":
        # Forward Subst --> solving Ly=b
        y[o[0]] = b[o[0]]
        for i in range(1, n):
            s = b[o[i]]
            for j in range(i):
                s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
            y[o[i]] = s

        # Backward Subst --> solving Ux=y
        x[n-1] = round_sig(y[o[n-1]] / A[o[n-1]][n-1], sig_figs)
        for i in range(n-2, -1, -1):
            s=0
            for j in range(i+1, n):
                s += round_sig(A[o[i]][j] * x[j], sig_figs)
            x[i] = round_sig((y[o[i]] - s) / A[o[i]][i], sig_figs)

    if type == "crout":
        # Forward Subst --> solving Ly=b
        y[o[0]] = b[o[0]] / A[o[0]][0]
        for i in range(1, n):
            s = b[o[i]]
            for j in range(i):
                s -= round_sig(A[o[i]][j] * y[o[j]], sig_figs)
            y[o[i]] = round_sig(s / A[o[i]][i], sig_figs)

        # Backward Subst --> solving Ux=y
        x[n - 1] = y[o[n - 1]]
        for i in range(n - 2, -1, -1):
            s = 0
            for j in range(i + 1, n):
                s += round_sig(A[o[i]][j] * x[j], sig_figs)
            x[i] = round_sig(y[o[i]] - s, sig_figs)

    return x





