# Rain and Drought Records

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
- **[plot_records.qmd](plot_records.qmd)**: A Quarto document utilizing **[Plotly](https://plotly.com/python/)** to build interactive, responsive visualizations:
  - **10-Year Timelines**: Plots weekly drought indices (DSCI) for both counties and the statewide rolling precipitation in a 3-panel layout.
  - **Time vs. Cumulative values**: Plots time within the year (standardized month, X-axis) vs. annual cumulative values (Y-axis) in a 3-panel layout with separate colored curves by year and month-end markers.
  - **Annual Cumulative Trajectories**: Plots annual cumulative rain vs. cumulative drought index (DSCI) for both counties as two facets side-by-side on the same plot surface, with separate colored curves by year and month-end markers.

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
