# GamePulse - Mobile Game A/B Testing

**Player Retention | Experiment Analytics | Data-Driven Decisions**

An end-to-end product analytics project that evaluates whether moving the first game gate from level 30 to level 40 affects player retention.

**[🚀 Deployed ](https://gamepulse-ab-testing-gamg4sxabtocjpqwh6ev67.streamlit.app/)**

## Key Findings

| Metric | Result |
|---|---:|
| Total Players | 90,189 |
| Control Group | 44,700 |
| Test Group | 45,489 |
| Day-1 Retention Difference | -0.59 pp |
| Day-7 Retention Difference | -0.82 pp |
| Day-7 P-value | 0.0016 |

## Analysis

- Exploratory Data Analysis (EDA)
- Player engagement and game-round analysis
- Day-1 and Day-7 retention comparison
- Two-proportion Z-test
- Bootstrap resampling and confidence intervals
- Statistical hypothesis testing
- Business recommendations

## Key Conclusion

The gate_40 group showed significantly lower Day-7 retention than gate_30.

**Recommendation:** Retain gate_30 based on the observed retention results.

## Tech Stack

- **Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Statistics:** SciPy, Statsmodels
- **Dashboard:** Streamlit
- **Testing:** Pytest
- **Tools:** Jupyter Notebook, Git, GitHub

## Dataset

[Cookie Cats — Mobile Games A/B Testing](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats)

Contains 90,189 player records with experiment versions, game rounds, and Day-1/Day-7 retention metrics.

## Methodology

`Data Validation` → `EDA` → `Retention Analysis` → `Hypothesis Testing` → `Bootstrap Analysis` → `Business Decision`

---

*Turning player data into better product decisions.*
