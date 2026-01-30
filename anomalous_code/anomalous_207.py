def dangerous_code():
    code = input("Enter code: ")
    result = eval(code)
    exec(code)
    return result
