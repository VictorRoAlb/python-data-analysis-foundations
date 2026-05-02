# Project notes

## Source material

The public Python rewrite was prepared from the first-semester coursework stored locally in:

- `Trabajo academico bueno.Rmd`
- `tema 2.Rmd`
- `tema 3.Rmd`
- `tema 4.Rmd`
- `tema 5.Rmd`

## Public-version decisions

- no original coursework PDF or HTML deliverables are copied into the public repository;
- no local spreadsheets or raw text datasets are redistributed;
- no local absolute paths are kept in the code;
- the public scripts expect user-provided data paths through environment variables.

## Translation strategy

The goal was not to reproduce every R line literally. The public version keeps the analytical structure while rewriting it in Python:

- `pandas` for loading and cleaning;
- `matplotlib` for exploratory figures;
- `scipy.stats` for the main contrasts and transformations.

## What the figures summarize

- `sleep_missingness_profile.png`
  Variables with missing values and the effect of simple median imputation on `AverageSleep`.
- `sleep_statistical_summary.png`
  Relation between average sleep and GPA plus a chronotype-based comparison of poor sleep quality.
- `toyota_transformations_and_tests.png`
  Distribution checks and a simple group-comparison example using the Toyota case study.
- `python_data_analysis_summary.png`
  Compact portfolio panel combining the most representative visuals.
