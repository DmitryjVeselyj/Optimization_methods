import numpy as np
import random
import math

def printOut(aCost, aDemand, aSupply, aRoute, aDual, n, m):
    nCost = 0
    sumRow = 0
    sumCol = [0] * m
    res = []
    for i in range(m):
        print('   %4i' % aDemand[i], end ="    ")
    print()
    for x in range(n):
        for y in range(m):
            nCost += aCost[x][y] * round(aRoute[x][y])
            if aRoute[x][y] == 0:
                res.append(0)
                print('[<%2i>%4i]' % (aCost[x][y], aDual[x][y]), end=" ")
            else:
                res.append(round(aRoute[x][y]))
                sumRow +=aRoute[x][y]
                sumCol[y]+= aRoute[x][y]
                print('[<%2i>(%2i)]' % (aCost[x][y], aRoute[x][y] + 0.5), end = " ")
        print(' sum %i   %i' % (sumRow, aSupply[x]))
        sumRow=0
    for i in range(m):
        print('sum%4i' % sumCol[i], end ="    ")
    print(f"\nResult: {res}")
    print(nCost)
    print()
    return res


def northWest(aRoute, aDemand, aSupply, n, m):
    u = 0
    v = 0
    aS = [0] * m
    aD = [0] * n
    while u <= n - 1 and v <= m - 1:
        if aDemand[v] - aS[v] < aSupply[u] - aD[u]:
            z = aDemand[v] - aS[v]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            v += 1
        else:
            z = aSupply[u] - aD[u]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            u += 1

def notOptimal( aDual, n, m):
    nMin = math.inf
    global PivotN, PivotM
    for u in range(0, n):
        for v in range(0, m):
            x = aDual[u][v]
            if x < nMin:
                nMin = x
                PivotN = u
                PivotM = v
    return (nMin < 0)

def getDual(aRoute, aCost, aDual, n, m):
    u2 = [0] * n
    v2 = [0] * m
    A = []
    b = []
    flag = False
    indx = 0
    for i in range(n):
        for j in range(m):
            if aRoute[i][j] != 0:
                if not flag:
                    indx = i
                    flag = True
                u2[i] = 0 if i == indx else -1
                v2[j] = 1
                A.append(np.concatenate((u2, v2), axis=0))
                b.append(aCost[i][j])
                u2[i] = 0
                v2[j] = 0
    m1 = list(range(0, np.array(A).shape[1]))
    m1.remove(indx)
    n1 = list(range(np.array(A).shape[0]))

    A = np.array(A)
    b = np.array(b)
    A = A[np.ix_(n1,m1)]
    try:
        x = np.linalg.solve(A, b)
    except:
        print("ERROR in potential calculation. Trying another nonBasic cell")
        return False
    y = x.tolist()
    y.insert(indx, 0)
    u1 = y[:n]
    v1 = y[n:n+m]
    for i in range(n):
        for j in range(m):
            aDual[i][j] = 0.5  # zero numb
            if aRoute[i][j] == 0:
                aDual[i][j] = aCost[i][j] + u1[i] - v1[j]

    return True

def addFictionsBasis(aRoute, fictionsBasis, n, m, iteration):
    if iteration != 0:
        if any(fictionsBasis):
            for w in fictionsBasis:
                aRoute[w[0]][w[1]] = 0
            fictionsBasis.clear()
    else:
        fictionsBasis.clear()
    cntBasis = 0
    nonBasis = []
    for i in range(n):
        for j in range(m):
            if aRoute[i][j] != 0:
                cntBasis+=1
            else:
                nonBasis.append([i, j])

    print(nonBasis)
    while cntBasis < m + n - 1:
        tmp = random.choice(nonBasis)
        print(f"tmp {tmp}")
        if fictionsBasis.count(tmp) != 0:
            continue
        aRoute[tmp[0]][tmp[1]] = 1e-5
        fictionsBasis.append([tmp[0], tmp[1]])
        cntBasis+=1


def findPath(aRoute, u, v, n, m):
    aPath = [[u, v]]
    if not lookHorizontaly(aPath,aRoute, u, v, u, v, n, m):
        print(f"Path error")
    return aPath

def lookHorizontaly(aPath, aRoute, u, v, u1, v1, n, m):
    for i in range(0, m):
        if i != v and aRoute[u][i] != 0:
            if i == v1:
                aPath.append([u, i])
                return True  # complete circuit
            if lookVerticaly(aPath, aRoute, u, i, u1, v1, n, m):
                aPath.append([u, i])
                return True
    return False  # not found


def lookVerticaly(aPath, aRoute,  u, v, u1, v1, n, m):
    for i in range(0, n):
        if i != u and aRoute[i][v] != 0:
            if lookHorizontaly(aPath, aRoute, i, v, u1, v1, n, m):
                aPath.append([i, v])
                return True
    return False  # not found

def betterOptimal(aRoute, n, m):
    global PivotN, PivotM
    aPath = findPath(aRoute, PivotN, PivotM, n, m)
    nMin = math.inf
    for w in range(1, len(aPath), 2):
        t = aRoute[aPath[w][0]][aPath[w][1]]
        if t < nMin:
            nMin = t
    for w in range(1, len(aPath), 2):
        aRoute[aPath[w][0]][aPath[w][1]] -= nMin
        aRoute[aPath[w - 1][0]][aPath[w - 1][1]] += nMin


def convertToClose(aCost, aDemand, aSupply, aFine):
    a = sum(aSupply)
    b = sum(aDemand)
    aSupplyConv = aSupply.copy()
    aDemandConv = aDemand.copy()
    if a == b:
        return aCost, aDemand, aSupply
    elif a < b:
        aSupplyConv.append(b - a)
        if np.array(aFine).shape[1]!= np.array(aCost).shape[1]:
            raise ValueError('aFine dimension isnt good')
        else:
            aCostConverted = np.concatenate((aCost, aFine), axis=0)
    else:
        aDemandConv.append(a - b)
        if np.array(aFine).shape[1]!= np.array(aCost).shape[0]:
            raise ValueError('aFine dimension isnt good')
        else:
            aCostConverted = np.concatenate((aCost, np.array(aFine).transpose()), axis=1)
    return aCostConverted, aDemandConv, aSupplyConv


PivotN = -1
PivotM = -1
def potential(aCost, aDemand, aSupply, aFine):
    aCostConv, aDemandConv, aSupplyConv = convertToClose(aCost, aDemand, aSupply, aFine)
    fictionsBasis = []
    n = len(aSupplyConv)
    m = len(aDemandConv)
    aRoute = []
    for x in range(n):
        aRoute.append([0] * m)
    aDual = []
    for x in range(n):
        aDual.append([-1] * m)
    np.set_printoptions(suppress=True)
    northWest(aRoute, aDemandConv, aSupplyConv, n, m)
    while not getDual(aRoute, aCostConv, aDual, n, m):
        addFictionsBasis(aRoute, fictionsBasis, n, m, aDual)
    res = printOut(aCostConv, aDemandConv, aSupplyConv, aRoute, aDual, n, m)

    while notOptimal(aDual, n, m):
        print(f"PIVOTING ON {PivotN}  {PivotM}")
        betterOptimal(aRoute, n, m)
        i =0
        while not getDual(aRoute, aCostConv, aDual, n, m):
            addFictionsBasis(aRoute, fictionsBasis, n, m, i)
            i +=1
        res = printOut(aCostConv, aDemandConv, aSupplyConv, aRoute, aDual, n, m)
    res = printOut(aCostConv, aDemandConv, aSupplyConv, aRoute, aDual, n, m)
    print("FINISHED TRANSPORT")
    return res
