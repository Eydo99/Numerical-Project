from flask import Blueprint, request, Response
from RootFinding.OpenMethods.secant_method import SecantSolver
from RootFinding.utils.auxilary import *
from RootFinding.utils.models import SecantStep
from RootFinding.utils.step_recorder import SecantMethodStepRecorder
from RootFinding.plotter import FunctionPlotter
import json
import io

rootf = Blueprint("rootfinding", __name__)

@rootf.route("/secant", methods= ["POST"])
def handle_secant():
    data = request.json
    func_str = data.get("func")

    start = data.get("start")
    end = data.get("end")

    first = data.get("first")
    second = data.get("second")

    tol = data.get("tol")
    max_itrs = data.get("max_itrs")

    sig_figs = data.get("sig_figs")

    lambda_func = get_lambda_func(func_str)
    solver = SecantSolver(lambda_func, true)
    res, itrs = solver.solve(first, second, max_itrs, tol, sig_figs)
    steps  = []
    for step in solver.recorder.steps :
        steps.append({
            "first" : step.first,
            "second" : step.second,
            "result" : step.result,
            "f_result" : step.f_result
        })
        
    response = {
        "sol" : res,
        "itrs" : itrs,
        "steps" : steps
    }


    return json.dumps(response)

@rootf.route("/plot", methods = ["POST"])
def plot_func():
    data = request.json
    func_str = data.get("func")

    start = data.get("start")
    end = data.get("end")

    lambda_func = get_lambda_func(func_str)

    buffer = FunctionPlotter.get_plot_buffer(lambda_func, start, end)
    
    return Response(buffer.getvalue(), mimetype="image/png")
