"""Simulation study (synthetic data only). Run: python examples/coverage_study.py"""
from simulate import coverage_study

scenarios = {
    "A prior correct   (eps~Beta(1.2,4.9), assumed Beta(1.2,4.9))": dict(true_eps_params=(1.2, 4.9)),
    "B prior shifted   (eps~Beta(4,4),     assumed Beta(1.2,4.9))": dict(true_eps_params=(4.0, 4.0)),
    "C prior shifted   (eps~Beta(1.2,12),  assumed Beta(1.2,4.9))": dict(true_eps_params=(1.2, 12.0)),
}
print(f"{'scenario':64s} coverage  mean width  median |error|")
for name, kw in scenarios.items():
    r = coverage_study(n_rep=300, **kw)
    print(f"{name:64s} {r['coverage']:.3f}    {r['mean_width']:.4f}      {r['median_abs_error']:.4f}")
