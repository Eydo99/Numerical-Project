
class ConvStatus :
    CONVERGENT = 1,
    UNDETERMINED = 0,
    DIVERGENT = -1,

def check_diagonal_dominance(A, C):
    strict = 0
    DD = False
    newA = A
    newC = C[:]  

    print("==============================")
    print("\nChecking Diagonal Dominance......\n\n")

    failed_rows = []
    dompivot = 0

    for i in range(len(A)):
        print("==============================")
        summtion = 0
        print("row", i+1, "=", A[i], "\n")

        for j in range(len(A[i])):
            if i == j:
                continue
            summtion += abs(A[i][j])

        print("summtion of not-diagonal elements =", summtion, "\n")
        print("diagonal element =", abs(A[i][i]), "\n")

        if abs(A[i][i]) >= summtion:
            print("row satisfies")
            dompivot += 1
            if abs(A[i][i]) > summtion:
                strict += 1
                print("row is strictly dominant\n")
            else:
                print("row is not strictly dominant\n")
        else:
            print(" row fail\n")
            failed_rows.append(i)

    print("==============================")

    
    if not ((dompivot == len(A)) and (strict > 0)):
        print("trying to find possible row exchanges...\n")
        used_replacements = set()   
        possible_swaps = {}         
        fixable_failed_rows = 0

        for f in failed_rows:
            print("row", f+1, "trying to find swaps\n")
            found_swap = False

            for k in range(len(A)):
                if k == f:
                    continue
                if k in used_replacements:
                    continue

                diag = abs(A[k][f])
                others = sum(abs(A[k][j]) for j in range(len(A)) if j != f)

                if diag >= others:
                    print("row", k+1, "can replace row ", f+1)
                    print("==============================")
                    possible_swaps[f] = k
                    used_replacements.add(k)
                    found_swap = True
                    break

            if not found_swap:
                print("this row can not be swapped")
                print("This diagonal position cannot be dominated.\n")
                print("==============================")
            else:
                fixable_failed_rows += 1

            print()

        if fixable_failed_rows == len(failed_rows):
            DD = True
            print("all failed rows CAN be fixed by swapping.")
            print("Performing swaps...\n")

            newA = [row[:] for row in A]
            newC = C[:]

            swapped = set()
            for f, k in possible_swaps.items():
                if f in swapped or k in swapped:
                    continue
                print("Swapping row", f+1, "with row", k+1)
                newA[f], newA[k] = newA[k], newA[f]
                newC[f], newC[k] = newC[k], newC[f]
                swapped.add(f)
                swapped.add(k)

            print("\nnew matrix after swaps:")
            for row in newA:
                print(row)
            print("new vector C after swaps:", newC)
            print("\nnow the matrix is DIAGONALLY DOMINANT ")

        else:
            print("at least one failed row can not be fixed by swapping.")
            print("matrix can not be made diagonally dominant.\n")

    if (dompivot == len(A)) and (strict > 0):
        DD = True
        print("The matrix is diagonally dominant")

    return DD, newA, newC


def convergence_status(error_history, margin, DD, reached_max_iterations):
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

    last  = error_history[-1]
    prev  = error_history[-2]
    prev2 = error_history[-3]

    r1 = (last / prev) if prev != 0 else float('inf')
    r2 = (prev / prev2) if prev2 != 0 else float('inf')
    avg_r = (r1 + r2) / 2.0

    if avg_r > 1.05:
        return ConvStatus.DIVERGENT

    return ConvStatus.UNDETERMINED