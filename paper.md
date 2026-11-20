---
title: 'EC-CODE: An Open-Source Python Package for Prior-Conditional Estimation of Chlorine Production in Membrane-Free NaCl Electrolysis'
tags:
  - Python
  - electrochemistry
  - chlorine production
  - Bayesian inference
  - open-source software
authors:
  - name: Ahmed Kasem
    orcid: 0009-0002-1395-5378
    affiliation: 1
affiliations:
  - name: Independent Researcher, Egypt
    index: 1
date: 19 November 2026
bibliography: paper.bib
---

# Summary

EC-CODE is a small Python package for estimating the current efficiency of chlorine formation ($x_1$) in membrane-free (undivided) NaCl electrolysis cells from the charge passed and a DPD free-chlorine reading [@standardmethods]. It combines Faraday accounting, a grid-based Bayesian inference with a Beta prior on the loss fraction $\epsilon$, and a single lumped thermal balance used as a diagnostic. It is a pilot tool: it has software tests but no experimental validation.

# Statement of need

In an undivided cell, part of the chlorine formed at the anode is lost (volatilisation, reduction at the cathode), so a DPD reading reports only what survived [@kraft2008]. The reading fixes the *apparent* efficiency $\eta_\mathrm{app} = x_1(1-\epsilon)$ but not $x_1$ and $\epsilon$ separately. Any estimate of $x_1$ therefore rests on an assumption about $\epsilon$. EC-CODE makes that assumption explicit (a Beta prior) and returns the resulting interval together with the prior-only interval for comparison, so that users can see how much the data add. It is aimed at researchers and students running small bench experiments who want a transparent, auditable calculation rather than a spreadsheet.

# State of the field

General electrochemical modelling environments (finite-element multiphysics packages) can represent such cells but need extensive parameterisation, and we are not aware of an open-source package dedicated to this inverse problem. We have not performed a systematic software survey. Measurement uncertainty conventions follow the GUM [@gum2008]; the diffusion-layer background is textbook material [@bard2001].

# Software design

The package is a flat set of modules installed with `pip install .`:

- `chlorine`: Faraday accounting, $\mu = x_1 \frac{Q}{2F}(1-\epsilon) M_{\mathrm{Cl_2}} \frac{1000}{V_L}$ (mg/L) and $\eta_\mathrm{app}$.
- `inference`: posterior of $x_1$ on a grid with $C_\mathrm{meas}\sim\mathcal{N}(\mu,\sigma)$ and $\epsilon\sim\mathrm{Beta}(1.2, 4.9)$, plus `prior_only_interval`. It raises an error for incompatible data and warns when the grid is too coarse to resolve the likelihood ridge.
- `thermal`: lumped energy balance $C_\mathrm{tot}\,dT/dt = I(V-E_\mathrm{tn}) - K_\mathrm{dry}(T-T_\mathrm{air}) - Q_\mathrm{evap}$, with an integrator and a maximum-error diagnostic. It does not determine $x_1$.
- `utils`: CSV loading and column validation.

A grid was chosen over MCMC because there are two unknowns on bounded domains and the result is easy to audit; the cost is that the grid must be refined until the answer stops changing.

# Research impact statement

The package has not yet been used in published research, has no external users, and has not been compared with laboratory measurements. Its current contribution is an open, tested, citable implementation (Zenodo archive) of an explicit prior-conditional calculation. Experimental validation with DPD data is the next step and is not claimed here.

# Quality control and limitations

The test suite (`pytest`, run on Python 3.9, 3.11 and 3.12 through GitHub Actions) covers the simulation utilities, the Faraday relations (including the identity $\eta_\mathrm{app}=x_1(1-\epsilon)$), input validation, normalisation and grid convergence of the posterior, and the thermal integrator against its analytic solution. These tests check internal consistency, not agreement with experiments.

For the synthetic demonstration in `examples/demo.py` ($x_1=0.05$, $\epsilon=0.20$, $Q=1000$ C, $V_L=1$ L, noise-free reading 14.70 mg/L), the conditional 95% interval for $x_1$ is [0.0405, 0.0880] (median 0.0495) and the prior-only interval is [0.0404, 0.0909] (median 0.0478). The intervals are nearly the same: with a single DPD reading the data add almost nothing beyond the prior, because only $x_1(1-\epsilon)$ is identified. Additional information on $\epsilon$ (for example separate loss measurements) would be needed to narrow it. The result also depends on the assumed measurement standard deviation ($\sigma$, default 0.01 mg/L) and the Beta prior, neither of which is empirically validated.

# Simulation study

To test the inference where the truth is known, `simulate.py` generates synthetic runs ($x_1\sim U(0.02,0.30)$, $Q=1000$ C, $V_L=1$ L, $\sigma=0.1$ mg/L, 300 runs per scenario, seed 0). These are simulated data, not measurements. When $\epsilon$ follows the assumed prior, the 95% interval contained the true $x_1$ in 95.7% of runs (mean width 0.106). When the true losses were much larger than the prior assumes ($\epsilon\sim\mathrm{Beta}(4,4)$), coverage fell to 83.7%; when they were smaller ($\mathrm{Beta}(1.2,12)$), coverage was 94.3%. Thus the method is calibrated only to the extent that the prior on $\epsilon$ is right, and intervals are wide. This is a test of the statistical procedure, not experimental validation.

# Software availability

Source code: <https://github.com/ahmedabokasem555-pixel/ec-code-package> (MIT licence). Archived release v2.5.7: Zenodo, DOI 10.5281/zenodo.24377879. No experimental data are distributed with the package.

# AI usage disclosure

Generative AI assistants (Claude, Anthropic, and others) were used to help draft and review code, tests, documentation and this paper. The author reviewed, ran and takes responsibility for all content; all numbers reported here come from running the package.

# Acknowledgements

None.

# References
