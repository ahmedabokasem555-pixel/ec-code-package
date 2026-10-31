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

DOI: 10.5281/zenodo.23822823 (v2.5.6)

# Summary

EC-CODE is a Python package designed to estimate the current efficiency of chlorine production (x1) in membrane-free NaCl electrolysis cells. The package combines a single lumped thermal energy balance with grid-based Bayesian inference, utilizing DPD free-chlorine readings, charge, and conductivity data. It addresses the challenge of separating true chlorine production from losses due to volatilization and cathodic reduction. The software is designed for researchers conducting small-scale electrochemical experiments where direct measurement of chlorine production is difficult.

# Statement of need

Membrane-free NaCl electrolysis is a cost-effective method for on-site chlorine generation. However, accurately estimating the true current efficiency is challenging due to chlorine losses (volatilization and cathodic reduction). EC-CODE provides a robust, open-source framework to estimate this efficiency by combining experimental data with a physical thermal model and Bayesian inference. This allows researchers to quantify uncertainty and separate true production from losses.

# State of the field

While comprehensive multiphysics packages exist for electrochemical modeling, they often require extensive parameterization. EC-CODE focuses specifically on the inverse problem: estimating chlorine production from accessible measurements (DPD readings) using a lightweight Bayesian approach, making it highly suitable for small-scale experimental setups.

# Software design

The package is distributed as a standard Python package, installable via `pip`. It is structured into distinct modules:
1. **Chlorine Model:** Implements the Faraday-based accounting to calculate expected production.
2. **Thermal Model:** A single lumped energy balance serves as a diagnostic consistency check.
3. **Inference:** Employs a grid-based Bayesian approach to estimate x1, using a Beta prior.
4. **Utils:** Provides helper functions for data loading and validation.

# Quality control and limitations

The package includes an initial suite of automated software tests for the core functionality (e.g., the chlorine model), with the full integration of the 69 tests from the original notebook planned for future releases.

The package is a pilot tool and has several documented limitations:
- The estimate of x1 depends on the Beta prior for ε, which is an assumption and has not been empirically validated.
- The thermal model is a diagnostic tool and does not directly calculate x1.
- The included DEMO uses synthetic data; no experimental validation has been performed yet.

# Acknowledgements

None.

# References
