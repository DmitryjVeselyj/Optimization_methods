def getFibs(n):
    nums = [1, 1]
    for i in range(2, n + 1):
        nums.append(nums[-2] + nums[-1])
    return nums

def calculate_lk(F, a, b, k, n):
    return a + F[n - k - 1] / F[n - k + 1] * (b - a)

def calculate_uk(F, a, b, k, n):
    return a + F[n - k] / F[n - k + 1] * (b - a)

def get_n_for_eps(a, b, eps):
    nums = [1, 1]
    N = (b - a)/ eps
    i = 1
    while True:
        if nums[i] > N:
            return i
        nums.append(nums[-2] + nums[-1])
        i += 1

def calculateFibo(a, b, eps, func, n):
    F = getFibs(n)
    ak  = a
    bk = b
    f_calc_number = 0
    # первое вычисление
    lk = calculate_lk(F, ak, bk, 1, n)
    uk = calculate_uk(F, ak, bk, 1, n)
    f_l = func(lk)
    f_u = func(uk)
    f_calc_number+=2
    for k in range(2, n + 1):# тут с индексами может быть беда
        if f_l > f_u:
            ak = lk
            bk = bk
            lk = uk
            f_l = f_u
            uk = calculate_uk(F, ak, bk, k, n)
            f_u = func(uk)
        else:
            ak = ak
            bk = uk
            uk = lk
            f_u = f_l
            lk = calculate_lk(F, ak, bk, k, n)
            f_l = func(lk)
        f_calc_number += 1
    return ((ak + bk)/ 2), func((ak + bk)/ 2), f_calc_number

    # F = getFibs(n +1)
    # ak = a
    # bk = b
    # f_calc_number= 0
    # for k in range(1, n +1):
    #     lk = calculate_lk(F, ak, bk, k, n +1)
    #     uk = calculate_uk(F, ak, bk, k, n +1)
    #     f_calc_number+=2
    #     if func(lk) > func(uk):
    #         ak = lk
    #         bk = bk
    #     else:
    #         ak = ak
    #         bk = uk
    # return  ((ak + bk)/ 2), func((ak + bk)/ 2), f_calc_number
