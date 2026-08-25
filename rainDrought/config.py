"""
Configuration Loader for South Dakota Rain and Drought Analysis.

This module handles parsing the `config.csv` configuration file if it exists,
falling back to default settings (South Dakota state mean precipitation, Oglala 
Lakota County, and Todd County drought statistics) if the file is missing or invalid.
"""

import os
import pandas as pd

# Helper to read configuration with defaults
DEFAULT_STATE = "sd"
DEFAULT_STATE_NAME = "South Dakota"
DEFAULT_COUNTIES = [
    {
        "fips": "46102",
        "name": "Oglala Lakota County",
        "label": "Pine Ridge",
        "filename": "oglala_lakota_drought_weekly.csv"
    },
    {
        "fips": "46121",
        "name": "Todd County",
        "label": "Rosebud",
        "filename": "todd_drought_weekly.csv"
    }
]
DEFAULT_PRECIP_FILENAME = "south_dakota_precipitation_daily.csv"

def get_config():
    """
    Parses config.csv from the root folder or falls back to defaults.

    Returns:
        dict: A dictionary containing:
            - "state" (str): The state postal abbreviation (lowercase).
            - "state_name" (str): Full official name of the state.
            - "counties" (list of dict): List of county configurations with keys
              "fips", "name", "label", and "filename".
            - "precip_filename" (str): Filename for caching daily precipitation.
    """
    config = {
        "state": DEFAULT_STATE,
        "state_name": DEFAULT_STATE_NAME,
        "counties": DEFAULT_COUNTIES,
        "precip_filename": DEFAULT_PRECIP_FILENAME
    }
    config_path = "config.csv"
    if os.path.exists(config_path):
        try:
            df_cfg = pd.read_csv(config_path)
            # Parse state
            df_state = df_cfg[df_cfg["type"].str.lower().str.strip() == "state"]
            if not df_state.empty:
                row = df_state.iloc[0]
                config["state"] = str(row["code"]).strip().lower()
                config["state_name"] = str(row["name"]).strip()
                # Dynamic precip filename for custom state
                config["precip_filename"] = f"{config['state_name'].lower().replace(' ', '_')}_precipitation_daily.csv"
            
            # Parse counties
            df_counties = df_cfg[df_cfg["type"].str.lower().str.strip() == "county"]
            if not df_counties.empty:
                counties_list = []
                for _, row in df_counties.iterrows():
                    fips = str(row["code"]).strip()
                    name = str(row["name"]).strip()
                    label = str(row["label"]).strip() if pd.notna(row["label"]) and str(row["label"]).strip() != "" else name
                    # Dynamic filename for custom county
                    filename = f"{name.lower().replace(' ', '_').replace('.', '')}_drought_weekly.csv"
                    counties_list.append({
                        "fips": fips,
                        "name": name,
                        "label": label,
                        "filename": filename
                    })
                config["counties"] = counties_list
        except Exception as e:
            print(f"Warning: Failed to load config.csv ({e}). Using defaults.")
    return config
