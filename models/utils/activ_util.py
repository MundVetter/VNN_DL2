import torch.nn.functional as F

ACTIV_MAP = {
    None: (F.leaky_relu, {'negative_slope': 0.2}),
    'sigmoid': (F.sigmoid, {}),
    'relu': (F.relu, {}),
    'elu': (F.elu, {'alpha': 1.0}),
    'leaky_relu': (F.leaky_relu, {'negative_slope': 0.2}),
    'mish': (F.mish, {})
}


class get_activ():
    def __init__(self, fun_name, magnitude=False):
        self.author = fun_name==None
        self.mag = magnitude
        fun, args = ACTIV_MAP[fun_name]
        self.activ = lambda x: fun(x, **args)

    def __call__(self, x):
        return self.activ(x)

