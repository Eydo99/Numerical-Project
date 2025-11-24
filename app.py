from flask import Flask, app, request
from utils.models import *
from utils.auxilary import *
from GaussEliminationStandard.gauss_jordan import GaussJordanSolver
from GaussEliminationStandard.gauss_solver import GaussSolver
import json

app = Flask(__name__)


@app.route('/solve/gaussjordan', methods = ['POST'])
def handle_gauss_jordan():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")

    solver = GaussJordanSolver(LinearSystem(matrix, answers), True)
    steps,ans = solver.solve(10,scaling=False)


    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "matrix" : step.matrix, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList}
    return json.dumps(output)

@app.route('/solve/gausselim', methods = ['POST'])
def handle_gauss_elim():
    # getting the needed values
    data = request.json
    dim : int = int(data.get("dim"))
    matrix : list[list] = data.get("coeff")
    answers : list = data.get("answers")

    solver = GaussSolver(LinearSystem(matrix, answers), True)
    steps,ans = solver.solve(10,scaling=True)


    stepList = []
    for step in steps :
        stepList.append({"type" : step.stepType, "matrix" : step.matrix, "answers" : step.answers})

    output = {"result" : ans, "steps" : stepList}
    return json.dumps(output)



# if app.name == "__main__" :
app.run(debug= True, port= 8080)