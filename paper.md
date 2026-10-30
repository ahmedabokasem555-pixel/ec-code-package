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
DOI: 10.5281/zenodo.23822823
# Summary

EC-CODE is a Python package designed to estimate the current efficiency of chlorine production (x1) in membrane-free NaCl electrolysis cells. The package combines a single lumped thermal energy balance with grid-based Bayesian inference, utilizing DPD free-chlorine readings, charge, and conductivity data. It addresses the challenge of separating true chlorine production from losses due to volatilization and cathodic reduction. The software is designed for researchers conducting small-scale electrochemical experiments who require a transparent, reproducible, and lightweight estimation tool.

# Statement of need

Membrane-free NaCl electrolysis is a cost-effective method for on-site chlorine generation. However, accurately estimating x1 is difficult because a fraction of the generated chlorine is lost. Standard multiphysics packages are often too complex or costly for routine bench work. EC-CODE fills this gap by providing a lightweight, open-source Python package that uses a Bayesian framework to estimate x1 from simple bench measurements. The package is specifically designed for pilot-scale setups, exposing all assumptions as named constants or documented limitations.

# State of the field

While comprehensive multiphysics packages exist for electrochemical modeling, they are often overkill for small bench experiments. EC-CODE specifically targets the calibration of current efficiency in pilot-scale setups. It does not replace full-scale modeling tools but provides a transparent, reproducible, and lightweight alternative for researchers who need a quick estimation of x1 from DPD and conductivity data.

# Software design

The package is distributed as a standard Python package, installable via `pip`. It is structured into four main modules:
1. **Chlorine Model:** Implements the Faraday-based accounting to calculate the expected dissolved chlorine.
2. **Thermal Model:** A single lumped energy balance serves as a diagnostic consistency check.
3. **Inference:** Employs a grid-based Bayesian approach to estimate x1, using a Beta(1.2, 4.9) prior for the loss fraction (ε).
4. **Utils:** Provides helper functions for data loading and validation.

# Quality control and limitations

The package includes 69 automated software tests (68 passing, 1 informational check). These tests verify input validation, unit consistency, and the internal logic of the thermal and charge balances. The tests confirm the code's internal consistency but do not constitute experimental validation.

The package is a pilot tool and has several documented limitations:
- The estimate of x1 depends on the Beta prior for ε, which is an assumption and has not been calibrated against measured data.
- The thermal model is a diagnostic tool and does not directly calculate x1. Its parameter T_CL is set to 0.51 (a KCl-derived value), whereas approx. 0.60 is expected for NaCl; this bias is flagged, and re-running the DEMO with 0.60 left the x1 posterior unchanged.
- The archived version (v2.5.1) passes its test suite only with a documented patch ("PATCH 2"), which is integrated in the next release.
- The included DEMO uses synthetic data; no experimental validation has been performed.

# Acknowledgements

None.

# References
