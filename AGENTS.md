# Style Guide & Instructions for AI Agents

Welcome, AI coding agent! Please follow these guidelines when editing or adding code to this repository:

---

## 1. Project Context & Scope
- **Domain**: Historical daily precipitation records (statewide average for South Dakota) and weekly U.S. Drought Monitor (USDM) statistics for South Dakota counties:
  - **Oglala Lakota County** (FIPS code `46102`, formerly Shannon County `46113`).
  - **Todd County** (FIPS code `46121`).
- **Timeframe**: 10 years of historical data from July 2016 to the present.

---

## 2. Environment & Dependencies
- **Target Python Executable**: Always run Python commands and scripts using the Conda environment configured for Quarto:
  ```bash
  /users/brianyandell/miniconda3/envs/earth-analytics-python/bin/python
  ```
- **Pip Installations**: If installing Python packages, run:
  ```bash
  /users/brianyandell/miniconda3/envs/earth-analytics-python/bin/python -m pip install <package>
  ```
- **Plotting Library**: Use **Plotly** (`plotly.graph_objects`, `plotly.express`) for main visualizations in `plot_records.qmd` to create interactive dashboards.

---

## 3. Quarto Website & Build Output
- **Project Structure**: This repository is a Quarto Website configured via `_quarto.yml`.
- **Output Directory**: The website builds into the `/docs` folder for GitHub Pages.
- **Embedded Resources**: Resource embedding is enabled via `embed-resources: true` under `format.html` in `_quarto.yml`. Each page is compiled as a self-contained standalone HTML file.
- **Git Ignoring**: The folder `docs/site_libs/` is ignored in `.gitignore`. **Do not track or commit `docs/site_libs/`** to the repository, as all scripts are embedded in the HTML files. Only stage the HTML files and `docs/search.json`.
- **Build Command**: Render the entire website by running:
  ```bash
  quarto render
  ```

---

## 4. Data Processing Standards
- **Drought Severity and Coverage Index (USDM DSCI)**:
  - Computed using cumulative percentages: `DSCI = D0 + D1 + D2 + D3 + D4` (range `0` to `500`).
- **Precipitation Units**: Precipitation values are in **inches**.
- **Trace Amounts**: Convert daily trace precipitation values (`'T'` or `'T '`) to `0.0001` inches.
- **Cumulative Calculations**: When visualizing annual progressions, group values by year (`date.dt.year`) and perform a cumulative sum (`cumsum()`) on `precipitation_inches` and `dsci`.
