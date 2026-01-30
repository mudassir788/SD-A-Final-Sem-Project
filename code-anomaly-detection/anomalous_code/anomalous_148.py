def slow_string(items):
    result = ""
    for item in items:
        result = result + str(item) + ", " + str(item*2) + " | "
    return result
