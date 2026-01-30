def dangerous():
    try:
        exec("arbitrary code")
        eval(input())
    except:
        pass
