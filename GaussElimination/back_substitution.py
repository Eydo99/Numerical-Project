import math

def round_sig(x, sig=6):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

class back_substitution:
    @staticmethod
    def solve(A, b, sig=6):
        n = len(b)
        x = [0]*n
        x[n-1] = round(b[n-1] / A[n-1][n-1], sig)
        for i in range(n-2, -1, -1):
            tot = 0
            for j in range(i+1,n):
                tot +=  round(A[i][j] * x[j], sig)
            x[i] =  round((b[i]-tot)/A[i][i], sig)

        return x