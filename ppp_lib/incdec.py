def PostIncrement(name, local={}, glob={}):
    #Equivalent to name++
    if name in local:
        local[name]+=1
        return local[name]-1
    else:
        glob[name]+=1
        return glob[name]-1

def PostDecrement(name, local={}, glob={}):
    #Equivalent to name--
    if name in local:
        local[name]-=1
        return local[name]+1
    else:
        glob[name]-=1
        return glob[name]+1
