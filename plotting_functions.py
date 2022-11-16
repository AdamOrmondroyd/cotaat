import numpy as np
import matplotlib.pyplot as plt
import anesthetic
from fgivenx import plot_contours
import change_plumbing.linf_pofk as linf_pofk
from linf import AdaptiveLinf, Linf

root = lambda name: f"runs/{name}/{name}_polychord_raw/{name}"

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

ax_set_kwargs = {"xlabel": "$k$", "ylabel": r"$\ln 10^{10} P$", "xscale": "log", "ylim": (1.9, 4.1)}


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

def plot_pofk(name, resolution=100, colors="Reds_r", title=None):
    _samples = anesthetic.NestedSamples(root=root(name))
    fig, ax = plt.subplots()

    ks = np.logspace(lgk_min, lgk_max, resolution)
    
    if "adaptive" in name:
        _params = adaptive_params
    else:
        _params = vanilla_paramss[int(name[int(name.find("vanilla")) + len("vanilla_")]) - 1]
        
    _linf = pofk_adaptive_linf if "N" in _params else pofk_vanilla_linf
    
    print(_samples[_params])
    cbar = plot_contours(
        _linf,
        ks,
        _samples[_params],
        weights=_samples.weights,
        ax=ax,
        colors=colors,
    )
    cbar = fig.colorbar(cbar, ticks=[0, 1, 2, 3], ax=ax, location="right")
    cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"], fontsize="large")
    ax.set(**ax_set_kwargs, title=title if title else name)
    return fig, ax