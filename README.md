# SD Rain and Drought Analysis Project

This repository programmatically collects, aligns, and visualizes 10 years of daily precipitation records for the state of South Dakota and weekly U.S. Drought Monitor (USDM) data for Oglala Lakota County (FIPS `46102`) and Todd County (FIPS `46121`).

It compiles into a fully interactive, self-contained multi-page website published via GitHub Pages.

---

## Website Navigation

The compiled website is located in the **[docs/](docs/)** folder and contains:
- **[Overview (docs/index.html)](docs/index.html)**: Project overview, data sources, and links.
- **[Data Collection (docs/collect_data.html)](docs/collect_data.html)**: Historical API download pipeline and documentation.
- **[Interactive Analysis (docs/plot_records.html)](docs/plot_records.html)**: Interactive climate dashboards displaying faceted timelines, time-vs-cumulative metrics, and side-by-side annual trajectories.

---

## File Directory

- **`_quarto.yml`**: Quarto website configuration file.
- **`index.qmd`**: Welcome page of the Quarto website.
- **[rainDrought.md](rainDrought.md)**: Repository overview documenting project requirements and authoritative data sources.
- **`collect_data.qmd`**: Python script that queries the ACIS GridData and USDM APIs to download data.
- **`plot_records.qmd`**: Python script that parses, merges, and visualizes the records using Plotly.
- **`data/`**: Directory containing retrieved CSV files:
  - `oglala_lakota_drought_weekly.csv` (Oglala Lakota weekly drought)
  - `todd_drought_weekly.csv` (Todd County weekly drought)
  - `south_dakota_precipitation_daily.csv` (South Dakota daily mean precipitation)
- **`docs/`**: Output directory for the compiled site. All resources are embedded directly in the HTML pages. The local `docs/site_libs/` asset directory is excluded from Git.

---

## Getting Started

### 1. Build and Compile the Website
To compile all `.qmd` pages into the self-contained static site inside `/docs`, run:
```bash
quarto render
```

### 2. Run Data Updates
To query the endpoints and refresh the local CSV files, render the collection pipeline:
```bash
quarto render collect_data.qmd
```
