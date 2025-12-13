import matplotlib.pyplot as plt
import scipy as sc
import numpy as np
import io

class FunctionPlotter :

    @staticmethod    
    def plot_func(lambda_func, start, end):
        plt.figure()
        x = np.arange(start, end, 0.1)
        y = []
        for i in range(len(x)):
            y.append(lambda_func(x[i]))
        plt.plot(x, y)
        plt.show()
    
    @staticmethod
    def get_plot_buffer(lambda_func, start, end):
        fig = plt.figure()
        plt.axhline(0, linestyle= "dashed", color= "black")
        plt.axvline(0, linestyle= "dashed", color= "black")
        plt.xlim(start,end)
        x = np.arange(start, end, 0.1)
        y = []
        for i in range(len(x)):
            y.append(lambda_func(x[i]))
        plt.plot(x, y)
        buffer = io.BytesIO()
        fig.savefig(buffer, format= "png")
        return buffer

        




