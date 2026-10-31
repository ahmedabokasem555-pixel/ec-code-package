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
    affiliation: 1
affiliations:
  - name: Independent Researcher, Egypt
    index: 1
date: 30 October 2026
bibliography: paper.bib
---

# Summary

EC-CODE is a Python package designed to estimate the current efficiency of chlorine production (x1) in membrane-free NaCl electrolysis cells. The package combines a single lumped thermal energy balance with grid-based Bayesian inference, utilizing DPD free-chlorine readings, charge, and conductivity data. It addresses the challenge of separating estimated chlorine production from losses due to volatilization and cathodic reduction. The software is intended for researchers conducting small-scale electrochemical experiments where direct measurement of chlorine production is difficult.

# Statement of need

Membrane-free NaCl electrolysis is a cost-effective method for on-site chlorine generation. However, accurately estimating the true current efficiency is challenging due to chlorine losses. EC-CODE provides a lightweight, open-source framework to estimate this efficiency by combining experimental data with a physical thermal model and Bayesian inference. This allows researchers to estimate uncertainty, conditional on a prior, and separate estimated production from losses [@Bard2001; @GUM2008].

# State of the field

While comprehensive multiphysics packages exist for electrochemical modeling (such as COMSOL or similar finite-element tools), they often require extensive parameterization. EC-CODE focuses specifically on the inverse problem: estimating chlorine production from accessible measurements (DPD readings, as outlined in @DPD2017) using a lightweight Bayesian approach. It is intended for small-scale experimental setups where full multiphysics modeling is impractical.

# Software design

The package is distributed as a standard Python package, installable via `pip install .`. It is structured into distinct modules:
1. **Chlorine Model:** Implements the Faraday-based accounting to calculate expected production.
2. **Thermal Model:** A single lumped energy balance serves as a diagnostic consistency check.
3. **Inference:** Employs a grid-based Bayesian approach to estimate x1, using a Beta prior.
4. **Utils:** Provides helper functions for data loading and validation.

# Quality control and limitations

The package includes an initial suite of automated software tests for the core functionality (e.g., the chlorine model) located in the `tests/` directory. These can be run via `pytest tests/`. The full integration of the 69 tests from the original notebook is planned for future releases.

The package is a pilot tool and has several documented limitations:
- The estimate of x1 depends on the Beta prior for ε, which is an assumption and has not been empirically validated.
- The thermal model is a diagnostic tool and does not directly calculate x1.
- The included DEMO uses synthetic data; no experimental validation has been performed yet.
- For the DEMO inputs, the prior-only interval for x1 is [0.0407, 0.0828] (median 0.0480), wider than the conditional interval reported by the package [0.0459, 0.0584]. The latter must be read as conditional on the model and prior, not as a validated coverage statement.
- The thermal parameter T_CL is set to 0.51 (a KCl-derived value), whereas ≈0.60 is expected for NaCl. This bias is flagged; re-running the DEMO with 0.60 left the x1 posterior unchanged.

# Acknowledgements

None.

# References