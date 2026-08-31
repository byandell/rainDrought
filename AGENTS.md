# AGENTS.md — rainDrought

## Context

- **Repository**: rainDrought — Python library for historical daily precipitation records (statewide average) and weekly U.S. Drought Monitor (USDM) statistics for counties
- **Timeframe**: 10 years of historical data from July 2016 to the present
- **Key Directories**: `rainDrought/`, `data/`, `docs/`
- **Environment**: Active Python virtual environment (`~/miniconda3/envs/earth-analytics-python/bin/python`)

## Role

Act as a scientific Python developer and geospatial data engineer.

## Action & Verification

- Run tests: `pytest`
- Run linting/formatting: `ruff check` / `mypy`
- Ensure notebooks execute cleanly from top to bottom with relative data paths.

## Format & Conventions

- Modern Python type hints (`str | None`, `list[int]`, `dict[str, Any]`).
- NumPy or Google-style docstrings on all exported functions/classes.
- **Plotting Library**: Use **Plotly** (`plotly.graph_objects`, `plotly.express`) for main visualizations to create interactive dashboards.

## Tone & Collaboration

- Concise, clear, and actionable. Provide verified diffs.

## Quarto Website & Build Output

- **Project Structure**: This repository is a Quarto Website configured via `_quarto.yml`.
- **Output Directory**: The website builds into the `/docs` folder for GitHub Pages.
- **Embedded Resources**: Resource embedding is enabled via `embed-resources: true` under `format.html` in `_quarto.yml`. Each page is compiled as a self-contained standalone HTML file.
- **Git Ignoring**: The folder `docs/site_libs/` is ignored in `.gitignore`. **Do not track or commit `docs/site_libs/`** to the repository, as all scripts are embedded in the HTML files. Only stage the HTML files and `docs/search.json`.
- **Build Command**: Do not render the entire website. Prompt user to run `quarto render` after significant changes.

## Data Processing Standards

- **Drought Severity and Coverage Index (USDM DSCI)**:
  - Computed using cumulative percentages: `DSCI = D0 + D1 + D2 + D3 + D4` (range `0` to `500`).
- **Precipitation Units**: Precipitation values are in **inches**.
- **Trace Amounts**: Convert daily trace precipitation values (`'T'` or `'T '`) to `0.0001` inches.
- **Cumulative Calculations**: When visualizing annual progressions, group values by year (`date.dt.year`) and perform a cumulative sum (`cumsum()`) on `precipitation_inches` and `dsci`.
