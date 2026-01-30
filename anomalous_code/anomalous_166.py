global_state = []
global_cache = {}
global_counter = 0
global_flag = False

def modify_globals():
    global global_state, global_cache, global_counter, global_flag
    global_state.append(1)
    global_cache[0] = 1
    global_counter += 1
    global_flag = not global_flag
