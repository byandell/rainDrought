# Developer Documentation

Welcome to the Developer Documentation for the South Dakota Rain and Drought Analysis project. This guide provides technical onboarding, architectural details, data pipeline schema description, and local build instructions.

***

## 1. Project Directory & Architecture

This repository is structured as a **Quarto Website** that processes and visualizes 10 years of South Dakota mean daily precipitation and county-level weekly U.S. Drought Monitor (USDM) statistics. 

### Key Files
- **[`_quarto.yml`](_quarto.yml)**: The main configuration file specifying the website title, navigation bar, format options (such as `embed-resources: true` to generate self-contained HTML files), and the output directory (`docs`).
- **[`index.qmd`](index.qmd)**: The website's welcome page containing project goals, background, and data source links.
- **[`collect_data.qmd`](collect_data.qmd)**: A Python-based data collection pipeline. It queries external REST APIs, processes raw inputs, and caches the records as CSVs in `data/`.
- **[`plot_records.qmd`](plot_records.qmd)**: A Python-based interactive dashboard that leverages **Plotly** to visualize trends and trajectories.
- **[`AGENTS.md`](AGENTS.md)**: Coding style guide and instructions for AI agents.
- **[`README.md`](README.md)**: Quick-start guide and general repository overview.

### Output Layout
The site is compiled into the **[`docs/`](docs/)** directory:
- `docs/index.html` (rendered overview)
- `docs/collect_data.html` (rendered pipeline logs and summaries)
- `docs/plot_records.html` (rendered interactive charts)
- `docs/search.json` (search index for the site)

> [!IMPORTANT]
> The directory `docs/site_libs/` is ignored via [`.gitignore`](.gitignore) because all pages are compiled as standalone HTML documents with assets embedded natively. Do not stage or commit files inside `docs/site_libs/`.

***

## 2. Local Environment Setup

The workspace is configured to use a specific Python Conda environment.

### Target Executable
Always run commands and scripts using the Earth Analytics Python environment:
```bash
/users/brianyandell/miniconda3/envs/earth-analytics-python/bin/python
```

### Dependencies
The Python script blocks require the following libraries:
- `pandas` (Data manipulation)
- `numpy` (Vector operations)
- `requests` (API requests)
- `plotly` (Interactive visualizations)
- `matplotlib` & `seaborn` (Static data validation charts)

To install or update dependencies in the environment, run:
```bash
/users/brianyandell/miniconda3/envs/earth-analytics-python/bin/python -m pip install pandas requests plotly matplotlib seaborn
```


***

## 2.5. Location Configuration (`config.csv`)

By default, the project processes data for South Dakota, Oglala Lakota County, and Todd County. You can customize the state and counties analyzed by creating a `config.csv` file in the root of the repository.

### Configuration Templates
The repository includes two pre-configured CSV templates:
- **[`config.csv.default`](config.csv.default)**: The default configuration (South Dakota, Pine Ridge, Rosebud) used for the live site.
- **[`config.csv.example`](config.csv.example)**: An example configuration (Nebraska, Lancaster County) showing custom region setups.

To set up a custom analysis, copy either of these templates to a new `config.csv` file in the root directory:
```bash
cp config.csv.default config.csv
# or
cp config.csv.example config.csv
```


### Schema Parameters
- **`type`**: Row type, either `state` or `county`.
- **`code`**: The lowercase state abbreviation (e.g. `ne`) or the FIPS county code (e.g. `31107`).
- **`name`**: Full official name of the state or county.
- **`label`**: Short label for plots and legends (e.g. `Rosebud` or `Lancaster`).

### Output Naming Convention
- **Default state**: `data/south_dakota_precipitation_daily.csv`
- **Custom state**: `data/{state_name_lower}_precipitation_daily.csv`
- **Default counties**: `data/oglala_lakota_drought_weekly.csv`, `data/todd_drought_weekly.csv`
- **Custom counties**: `data/{county_name_lower}_drought_weekly.csv`

The file `config.csv` is ignored in Git to prevent local region settings from overriding the default South Dakota pages deployed to GitHub Pages.

***

## 3. Data Pipeline & Endpoints

Data collection is automated within [`collect_data.qmd`](collect_data.qmd). When executed, the pipeline performs two main API tasks:

