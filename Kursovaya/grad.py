import numpy as np
import task as td


def grad_calc_min(x_start, grad_eps, method):
    x = x_start
    while (np.linalg.norm(td.grad(x), ord=2)) >= grad_eps:
        alpha = method(0, 1, lambda a1: td.func(x - a1 * td.grad(x)), grad_eps)
        x = x - alpha * td.grad(x)
    return x
