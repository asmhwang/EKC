# Panel Analysis of Environmental Kuznets Curve Hypothesis in South Korea

Research code for the paper **"Panel Analysis of Environmental Kuznets Curve Hypothesis in South Korea"**, published in *NHSJS* (National High School Journal of Science).

## Overview

This project tests the **Environmental Kuznets Curve (EKC) hypothesis** across South Korean provinces and regions using panel data methods. The EKC hypothesis posits an inverted-U relationship between economic growth (GDP per capita) and environmental degradation — pollution rises with early industrialization, then falls as income crosses a threshold.

Four pollutants are analyzed using regional panel data from South Korea:

| Script | Pollutant |
|--------|-----------|
| `co.py` | Carbon monoxide (CO) |
| `no.py` | Nitric oxide (NO) |
| `pm10.py` | Particulate matter PM10 |
| `pm25.py` | Particulate matter PM2.5 |

## Methodology

Each script runs the following pipeline for its respective pollutant:

1. **Data preparation** — Merges pollutant emissions, regional GDP, population density, and total population into a panel dataset indexed by region and year.
2. **Log transformation** — Pollutant per capita and GDP are log-transformed; GDP² is added to capture the non-linear EKC relationship.
3. **Random Effects (RE) estimation** — Fits a GLS random-effects panel model.
4. **Fixed Effects (FE) estimation** — Fits a within-estimator fixed-effects panel model.
5. **Hausman test** — Tests whether RE or FE is the consistent estimator; a significant result favors fixed effects.

**Model:**
```
ln(Pollutant per capita) = β₀ + β₁·ln(GDP) + β₂·ln(GDP)² + β₃·Density + ε
```

An inverted-U (EKC confirmed) requires β₁ > 0 and β₂ < 0.

## Project Structure

```
.
├── co.py               # CO panel analysis
├── no.py               # NO panel analysis
├── pm10.py             # PM10 panel analysis
├── pm25.py             # PM2.5 panel analysis
├── requirements.txt    # Python dependencies
└── data/
    ├── 1gdpkor.csv         # Regional GDP per capita (South Korea)
    ├── coEmissions.csv     # CO emissions by region
    ├── noEmissions.csv     # NO emissions by region
    ├── pm10Emissions.csv   # PM10 emissions by region
    ├── pm2_5Emissions.csv  # PM2.5 emissions by region
    ├── population.csv      # Population density by region
    ├── totalPop.csv        # Total population by region
    └── ...                 # Raw/intermediate data files
```

## Setup

```bash
# Create and activate a virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run each script from the project root:

```bash
python co.py    # CO emissions EKC analysis
python no.py    # NO emissions EKC analysis
python pm10.py  # PM10 emissions EKC analysis
python pm25.py  # PM2.5 emissions EKC analysis
```

Each script prints:
- The merged panel dataset
- Random effects model summary
- Fixed effects model summary
- Model comparison table
- Hausman test statistic, degrees of freedom, and p-value
- Coefficient and covariance matrix comparison

## Dependencies

- Python 3.12+
- `numpy`, `pandas`, `matplotlib`, `scipy`
- `statsmodels`
- [`linearmodels`](https://bashtage.github.io/linearmodels/) — for PanelOLS and RandomEffects
- `pycountry_convert`

## Citation

If referencing this code, please cite the associated paper published in NHSJS.