### Task 1: Weekly U.S. Drought Monitor (USDM) County Data
- **Source**: National Drought Mitigation Center (NDMC)
- **API Endpoint**: `https://usdmdataservices.unl.edu/api/CountyStatistics/GetDroughtSeverityStatisticsByAreaPercent`
- **Request Parameters**:
  - `aoi`: FIPS county code (`46102` for Oglala Lakota County, `46121` for Todd County)
  - `startdate`: Dynamic start date from 10 years ago (`YYYY-MM-DD`)
  - `enddate`: Today's date (`YYYY-MM-DD`)
  - `statisticsType`: `1` (representing area percent)
- **Outputs**:
  - [`data/oglala_lakota_drought_weekly.csv`](data/oglala_lakota_drought_weekly.csv)
  - [`data/todd_drought_weekly.csv`](data/todd_drought_weekly.csv)

### Task 2: Daily Precipitation (ACIS GridData)
- **Source**: NOAA Regional Climate Centers (RCCs)
- **API Endpoint**: `https://data.rcc-acis.org/GridData`
- **JSON Payload Parameters**:
  - `state`: `"sd"` (South Dakota)
  - `sdate` / `edate`: Start and end date range
  - `grid`: `"1"` (NRCC Interpolated Grid)
  - `elems`: `[{"name": "pcpn", "area_reduce": "state_mean"}]`
- **Output**:
  - [`data/south_dakota_precipitation_daily.csv`](data/south_dakota_precipitation_daily.csv)

***

## 4. Data Processing Standards & Formulas

When fetching and cleaning raw data, follow these standards:

### Drought Severity and Coverage Index (DSCI)
The weekly county-level USDM statistics include five severity categories (`D0` to `D4`), representing the percentage area of the county experiencing that level of drought (or worse). The DSCI is calculated as the sum of these percentages:
$$\text{DSCI} = \text{D0} + \text{D1} + \text{D2} + \text{D3} + \text{D4}$$
- The resulting DSCI ranges between `0` (no drought) and `500` (100% of the county is in D4 Exceptional Drought).

### Precipitation Clean-Up
- **Trace Amounts**: Daily precipitation data containing `'T'` or `'T '` are parsed and converted to `0.0001` inches.
- **Missing Data**: Entries containing `'M'` or empty strings are set to `None` / `NaN` in the data frame.

### Cumulative Aggregations
To evaluate annual progressions:
- Group records by year (`date.dt.year`).
- Compute cumulative sums (`cumsum()`) for precipitation and DSCI values starting January 1st of each year.

***

## 5. Visualizations & Plotly Controls

The dashboard page [`plot_records.qmd`](plot_records.qmd) compiles three primary interactive dashboards:

1. **10-Year Timelines**: Displays weekly DSCI for both counties and the 365-day rolling statewide precipitation.
2. **Annual Progression over the Year**: Standardizes month on the X-axis (`tickformat="%b"`) and cumulative values on the Y-axis. Open circles mark the end of each month.
3. **Annual Trajectories of Rain vs. DSCI**: Facets the cumulative rain (X-axis) vs. cumulative DSCI (Y-axis) side-by-side. 
   - Overlaid watermark annotations (`DRY` in top-left, `WET` in bottom-right) indicate climate zones.

### Plotly Interactive Legend Toggling
To allow simultaneous visibility toggling of a specific year across multiple subplots:
- Curves share the same `legendgroup` name (e.g. `legendgroup="2020"`).
- The parent layout has `groupclick="togglegroup"` set under the legend configuration.

### Custom Reset Button
Each Plotly figure implements a custom update menu button to restore the default zoom scale:
```python
updatemenus=[
    dict(
        type="buttons",
        buttons=[
            dict(
                label="Reset View",
                method="update", # or "relayout"
                args=[{"visible": [True] * len(fig.data)}, {"xaxis.autorange": True, "yaxis.autorange": True}]
            )
        ]
    ]
]
```

***

## 6. Local Build & Deployment

### Build the Entire Site
To compile the website assets locally, execute:
```bash
quarto render
```
This command compiles `index.qmd`, `collect_data.qmd`, and `plot_records.qmd` into their corresponding HTML pages under the `docs/` folder.

### Run Data Updates
To run the pipeline and update the data caches:
```bash
quarto render collect_data.qmd
```

### GitHub Pages Deployment
1. Commit all modified source files (`.qmd`, `_quarto.yml`, `data/*.csv`, `DEVELOPER.md`) and the compiled HTML outputs in `/docs`.
2. Do not commit files inside `docs/site_libs/`.
3. Push the changes to GitHub.
4. Set the GitHub Pages source branch to `main` (or your active branch) and select `/docs` as the source folder in your repository settings.
