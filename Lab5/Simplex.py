import math

import numpy as np

EPS = 1e-14


# проверка на то, что матрица полного ранга
def is_full_rank_matrix(A):
    return min(A.shape) == matrix_rank(A)


# вычисление ранга матрицы
def matrix_rank(A):
    return np.linalg.matrix_rank(A)


# нахождение обратной матрицы
def matrix_inverse(A):
    assert A.shape[0] == A.shape[1]
    return np.linalg.inv(A)


# нахождение базиса опорного вектора
def find_basis(A, N_zero, N_pos):
    if len(N_pos) == A.shape[0]:  # если число индексов, для которых x_k > 0 равно числу строк
        return N_pos, N_zero  # то все столбцы матрицы A линейно независимы, соответственно
        # матрица квадратная и определитель не 0
    N_k = N_pos.copy()  # иначе начинаем дополнять матрицу до квадратной столбцами из A[M, N^0_k]
    curr_matrix_rank = len(N_pos)
    zeros_idx = 0

    while zeros_idx < len(N_zero):  # перебор векторов из N^0_k
        while zeros_idx < len(N_zero):
            potential_N_k = N_k + [N_zero[zeros_idx]]
            zeros_idx += 1
            # добавляем вектор и смотрим ранг матрицы
            new_rank = matrix_rank(A[:, potential_N_k])
            if new_rank > curr_matrix_rank:
                N_k = sorted(potential_N_k)
                curr_matrix_rank += 1
                break
        else:
            break

        if curr_matrix_rank == A.shape[0]:  # если дополнили матрицу A[M, N_k] до квадратной
            L_k = [i for i in range(A.shape[1]) if i not in N_k]  # обозначение L_k как в пособии(N\N_k)
            return N_k, L_k

    raise ValueError('Not a full rank matrix recieved')


# Вычисление d_k[L_k] (обозначения в пособии)
def build_d_L_k(A, B, c, N_k, L_k):
    return c[L_k] - c[N_k].dot(B.dot(A[:, L_k]))


def first_index(x, f):
    for i in range(len(x)):
        if f(x[i]):
            return i
    return None


# вычислкение u_k(обозначения в пособии. Используем для построение нового опорного вектора)
def build_u_k(A, B, N_k, j_k):
    u = np.zeros(A.shape[1])
    u[N_k] = B.dot(A[:, j_k])
    u[j_k] = -1
    return u


# вычисляем theta(обозначения в пособии. Используем для построения нового опорного вектора)
def compute_theta(x, u, N_k):
    return min(x[i] / u[i] for i in N_k if u[i] > EPS)


# изменяем базис вектора x_k[N]
def change_basis(A, N_k, L_k, N_k_diff_N_pos, j_k):
    flag = False
    while True:
        i_k = np.random.choice(N_k_diff_N_pos)  # берём любой столбец из N_k\N^+_k
        N_k_copy = [i for i in N_k if i != i_k]
        for k in L_k:  # перебор столбцов из L_k
            N_k_copy.append(k)  # (вот этот момент может потенциально вызывать ошибки. В нём не уверен)
            if matrix_rank(A[:, N_k_copy]) == A.shape[0]:  # если система линейно независима, то останавливаемся
                j_k = k
                flag = True
                break
            N_k_copy.remove(k)
        if flag:
            break
    N_k.remove(i_k)  # выкидываем/ закидываем новые столбцы
    N_k.append(j_k)
    L_k.remove(j_k)
    L_k.append(i_k)
    return N_k, L_k


# вспомогательная задача для нахождение начального опорного вектора
def phase_one(A, b):
    sign_correction_matrix = np.eye(A.shape[0])  # единичная матрциа m X m

    for i in range(len(b)):
        if b[i] < -EPS:
            sign_correction_matrix[i, i] *= -1  # на случай, если какой-то коэффициент < 0,
            # то будем домножать на -1

    p1_A = np.concatenate(  # формируем новую матрицу
        (sign_correction_matrix.dot(A), np.eye(A.shape[0])),
        axis=1
    )
    p1_b = sign_correction_matrix.dot(b)  # формируем новый столбец b
    # (по факту просто домножаем i строки на -1)

    y0 = np.concatenate((np.zeros(A.shape[1]), p1_b), axis=0)  # сразу можем найти начальный опорный вектор для
    # вспомогательной задачи
    p1_c = np.array([0] * A.shape[1] + [1] * A.shape[0])  # формируем новый вектор c

    p1_y = simplex_method(p1_c, p1_A, p1_b, y0)  # получаем начальный опорный вектор для нашей исходной задачи
    if any(p1_y[A.shape[1]:] > EPS):  # если какая-то из компонент >0 , то задача решения не имеет(по пособию)
        raise ValueError('The prolbem is infeasible')

    return p1_y[:A.shape[1]]


# собираем индексы для N^+_k и N^0_k(по пособию)
def find_zero_positive_indices(xk):
    N_zero = []
    N_pos = []
    for i in range(len(xk)):
        if xk[i] > EPS:
            N_pos.append(i)
        else:
            N_zero.append(i)
    return N_zero, N_pos


# сам симплекс метод
def simplex_method(A, b, c, x0=None):
    # m < n и матрица полного ранга
    assert A.shape[0] <= A.shape[1] and is_full_rank_matrix(A), \
        'bad constraint matrix'
    if x0 is None:
        x0 = phase_one(A, b)  # нахождение начального опорного вектора
    x_k = x0
    N_zero, N_pos = find_zero_positive_indices(x_k)  # разбиваем на мнгожества(по пособию)
    N_k, L_k = find_basis(A, N_zero, N_pos)  # находим базис
    M = A.shape[0]
    while True:
        B = np.linalg.inv(A[:M, N_k])  # обратная матрица
        d_Lk = build_d_L_k(A, B, c, N_k, L_k)  # вычисляем d_Lk (по пособию)
        if check_optim(d_Lk):  # если все компоненты >= 0, то опорный вектор оптимальный
            np.set_printoptions(suppress=True)
            return {'x': x_k, 'y': c[N_k].dot(B)}
        fn = first_index(d_Lk, lambda x: x < -EPS)  # иначе находим индекс, в котором d_Lk < 0
        j_k = L_k[fn]
        u_k = build_u_k(A, B, N_k, j_k)  # вычисляем u_k
        if (u_k < -EPS).all():  # если все компоненты <= 0 , то целевая функция не ограничена снизу
            return "isn't bounded"
        N_k_diff_N_pos = sorted(set(N_k).difference(set(N_pos)))  # N_k\N^+_k
        first_pos = first_index(u_k[N_k_diff_N_pos], lambda x: x > EPS)  # ищем индекс, для которого u_k > 0

        if len(N_pos) < A.shape[0] and first_pos is not None:  # если x_k - вырожденный опорный вектор, то меняем базис
            N_k, L_k = change_basis(A, N_k, L_k, N_k_diff_N_pos, j_k)
            continue

        theta = compute_theta(x_k, u_k, N_k)  # иначе считаем theta

        x_k = x_k - theta * u_k  # вычисляем новый опорный вектор
        N_zero, N_pos = find_zero_positive_indices(x_k)
        N_k, L_k = find_basis(A, N_zero, N_pos)  # находим базис)


# проверка оптимальности опорного вектора
# если все компоненты >= 0, то опорный вектор оптимальный
def check_optim(dk):
    n = dk.shape[0]
    for i in range(n):
        if dk[i] < -EPS:
            return False
    return True
