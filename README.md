# EC-CODE

**Pilot status:** EC-CODE has automated software tests but **no experimental validation**. Results are conditional on a model and a prior and must not be read as validated measurements.

EC-CODE is a small Python package for estimating the current efficiency of chlorine formation (`x1`) in membrane-free NaCl electrolysis from the charge passed and a DPD free-chlorine reading. A DPD reading fixes only the apparent efficiency `x1 * (1 - eps)`, where `eps` is the fraction of chlorine lost before the reading. The package therefore reports `x1` **conditional on a Beta prior for `eps`**, and also reports the prior-only interval so you can see how much your data add.

## Install

```bash
git clone https://github.com/ahmedabokasem555-pixel/ec-code-package
cd ec-code-package
pip install .            # numpy, scipy, pandas
pip install ".[dev]"     # adds pytest
pytest
```

Python >= 3.9. The package is not on PyPI.

## Modules

| Module | Purpose |
|---|---|
| `chlorine` | `calculate_expected_chlorine`, `calculate_apparent_efficiency` (Faraday accounting) |
| `inference` | `run_inference` (grid posterior of `x1`), `prior_only_interval` |
| `thermal` | lumped energy balance: derivative, `simulate_temperature`, `max_abs_error` (diagnostic only) |
| `utils` | `load_csv_data`, `validate_columns` |
| `simulate` | synthetic runs and a calibration (coverage) study — simulated data only |

## Model

```
mu      = x1 * Q/(2F) * (1 - eps) * M_Cl2 * 1000 / V_L     [mg/L as Cl2]
eta_app = 2 F C_meas V_L / (1000 M_Cl2 Q) = x1 * (1 - eps)
C_meas ~ Normal(mu, sigma)      eps ~ Beta(1.2, 4.9)      x1 flat
```

`C_meas` must already include the DPD dilution factor. `sigma` defaults to 0.01 mg/L, an assumption: set your own.

## Usage

```python
import numpy as np
from chlorine import calculate_apparent_efficiency
from inference import run_inference, prior_only_interval

F, M_Cl2 = 96485.33212, 70.906      # C/mol, g/mol
Q, V_L, C_meas = 1000.0, 1.0, 14.70  # C, litres, mg/L (synthetic)

eta = calculate_apparent_efficiency(C_meas, V_L, F, M_Cl2, Q)

x1_grid = np.linspace(1e-4, 0.35, 2000)
eps_grid = np.linspace(0.001, 0.60, 2000)
_, median, lo, hi, _ = run_inference(C_meas, V_L, F, M_Cl2, Q, x1_grid, eps_grid)
print("conditional:", lo, median, hi)
print("prior-only :", prior_only_interval(eta))
```

Run the full synthetic demo with `python examples/demo.py`. Output from this version:

```
synthetic C_meas      = 14.6978 mg/L (x1=0.05, eps=0.2)
apparent efficiency   = 0.04000
conditional x1        = median 0.0495, 95% interval [0.0405, 0.0880]
prior-only x1         = median 0.0478, 95% interval [0.0404, 0.0909]
```

The two intervals are almost identical: **one DPD reading adds little beyond the prior**.

## Simulation study (synthetic data only)

`simulate.py` and `examples/coverage_study.py` simulate runs with known `x1` and `eps`, infer, and check how often the 95% interval contains the truth (300 runs per scenario, `sigma = 0.1 mg/L`, `x1 ~ U(0.02, 0.30)`, seed 0). These are **simulated data, not measurements**; they test the method, not the chemistry.

| Scenario (true `eps` vs assumed Beta(1.2, 4.9)) | Coverage of 95% interval | Mean width | Median abs. error |
|---|---|---|---|
| A. prior correct | 0.957 | 0.106 | 0.014 |
| B. true eps ~ Beta(4, 4) (much larger losses) | 0.837 | 0.100 | 0.039 |
| C. true eps ~ Beta(1.2, 12) (smaller losses) | 0.943 | 0.112 | 0.016 |

Reading: the interval is calibrated when the prior on `eps` is right, and under-covers when real losses are much larger than the prior assumes. The intervals are wide (about 0.1 in `x1`), so single-reading estimates are coarse.

## Grid resolution

The likelihood is a thin ridge in the (`x1`, `eps`) plane. Coarse grids give wrong intervals (the package warns when it detects this). Always refine both grids until the result stops changing. Use a `sigma` that matches your real measurement error.

## Using real measurements

The default grids above (`x1` up to 0.35, `eps` up to 0.60) suit the synthetic demo only. For real data choose grids that cover every plausible value (for example `x1` up to 1.0), use your own measurement `sigma`, refine until the interval stops changing, and keep the prior-only interval next to every result. Report DPD dilution factors, the number of replicates and the measured loss (`eps`) runs alongside the estimate. No experimental data are distributed with this package.

## Input data (optional)

```python
from utils import load_csv_data, validate_columns
df = load_csv_data("run.csv")
validate_columns(df, ["t_s", "T_C"])
```

## Limitations

- No laboratory validation; the demo uses synthetic data.
- `x1` is not identifiable from DPD alone: the interval depends on the Beta prior (an assumption) and on `sigma`.
- The thermal model is a diagnostic and does not estimate `x1`.
- Transference number / diffusion constants from earlier notebook versions are not part of this package.

## Citation and licence

See `CITATION.cff`. MIT licence (`LICENSE`). Contributions: see `CONTRIBUTING.md`.

