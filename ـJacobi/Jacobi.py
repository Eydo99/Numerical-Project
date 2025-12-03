from DiagonalDominantTest import check_diagonal_dominance
import time



A=[[5,-1,1],[2,8,-1],[-1,1,4]]
C=[10,11,3]
Intial =[0,0,0]
Helper =Intial.copy()
It=6
margin=0.8
sig=5
n=3
start1=time.perf_counter()


DD, newA = check_diagonal_dominance(A)


if DD:
    print("matrix is diagonally dominant => Jacobi will to converge.")
    A = newA
else:
    print("matrix is not diagonally dominant => Jacobi may not converge.")


X= [ "X"+str(i+1) for i in range(n) ]


start2=time.perf_counter()


print("\n jacobi start \n")

print("Initial Matrix A:")
for row in A:
    print(row)
print("\nVector C:", C)
print("\nInitial Guess:", Intial)
print("\n---------------------------------------------\n")


for i in range(It):
    print("Iteration no. ",i+1,"\n")

    for row in range(len(A)):
        computation=0
        for col in range (len(A[row])):
            if row == col:
                continue
            else:
                computation-=A[row][col]*Intial[col]
        Helper[row]=(C[row]+computation)*(1/A[row][row])
   
    Helper = [float(f"{val:.{sig}g}") for val in Helper]

    errors = []
    for j in range(n):
        if Helper[j] != 0:
            Ea=abs((Helper[j]-Intial[j])/Helper[j])*100
        else:
            Ea = 0
        errors.append(round(Ea, 6))


    for j in range(n):    
       print(X[j]+"="+str(Helper[j])+"   (error = "+str(errors[j])+"%)")
       print()


    stop = True
    for e in errors:
       if e >= margin:
         stop = False
         break

    if stop and (i+1)!=It:
      print("stopping early because all relative errors < margin\n")
      break
    
    
    Intial=Helper.copy()


print("Jacobi End")

end =time.perf_counter()

print("execution time without diagoanlly dominant check:",round((end-start2)*1_000_000,3)," microsecond")
print("execution time with diagoanlly dominant check:",round((end-start1)*1_000_000,3)," microsecond")





