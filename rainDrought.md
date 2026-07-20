# Rain and Drought Records

**Prompt:**

- Find periodic (daily, weekly, monthly) records of rainfall and drought index
for South Dakota, ideally for Oglala Lakota County.
- Collect and store locally in folder `data/` weekly drought records for Oglala Lakota County and daily precipitation records for South Dakota for the past 10 years. Cite sources.Write code in python as a Quarto document for this.
- Create a Quarto document that plots the drought and precipitation records using python package
[plotnine](https://plotnine.org/).
First plot data over time.

**Results:**
You can track both precipitation and drought index metrics for South Dakota and
Oglala Lakota County across periodic intervals (daily, weekly, and monthly)
through several authoritative repositories:

### 1. Weekly & Monthly Drought Tracking

- **[Oglala Lakota County Conditions (Drought.gov)](https://www.drought.gov/states/south-dakota/county/oglala%20lakota):** This is the most direct comprehensive dashboard for the county. It aggregates weekly **U.S. Drought Monitor** updates (released every Thursday) alongside the **Standardized Precipitation Index (SPI)**, which measures objective departures from normal rainfall across historical timelines.
- **[U.S. Drought Monitor (South Dakota)](https://droughtmonitor.unl.edu/CurrentMap/StateDroughtMonitor.aspx?SD):** Tracks percentage area classifications (from D0 "Abnormally Dry" to D4 "Exceptional Drought") on a weekly basis across the state. You can download spatial and tabular data summaries filtered explicitly down to individual counties like Oglala Lakota.

### 2. Daily & Historical Precipitation Records

- **[South Dakota Mesonet Archives](https://sdgrass.org/tools-for-drought-planning/):** Operated via South Dakota State University, the Mesonet offers **daily** cumulative curves of precipitation plotted against 30-year climate normals. You can use their "Local Data" climate archives tab to isolate specific weather stations, dates, or individual monthly records. It also maps real-time soil moisture and the 4-week Evaporative Demand Drought Index (EDDI).
- **[South Dakota Drought Dashboard](https://toolkit.climate.gov/tool/south-dakota-drought-dashboard):** Hosted via the U.S. Climate Resilience Toolkit, this offers map-based regional tracking combining short-term 1–7 day precipitation forecasts with historical monthly monitoring.
- **[NCEI County-Level Climate Data](https://data.pressconnects.com/weather-data/oglala-lakota-county/46102/2024-01-01/):** For raw monthly records dating back to 1895, the National Centers for Environmental Information (NCEI) updates monthly precipitation, rainfall, and temperature data specifically mapped to Oglala Lakota County.

### 3. Local Data Collection Pipeline

* **[collect_data.qmd](file:///Users/brianyandell/Documents/GitHub/rainDrought/collect_data.qmd)**: A Python-based Quarto pipeline that fetches and stores the 10-year datasets in the `data/` directory.
  - Saves weekly drought records to [oglala_lakota_drought_weekly.csv](file:///Users/brianyandell/Documents/GitHub/rainDrought/data/oglala_lakota_drought_weekly.csv).
  - Saves daily statewide average precipitation records to [south_dakota_precipitation_daily.csv](file:///Users/brianyandell/Documents/GitHub/rainDrought/data/south_dakota_precipitation_daily.csv).
  - To run the pipeline and generate the report and visualizations, execute `quarto render collect_data.qmd` in the terminal.
* **[plot_records.qmd](file:///Users/brianyandell/Documents/GitHub/rainDrought/plot_records.qmd)**: A Quarto document utilizing `plotnine` to visualize the datasets:
  - Plots both variables (DSCI and 365-day rolling rain) over time in a faceted layout.
  - Plots cumulative precipitation vs. DSCI (overall) as a scatter plot.
  - Plots annual cumulative rain vs. cumulative drought index (DSCI) as separate curves by year, colored in a rainbow series with an explicit legend.
  - To generate the report, run `quarto render plot_records.qmd` in the terminal.
