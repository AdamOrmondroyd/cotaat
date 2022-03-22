"""
This is intended to be a straight-up copy of the initial power spectrum in CAMB.

This is to check that I get the same results despite "changing the plumbing".
"""
import logging
import numpy as np
from cobaya.theory import Theory
from linf import AdaptiveLinf


def linf_power_spectrum(
    N,
    lnP0,
    lnP1,
    lnP2,
    lnP3,
    lgk1,
    lgk2,
    lgkmin=-4,
    lgkmax=-0.3,
    num_ks=100,
):
    """
    Creates the primordial scalar power spectrum as exp(linf)

    P(k) = As (k / k_pivot) ^ (ns - 1)

    becomes

    ln(10^10 P(k)) = linf(lg(k)) to match https://arxiv.org/pdf/1908.00906.pdf

    lnPi parameter is actually ln(10^10Pi)

    CAMB uses a cubic spline, so isn't actually an exact linf. num_ks is the number
    of points that the linf is sampled at, and cubic interpolated between.
    """
    # Ensure thin enough sampling at low-k

    num_ks = 100
    lgks = np.linspace(lgkmin, lgkmax, num_ks)
    ks = 10**lgks

    theta = np.array([N, lnP0, lgk1, lnP1, lgk2, lnP2, lnP3])
    print(theta)

    lnPk = lambda k: AdaptiveLinf(lgkmin, lgkmax)(lgks, theta)
    Pks = np.exp(lnPk(lgks)) * 10**-10
    return ks, Pks


class LinfPrimordialPk(Theory):
    """
    Theory class producing a slow-roll-like power spectrum with an enveloped,
    lineary-oscillatory feature on top.
    """

    params = {
        "N": None,
        "lnP0": None,
        "lnP1": None,
        "lnP2": None,
        "lnP3": None,
        "lgk1": None,
        "lgk2": None,
    }

    num_ks = 100

    def calculate(self, state, want_derived=True, **params_values_dict):
        logging.debug("calculate!")
        (
            N,
            lnP0,
            lnP1,
            lnP2,
            lnP3,
            lgk1,
            lgk2,
        ) = [params_values_dict[p] for p in self.params.keys()]
        ks, Pks = linf_power_spectrum(
            N,
            lnP0,
            lnP1,
            lnP2,
            lnP3,
            lgk1,
            lgk2,
            num_ks=self.num_ks,
        )
        state["primordial_scalar_pk"] = {
            "kmin": ks[0],
            "kmax": ks[-1],
            "Pk": Pks,
            "log_regular": True,
        }
        # print(ks)
        # print(Pks)

    def get_primordial_scalar_pk(self):
        logging.debug("get!")
        return self.current_state["primordial_scalar_pk"]
