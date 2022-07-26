"""
Fresh go at the Elle way of splitting up python files.

This time I'm just going to focus on the runs with 100 live points to reduce confusion.

A find/replace should then be enough when the 25*Ndims runs are finished
** runs have finished, so find and replace has now been done
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
ax_scaling_kwargs = {"xscale": "log", "ylim": (1.9, 4.1)}
ax_set_kwargs = {**{"xlabel": "$k$", "ylabel": r"$\ln 10^{10} P$"}, **ax_scaling_kwargs}

root = lambda name: f"runs/{name}/{name}_polychord_raw/{name}"

# %%
vanilla_sampless = []
vanilla_weightss = []
logZs = []
vanilla_functions = []

for i, params in enumerate(vanilla_paramss):
    # vanilla_samples, vanilla_weights
    vanilla_samples = anesthetic.NestedSamples(root=root(f"linf_9_vanilla_{i+1}"))
    vanilla_weightss.append(vanilla_samples.weights)
    vanilla_sampless.append(vanilla_samples[vanilla_paramss[i]])
    vanilla_functions.append(pofk_vanilla_linf)
    logZs.append(vanilla_samples.logZ())
    print(vanilla_samples.logZ())
# %%
## individual vanilla plots
fig, axs = plt.subplots(
    3,
    3,
    figsize=(14, 11),
    sharex=True,
    sharey=True,
    gridspec_kw={"hspace": 0, "wspace": 0},
    subplot_kw=ax_scaling_kwargs,
)
for i, (params, ax) in enumerate(zip(vanilla_paramss, axs.flatten())):

    cbar = plot_contours(
        pofk_vanilla_linf,
        ks,
        vanilla_sampless[i],
        weights=vanilla_sampless[i].weights,
        ax=ax,
    )
    # ax.tick_params(bottom=True, top=True, left=True, right=True)
    if i < 3:
        ax.tick_params(which="major", top=False, bottom=True)
        ax.tick_params(which="minor", top=False, bottom=True)
    else:
        ax.tick_params(which="major", top=True, bottom=True)
        ax.tick_params(which="minor", top=True, bottom=True)
    # ax.set(**ax_scaling_kwargs)
    title = f"{i+1} node"
    if i > 0:
        title += "s"
    ax.text(
        0.5,
        0.9,
        title,
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize="large",
    )
    # plt.setp(ax.get_xticklabels(), visible=True)

cbar = fig.colorbar(cbar, ticks=[0, 1, 2, 3], ax=axs.flatten(), location="right")
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"], fontsize="large")
# fig.tight_layout()
fig.text(0.44, 0.08, "$\lg k$", ha="center", fontsize="x-large")
fig.text(
    0.07, 0.5, r"$\ln 10^{10} P$", va="center", rotation="vertical", fontsize="x-large"
)
fig.savefig("vanilla100.jpg", dpi=600, bbox_inches="tight")
fig.savefig("vanilla100.eps", dpi=1200, bbox_inches="tight")
plt.show()

# %%
fig, ax = plt.subplots(figsize=(8, 8))
ax.bar(np.arange(1, 10), logZs, color="#DB181D", edgecolor="black")
ax.set(xlabel="$N$", ylim=(-1480, -1440))

plt.show()
# %%
## linear lensing
linear_ax_set_kwargs = {"xlabel": "k", "ylabel": "lnP", "xscale": "log"}
linear_samples = anesthetic.NestedSamples(
    # root=root("linf_100_vanilla_3_linear_lensing")
    root=root("linf_100_vanilla_3_potential_accuracy")
)

fig, ax = plt.subplots()

cbar = plot_contours(
    pofk_vanilla_linf,
    ks,
    linear_samples[vanilla_paramss[2]],
    weights=linear_samples.weights,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"linear lensing N=3 (100 live points)", **linear_ax_set_kwargs)
plt.show()

linear_samples = anesthetic.NestedSamples(
    root=root("linf_9_vanilla_3_potential_accuracy")
)
fig, ax = plt.subplots()

cbar = plot_contours(
    pofk_vanilla_linf,
    ks,
    linear_samples[vanilla_paramss[2]],
    weights=linear_samples.weights,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"linear lensing N=3", **linear_ax_set_kwargs)
plt.show()

# %%
## N=3 try 2 100 live points
custom_ax_set_kwargs = {"xlabel": "k", "ylabel": "lnP", "xscale": "log"}
custom_samples = anesthetic.NestedSamples(root=root("linf_100_vanilla_3_try_2"))

fig, ax = plt.subplots()

cbar = plot_contours(
    pofk_vanilla_linf,
    ks,
    custom_samples[vanilla_paramss[2]],
    weights=custom_samples.weights,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"custom cluster N=3 (100 live points) try 2", **custom_ax_set_kwargs)
plt.show()

# %%
## custom cluster
custom_ax_set_kwargs = {"xlabel": "k", "ylabel": "lnP", "xscale": "log"}
custom_samples = anesthetic.NestedSamples(
    root=root("linf_100_vanilla_3_custom_cluster")
)

fig, ax = plt.subplots()

cbar = plot_contours(
    pofk_vanilla_linf,
    ks,
    custom_samples[vanilla_paramss[2]],
    weights=custom_samples.weights,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"custom cluster N=3 (100 live points)", **custom_ax_set_kwargs)
plt.show()

custom_samples = anesthetic.NestedSamples(
    root=root("linf_9_vanilla_3_custom_cluster")
)

fig, ax = plt.subplots()

cbar = plot_contours(
    pofk_vanilla_linf,
    ks,
    custom_samples[vanilla_paramss[2]],
    weights=custom_samples.weights,
    ax=ax,
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax.set(title=f"custom cluster N=3", **custom_ax_set_kwargs)
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
fig, ax = plt.subplots(
    1,
    2,
    figsize=(11, 5),
    sharex=True,
    sharey=True,
    gridspec_kw={"hspace": 0, "wspace": 0},
)

cbar = plot_contours(
    vanilla_functions,
    ks,
    vanilla_sampless,
    weights=vanilla_weightss,
    logZ=logZs,
    ax=ax[0],
)
# cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], label="fgivenx", ax=ax)
# cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax[0].set(**ax_scaling_kwargs)
ax[0].text(
    0.5,
    0.9,
    "vanilla combined",
    horizontalalignment="center",
    verticalalignment="center",
    transform=ax[0].transAxes,
    fontsize="large",
)
## adaptive case
adaptive_samples = anesthetic.NestedSamples(root=root("linf_100_adaptive"))

cbar = plot_contours(
    pofk_adaptive_linf,
    ks,
    adaptive_samples[adaptive_params],
    weights=adaptive_samples.weights,
    ax=ax[1],
)
cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 3], ax=ax)
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
ax[1].set(**ax_scaling_kwargs)
ax[1].text(
    0.5,
    0.9,
    "adaptive",
    horizontalalignment="center",
    verticalalignment="center",
    transform=ax[1].transAxes,
    fontsize="large",
)
fig.text(0.53, 0.04, "$\lg k$", ha="center", fontsize="large")
fig.text(
    0.06, 0.5, r"$\ln 10^{10} P$", va="center", rotation="vertical", fontsize="large"
)
plt.show()
# %%
# ax.bar(np.arange(1, 10), logZs, color="#DB181D", edgecolor="black")
logZs_adaptive = []
for i in np.arange(1, 10):
    split = adaptive_samples[adaptive_samples["N"] >= i]
    split = split[adaptive_samples["N"] < i + 1]
    split = split.recompute()
    logZs_adaptive.append(split.logZ())

# ax.bar(np.arange(1, 10), logZs_adaptive)
width = 0.35  # the width of the bars
x = np.arange(1, 10)
fig, ax = plt.subplots(figsize=(8, 6))
rects1 = ax.bar(
    x - width / 2, logZs, width, label="vanilla", color="#900A12", edgecolor="k"
)
rects2 = ax.bar(
    x + width / 2,
    logZs_adaptive,
    width,
    label="adaptive",
    color="#F34A36",
    edgecolor="k",
)

ax.set(
    xlabel="$N$",
    ylim=(-1505, -1440),
    ylabel=r"$\log{Z}$",
    xticks=x,
    yticks=np.arange(-1500, -1435, 5),
)
ax.legend(loc="center")
ax.bar_label(rects1, padding=3, rotation="vertical")
ax.bar_label(rects2, padding=3, rotation="vertical")
ax.text(8 + 2 * width, -1504, f"{logZs_adaptive[-1]:.2f}", rotation="vertical")
fig.savefig("PklogZ.jpg", dpi=600, bbox_inches="tight")
fig.savefig("PklogZ.eps", dpi=1200, bbox_inches="tight")

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
for i, adaptive_split in enumerate(adaptive_splits[1:]):
    print(
        f"effective sample size: {adaptive_split.weight.sum() ** 2 / (adaptive_split.weight**2).sum()}"
    )
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
## focus on N=3:
fig, axs = plt.subplots(2, 2, gridspec_kw={"hspace": 0}, figsize=(12, 8), sharey=True)
for i, (label, ax) in enumerate(zip(["100", "9"], axs)):
    samples = anesthetic.NestedSamples(root=root(f"linf_{label}_vanilla_3"))

    samples.plot(ax[0], "lgk1", "lnP1", plot_type="scatter", color="darkred")
    ax[0].set(xlabel="$\lg k_1$", ylabel=r"$\ln 10^{10} P_1$")
    cbar = plot_contours(
        pofk_vanilla_linf,
        ks,
        samples[vanilla_paramss[2]],
        weights=samples.weights,
        ax=ax[1],
    )
    ax[1].set(**ax_set_kwargs)
    for a in ax:
        if i == 0:
            a.tick_params(which="major", top=False, bottom=True)
            a.tick_params(which="minor", top=False, bottom=True)
            title = "100 live points"
        if i == 1:
            a.tick_params(which="major", top=True, bottom=True)
            a.tick_params(which="minor", top=True, bottom=True)
            title = r"$25 \times N_\mathrm{dims}$ = 725 live points"

        a.text(
            0.5,
            0.9,
            title,
            horizontalalignment="center",
            verticalalignment="center",
            transform=a.transAxes,
            fontsize="large",
        )
    # anesthetic_ax = anesthetic.make_2d_axes(["lgk1", "lnP1"], upper=True, lower=False, diagonal=False)[1]
    # anesthetic_ax = samples.plot_2d(anesthetic_ax)[1]
    # ax[1].plot(samples["lgk1"], samples["lnP1"], linestyle="None", marker="o")
    # anesthetic_ax.loc["lgk1", "lnP1"].set(ylim=(-4, -0.3))

cbar = fig.colorbar(cbar, ticks=[0, 1, 2, 3], ax=axs, location="right")
cbar.set_ticklabels(["", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"])
fig.savefig("N3comparison.eps", dpi=1200, bbox_inches="tight")
# %%
