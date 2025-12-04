import math

def round_sig(x, sig=6):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)



def back_sub(A, b, sig=6):
    n = len(b)
    x = [0]*n
    x[n-1] = round_sig(b[n-1] / A[n-1][n-1], sig)
    for i in range(n-2, -1, -1):
        tot = 0
        for j in range(i+1,n):
            tot = round_sig(tot + round_sig(A[i][j] * x[j], sig), sig)
        x[i] =  round_sig((b[i]-tot)/A[i][i], sig)

    return x

def pivot(A, b, col, scaling : bool = False, scales : list = None, tol=1e-12):
    n = len(b)
    print(scales)
    print(scaling)
    scales = scales if (scaling) else [1]*n
    max_row = max(range(col, n), key=lambda r: abs(A[r][col]/scales[r]))
    if abs(A[max_row][col]/ scales[max_row]) < tol:
        return -1
    
    if max_row != col:
        A[col], A[max_row] = A[max_row], A[col]
        b[col], b[max_row] = b[max_row], b[col]
        scales[col], scales[max_row] = scales[max_row],scales[col]

    # return A, b, 0
    # no need to return A,b and assign it since its passed by reference 
    return 0



# Instead of having two methods and adding an if condition on use i merged the two methods 
# and the flag will be just passed and internally handled
def pivot_lu(A : list[list], col : int, o : list, scaling : bool = False, s: list = None, sig_figs=8):
    n=len(A)
    p = col
    # This is the line that was modified
    s = s if (scaling and s != None and len(s) == n) else [1]*n

    big = round_sig(abs(A[o[col]][col] / s[o[col]]), sig_figs)

    for i in range(col+1, n):
        dummy = round_sig(abs(A[o[i]][col] /s[o[i]]), sig_figs)
        if dummy > big:
            big = dummy
            p = i
    
    o[col], o[p] = o[p], o[col]


def scaling_factors(A):
    n = len(A)
    s=[0]*n
    for i in range(n):
        s[i] = max(abs(val) for val in A[i])
    return s
