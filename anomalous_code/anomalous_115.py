def leak():
    f = open("file.txt")
    data = f.read()
    f.close()
    return data
