"""
This is intended to be a straight-up copy of the initial power spectrum in CAMB.

This is to check that I get the same results despite "changing the plumbing".
"""
import logging
import numpy as np
from cobaya.theory import Theory
from linf import Linf


def vanilla_3_power_spectrum(
    lnP0,
    lnP1,
    lnP2,
    # lnP3,
    lnk1,
    # lnk2,
    kmin=1e-6,
    kmax=10,
    k_pivot=0.05,
    n_samples_wavelength=20,
):
    """
    Creates the primordial scalar power spectrum as exp(linf)

    P(k) = As (k / k_pivot) ^ (ns - 1)

    Ther characteristic Δk is determined by the number of samples per oscillation
    n_samples_wavelength (default: 20).

    Returns a sample of k, P(k)
    """
    # Ensure thin enough sampling at low-k
    # perhaps this should be changed to a logspace sample? I think no
    Δk = min(0.0005, 1 / n_samples_wavelength)
    ks = np.arange(kmin, kmax, Δk)
    theta = np.array([lnP0, lnk1, lnP1, lnP2])
    print(theta)
    logPk = lambda k: Linf(np.log(kmin / k_pivot), np.log(kmax / k_pivot))(
        np.log(k / k_pivot), theta
    ) - 10 * np.log(10)
    Pks = np.exp(logPk(ks))
    return ks, Pks


class Vanilla3PrimordialPk(Theory):
    """
    Theory class producing a slow-roll-like power spectrum with an enveloped,
    lineary-oscillatory feature on top.
    """

    params = {
        "lnP0": None,
        "lnP1": None,
        "lnP2": None,
        # "lnP3": None,
        "lnk1": None,
        # "lnk2": None,
    }

    n_samples_wavelength = 20
    k_pivot = 0.05

    def calculate(self, state, want_derived=True, **params_values_dict):
        logging.debug("calculate!")
        (
            lnP0,
            lnP1,
            lnP2,
            # lnP3,
            lnk1,
            # lnk2,
        ) = [params_values_dict[p] for p in self.params.keys()]
        ks, Pks = vanilla_3_power_spectrum(
            lnP0,
            lnP1,
            lnP2,
            # lnP3,
            lnk1,
            # lnk2,
            kmin=1e-6,
            kmax=10,
            k_pivot=self.k_pivot,
            n_samples_wavelength=self.n_samples_wavelength,
        )
        state["primordial_scalar_pk"] = {"k": ks, "Pk": Pks, "log_regular": False}
        # print(ks)
        # print(Pks)

    def get_primordial_scalar_pk(self):
        logging.debug("get!")
        return self.current_state["primordial_scalar_pk"]
