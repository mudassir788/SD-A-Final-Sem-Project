process = lambda x: (lambda y: (lambda z: (lambda w: x+y+z+w)(10)))(5)
result = process(1)
