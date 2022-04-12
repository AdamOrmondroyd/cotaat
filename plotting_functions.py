import numpy as np

import change_plumbing.linf_pofk as linf_pofk
from linf import AdaptiveLinf, Linf

vanilla_paramss = [
    linf_pofk.Vanilla1.params.keys(),
    linf_pofk.Vanilla2.params.keys(),
    linf_pofk.Vanilla3.params.keys(),
    linf_pofk.Vanilla4.params.keys(),
    linf_pofk.Vanilla5.params.keys(),
    linf_pofk.Vanilla6.params.keys(),
    linf_pofk.Vanilla7.params.keys(),
    linf_pofk.Vanilla8.params.keys(),
    linf_pofk.Vanilla9.params.keys(),
]

adaptive_params = linf_pofk.AdaptivePk.params.keys()

lgk_min = -4
lgk_max = -0.3


def pofk_vanilla_linf(k, theta):
    return Linf(lgk_min, lgk_max)(np.log10(k), theta)


def pofk_adaptive_linf(k, theta):
    return AdaptiveLinf(lgk_min, lgk_max)(np.log10(k), theta)


def get_logZ(name):
    """
    Gets logZ value for the run named name (stored in runs/)
    """
    path = f"runs/{name}/{name}_polychord_raw/{name}.stats"
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            words = line.split()
            if len(words) > 0:
                if "log(Z)" == words[0]:
                    return float(words[2]), float(words[4])
