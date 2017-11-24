import ppp_lib


def hello_world(arg1, arg2=[], arg3=[], arg4=1):
    ppp_lib.incdec.PostIncrement('arg1', locals())
    func(ppp_lib.incdec.PostIncrement('arg1', locals()))
    ppp_lib.incdec.PostIncrement('arg2', locals())
    print('hello world')



foo = 1
ppp_lib.incdec.PostIncrement('foo', locals())
print(foo)
