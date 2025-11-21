from gauss_solver import GaussSolver
from linear_system import LinearSystem
from step_recorder import StepRecorder 
from pivot_manager import pivot_manager
from back_substitution import back_substitution

# Example system
A = [
    [1, 2, 3],
    [2, 4, 6],   # This row is multiple of the first → singular
    [3, 1, 2]
]
b = [6, 12, 5]
sig_figs = 13
single_step = False
status = ""
system = LinearSystem(A, b)

solver = GaussSolver(system, single_step, sig_figs)
solution, steps, time, status = solver.solve()
if(status == "singular"):
    print("The matrix is singular or nearly singular. No unique solution exists.")
else:
    print("Solution:", solution)
    print(f"Execution time: {time:.10f} seconds")

print("\nSingle-step details:")
for step in steps:
    print(step[2])  # message
    print(step[0], step[1])  # current matrix and RHS
