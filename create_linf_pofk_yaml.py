import numpy as np
import yaml


def create_pofk_yaml(
    input_filepath, output_filepath, N, lgkmin, lgkmax, lnPmin, lnPmax, adaptive=False
):
    with open(input_filepath) as in_file:
        yaml_dict = yaml.load(in_file, Loader=yaml.FullLoader)

        yaml_dict["theory"]["camb"]["external_primordial_pk"] = True

        if adaptive:
            # TODO: remember the lower bound will need changing to 0 for w(z)
            yaml_dict["params"]["N"] = {"prior": [1, N + 1], "latex": "N"}
            yaml_dict["theory"]["linf_pofk.AdaptivePk"] = {
                "python_path": "change_plumbing/",
                "num_ks": 100,
                "lgkmin": -4,
                "lgkmax": -0.3,
            }
        else:
            yaml_dict["theory"][f"linf_pofk.Vanilla{N}"] = {
                "python_path": "change_plumbing/",
                "num_ks": 100,
                "lgkmin": -4,
                "lgkmax": -0.3,
            }

        # lnP nodes

        for i in np.arange(N):

            yaml_dict["params"][f"lnP{i}"] = {
                "prior": [lnPmin, lnPmax],
                "latex": f"\\ln{{P_{i}}}",  # \ is making my head explode but ignore for now
            }

        # lgk nodes
        # if 4 or more nodes (i.e. 2 or more internal nodes),
        # they need to be sorted

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
            sorted_prior = (
                f"lambda {sorted_prior_arguments}: np.log({sorted_prior_expression})"
            )

        print(sorted_prior)

        if sorted_prior:
            yaml_dict["prior"] = {"sorted_prior": sorted_prior}

        print(yaml_dict)

        out_file = open(output_filepath, "w")
        yaml.dump(yaml_dict, out_file)


if __name__ == "__main__":
    create_pofk_yaml("linf_pofk_template.yaml", "test.yaml", 5, -4, -0.3, 2, 4, True)
