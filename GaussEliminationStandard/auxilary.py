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
            tot +=  round_sig(A[i][j] * x[j], sig)
        x[i] =  round_sig((b[i]-tot)/A[i][i], sig)

    return x

def pivot(A, b, col, scaling : bool = False, scales : list = None, tol=1e-12):
    n = len(b)
    scales = scales if (scaling and scales != None and len(scales) == n) else [1]*n
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