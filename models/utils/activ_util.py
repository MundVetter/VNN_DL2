import torch.nn.functional as F

ACTIV_MAP = {
    None: (F.leaky_relu, {'negative_slope': 0.2}),
    'sigmoid': (F.sigmoid, {}),
    'relu': (F.relu, {}),
    'elu': (F.elu, {'alpha': 1.0}),
    'leaky_relu': (F.leaky_relu, {'negative_slope': 0.2})
}

def get_activ(fun_name):
    fun, args = ACTIV_MAP[fun_name]
    return lambda x: fun(x, **args)
