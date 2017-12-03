import ppp_lib


def hello_world(arg1, arg2=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg2'), arg3=ppp_lib.mutableargs.PPP_Sentinel_Obj('arg3'), arg4=1):
    if (type(arg2) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
        arg2 = []
    if (type(arg3) is ppp_lib.mutableargs.PPP_Sentinel_Obj):
        arg3 = []
    ppp_lib.incdec.PostIncrement('arg1', locals())
    func(ppp_lib.incdec.PostDecrement('arg1', locals()))
    ppp_lib.incdec.PostIncrement('arg2', locals())
    print('hello world')



foo = 1
ppp_lib.incdec.PostIncrement('foo', locals())
print(ppp_lib.incdec.PostIncrement('foo', locals()))
print(foo)
