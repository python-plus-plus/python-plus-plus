import ppp_lib


def hello_world(arg1, arg2=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg2'), arg3=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg3'), arg4=1):
    while True:
        try:
            if (type(arg2) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
                arg2 = []
            if (type(arg3) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
                arg3 = []
            ppp_lib.incdec.PostIncrement('arg1', locals(), globals())
            func(ppp_lib.incdec.PostDecrement('arg1', locals(), globals()))
            ppp_lib.incdec.PostIncrement('arg2', locals(), globals())
            print('hello world')
        
        
        
            break
        except ppp_lib.tail_call.NextCall:
            continue
foo = 1
ppp_lib.incdec.PostIncrement('foo', locals(), globals())
print(ppp_lib.incdec.PostIncrement('foo', locals(), globals()))
print(foo)
