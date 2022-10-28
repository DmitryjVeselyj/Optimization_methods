import grad
from scipy.optimize import fmin
import task as td
import math
import numpy as np
from matplotlib import pyplot as plt

def plot_and_other_dangerous_things(res):
    xAxis = []
    yAxis = []
    for i in range(len(res[1]) - 2):
        v1 = res[1][i + 1] - res[1][i]
        v2 = res[1][i + 2] - res[1][i + 1]
        print(f'скалярное произведение векторов: {np.dot(v1, v2)}') #для того, чтобы ортогональность показать

    for i in range(len(res[1])):
        xAxis.append(res[1][i][0])
        yAxis.append(res[1][i][1])
    plt.xlim(0, 0.4)
    plt.ylim(-0.4, -0.8)
    plt.plot(xAxis, yAxis)
    plt.show()

def prove_linear(res):
    x_zvezda = res[0]
    xAxis = []
    yAxis = []
    for i in range(0, len(res[1]) - 1):
        xAxis.append(np.linalg.norm(res[1][i] - x_zvezda))
        yAxis.append(np.linalg.norm(res[1][i + 1] - x_zvezda))
    plt.xlim(0, 0.5)
    plt.ylim(0, 0.5)
    plt.plot(xAxis, yAxis)
    plt.show()

    q = 1/2
    for i in range(len(xAxis)):# типа аналитически по определению обосновали
        print(yAxis[i] - q * xAxis[i] )

if __name__ == '__main__':
    x0 = [0, -0.8]
    eps = 10**(-3)
    res = grad.calc_min_with_uniform(x0, eps)
    print(res[0], td.func(res[0]))
    plot_and_other_dangerous_things(res)
    prove_linear(res)

    alpha_start = 1 #всегда
    lyamda = 1/10
    epsPh = 10**(-3)
    res2 = grad.calc_min_with_psheno(x0, eps, alpha_start, lyamda, epsPh)
    print(res2[0], td.func(res2[0]))




    #x1 = fmin(td.func, x0, ftol = eps)[0]
   # y1 = fmin(td.func, x0, ftol = eps)[1]
  #  bestres = td.func([x1,y1])
   # print(x1, y1)