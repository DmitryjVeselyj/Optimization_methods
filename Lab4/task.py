import numpy as np
import math

def func(arg):
    x = arg[0]
    y = arg[1]
    return x**2 + y**2 + math.exp(x**2 + y**2) - x + 2*y


def grad(arg):
    x = arg[0]
    y = arg[1]
    return np.array([2*x + 2*x*math.exp(x**2 + y**2) - 1, 2*y + 2*y*math.exp(x**2 + y**2) + 2])

def hessian(arg):
    x = arg[0]
    y = arg[1]
    return np.array([[2 + 2 * math.exp(x**2 + y**2) + 4 * x**2 * math.exp(x**2 + y**2), 2 * x * 2 * y * math.exp(x**2 + y**2)],
                     [2 * x * 2 * y * math.exp(x**2 + y**2), 2 + 2 * math.exp(x**2 + y**2) + 4 * x**2 * math.exp(x**2 + y**2)]])