# AI Conversation Record

**Prompt:**

- Find periodic (daily, weekly, monthly) records of rainfall and drought index
for South Dakota, ideally for Oglala Lakota County.
- Collect and store locally in folder `data/` weekly drought records for Oglala Lakota County and daily precipitation records for South Dakota for the past 10 years. Cite sources.Write code in python as a Quarto document for this.
- Create a Quarto document that plots the drought and precipitation records using python package
[plotnine](https://plotnine.org/).
First plot data over time.

**Results:**
You can track both precipitation and drought index metrics for South Dakota, Oglala Lakota County, and Todd County across periodic intervals (daily, weekly, and monthly) through several authoritative repositories:

### 1. Weekly & Monthly Drought Tracking

- **County Conditions dashboards (Drought.gov)**:
  - **[Oglala Lakota County Conditions](https://www.drought.gov/states/south-dakota/county/oglala%20lakota)**
  - **[Todd County Conditions](https://www.drought.gov/states/south-dakota/county/todd)**
  These are the most direct dashboards for each county, aggregating weekly **U.S. Drought Monitor** updates (released every Thursday) alongside the **Standardized Precipitation Index (SPI)**, which measures objective departures from normal rainfall.
- **[U.S. Drought Monitor (South Dakota)](https://droughtmonitor.unl.edu/CurrentMap/StateDroughtMonitor.aspx?SD):** Tracks percentage area classifications (from D0 "Abnormally Dry" to D4 "Exceptional Drought") on a weekly basis across the state. You can download spatial and tabular data summaries filtered explicitly down to individual counties like Oglala Lakota and Todd.

### 2. Daily & Historical Precipitation Records

- **[South Dakota Mesonet Archives](https://sdgrass.org/tools-for-drought-planning/):** Operated via South Dakota State University, the Mesonet offers **daily** cumulative curves of precipitation plotted against 30-year climate normals. You can use their "Local Data" climate archives tab to isolate specific weather stations, dates, or individual monthly records. It also maps real-time soil moisture and the 4-week Evaporative Demand Drought Index (EDDI).
- **[South Dakota Drought Dashboard](https://toolkit.climate.gov/tool/south-dakota-drought-dashboard):** Hosted via the U.S. Climate Resilience Toolkit, this offers map-based regional tracking combining short-term 1–7 day precipitation forecasts with historical monthly monitoring.
- **[NCEI County-Level Climate Data](https://data.pressconnects.com/weather-data/oglala-lakota-county/46102/2024-01-01/):** For raw monthly records dating back to 1895, the National Centers for Environmental Information (NCEI) updates monthly precipitation, rainfall, and temperature data specifically mapped to counties like Oglala Lakota and Todd.

### 3. Local Data Collection & Visualization Website

The project is structured as a multi-page Quarto website configured via **[_quarto.yml](_quarto.yml)**. All compiled HTML pages have resources fully embedded and are output directly to the **[docs/](docs/)** folder (with local `site_libs` excluded from git), ready for seamless deployment to GitHub Pages.

- **[index.qmd](index.qmd)**: The home page for the Quarto website, serving as an overview of project goals, sources, and data workflows.
- **[collect_data.qmd](collect_data.qmd)**: A Python-based Quarto pipeline that fetches and stores the 10-year datasets in the `data/` directory.
  - Saves weekly drought records for Oglala Lakota County to [oglala_lakota_drought_weekly.csv](data/oglala_lakota_drought_weekly.csv).
  - Saves weekly drought records for Todd County to [todd_drought_weekly.csv](data/todd_drought_weekly.csv).
  - Saves daily statewide average precipitation records to [south_dakota_precipitation_daily.csv](data/south_dakota_precipitation_daily.csv).
  - Generates static 10-year climate visualizations inside the report.
- **[plot_records.qmd](plot_records.qmd)**: A Quarto document utilizing **[Plotly](https://plotly.com/python/)** to build interactive, responsive visualizations. Code blocks are **hidden/folded by default** (`code-fold: true`) for a clean visual presentation, but can be expanded interactively. Double-click explicitly included in legend with `groupclick="togglegroup"`;
allow `Reset View` with `buttons` update in lower right to re-render the plots from stored data.
  - **10-Year Timelines**: Plots weekly drought indices (DSCI) for both counties and the statewide rolling precipitation in a 3-panel layout.
  - **Time vs. Cumulative values**: Plots time within the year (standardized month, X-axis) vs. annual cumulative values (Y-axis) in a 3-panel layout with separate colored curves by year and month-end markers.
  - **Annual Cumulative Trajectories**: Plots annual cumulative rain vs. cumulative drought index (DSCI) for both counties as two facets side-by-side on the same plot surface, with separate colored curves by year and month-end markers. Features overlaid **DRY** (upper-left) and **WET** (lower-right) background watermark labels, group-toggled legends for isolating individual years, and a detailed interpretation guide.

To build and compile the entire website, run:

```bash
quarto render
```

### 4. Deploying to GitHub Pages

To publish the interactive site:

1. Commit and push the repository, including the compiled `/docs` folder, to GitHub.
2. Navigate to your repository page on GitHub.
3. Select **Settings** -> **Pages** (under the "Code and automation" section).
4. Under **Build and deployment**:
   - Set **Source** to `Deploy from a branch`.
   - Set **Branch** to `main` (or your active branch) and select `/docs` as the source folder.
5. Click **Save**.

The interactive dashboards will be live shortly at `https://<your-username>.github.io/<your-repo-name>/`.

---

## August 2026 Updates: Refactoring, Dynamic Locations, and Standalone Scripting

During this phase, the codebase was reorganized to support user-defined regions and clean up the visual presentation of code blocks on GitHub Pages:

### 1. Dynamic Regional Configurations (`config.csv`)
- **Schema & Defaults**: Introduced a configuration loader (`config.csv`) that dynamically overrides the default South Dakota dataset cache with user-specified states and counties (using FIPS codes).
- **Template Layouts**: Included [`config.csv.default`](config.csv.default) for default South Dakota conditions and [`config.csv.example`](config.csv.example) showing a custom Nebraska/Lancaster County setup.
- **Git Hygiene**: Updated [`.gitignore`](.gitignore) to exclude custom configuration settings and custom local cache files (`data/*.csv`) from Git tracking, ensuring the default South Dakota pages remain intact for the main web deployment.

### 2. Modular Package Structure (`rainDrought/` Package)
- Moved Python logic out of Quarto documents and into a structured package folder:
  - [`config.py`](rainDrought/config.py): Dynamic county/state configuration parser.
  - [`data_pipeline.py`](rainDrought/data_pipeline.py): REST API collection (USDM, ACIS GridData) and summary printing.
  - [`visualizations.py`](rainDrought/visualizations.py): Math preprocessing, Matplotlib static charts, and interactive Plotly subplots.
- Documented all modules and functions with PEP 257-compliant docstrings.
- **Simplified Notebooks**: Refactored `collect_data.qmd` and `plot_records.qmd` to only contain imports and function calls, keeping published code blocks on GitHub Pages minimal, clean, and legible.

### 3. Dynamic Visualizations & Summaries
- **Flexible Subplots**: Matplotlib and Plotly figures now dynamically adjust subplot grids, titles, legend groups, height limits, and Reset View updates based on the count and labels of configured counties.
- **Dynamic Text Elements**: Moved the Introduction sections below the config initialization cell and replaced static markdown text with dynamic `output: asis` code cells to print official state and county names dynamically.

### 4. Standalone Runner Script
- **[`rainDrought/run_analysis.py`](rainDrought/run_analysis.py)**: Added a command-line script to collect data, print statistics, export interactive Plotly charts as HTML files into the ignored `/output/` folder, and launch them in the browser. It runs relative to the active folder in which you run the shell command.

### 5. Developer Onboarding & Documentation (`DEVELOPER.md`)
- **[`DEVELOPER.md`](DEVELOPER.md)**: Created a comprehensive, root-level developer guide outlining:
  - **Directory Architecture**: The mapping of Quarto pages (`index.qmd`, `collect_data.qmd`, `plot_records.qmd`) to self-contained HTML outputs in `/docs`.
  - **Environment Setup**: Standardized usage of the `earth-analytics-python` Conda environment.
  - **Data Endpoints**: Specs for the weekly USDM REST services and daily ACIS GridData APIs.
  - **Data Standards**: Formula details for DSCI calculations ($\text{DSCI} = \sum \text{D}_i$) and daily trace precipitation mapping.
  - **Visualization Controls**: Legend grouping (`groupclick="togglegroup"`) and zoom reset menu behaviors.
  - **Deployment**: Local compilation instructions (`quarto render`) and GitHub Pages publication steps.

