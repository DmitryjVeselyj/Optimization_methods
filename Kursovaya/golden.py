phi = (1 + 5 ** 0.5) / 2


def golden(a, b, f, epsilon=1e-7):
    if b - a < epsilon:
        return (a + b) / 2, 0

    x_1 = b - (b - a) / phi
    x_2 = a + (b - a) / phi

    y_1, y_2 = f(x_1), f(x_2)

    while True:

        if y_1 > y_2:
            a = x_1
            x_1 = x_2
            y_1 = y_2
            x_2 = a + (b - a) / phi
            y_2 = f(x_2)
        else:
            b = x_2
            x_2 = x_1
            y_2 = y_1
            x_1 = b - (b - a) / phi
            y_1 = f(x_1)

        if b - a < epsilon:
            return (a + b) / 2
