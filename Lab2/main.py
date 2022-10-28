import numpy as np

import transport as tp
import Simplex as sp

def formDataForSimplex(aCost, aDemand, aSupply, aFine):
    aCostConv, aDemandConv, aSupplyConv = tp.convertToClose(aCost, aDemand, aSupply, aFine)
    m = len(aDemandConv)
    n = len(aSupplyConv)
    tmp = [0] * m * n
    A = []
    b = []
    c = []
    for i in range(n):
        for j in range(m):
            tmp[i * m + j] = 1
        A.append(tmp)
        tmp = [0] * m * n
    for i in range(m - 1):#-1 потому что выкидываем одну линейно зависимую строку(она последняя)
        for j in range(n):
            tmp[j * m + i] = 1
        A.append(tmp)
        tmp = [0] * m * n

    b = aSupplyConv + aDemandConv[:m-1]
    for i in range(n):
        for j in range(m):
            c.append(aCostConv[i][j])
    return np.array(c), np.array(A), np.array(b)


if __name__ == "__main__":

    aCost = [[3, 17, 2, 19, 6]
        , [15, 8, 12, 5, 10]
        , [8, 9, 8, 9, 14]
        , [5, 7, 6, 3, 18]]

    aDemand = [24, 13, 4, 17, 12]
    aSupply = [22, 19, 14, 15]

    aFine = [[0, 0, 0, 0, 0]]
    transportRes = tp.potential(aCost, aDemand, aSupply, aFine)

    c, A, b = formDataForSimplex(aCost, aDemand, aSupply, aFine)
    res = sp.simplex_method(c, A, b)
    print(f"Симплекс метод задача\nОпорный вектор x*:  {res.tolist()}")
    print(f"Значение целевой функции: {np.dot(c, res)}\n")



    y = [1, 5, 6, 3, 2, 3, 1, 0, 5]
    A1 = []
    aCostConv, aDemandConv, aSupplyConv = tp.convertToClose(aCost, aDemand, aSupply, aFine)
    m = len(aDemandConv)
    n = len(aSupplyConv)
    tmp = [0] * m * n
    for i in range(n):
        for j in range(m):
            tmp[i * m + j] = 1
        A1.append(tmp)
        tmp = [0] * m * n
    for i in range(m):
        for j in range(n):
            tmp[j * m + i] = 1
        A1.append(tmp)
        tmp = [0] * m * n
    print(c - np.dot(y, A1))
    print(np.dot(c - np.dot(y, A1),res))
   # print(np.dot(c - np.dot(y, A1), transportRes)) не обязательно, тк критерий оптимальности формально задан в самом методе


