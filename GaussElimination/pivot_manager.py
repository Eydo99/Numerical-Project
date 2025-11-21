class pivot_manager:
    @staticmethod
    def pivot(A, b, col, tol=1e-12):
        n = len(b)
        max_row = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[max_row][col]) < tol:
            return None, None, -1
        
        if max_row != col:
            A[col], A[max_row] = A[max_row], A[col]
            b[col], b[max_row] = b[max_row], b[col]
        return A, b, 0