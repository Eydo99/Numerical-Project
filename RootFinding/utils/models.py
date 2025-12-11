
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


