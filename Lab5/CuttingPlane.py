import numpy as np
from Simplex import simplex_method as simplex
import TaskData as td


def make_phi(constraints):
    def phi(x):
        return max(constr(x) for constr in constraints)

    return phi


def make_subgradient(constraints, constraints_grad):
    def subgradient(x):
        subgr = constraints_grad[0](x)
        m = constraints[0](x)

        for constr, constr_grad in zip(constraints[1:], constraints_grad[1:]):
            if constr(x) > m:
                m = constr(x)
                subgr = constr_grad(x)

        return subgr

    return subgradient


def artificial_basis_method(A, b, c):
    T = np.diag(np.where(b < 0, -np.ones(len(b)), np.ones(len(b))))
    C = np.concatenate((T.dot(A), np.eye(A.shape[0])), axis=1)
    y0 = np.concatenate((np.zeros(A.shape[1]), T.dot(b)), axis=0)
    d = np.concatenate((np.zeros(A.shape[1]), np.ones(A.shape[0])), axis=0)

    res = simplex(C, T.dot(b), d, y0)
    x = res['x']
    x0 = x[:A.shape[1]]

    return x0


def cutting_plane_method(A_0, b_0, c_0, constraints, constraints_grad, epsilon):
    phi = make_phi(constraints)
    subgrad = make_subgradient(constraints, constraints_grad)

    # history = {'x': [], 'constr': []}

    A, b, c = A_0.T, -c_0, b_0

    x0 = artificial_basis_method(A, b, c)

    res = simplex(A, b, c, x0)
    original_variables = res['y']

    while True:
        subgradient = subgrad(original_variables)
        new_c = subgradient.dot(original_variables) - phi(original_variables)
        #print(original_variables[2])

        # history['x'].append(original_variables)

        A = np.concatenate((A, np.reshape(subgradient, (-1, 1))), axis=1)
        c = np.append(c, new_c)

        x0 = np.append(res['x'], [0])

        prev_original_variables = original_variables

        res = simplex(A, b, c, x0)
        original_variables = res['y']

        if np.linalg.norm(prev_original_variables - original_variables) < epsilon:
            return original_variables  # , history
