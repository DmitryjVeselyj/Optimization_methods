import numpy as np

import unform as un
import fibo as fb
import math
from scipy.optimize import fmin

def f(x):
    return math.tan(x) - 2 * math.sin(x)

def funcUni(n, a, b, eps):
    return n* (math.log(b - a) - math.log(eps)) / math.log(n / 2)

if __name__ == '__main__':
    a = 0
    b = math.pi/4
    n = 5
    eps = 10**(-2)
    x_min, f_x_min, f_calc_number = un.calc_uniform_searc(a, b, eps, n, f)
    print(f"xmin {x_min}  f_xmin {f_x_min} ")
    print(f"число обращений к функции цели {f_calc_number}  аналитическая оценка {funcUni(n, a , b , eps)}")#оценка вроде снизу получается
    print(math.fabs(f(fmin(f , 0)) - f_x_min))#чисто для того, чтобы посмотреть, какая точность получается

    n = fb.get_n_for_eps(a ,b, eps)
    x_min, f_x_min, f_calc_number = fb.calculateFibo(a, b, eps, f, n)
    print(f"xmin {x_min}  f_xmin {f_x_min} ")
    print(f"число обращений к функции цели {f_calc_number}  аналитическая оценка {n + 1}")
    print(math.fabs(f(fmin(f, 0)) - f_x_min))


