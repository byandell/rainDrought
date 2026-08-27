---
title: "User Guide"
subtitle: "How to Configure, Run, and Interact with the Climate Dashboards"
author: "Antigravity Coding Assistant"
date: "2026-08-27"
format:
  html:
    theme: cosmo
    toc: true
    embed-resources: true
---

# User Guide: Climate & Drought Dashboard

Welcome to the User Guide for the **Rain & Drought Analysis Project**. This document provides simple, step-by-step instructions on how to configure your active region, run standalone or website builds, and interact with the Plotly dashboards.

***

## 1. Quick-Start (Default Settings)

By default, the project is configured to analyze **South Dakota** (precipitation) and two counties containing parts of the Pine Ridge and Rosebud reservations:
- **Oglala Lakota County** (FIPS `46102`)
- **Todd County** (FIPS `46121`)

If no local configuration file is created, running the pipeline will automatically fetch and compile these defaults.

***

## 2. Customizing Your Region (`config.csv`)

You can customize the state and counties analyzed by creating a `config.csv` file in the root folder of the repository.

### Setup Instructions
1. Copy one of the provided templates to a new file named `config.csv` in the root folder:
   ```bash
   # Option A: Copy the default South Dakota configuration
   cp config.csv.default config.csv

   # Option B: Copy the custom Nebraska test configuration
   cp config.csv.example config.csv
   ```
2. Open `config.csv` in any text editor or spreadsheet program (such as Excel).
3. Modify the rows to fit your target locations:
   - **`type`**: Set to `state` (exactly one row) or `county` (one or more rows).
   - **`code`**: Use the lowercase two-letter state postal code (e.g., `az` or `ne`) or the five-digit county FIPS code (e.g., `04007` or `31107`).
   - **`name`**: Specify the official full name of the state or county.
   - **`label`**: (Optional for counties) Short name to use in legends and chart titles.

*Note: The file `config.csv` is ignored in Git so that your local regional choices do not override the default South Dakota deployment.*

***

## 3. Standalone Execution Script

For command-line execution outside of a Quarto environment, you can run the standalone Python script from the root folder:

```bash
python rainDrought/run_analysis.py
```

### CLI Command Flags
You can append arguments to the command to control execution:
- **`--skip-data`**: Skips query requests to the NOAA ACIS and USDM APIs, and immediately generates the visualizations using your existing cached CSV files under `data/`.
  ```bash
  python rainDrought/run_analysis.py --skip-data
  ```

### Script Outputs
Running the script generates:
- **Console Log**: Prints summary tables and data statistics.
- **Cached Datasets**: Updates CSV files in the `data/` directory.
- **Interactive Dashboards**: Exports self-contained interactive Plotly HTML pages to the `output/` directory:
  - `output/time_series.html` (Timeline plots)
  - `output/cumulative_progression.html` (Annual progressions)
  - `output/trajectories.html` (Rain vs. Drought index curves)
- **Browser launch**: Automatically opens the generated dashboards in your default web browser.

***

## 4. Web Build Compilation (Quarto)

To rebuild the entire project website (incorporating any updated configuration and cached datasets), run the Quarto render command in the root folder:

```bash
quarto render
```

This compiles all `.qmd` and `.md` files into standalone HTML pages located inside the `docs/` folder, ready to be served on GitHub Pages:
- `docs/index.html` (Home Overview)
- `docs/collect_data.html` (Dynamic logs of data collection)
- `docs/plot_records.html` (Interactive Plotly graphs)

***

## 5. Interacting with the Dashboards

The dashboards compiled via Plotly on the **[Interactive Analysis](plot_records.html)** page are fully responsive and offer several interactive controls:

### Legending & Year Toggling
- **Hide/Show a Year**: Click once on a year (e.g., `2020`) in the right-hand legend. The curve corresponding to that year will toggle hide/show.
- **Isolate a Year**: Double-click on any year in the legend. This will hide all other years, allowing you to trace that specific year's timeline and trajectory. Double-click again to restore all curves.

### Zooming & Panning
- **Zoom In**: Click and drag your mouse cursor to draw a box over any region of a chart.
- **Pan**: Select the "Pan" tool (hand icon) in the plot toolbar at the top-right of the graph to slide the axes.
- **Reset Zoom**: Double-click anywhere inside the plot area, or click the **Reset View** button in the lower-right corner of the layout to restore default axes scales.

### Facet Trajectory Charts (Rain vs. Drought Index)
This chart displays annual cumulative rain (X-axis) against the cumulative weekly drought index (Y-axis):
- **DRY zone (Upper-Left)**: Curves that bend steeply upwards indicating low rainfall but persistent severe drought levels.
- **WET zone (Lower-Right)**: Curves that extend far to the right but remain close to the bottom, indicating high precipitation and little-to-no drought severity.
- **Month Circles**: Open circles correspond to the end of each month (January to December), allowing you to trace the exact periods when drought escalated (steep slope) or resolved (flattening slope).
