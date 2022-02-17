import cobaya

resume = False

cobaya.run(
    "camb_mcmc.yaml",
    "packages",
    "runs/camb_mcmc/camb_mcmc",
    resume=resume,
    force=not resume,
    test=False,
    debug=False,
)
