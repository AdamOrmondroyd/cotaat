import numpy as np
import yaml


def create_pofk_yaml(
    output_filepath,
    Nmax,
    lgkmin,
    lgkmax,
    lnPmin,
    lnPmax,
    adaptive=True,
    N=None,
    input_filepath="linf_pofk_template.yaml",
    nlive=None,
):
    with open(input_filepath) as in_file:
        yaml_dict = yaml.load(in_file, Loader=yaml.FullLoader)

        yaml_dict["sampler"] = {"polychord": {}}
        if nlive:
            yaml_dict["sampler"]["polychord"]["nlive"] = nlive

        yaml_dict["theory"]["camb"]["external_primordial_pk"] = True

        if adaptive:
            # TODO: remember the lower bound will need changing to 0 for w(z)
            yaml_dict["params"]["N"] = {"prior": [1, Nmax + 1], "latex": "N"}
            yaml_dict["theory"]["linf_pofk.AdaptivePk"] = {
                "python_path": "change_plumbing/",
                "num_ks": 100,
                "lgkmin": -4,
                "lgkmax": -0.3,
            }
            for i in np.arange(Nmax):

                yaml_dict["params"][f"lnP{i}"] = {
                    "prior": [lnPmin, lnPmax],
                    "latex": f"\\ln{{P_{i}}}",  # \ is making my head explode but ignore for now
                }
        else:
            yaml_dict["theory"][f"linf_pofk.Vanilla{N}"] = {
                "python_path": "change_plumbing/",
                "num_ks": 100,
                "lgkmin": -4,
                "lgkmax": -0.3,
            }
            for i in np.concatenate((np.arange(N - 1), [Nmax - 1])):

                yaml_dict["params"][f"lnP{i}"] = {
                    "prior": [lnPmin, lnPmax],
                    "latex": f"\\ln{{P_{i}}}",  # \ is making my head explode but ignore for now
                }

        # lnP nodes

        # lgk nodes
        # if 4 or more nodes (i.e. 2 or more internal nodes),
        # they need to be sorted

        if adaptive:
            N = Nmax

        if N >= 4:
            sorted_prior_arguments = ""
            sorted_prior_expression = ""

        for i in np.arange(N - 2) + 1:
            yaml_dict["params"][f"lgk{i}"] = {
                "prior": [lgkmin, lgkmax],
                "latex": f"\\lg{{k_{i}}}",  # \ is making my head explode but ignore for now
            }

            if N >= 4:
                sorted_prior_arguments += f"lgk{i}"
                if i < N - 2:
                    sorted_prior_arguments += ", "
                if i > 1:
                    sorted_prior_expression += " < "

                sorted_prior_expression += f"lgk{i}"

        if N >= 4:
            if adaptive:
                sorted_prior = (
                    f"lambda N, {sorted_prior_arguments}: np.log(np.all(np.diff(np.array([{sorted_prior_arguments}])[:max(int(N) - 2, 0)]) > 0))"
                )
            else:
                sorted_prior = (
                    f"lambda {sorted_prior_arguments}: np.log({sorted_prior_expression})"
                )

            yaml_dict["prior"] = {"sorted_prior": sorted_prior}

        out_file = open(output_filepath, "w")
        yaml.dump(yaml_dict, out_file)


if __name__ == "__main__":
    lgkmin, lgkmax = -4, -0.3
    lnPmin, lnPmax = 2, 4

    Nmax = 9

    create_pofk_yaml(
        "../linf_9_adaptive.yaml",
        Nmax,
        lgkmin,
        lgkmax,
        lnPmin,
        lnPmax,
        adaptive=True,
    )
    for i in np.arange(Nmax) + 1:
        create_pofk_yaml(
            f"../linf_9_vanilla_{i}.yaml",
            Nmax,
            lgkmin,
            lgkmax,
            lnPmin,
            lnPmax,
            adaptive=False,
            N=i,
        )
