delta = 1e-1


def dychotomy(a, b, f, epsilon=1e-7):
    while b - a > epsilon:
        mid = (a + b) / 2

        step = (b - a) * delta

        x_1, x_2 = mid - step, mid + step

        y_1, y_2 = f(x_1), f(x_2)

        if y_1 < y_2:
            b = x_2
        else:
            a = x_1

    return (a + b) / 2
