import math
import numpy as np


def func(arg):
    x = arg[0]
    y = arg[1]
    return x**2 + 2 * y**2 + math.exp(x**2 + y**2) - x + 2*y


def grad(arg):
    x = arg[0]
    y = arg[1]
    return np.array([2*x + 2*x*math.exp(x**2 + y**2) - 1, 4*y + 2*y*math.exp(x**2 + y**2) + 2])


constraints = [
    lambda x: np.exp(-x[0])-1.4 - x[1],
    lambda x: x[0]+0.1*x[1] - 0.5,
    lambda x: 0.1*x[0] + x[1] + 0.1,
    lambda x: func(x[:2]) - x[2]
]

constraints_grad = [
    lambda x: np.array([-np.exp(-x[0]), -1, 0]),
    lambda x: np.array([1, 0.1, 0]),
    lambda x: np.array([0.1, 1, 0]),
    lambda x: np.array([*grad(x[:2]), -1])
]