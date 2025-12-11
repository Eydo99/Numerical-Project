
class SecantStep :
    first : float
    second : float
    result : float
    f_result : float

    def __init__(self, first, second, result, f_result):
        self.first = first
        self.second = second
        self.result = result
        self.f_result = f_result

class originalNewtonStep:
    point: float
    result: float
    f_result: float

    def __init__(self, point, result, f_result):
        self.point = point
        self.result = result
        self.f_result = f_result

class bisectionStep :
    xl: float
    xu: float
    xr : float
    f_xr: float

    def __init__(self, xl, xu, xr, f_xr):
        self.xl = xl
        self.xu = xu
        self.xr = xr
        self.f_xr = f_xr


class fixedPointStep:
    point:float
    result:float
    f_result:float
    def __init__(self, point, result, f_result):
        self.point = point
        self.result = result
        self.f_result = f_result