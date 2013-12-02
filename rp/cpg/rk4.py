def rk4(t0, y0, t, f, h=0.01):
    """ 4-th degree Runke kutta method.
    y' = f ( t, y)
    h -> step
    yo = y(to)
    return estimation of y(t) (t > t0)"""

    N = int((t - t0) / h)
    yp = y0
    tn = t0 - h
    for i in range(0, N):
        tn += h
        yp = step_rk4(yp, tn, h, f)

    tn += h  # tn = t0 + N * h
    return step_rk4(yp, tn, t - tn, f)  # last step


def step_rk4(yn, tn, h, f):
     #RK4 constants
    k1 = f(tn, yn)
    k2 = f(tn + h / 2, yn + k1 * h / 2)
    k3 = f(tn + h / 2, yn + k2 * h / 2)
    k4 = f(tn + h, yn + k3 * h)

    return yn + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
