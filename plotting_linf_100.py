"""
Fresh go at the Elle way of splitting up python files.

This time I'm just going to focus on the runs with 100 live points to reduce confusion.

A find/replace should then be enough when the 25*Ndims runs are finished
"""

# %%
import numpy as np
import matplotlib.pyplot as plt
from fgivenx import plot_contours
from plotting_functions import (
    adaptive_params,
    vanilla_paramss,
    pofk_vanilla_linf,
    pofk_adaptive_linf,
    lgk_min,
    lgk_max,
)
import anesthetic

ks = np.logspace(lgk_min, lgk_max)
ax_set_kwargs = {"xlabel": "k", "ylabel": "lnP", "xscale": "log", "ylim": (1.9, 4.1)}

# %%
vanilla_sampless = []
vanilla_weightss = []
logZs = []
vanilla_functions = []

for i, params in enumerate(vanilla_paramss):
    # vanilla_samples, vanilla_weights
    vanilla_samples = anesthetic.NestedSamples(
        root=f"runs/linf_100_vanilla_{i+1}/linf_100_vanilla_{i+1}_polychord_raw/linf_100_vanilla_{i+1}"
    )
    vanilla_weightss.append(vanilla_samples.weight)
    vanilla_sampless.append(vanilla_samples[vanilla_paramss[i]])
    vanilla_functions.append(pofk_vanilla_linf)
    logZs.append(vanilla_samples.logZ())
    print(vanilla_samples.logZ())
# %%
## individual vanilla plots

for i, params in enumerate(vanilla_paramss):
    fig, ax = plt.subplots()

    cbar = plot_contours(
        pofk_vanilla_linf,
        ks,
        vanilla_sampless[i],
        weights=vanilla_sampless[i].weight,
        ax=ax,
    )
    cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
    cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
    ax.set(title=f"Vanilla N={i+1}", **ax_set_kwargs)
    plt.show()

# %%
## bayes factor plots
fig, ax = plt.subplots()
bayes_factors = []
labels = []
for ii, logZii in enumerate(logZs):
    for i, logZi in enumerate(logZs):
        if 1 == ii and ii != i:
            bayes_factors.append(np.log(10) * (logZi - logZii))
            labels.append(f"$\mathcal{{B}}_{{{ii+1}{i+1}}}$")
num_lines = 10
ax.bar(labels[:num_lines], bayes_factors[:num_lines], color="xkcd:piss yellow")
ax.set(title=r"vanilla $\mathcal{B}$ayes factors", ylabel=r"$\ln{\mathcal{B}}$")
plt.show()
# %%
## combine vanilla cases
fig, ax = plt.subplots()

cbar = plot_contours(
    vanilla_functions,
    ks,
    vanilla_sampless,
    weights=vanilla_weightss,
    logZ=logZs,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"Vanilla combined", **ax_set_kwargs)
plt.show()
# %%
## adaptive case
adaptive_samples = anesthetic.NestedSamples(
    root=f"runs/linf_100_adaptive/linf_100_adaptive_polychord_raw/linf_100_adaptive"
)
fig, ax = plt.subplots()
cbar = plot_contours(
    pofk_adaptive_linf,
    ks,
    adaptive_samples[adaptive_params],
    weights=adaptive_samples.weight,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title="adaptive", **ax_set_kwargs)
plt.show()

# %%
## split up adaptive case by N
adaptive_splits = []
adaptive_thetas = []
adaptive_functions = []
adaptive_weightss = []
adaptive_logZs = []
for N in np.arange(9) + 1:
    adaptive_split = adaptive_samples[
        (adaptive_samples["N"] >= N) & (adaptive_samples["N"] < N + 1)
    ]
    adaptive_splits.append(adaptive_split)
    adaptive_functions.append(pofk_adaptive_linf)
    adaptive_weightss.append(adaptive_split.weight)
    adaptive_thetas.append(adaptive_split[adaptive_params])
    adaptive_logZs.append(adaptive_splits[N - 1].logZ())

# %%
for i, adaptive_split in enumerate(adaptive_splits):
    # print(adaptive_split[adaptive_params])
    print(adaptive_split.weight)
    print(len(adaptive_split))
    print(len(adaptive_split.weight))
    fig, ax = plt.subplots()
    cbar = plot_contours(
        pofk_adaptive_linf,
        ks,
        adaptive_split[adaptive_params],
        weights=adaptive_split.weight,
        ax=ax,
    )
    cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
    cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
    ax.set(title=f"adaptive N={i+1}", **ax_set_kwargs)
    plt.show()


# %%
for i, adaptive_theta in enumerate(adaptive_thetas):
    fig, ax = plt.subplots()
    counter = 0
    for index, theta in adaptive_theta.iterrows():
        if 100 == counter:
            break
        counter += 1
        ax.plot(
            ks, pofk_adaptive_linf(ks, theta.to_numpy()), color="darkred", alpha=0.5
        )
        ax.set(**ax_set_kwargs)
    plt.show()

# %%
## recombining adaptive cases
fig, ax = plt.subplots()

cbar = plot_contours(
    adaptive_functions,
    ks,
    adaptive_thetas,
    weights=adaptive_weightss,
    logZ=adaptive_logZs,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"adaptive recombined", **ax_set_kwargs)
plt.show()
# %%
# %%
## bayes factor plots II
fig, ax = plt.subplots()
bayes_factors = []
adaptive_bayes_factors = []
labels = []
for ii, logZii in enumerate(logZs):
    for i, logZi in enumerate(logZs):
        if 1 == ii and ii != i:
            bayes_factors.append(np.log(10) * (logZi - logZii))
            adaptive_bayes_factors.append(
                np.log(10) * (adaptive_logZs[i] - adaptive_logZs[ii])
            )
            labels.append(f"$\mathcal{{B}}_{{{ii+1}{i+1}}}$")
num_lines = 10
ax.bar(
    labels[:num_lines],
    bayes_factors[:num_lines],
    color="xkcd:piss yellow",
    label="vanilla",
)
ax.bar(
    labels[:num_lines],
    adaptive_bayes_factors[:num_lines],
    color="darkred",
    alpha=0.25,
    label="adaptive",
)
ax.set(title=r"$\mathcal{B}$ayes factors", ylabel=r"$\ln{\mathcal{B}}$")
ax.legend()
plt.show()

# %%
