def scaling_factors(A):
    n = len(A)
    s=[0]*n
    for i in range(n):
        s[i] = max(abs(val) for val in A[i])
    return s


def pivot_with_scaling(A, o, s, k):
    n=len(A)
    p = k
    big = abs(A[o[k]][k] / s[o[k]])

    for i in range(k+1, n):
        dummy = abs(A[o[i][k]] /s[o[i]])
        if dummy > big:
            big = dummy
            p = i
    
    o[k], o[p] = o[p], o[k]

def pivot_no_scaling(A, o, k):
    n = len(A)
    p = k
    big = abs(A[o[k]][k])

    for i in range(k+1, n):
        dummy = abs(A[o[i]][k])
        if dummy > big:
            big = dummy
            p = i
    
    o[k], o[p] = o[p], o[k]


def lu_solve(A, o, b):
    n = len(A)
    y = [0]*n
    x = [0]*n

    # Forward Subst --> solving Ly=b
    y[o[0]] = b[o[0]]
    for i in range (1, n):
        s = b[o[i]]
        for j in range(i):
            s -= A[o[i]][j] * y[o[j]]
        y[o[i]] = s
    
    # Backward Subst --> solving Ux=y
    x[n-1] = y[o[n-1]] / A[o[n-1]][n-1]
    for i in range(n-2, -1, -1):
        s=0
        for j in range(i+1, n):
            s += A[o[i]][j] * x[j]
        x[i] = (y[o[i]] - s) / A[o[i]][i]
    
    return x


