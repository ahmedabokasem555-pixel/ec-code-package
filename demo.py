"""Synthetic demo (not experimental data). Run: python examples/demo.py"""
import numpy as np

from chlorine import calculate_apparent_efficiency, calculate_expected_chlorine
from inference import prior_only_interval, run_inference

F, M, V, Q = 96485.33212, 70.906, 1.0, 1000.0
x1_true, eps_true = 0.05, 0.20
C = calculate_expected_chlorine(x1_true, Q, F, eps_true, M, V)  # noise-free synthetic reading
eta = calculate_apparent_efficiency(C, V, F, M, Q)

x1_grid = np.linspace(1e-4, 0.35, 2000)
eps_grid = np.linspace(0.001, 0.60, 2000)
_, med, lo, hi, _ = run_inference(C, V, F, M, Q, x1_grid, eps_grid)
plo, pmed, phi = prior_only_interval(eta)

print(f"synthetic C_meas      = {C:.4f} mg/L (x1={x1_true}, eps={eps_true})")
print(f"apparent efficiency   = {eta:.5f}")
print(f"conditional x1        = median {med:.4f}, 95% interval [{lo:.4f}, {hi:.4f}]")
print(f"prior-only x1         = median {pmed:.4f}, 95% interval [{plo:.4f}, {phi:.4f}]")
