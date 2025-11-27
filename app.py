from flask import Flask, app, request
from utils.models import *
from utils.auxilary import *
from GaussEliminationStandard.gauss_jordan import GaussJordanSolver
from GaussEliminationStandard.gauss_solver import GaussSolver
from LUStandard.cholesky_solver import CholeskySolver
from LUStandard.dolittle_solver import DolittleSolver
from LUStandard.crout_solver import CroutSolver
from Iterative.gauss_seidel_solver import GaussSeidelSolver
from Iterative.jacobi_solver import JacobiSolver
import time
import json

app = Flask(__name__)


@app.route('/solve/gaussjordan', methods = ['POST'])
def handle_gauss_jordan():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    single_step : bool = data.get("single_step")
    
    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    start = time.time()
    solver = GaussJordanSolver(LinearSystem(matrix, answers), False)
    ans,_ = solver.solve(sig_figs, tol,scaling=False)
    end = time.time()
    exec_time = end - start

    if single_step :
        solver = GaussJordanSolver(LinearSystem(matrix, answers), True)
        solver.solve(sig_figs, tol,scaling=False)
    
    steps : list[GaussStep] = solver.step_recorder.steps

    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "matrix" : step.matrix, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList, "exec_time" : exec_time}
    return json.dumps(output)

@app.route('/solve/gausselim', methods = ['POST'])
def handle_gauss_elim():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    single_step : bool = data.get("single_step")
    
    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")


    start = time.time()
    solver = GaussSolver(LinearSystem(matrix, answers), False)
    ans,_ = solver.solve(sig_figs, tol,scaling=False)
    end = time.time()
    exec_time = end - start

    if single_step :
        solver = GaussSolver(LinearSystem(matrix, answers), True)
        solver.solve(sig_figs, tol,scaling=False)
        
    steps : list[GaussStep] = solver.step_recorder.steps


    stepList = []

    for step in steps :
        stepList.append({"type" : step.stepType, "matrix" : step.matrix, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList, "exec_time" : exec_time}
    return json.dumps(output)


@app.route('/solve/cholesky', methods = ['POST'])
def handle_cholesky():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    single_step : bool = data.get("single_step")

    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    solver = CholeskySolver(LinearSystem(matrix, answers), False)
    ans = solver.solve(sig_figs)
    steps : list[LUStep] = solver.recorder.steps

    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "L" : step.L, "U" : step.U})

    output = {"result" : ans, "steps" : stepList}
    return json.dumps(output)

@app.route('/solve/crout', methods = ['POST'])
def handle_crout():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    single_step : bool = data.get("single_step")

    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    solver = CroutSolver(LinearSystem(matrix, answers), False)
    ans,exec_time = solver.solve(sig_figs)
    steps : list[LUStep] = solver.recorder.steps

    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "L" : step.L, "U" : step.U})

    output = {"result" : ans, "steps" : stepList, "exec_time" : exec_time}
    return json.dumps(output)


@app.route('/solve/dolittle', methods = ['POST'])
def handle_dolittle():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim")) 
    single_step : bool = data.get("single_step")

    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    start = time.time()
    solver = DolittleSolver(LinearSystem(matrix, answers), False)
    ans,_ = solver.solve(sig_figs, tol,scaled=True)
    end = time.time()
    exec_time = end - start

    if single_step :
        solver = DolittleSolver(LinearSystem(matrix, answers), True)
        solver.solve(sig_figs, tol,scaled=True)  

    steps : list[LUStep] = solver.recorder.steps

    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "L" : step.L, "U" : step.U})

    output = {"result" : ans, "steps" : stepList}
    return json.dumps(output)

@app.route('/solve/jacobi', methods = ['POST'])
def handle_jacobi():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim")) 
    single_step : bool = data.get("single_step")

    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    
    init_guess : list = data.get("initial") 
    max_itrs : int = data.get("max_itrs")
    
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    start = time.time()
    solver = JacobiSolver(LinearSystem(matrix, answers), False)
    ans,_,_ = solver.solve(init_guess, sig_figs, tol, max_itrs)
    end = time.time()
    
    exec_time : float = end - start

    if single_step :
        solver = JacobiSolver(LinearSystem(matrix, answers), True)
        solver.solve( init_guess, sig_figs, tol, max_itrs)

    steps : list[IterativeStep] = solver.recorder.steps

    stepList = []

    for step in steps :
        stepList.append({"type" : step.stepType, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList, "exec_time" : exec_time}
    return json.dumps(output)

@app.route('/solve/gauss_seidel', methods = ['POST'])
def handle_gauss_seidel():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    single_step : bool = data.get("single_step")

    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")
    
    init_guess : list = data.get("initial") 
    max_itrs : int = data.get("max_itrs")
    
    tol : float = data.get("tol")
    sig_figs : int = data.get("sig_figs")

    start = time.time()
    solver = GaussSeidelSolver(LinearSystem(matrix, answers), False)
    ans,_,_ = solver.solve( init_guess, sig_figs, tol, max_itrs)
    end = time.time()
    
    exec_time : float = end - start

    if single_step :
        solver = GaussSeidelSolver(LinearSystem(matrix, answers), True)
        solver.solve(init_guess, sig_figs, tol,  max_itrs)

    steps : list[IterativeStep] = solver.recorder.steps

    stepList = []

    for step in steps :
        stepList.append({"type" : step.stepType, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList, "exec_time" : exec_time}
    return json.dumps(output)
# if app.name == "__main__" :
app.run(debug= True, port= 8080)

