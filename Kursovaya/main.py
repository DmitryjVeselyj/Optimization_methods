import dichotomy as dt
import golden as gd
import grad as grad
import task as td
import math

if __name__ == '__main__':
    x0 = [1, 1]
    eps = 10 ** (-2)
    res = grad.grad_calc_min(x0, eps, dt.dychotomy)
    print("Дихотомия")
    print(f'Результат: {res}\nЗначение функции: {td.func(res)}\n')

    res = grad.grad_calc_min(x0, eps, gd.golden)
    print("Золотое сечение")
    print(f'Результат: {res}\nЗначение функции: {td.func(res)}\n')