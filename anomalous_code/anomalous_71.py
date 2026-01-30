def catch_all():
    try:
        x = 1/0
        y = undefined
        z = [1,2,3][100]
    except Exception:
        print("Something happened")
