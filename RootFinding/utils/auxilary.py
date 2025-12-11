from sympy import *
import math

def get_lambda_func ( func_str : str) :
    x = Symbol('x')
    
    func_simpified = sympify(func_str)
    return lambdify(x, func_simpified, "numpy")

def get_lambda_diff(func_str : str) :
    x = Symbol('x')
    dydx = diff(func_str)
    return lambdify(x, dydx, "numpy")


def round_sig(x, sig=6):
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)
