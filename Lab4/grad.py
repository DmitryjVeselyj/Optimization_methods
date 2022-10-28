import unform as uni
import numpy as np
import task as td


def calc_min_with_uniform(x_start, grad_eps):
    x = x_start
    points = [x]
    n = 5
    while (np.linalg.norm(td.grad(x), ord=2)) >= grad_eps:
        alpha = uni.calc_uniform_searc(0, 1, grad_eps, n, lambda a1: td.func(x - a1 * td.grad(x)))
        x = x - alpha * td.grad(x)
        points.append(x)
    return (x, points)

def calc_min_with_psheno(x_start, grad_eps, alpha_start, lyamda, eps):
    x = x_start
    points = [x]
    while (np.linalg.norm(td.grad(x), ord=2)) >= grad_eps:
        hessian = td.hessian(x)
        inv_hessian = np.linalg.inv(hessian)
        p = -np.dot(inv_hessian, td.grad(x))
        alpha = get_alpha_with_psheno(alpha_start, lyamda, eps, p, x)
        x = x + alpha * p
        points.append(x)
    return (x, points)

def get_alpha_with_psheno(alpha_start , lyamda, eps, pk, xk):
    alpha = alpha_start
    while td.func(xk + alpha * pk) - td.func(xk) > alpha * eps * np.dot(td.grad(xk).transpose(), pk):
        alpha = lyamda * alpha
    return alpha