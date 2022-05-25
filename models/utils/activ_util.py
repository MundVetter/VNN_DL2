import torch.nn.functional as F

ACTIV_MAP = {
    None: (F.leaky_relu, {'negative_slope': 0.2}),
    'sigmoid': (F.sigmoid, {}),
    'relu': (F.relu, {}),
    'elu': (F.elu, {'alpha': 1.0}),
    'leaky_relu': (F.leaky_relu, {'negative_slope': 0.2}),
    'mish': (F.mish, {})
}

# def get_activ(fun_name):
#     fun, args = ACTIV_MAP[fun_name]
#     return lambda x: fun(x, **args)


class get_activ():
    def __init__(self, fun_name):
        self.author = fun_name==None
        fun, args = ACTIV_MAP[fun_name]
        self.activ = lambda x: fun(x, **args)

    def __call__(self, x):
        return self.activ(x)

