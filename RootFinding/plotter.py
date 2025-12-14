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
    def get_plot_buffer(lambda_funcs : list, startx, endx, starty = None, endy = None, steps = None, labels : list = []):
        fig = plt.figure()
        plt.axhline(0, linestyle= "dashed", color= "black")
        plt.axvline(0, linestyle= "dashed", color= "black")
        if(startx and endx ) :
            plt.xlim(startx,endx)
        if(starty and endy ) :
            plt.ylim(starty,endy)
        
        startx = startx or -100
        endx = endx or 100
        steps = steps or 1000

        x = np.arange(startx , endx , (endx - startx)/steps)
        lines = []
        if isinstance(lambda_funcs, list) :
            for idx,func in enumerate(lambda_funcs) :
                y = []
                for j in x:
                    y.append(func(j))
                label = labels[idx] if (isinstance(labels, list) and idx < len(labels)) else f"f{str(idx)}(x)"
                line = plt.plot(x, y, label= label)
                lines.append(line[0])
        elif callable(lambda_funcs) :
            y = []
            for j in x:
                y.append(lambda_funcs(j))
            label = labels[0] if (isinstance(labels, list) and len(labels) > 0) else "f(x)"
            line = plt.plot(x, y, label= label)
            lines.append(line[0])
                
        plt.legend(handles = lines)
        buffer = io.BytesIO()
        fig.savefig(buffer, format= "png")
        return buffer

        




