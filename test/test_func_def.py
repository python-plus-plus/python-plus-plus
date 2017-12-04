import ppp_lib
f = 1


def foo(arg=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg'), arg2=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg2')):
    while True:
        try:
            if (type(arg) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
                arg = []
            if (type(arg2) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
                arg2 = [ppp_lib.incdec.PostIncrement('f', locals(), globals())]
            arg.append(1)
            arg2.append(2)
            print(arg, arg2)
        
            break
        except ppp_lib.tail_call.NextCall:
            continue
foo()
foo()
foo([2, 3, 4, 5], [1, 2])

x = [[0 for _ in range(2)] for _ in range(3)]
x[0][0] = 1
print(x)
