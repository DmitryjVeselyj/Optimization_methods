import math

def calc_uniform_searc(a, b, eps, n, func):
    f_cals_number = 0
    xj_left = a
    xj_right = b
    j = 0
    while True:
        h = (xj_right - xj_left) / n
        min = math.inf
        for i in range(1, n + 1):
            f_cals_number+=1
            f_xj = func(xj_left + i*h)
            if f_xj < min:
                min = f_xj
                j = i
        xj_right = xj_left + (j + 1) * h
        xj_left = xj_left + (j - 1) * h
        if (xj_right - xj_left) < eps:
            break
    return (xj_right + xj_left) / 2, func((xj_right + xj_left) / 2), f_cals_number
