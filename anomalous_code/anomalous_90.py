def bad_immutable(x):
    x[0] = 100
    x = x + [1]
    return x
