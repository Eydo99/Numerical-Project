

def check_diagonal_dominance(A):
    strict=0
    DD=False        
    newA=A   

    print("==============================")
    print("\nChecking Diagonal Dominance......\n\n")

    failed_rows = []
    dompivot = 0

    for i in range(len(A)):
        print("==============================")

        summtion = 0
        print("row", i+1, "=", A[i], "\n")

        for j in range(len(A[i])):
            if (i == j):
                continue
            summtion += abs(A[i][j])
        
        print("summtion of not-diagonal elements =", summtion, "\n")
        print("diagonal element =", abs(A[i][i]), "\n")

        if (abs(A[i][i]) >= summtion):
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

    if not((dompivot == len(A)) and (strict > 0)):

        print("trying to find possible row exchanges...\n")
        swap_sources = set()
        fixable_failed_rows = 0
        possible_swaps = {}
        used_replacements = set()

        for f in failed_rows:  
            print("row", f+1, "trying to find swaps\n")

            found_swap = False   

            for k in range(len(A)):   
                if k == f:
                    continue

                if k in used_replacements or k in swap_sources:
                    continue

                diag = abs(A[k][f])
                others = sum(abs(A[k][j]) for j in range(len(A)) if j != f)

                if diag >= others:

                    print("row", k+1, "can replace row ", f + 1)
                    print("==============================")

                    used_replacements.add(k)
                    possible_swaps[f] = k
                    swap_sources.add(f) 
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

            for f, k in possible_swaps.items():
                print("Swapping row", f+1, "with row ", k+1)
                newA[f], newA[k] = newA[k], newA[f]

            print("\nnew matrix after swaps:")
            for row in newA:
                print(row)

            print("\nnow the matrix is DIAGONALLY DOMINANT ")

        else:
            print("at least one failed row can not be fixed by swapping.")
            print("matrix can not be made diagonally dominant.\n")

    if ((dompivot == len(A)) and (strict > 0)):
        DD = True
        print("The matrix is diagonally dominant")
    return DD, newA 