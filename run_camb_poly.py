import cobaya

resume = False

cobaya.run(
    "camb_poly.yaml",
    "packages",
    "runs/camb_poly/camb_poly",
    resume=resume,
    force=not resume,
    test=False,
    debug=False,
)
