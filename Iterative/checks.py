class ConvStatus:
    CONVERGENT = 1
    UNDETERMINED = 0
    DIVERGENT = -1


def check_diagonal_dominance(A, C):
    """
    Check if matrix A is diagonally dominant, and if not, attempt to make it so by row swapping.
    
    Returns:
        DD (bool): True if matrix is or can be made diagonally dominant
        newA (list): Possibly reordered matrix
        newC (list): Possibly reordered vector C
    """
    n = len(A)
    newA = [row[:] for row in A]
    newC = C[:]
    
    print("==============================")
    print("\nChecking Diagonal Dominance......\n")
    
    # Check initial diagonal dominance
    DD, strict_count, failed_rows = check_dd_status(A)
    
    if DD:
        print("The matrix is already diagonally dominant")
        return DD, newA, newC
    
    print(f"\nMatrix is not diagonally dominant. Failed rows: {[r+1 for r in failed_rows]}")
    print("\nAttempting to find row permutation...\n")
    
    # Try to find a valid permutation
    permutation = find_valid_permutation(A)
    
    if permutation is None:
        print("Matrix cannot be made diagonally dominant by row swapping.\n")
        return False, A, C
    
    # Apply the permutation
    print("Found valid permutation!")
    newA = [A[permutation[i]][:] for i in range(n)]
    newC = [C[permutation[i]] for i in range(n)]
    
    print("\nRow mapping:")
    for i in range(n):
        if permutation[i] != i:
            print(f"  New row {i+1} <- Old row {permutation[i]+1}")
    
    print("\nNew matrix after permutation:")
    for i, row in enumerate(newA):
        print(f"  Row {i+1}: {row}")
    print(f"\nNew vector C: {newC}")
    
    # Verify the result
    DD_verify, strict_verify, _ = check_dd_status(newA)
    if DD_verify:
        print("\n✓ Matrix is now DIAGONALLY DOMINANT")
    else:
        print("\n✗ Warning: Permutation failed verification")
    
    return DD_verify, newA, newC


def check_dd_status(A):
    """
    Check if matrix A is diagonally dominant.
    
    Returns:
        is_dd (bool): True if diagonally dominant
        strict_count (int): Number of strictly dominant rows
        failed_rows (list): Indices of rows that fail diagonal dominance
    """
    n = len(A)
    strict_count = 0
    failed_rows = []
    
    for i in range(n):
        diagonal = abs(A[i][i])
        off_diagonal_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        
        print(f"Row {i+1}: |a_{i+1}{i+1}| = {diagonal}, sum of off-diagonal = {off_diagonal_sum}")
        
        if diagonal > off_diagonal_sum:
            print(f"  ✓ Strictly dominant")
            strict_count += 1
        elif diagonal == off_diagonal_sum:
            print(f"  ~ Weakly dominant (not strict)")
        else:
            print(f"  ✗ Not dominant")
            failed_rows.append(i)
    
    print("==============================")
    
    is_dd = (len(failed_rows) == 0) and (strict_count > 0)
    return is_dd, strict_count, failed_rows


def find_valid_permutation(A):
    """
    Find a permutation of rows that makes the matrix diagonally dominant.
    Uses backtracking to try all possible permutations.
    
    Returns:
        permutation (list): Valid permutation, or None if not found
    """
    n = len(A)
    
    def is_dominant_at_position(row_idx, pos):
        """Check if row row_idx would be dominant at position pos"""
        diagonal = abs(A[row_idx][pos])
        off_diagonal = sum(abs(A[row_idx][j]) for j in range(n) if j != pos)
        return diagonal >= off_diagonal
    
    def is_strictly_dominant_at_position(row_idx, pos):
        """Check if row row_idx would be strictly dominant at position pos"""
        diagonal = abs(A[row_idx][pos])
        off_diagonal = sum(abs(A[row_idx][j]) for j in range(n) if j != pos)
        return diagonal > off_diagonal
    
    def backtrack(pos, used, permutation, has_strict):
        """Backtracking function to find valid permutation"""
        if pos == n:
            # Check if at least one row is strictly dominant
            return has_strict
        
        for row_idx in range(n):
            if row_idx in used:
                continue
            
            if not is_dominant_at_position(row_idx, pos):
                continue
            
            # Try this assignment
            permutation[pos] = row_idx
            used.add(row_idx)
            
            is_strict = is_strictly_dominant_at_position(row_idx, pos)
            
            if backtrack(pos + 1, used, permutation, has_strict or is_strict):
                return True
            
            # Backtrack
            used.remove(row_idx)
        
        return False
    
    permutation = [0] * n
    if backtrack(0, set(), permutation, False):
        return permutation
    
    return None


def convergence_status(error_history, margin, DD, reached_max_iterations):
    """Determine convergence status of iterative method"""
    if not error_history:
        return ConvStatus.UNDETERMINED

    if error_history[-1] < margin:
        return ConvStatus.CONVERGENT

    if not reached_max_iterations:
        return ConvStatus.UNDETERMINED

    if DD:
        return ConvStatus.UNDETERMINED

    if len(error_history) < 3:
        return ConvStatus.UNDETERMINED

    last = error_history[-1]
    prev = error_history[-2]
    prev2 = error_history[-3]

    r1 = (last / prev) if prev != 0 else float('inf')
    r2 = (prev / prev2) if prev2 != 0 else float('inf')
    avg_r = (r1 + r2) / 2.0

    if avg_r > 1.05:
        return ConvStatus.DIVERGENT

    return ConvStatus.UNDETERMINED