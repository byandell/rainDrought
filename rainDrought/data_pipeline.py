import os
import datetime
import requests
import pandas as pd
from IPython.display import display, Markdown

def run_pipeline(config):
    # Create target data directory
    os.makedirs("data", exist_ok=True)

    print(f"Active State: {config['state_name']} ({config['state']})")
    print("Active Counties:")
    for county in config["counties"]:
        print(f"  - {county['name']} (FIPS: {county['fips']}, Label: {county['label']})")

    # Calculate dynamic dates for the past 10 years
    today = datetime.date.today()
    try:
        start_date = today.replace(year=today.year - 10)
    except ValueError:
        # Handle leap year edge case (Feb 29)
        start_date = today.replace(year=today.year - 10, day=28)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = today.strftime("%Y-%m-%d")

    print(f"\nTimeframe: {start_date_str} to {end_date_str}")

    # --- Task 1: Fetch U.S. Drought Monitor Data for Counties ---
    for county in config["counties"]:
        fips_code = county["fips"]
        county_name = county["name"]
        filename = county["filename"]
        
        usdm_url = (
            f"https://usdmdataservices.unl.edu/api/CountyStatistics/GetDroughtSeverityStatisticsByAreaPercent"
            f"?aoi={fips_code}&startdate={start_date_str}&enddate={end_date_str}&statisticsType=1"
        )
        print(f"Querying USDM API for {county_name}...")
        usdm_response = requests.get(usdm_url)
        if usdm_response.status_code == 200:
            usdm_csv = usdm_response.text
            usdm_path = os.path.join("data", filename)
            with open(usdm_path, "w", encoding="utf-8") as f:
                f.write(usdm_csv)
            print(f"-> Successfully saved weekly drought data to {usdm_path}")
        else:
            print(f"-> Error fetching USDM data for {county_name}: {usdm_response.status_code}")
            print(usdm_response.text[:500])

    # --- Task 2: Fetch Daily Precipitation Records for State Mean ---
    acis_url = "https://data.rcc-acis.org/GridData"
    acis_payload = {
        "state": config["state"],
        "sdate": start_date_str,
        "edate": end_date_str,
        "grid": "1",
        "elems": [{"name": "pcpn", "area_reduce": "state_mean"}]
    }

    print(f"Querying ACIS GridData API...")
    acis_response = requests.post(acis_url, json=acis_payload)
    if acis_response.status_code == 200:
        acis_json = acis_response.json()
        raw_records = acis_json.get("data", [])
        
        # Process the nested list format into a standard DataFrame
        processed = []
        state_key = config["state"].upper()
        for date_val, val_dict in raw_records:
            val = val_dict.get(state_key) if isinstance(val_dict, dict) else None
            # Handle potential trace ('T') or missing ('M') string codes
            if val is None or val in ["M", "M ", " M", ""]:
                val_float = None
            elif val == "T" or val == "T ":
                val_float = 0.0001
            else:
                try:
                    val_float = float(val)
                except ValueError:
                    val_float = None
            processed.append({"date": date_val, "precipitation_inches": val_float})
            
        df_precip = pd.DataFrame(processed)
        precip_path = os.path.join("data", config["precip_filename"])
        df_precip.to_csv(precip_path, index=False)
        print(f"-> Successfully saved daily precipitation data to {precip_path}")
    else:
        print(f"-> Error fetching ACIS data: {acis_response.status_code}")
        print(acis_response.text[:500])

def show_summaries(config):
    for county in config["counties"]:
        name = county["name"]
        filename = county["filename"]
        csv_path = os.path.join("data", filename)
        
        if os.path.exists(csv_path):
            df_c = pd.read_csv(csv_path)
            df_c["ValidStart"] = pd.to_datetime(df_c["ValidStart"])
            df_c["ValidEnd"] = pd.to_datetime(df_c["ValidEnd"])
            df_c = df_c.sort_values("ValidStart").reset_index(drop=True)
            
            display(Markdown(f"## U.S. Drought Monitor Data Summary ({name})"))
            display(Markdown(f"**Weekly USDM records:** {len(df_c)}"))
            display(df_c[["ValidStart", "County", "None", "D0", "D1", "D2", "D3", "D4"]].tail())
            
            display(Markdown(f"### {name} Drought Summary Stats"))
            display(df_c[["None", "D0", "D1", "D2", "D3", "D4"]].describe())
            display(Markdown("***"))

    precip_path = os.path.join("data", config["precip_filename"])
    if os.path.exists(precip_path):
        df_precip = pd.read_csv(precip_path)
        df_precip["date"] = pd.to_datetime(df_precip["date"])
        df_precip = df_precip.sort_values("date").reset_index(drop=True)
        
        display(Markdown(f"## Daily Precipitation Data Summary ({config['state_name']})"))
        display(Markdown(f"**Number of daily precipitation records:** {len(df_precip)}"))
        display(df_precip.tail())
        
        display(Markdown(f"### Precipitation Summary Stats"))
        display(df_precip["precipitation_inches"].describe())
