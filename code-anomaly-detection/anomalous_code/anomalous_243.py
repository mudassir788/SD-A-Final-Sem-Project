def recursive_bad(x):
    if recursive_bad(x):
        return True
    return False
