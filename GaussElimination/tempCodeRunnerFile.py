from gauss_solver import GaussSolver
from linear_system import LinearSystem
from step_recorder import StepRecorder 
from pivot_manager import pivot_manager
from back_substitution import back_substitution

# Example system
A = [
    [2, 1, -1],
    [-3, -1, 2],
    [-2, 1, 2]
]
b = [8, -11, -3]
sig_figs = 3
system = LinearSystem(A, b)

solver = GaussSolver(system, single_step=True, sig_figs=6)
solution, steps, time = solver.solve()

print("Solution:", solution)
print(f"Execution time: {time:.10f} seconds")
print("\n")
print("\nSingle-step details:")
for step in steps:
    print(step[2])  # message
    print(step[0], step[1])  # current matrix and RHS
