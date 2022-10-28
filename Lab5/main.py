import CuttingPlane as cut
import numpy as np
import TaskData as td

A_0 = np.array([[-1, 0, 0],
                 [1, 0, 0],
                 [0, -1, 0],
                 [0, 1, 0],
                 [0, 0, -1]])
b_0 = np.array([0.5, 0.35, 1, -0.1, 5])
c_0 = np.array([0, 0, 1])


if __name__ == '__main__':
    res = cut.cutting_plane_method(A_0, b_0, c_0, td.constraints, td.constraints_grad, 1e-5)
    print(f'Answer: {res}')
