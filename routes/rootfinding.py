from flask import Blueprint, request, Response
from RootFinding.OpenMethods.secant_method import SecantSolver
from RootFinding.OpenMethods.original_newtonRaphson_method import originalNewtonSolver
from RootFinding.BracketingMethods.bisection_method import bisectionSolver
from RootFinding.OpenMethods.fixedPoint_method import fixedPointSolver
from RootFinding.utils.auxilary import *
from RootFinding.plotter import FunctionPlotter
import json
import io

rootf = Blueprint("rootfinding", __name__)

@rootf.route("/secant", methods= ["POST"])
def handle_secant():
    data = request.json
    func_str = data.get("func")

    first = data.get("first")
    second = data.get("second")

    tol = data.get("tol", 1e-6)
    max_itrs = data.get("max_itrs", 50)

    sig_figs = data.get("sig_figs", 6)

    single_step = data.get("single_step", False)

    lambda_func = get_lambda_func(func_str)
    solver = SecantSolver(lambda_func, single_step)
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

@rootf.route("/classic_newton", methods = ["POST"])
def handle_og_newton():
    data = request.json
    func_str = data.get("func")

    first = data.get("first")

    tol = data.get("tol", 1e-6)
    max_itrs = data.get("max_itrs", 50)

    sig_figs = data.get("sig_figs", 6)

    single_step = data.get("single_step", False)

    lambda_func = get_lambda_func(func_str)
    diff_func = get_lambda_diff(func_str)

    solver = originalNewtonSolver(lambda_func, diff_func, single_step)
    res,itrs = solver.solve(first, max_itrs, tol, sig_figs)

    steps  = []
    for step in solver.recorder.steps :
        steps.append({
            "point" : step.point,
            "result" : step.result,
            "f_result" : step.f_result
        })
        
    response = {
        "sol" : res,
        "itrs" : itrs,
        "steps" : steps
    }


    return json.dumps(response)

@rootf.route("/fixed_point", methods= ["POST"])
def handle_fixed_point():
    data = request.json
    func_str = data.get("func")

    first = data.get("first")

    tol = data.get("tol", 1e-6)
    max_itrs = data.get("max_itrs", 50)

    sig_figs = data.get("sig_figs", 6)

    single_step = data.get("single_step", False)

    func_lambda = get_lambda_func(func_str)
    g_x_lambda = get_lambda_gx(func_str)

    solver = fixedPointSolver(func_lambda, g_x_lambda, single_step)
    res,itrs = solver.solve(first, max_itrs, tol, sig_figs)

    steps  = []
    for step in solver.recorder.steps :
        steps.append({
            "point" : step.point,
            "result" : step.result,
            "f_result" : step.f_result
        })
        
    response = {
        "sol" : res,
        "itrs" : itrs,
        "steps" : steps
    }


    return json.dumps(response)

@rootf.route("/bisection", methods= ["POST"])
def handle_biseection():
    data = request.json
    func_str = data.get("func")

    low = data.get("first")
    high = data.get("second")


    tol = data.get("tol", 1e-6)
    max_itrs = data.get("max_itrs", 50)

    sig_figs = data.get("sig_figs", 6)

    single_step = data.get("single_step", False)

    func_lambda = get_lambda_func(func_str)

    solver = bisectionSolver(func_lambda, single_step)
    res,itrs = solver.solve(low,high, max_itrs, tol, sig_figs)

    steps  = []
    for step in solver.recorder.steps :
        steps.append({
            "first" : step.xl,
            "second" : step.xu,
            "result" : step.xr,
            "f_result" : step.f_xr
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
