#!/usr/bin/env python3
"""
Rain and Drought Standalone Analysis Runner.

This script executes the entire data collection and plotting pipeline using the 
`rainDrought` package, reading from the local `config.csv` settings if present.
It saves interactive Plotly visualizations as HTML files in the `output/` folder.
"""

import os
import sys

# Set path to the parent directory of this script (repo root)
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(repo_root)

from rainDrought.config import get_config
from rainDrought.data_pipeline import run_pipeline
from rainDrought.visualizations import load_and_preprocess, plot_time_series, plot_time_vs_cumulative, plot_combined_annual_trajectories

def main():
    print("==================================================")
    print("   South Dakota Rain & Drought Analysis Runner   ")
    print("==================================================")

    # 1. Loading Configuration
    print("\n[Step 1] Loading active configuration...")
    config = get_config()
    print(f"  - Active State: {config['state_name']} ({config['state'].upper()})")
    print("  - Active Counties:")
    for county in config["counties"]:
        print(f"    * {county['name']} (FIPS {county['fips']}, Label: {county['label']})")

    # 2. Run Data Collection Pipeline
    print("\n[Step 2] Executing data collection REST API requests...")
    run_pipeline(config)

    # 3. Load Data & Log Command Line Summaries
    print("\n[Step 3] Loading cached CSV files and preprocessing...")
    try:
        merged_dfs, df_precip = load_and_preprocess(config)
        
        print("\n>>> Daily Precipitation Data Summary:")
        print(df_precip.tail(5))
        print("\n>>> Daily Precipitation Summary Stats:")
        print(df_precip["precipitation_inches"].describe())
        
        for county in config["counties"]:
            fips = county["fips"]
            print(f"\n>>> Combined USDM / Precipitation Stats for {county['name']}:")
            print(merged_dfs[fips][["dsci", "precipitation_inches", "rolling_365d_rain"]].describe())
    except Exception as e:
        print(f"Error printing dataset summaries: {e}")

    # 4. Generate & Save Visualizations
    print("\n[Step 4] Building interactive Plotly dashboards...")
    try:
        os.makedirs("output", exist_ok=True)
        
        # Create figures
        print("  - Creating time-series timelines...")
        fig_time = plot_time_series(config, merged_dfs)
        
        print("  - Creating annual cumulative progressions...")
        fig_cum = plot_time_vs_cumulative(config, merged_dfs)
        
        print("  - Creating rain vs. drought index trajectories...")
        fig_traj = plot_combined_annual_trajectories(config, merged_dfs)
        
        # Save HTML outputs
        time_path = "output/time_series.html"
        cum_path = "output/cumulative_progression.html"
        traj_path = "output/trajectories.html"
        
        fig_time.write_html(time_path)
        fig_cum.write_html(cum_path)
        fig_traj.write_html(traj_path)
        
        print(f"\nInteractive Plotly dashboards successfully saved to:")
        print(f"  - {os.path.abspath(time_path)}")
        print(f"  - {os.path.abspath(cum_path)}")
        print(f"  - {os.path.abspath(traj_path)}")
        
        # Launch figures in the browser
        print("\nOpening dashboards in your default web browser...")
        fig_time.show()
        fig_cum.show()
        fig_traj.show()

    except Exception as e:
        print(f"Error building or saving visualizations: {e}")

    print("\nAnalysis execution complete!")

if __name__ == "__main__":
    main()
