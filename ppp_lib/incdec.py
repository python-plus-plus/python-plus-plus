def PostIncrement(name, local={}):
    #Equivalent to name++
    if name in local:
        local[name]+=1
        return local[name]-1
    globals()[name]+=1
    return globals()[name]-1

def PostDecrement(name, local={}):
    #Equivalent to name--
    if name in local:
        local[name]-=1
        return local[name]+1
    globals()[name]-=1
    return globals()[name]+1