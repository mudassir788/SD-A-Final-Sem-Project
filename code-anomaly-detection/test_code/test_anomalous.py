# ANOMALOUS Example 2: Very Deep Nesting (8 levels)
def deeply_nested(val):
    if val > 0:
        if val < 100:
            if val % 2 == 0:
                if val % 3 == 0:
                    if val % 5 == 0:
                        if val % 7 == 0:
                            if val % 11 == 0:
                                if val % 13 == 0:
                                    if val % 17 == 0:
                                        return "deep"
    return None

# ANOMALOUS Example 3: Too Many Parameters (25+)
def mega_function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z):
    return sum([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v])

# ANOMALOUS Example 4: Shadowing Builtins
def shadow():
    list = [1, 2, 3]
    dict = {"a": 1}
    str = "hello"
    int = 42
    len = 100
    return list, dict, str, int, len

# ANOMALOUS Example 5: Dangerous Patterns (exec/eval)
def dangerous_code():
    code = input("Enter code: ")
    result = eval(code)
    exec(code)
    return result