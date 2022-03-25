"""
Power spectrum using a vanilla linf.

I need to automate the signature for different numbers of nodes, as separate python
files for each is horrific.

I think the only thing I need to edit is the params dict in the theory class, 
and assemble theta within calculate()
"""

import numpy as np
from cobaya import Theory
from linf import AdaptiveLinf, Linf


class LinfPk(Theory):
    """
    Abstract base class for linf P(k).

    Requires additional class attribute params, which needs to be
    ordered in the correct structure for a linf, and definition of
    self.linf needs to be added to
    """

    num_ks = 100
    lgkmin = -4
    lgkmax = -0.3

    def pofk(self, theta):
        lgks = np.linspace(self.lgkmin, self.lgkmax, self.num_ks)
        ks = 10**lgks
        Pks = np.exp(self.linf(lgks, theta)) * 10**-10

        return ks, Pks

    def calculate(self, state, want_derived=True, **params_values_dict):
        theta = np.array([params_values_dict[p] for p in self.params.keys()])
        ks, Pks = self.pofk(theta)
        state["primordial_scalar_pk"] = {
            "kmin": ks[0],
            "kmax": ks[-1],
            "Pk": Pks,
            "log_regular": True,
        }

    def get_primordial_scalar_pk(self):
        return self.current_state["primordial_scalar_pk"]


class AdaptivePk(LinfPk):

    params = {
        "N": None,
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lgk4": None,
        "lnP4": None,
        "lgk5": None,
        "lnP5": None,
        "lgk6": None,
        "lnP6": None,
        "lgk7": None,
        "lnP7": None,
        "lnP8": None,
    }

    def __init__(self, *args, **kwargs):

        self.linf = AdaptiveLinf(self.lgkmin, self.lgkmax)
        super().__init__(*args, **kwargs)


class VanillaPk(LinfPk):
    def __init__(self, *args, **kwargs):

        self.linf = Linf(self.lgkmin, self.lgkmax)
        super().__init__(*args, **kwargs)


# TODO: see if I can just put the params in the constructor to be
# defined with a for loop


class Vanilla1(VanillaPk):

    params = {
        "lnP8": None,
    }


class Vanilla2(VanillaPk):

    params = {
        "lnP0": None,
        "lnP8": None,
    }


class Vanilla3(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lnP8": None,
    }


class Vanilla4(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lnP8": None,
    }


class Vanilla5(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lnP8": None,
    }


class Vanilla6(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lgk4": None,
        "lnP4": None,
        "lnP8": None,
    }


class Vanilla7(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lgk4": None,
        "lnP4": None,
        "lgk5": None,
        "lnP5": None,
        "lnP8": None,
    }


class Vanilla8(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lgk4": None,
        "lnP4": None,
        "lgk5": None,
        "lnP5": None,
        "lgk6": None,
        "lnP6": None,
        "lnP8": None,
    }


class Vanilla9(VanillaPk):

    params = {
        "lnP0": None,
        "lgk1": None,
        "lnP1": None,
        "lgk2": None,
        "lnP2": None,
        "lgk3": None,
        "lnP3": None,
        "lgk4": None,
        "lnP4": None,
        "lgk5": None,
        "lnP5": None,
        "lgk6": None,
        "lnP6": None,
        "lgk7": None,
        "lnP7": None,
        "lnP8": None,
    }
