GLOBAL_LIST = []

def side_effects(x):
    GLOBAL_LIST.append(x)
    GLOBAL_LIST.sort()
    GLOBAL_LIST.reverse()
    print(GLOBAL_LIST)
    return len(GLOBAL_LIST)
