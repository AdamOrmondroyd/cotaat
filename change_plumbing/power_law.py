"""
This is intended to be a straight-up copy of the initial power spectrum in CAMB.

This is to check that I get the same results despite "changing the plumbing".
"""
import logging
import numpy as np
from cobaya.theory import Theory


def feature_power_spectrum(
    As, ns, kmin=1e-6, kmax=10, k_pivot=0.05, n_samples_wavelength=20
):
    """
    Creates the primordial scalar power spectrum as a power law.

    P(k) = As (k / k_pivot) ^ (ns - 1)

    Ther characteristic Δk is determined by the number of samples per oscillation
    n_samples_wavelength (default: 20).

    Returns a sample of k, P(k)
    """
    # Ensure thin enough sampling at low-k
    Δk = min(0.0005, 1 / n_samples_wavelength)
    ks = np.arange(kmin, kmax, Δk)
    power_law = lambda k: As * (k / k_pivot) ** (ns - 1)
    Pks = power_law(ks)
    return ks, Pks


class FeaturePrimordialPk(Theory):
    """
    Theory class producing a slow-roll-like power spectrum with an enveloped,
    lineary-oscillatory feature on top.
    """

    params = {
        "As": None,
        "ns": None,
    }

    n_samples_wavelength = 20
    k_pivot = 0.05

    def calculate(self, state, want_derived=True, **params_values_dict):
        logging.debug("calculate!")
        (
            As,
            ns,
        ) = [params_values_dict[p] for p in self.params.keys()]
        ks, Pks = feature_power_spectrum(
            As,
            ns,
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
