"""
Data Visualization Helpers and Dashboards.

This module houses all the rendering and preprocessing functions, including dynamic 
markdown introductions, static Matplotlib charts, and interactive Plotly subplots 
for timelines, cumulative progress, and trajectory analyses.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def show_collect_data_intro(config):
    """
    Dynamically renders the Markdown Introduction section for collect_data.qmd.

    Args:
        config (dict): The active configuration dictionary.
    """
    county_bullets = "".join([f"1. **Weekly Drought Monitor records** for {c['name']} (FIPS {c['fips']}), {config['state_name']}.\n" for c in config["counties"]])
    display(Markdown(f"""
# Introduction

This document contains Python code to programmatically retrieve, process, and store 10-year historical climate records for:
{county_bullets}
2. **Daily Precipitation records** for the State of {config['state_name']} (state-wide mean).

The collected datasets are saved to the `data/` directory.

> [!NOTE]
> **Active Region Configuration**: Default configured for **{config['state_name']}** (precipitation) and counties: {", ".join([f"{c['name']} ({c['label']})" for c in config['counties']])}.
> To customize these locations, copy the layout from `config.csv.default` (or the example from `config.csv.example`) into a new `config.csv` file and re-run.
"""))

def show_plot_records_intro(config):
    """
    Dynamically renders the Markdown Introduction section for plot_records.qmd.

    Args:
        config (dict): The active configuration dictionary.
    """
    county_names_str = " and ".join([c["name"] for c in config["counties"]])
    county_labels_str = " and ".join([c["label"] for c in config["counties"]])
    display(Markdown(f"""
# Introduction

In this document, we visualize the weekly drought records for {county_names_str} alongside daily precipitation records for {config['state_name']} using Python's **[Plotly](https://plotly.com/python/)** library, providing interactive and responsive dashboards.

We will display:
1. County drought datasets ({county_labels_str}) and the statewide rolling precipitation plotted over time (10-year timeline).
2. Time within the year (standardized month, X-axis) vs. annual cumulative values (Y-axis) for cumulative precipitation and county cumulative drought indices.
3. Annual trajectories comparing cumulative precipitation (X-axis) vs. cumulative drought index (Y-axis) faceted side-by-side by county.

> [!NOTE]
> **Active Region Configuration**: Currently configured for **{config['state_name']}** (precipitation) and counties: {", ".join([f"{c['name']} ({c['label']})" for c in config['counties']])}.
> To customize these locations, copy the layout from `config.csv.default` (or the example from `config.csv.example`) into a new `config.csv` file and re-run.
"""))

def plot_matplotlib_trends(config):
    """
    Plots a static multi-panel chart of drought index and monthly precipitation totals using Matplotlib.

    Args:
        config (dict): The active configuration dictionary.
    """
    sns.set_theme(style="whitegrid")
    num_counties = len(config["counties"])
    fig, axes = plt.subplots(num_counties + 1, 1, figsize=(7.5, 3.2 * (num_counties + 1)), sharex=False)

    # Standardize axes indexing if only 1 plot
    if num_counties + 1 == 1:
        axes = [axes]
    elif not isinstance(axes, (list, np.ndarray)):
        axes = [axes]

    for idx, county in enumerate(config["counties"]):
        filename = county["filename"]
        csv_path = os.path.join("data", filename)
        if os.path.exists(csv_path):
            df_c = pd.read_csv(csv_path)
            df_c["ValidStart"] = pd.to_datetime(df_c["ValidStart"])
            df_c = df_c.sort_values("ValidStart").reset_index(drop=True)
            
            ax = axes[idx]
            ax.fill_between(df_c["ValidStart"], df_c["D0"], color="#ffff00", alpha=0.5, label="D0 (Abnormally Dry)")
            ax.fill_between(df_c["ValidStart"], df_c["D1"], color="#fcd37f", alpha=0.6, label="D1 (Moderate Drought)")
            ax.fill_between(df_c["ValidStart"], df_c["D2"], color="#ffaa00", alpha=0.7, label="D2 (Severe Drought)")
            ax.fill_between(df_c["ValidStart"], df_c["D3"], color="#e60000", alpha=0.8, label="D3 (Extreme Drought)")
            ax.fill_between(df_c["ValidStart"], df_c["D4"], color="#730000", alpha=0.9, label="D4 (Exceptional Drought)")
            ax.set_title(f"Weekly Drought Monitor Area Severity (%) - {county['name']}", fontsize=11, fontweight="bold")
            ax.set_ylabel("Cumulative % Area affected", fontsize=9)
            ax.set_ylim(0, 100)
            ax.legend(loc="upper right", frameon=True, fontsize=8)

    # Plot Monthly Aggregated Precipitation
    precip_path = os.path.join("data", config["precip_filename"])
    if os.path.exists(precip_path):
        df_precip = pd.read_csv(precip_path)
        df_precip["date"] = pd.to_datetime(df_precip["date"])
        df_precip = df_precip.sort_values("date").reset_index(drop=True)
        df_precip["year_month"] = df_precip["date"].dt.to_period("M")
        df_monthly = df_precip.groupby("year_month")["precipitation_inches"].sum().reset_index()
        df_monthly["date_index"] = df_monthly["year_month"].dt.to_timestamp()
        
        ax = axes[num_counties]
        ax.bar(df_monthly["date_index"], df_monthly["precipitation_inches"], width=25, color="#1f77b4", alpha=0.8)
        df_monthly["rolling_mean"] = df_monthly["precipitation_inches"].rolling(12, center=True).mean()
        ax.plot(df_monthly["date_index"], df_monthly["rolling_mean"], color="#d62728", linewidth=2.2, label="12-Month Rolling Mean")
        ax.set_title(f"{config['state_name']} Monthly Total Precipitation (Statewide Average)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Precipitation (inches)", fontsize=9)
        ax.legend(loc="upper right", frameon=True, fontsize=8)

    plt.tight_layout()
    plt.show()

def load_and_preprocess(config):
    """
    Loads daily precipitation and county drought records, aggregates calculations, and aligns them.

    This function cleans the datasets, computes the Drought Severity and Coverage Index (DSCI),
    calculates cumulative precipitation values since Jan 1st of each year, calculates 365-day 
    rolling precipitation sums, and merges dataframes on dates.

    Args:
        config (dict): The active configuration dictionary.

    Returns:
        tuple: A tuple containing:
            - merged_dfs (dict): Merged county dataframes indexed by FIPS code.
            - df_precip (pd.DataFrame): Preprocessed daily precipitation dataframe.
    """
    # Load precipitation daily data
    precip_path = os.path.join("data", config["precip_filename"])
    df_precip = pd.read_csv(precip_path)
    df_precip["date"] = pd.to_datetime(df_precip["date"])
    df_precip = df_precip.sort_values("date").reset_index(drop=True)
    df_precip["cumulative_rain"] = df_precip["precipitation_inches"].cumsum()
    df_precip["year"] = df_precip["date"].dt.year
    df_precip["cumulative_rain_year"] = df_precip.groupby("year")["precipitation_inches"].cumsum()
    df_precip["rolling_365d_rain"] = df_precip["precipitation_inches"].rolling(window=365, min_periods=1).sum()

    # Load and process each county's data
    county_dfs = {}
    merged_dfs = {}
    for county in config["counties"]:
        fips = county["fips"]
        name = county["name"]
        filename = county["filename"]
        csv_path = os.path.join("data", filename)
        
        df_c = pd.read_csv(csv_path)
        df_c["date"] = pd.to_datetime(df_c["ValidStart"])
        df_c["dsci"] = df_c["D0"] + df_c["D1"] + df_c["D2"] + df_c["D3"] + df_c["D4"]
        df_c["year"] = df_c["date"].dt.year
        df_c = df_c.sort_values("date")
        df_c["cumulative_dsci_year"] = df_c.groupby("year")["dsci"].cumsum()
        county_dfs[fips] = df_c
        
        # Merge with precipitation
        df_merged = pd.merge(
            df_c[["date", "year", "dsci", "cumulative_dsci_year"]], 
            df_precip[["date", "precipitation_inches", "cumulative_rain_year", "rolling_365d_rain"]], 
            on="date", 
            how="inner"
        ).sort_values("date").reset_index(drop=True)
        df_merged["year_str"] = df_merged["year"].astype(str)
        df_merged["day_in_year"] = pd.to_datetime(df_merged["date"].dt.strftime("2020-%m-%d"))
        merged_dfs[fips] = df_merged

    return merged_dfs, df_precip

def plot_time_series(config, merged_dfs):
    """
    Creates and returns a Plotly timeline subplot dashboard of climate metrics over 10 years.

    Args:
        config (dict): The active configuration dictionary.
        merged_dfs (dict): The merged county dataframes.

    Returns:
        go.Figure: The constructed Plotly figure.
    """
    num_counties = len(config["counties"])
    subplot_titles = [f"DSCI - {c['label']}" for c in config["counties"]] + [
        f"365-Day Rolling Precipitation (inches) [{config['state_name']} Mean]"
    ]

    fig_time = make_subplots(
        rows=num_counties + 1, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.06,
        subplot_titles=subplot_titles
    )

    # Plot each county
    colors_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for idx, county in enumerate(config["counties"]):
        fips = county["fips"]
        label = county["label"]
        df_merged = merged_dfs[fips]
        color = colors_palette[idx % len(colors_palette)]
        
        fig_time.add_trace(
            go.Scatter(
                x=df_merged["date"], 
                y=df_merged["dsci"], 
                name=f"{label} DSCI", 
                line=dict(color=color, width=1.5)
            ), 
            row=idx+1, col=1
        )

    # Plot precipitation
    first_fips = config["counties"][0]["fips"]
    df_first = merged_dfs[first_fips]
    fig_time.add_trace(
        go.Scatter(
            x=df_first["date"], 
            y=df_first["rolling_365d_rain"], 
            name="365-Day Rolling Precip", 
            line=dict(color="#2ca02c", width=1.5)
        ), 
        row=num_counties + 1, col=1
    )

    fig_height = 220 * num_counties + 210

    reset_args = {
        f"xaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 2)
    }
    reset_args.update({
        f"yaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 2)
    })

    fig_time.update_layout(
        height=fig_height, 
        template="plotly_white", 
        title=dict(
            text="10-Year Climate Metrics Over Time",
            y=0.98,
            x=0.5,
            xanchor="center",
            yanchor="top"
        ),
        margin=dict(t=50),
        showlegend=False,
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1,
                y=0,
                xanchor="left",
                yanchor="bottom",
                showactive=False,
                buttons=[
                    dict(
                        label="Reset View",
                        method="relayout",
                        args=[reset_args]
                    )
                ]
            )
        ]
    )
    return fig_time

def plot_time_vs_cumulative(config, merged_dfs):
    """
    Creates and returns a Plotly dashboard comparing annual cumulative progression over the months of the year.

    Args:
        config (dict): The active configuration dictionary.
        merged_dfs (dict): The merged county dataframes.

    Returns:
        go.Figure: The constructed Plotly figure.
    """
    first_fips = config["counties"][0]["fips"]
    df_first = merged_dfs[first_fips]
    years = sorted(df_first["year_str"].unique())
    colors = px.colors.sample_colorscale("turbo", [i / (len(years) - 1) for i in range(len(years))])
    year_colors = dict(zip(years, colors))

    num_counties = len(config["counties"])
    subplot_titles = [f"Cumulative Precipitation ({config['state_name']} Mean)"] + [
        f"Cumulative Drought Index ({c['label']})" for c in config["counties"]
    ]

    fig_cum_time = make_subplots(
        rows=num_counties + 1, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.06,
        subplot_titles=subplot_titles
    )

    # Identify month-end markers for each county
    month_ends_dfs = {}
    for county in config["counties"]:
        fips = county["fips"]
        df_merged = merged_dfs[fips]
        df_month_ends = df_merged.groupby(["year", df_merged["date"].dt.month]).tail(1).copy()
        df_month_ends["day_in_year"] = pd.to_datetime(df_month_ends["date"].dt.strftime("2020-%m-%d"))
        month_ends_dfs[fips] = df_month_ends

    for year in years:
        # 1. Cumulative Precipitation (row 1)
        df_y_p = df_first[df_first["year_str"] == year]
        df_pts_p = month_ends_dfs[first_fips][month_ends_dfs[first_fips]["year_str"] == year]
        
        fig_cum_time.add_trace(
            go.Scatter(
                x=df_y_p["day_in_year"], y=df_y_p["cumulative_rain_year"], 
                mode="lines", line=dict(color=year_colors[year]), 
                name=year, legendgroup=year, showlegend=True
            ), 
            row=1, col=1
        )
        fig_cum_time.add_trace(
            go.Scatter(
                x=df_pts_p["day_in_year"], y=df_pts_p["cumulative_rain_year"], 
                mode="markers", marker=dict(symbol="circle-open", size=5, color=year_colors[year], line=dict(width=1)), 
                name=year, legendgroup=year, showlegend=False
            ), 
            row=1, col=1
        )
        
        # 2..N+1. Counties DSCI
        for idx, county in enumerate(config["counties"]):
            fips = county["fips"]
            df_y_c = merged_dfs[fips][merged_dfs[fips]["year_str"] == year]
            df_pts_c = month_ends_dfs[fips][month_ends_dfs[fips]["year_str"] == year]
            
            fig_cum_time.add_trace(
                go.Scatter(
                    x=df_y_c["day_in_year"], y=df_y_c["cumulative_dsci_year"], 
                    mode="lines", line=dict(color=year_colors[year]), 
                    name=year, legendgroup=year, showlegend=False
                ), 
                row=idx+2, col=1
            )
            fig_cum_time.add_trace(
                go.Scatter(
                    x=df_pts_c["day_in_year"], y=df_pts_c["cumulative_dsci_year"], 
                    mode="markers", marker=dict(symbol="circle-open", size=5, color=year_colors[year], line=dict(width=1)), 
                    name=year, legendgroup=year, showlegend=False
                ), 
                row=idx+2, col=1
            )

    fig_height = 290 + 295 * num_counties

    reset_args = {
        f"xaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 2)
    }
    reset_args.update({
        f"yaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 2)
    })

    fig_cum_time.update_layout(
        height=fig_height,
        template="plotly_white",
        title=dict(
            text="Annual Progression of Cumulative Climate Metrics",
            y=0.96, x=0.5, xanchor="center", yanchor="top"
        ),
        margin=dict(t=90),
        legend=dict(
            groupclick="togglegroup",
            itemdoubleclick="toggleothers",
            itemclick="toggle",
            title_text="Year"
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1,
                y=0,
                xanchor="left",
                yanchor="bottom",
                showactive=False,
                buttons=[
                    dict(
                        label="Reset View",
                        method="update",
                        args=[
                            {"visible": [True] * len(fig_cum_time.data)},
                            reset_args
                        ]
                    )
                ]
            )
        ]
    )
    fig_cum_time.update_xaxes(tickformat="%b", dtick="M1")
    return attach_debounced_legend_listener(fig_cum_time)

def plot_combined_annual_trajectories(config, merged_dfs):
    """
    Creates and returns a Plotly dashboard showing cumulative rain vs cumulative drought index trajectories.

    Args:
        config (dict): The active configuration dictionary.
        merged_dfs (dict): The merged county dataframes.

    Returns:
        go.Figure: The constructed Plotly figure.
    """
    first_fips = config["counties"][0]["fips"]
    df_first = merged_dfs[first_fips]
    years = sorted(df_first["year_str"].unique())
    colors = px.colors.sample_colorscale("turbo", [i / (len(years) - 1) for i in range(len(years))])
    year_colors = dict(zip(years, colors))

    num_counties = len(config["counties"])
    subplot_titles = [county["label"] for county in config["counties"]]

    fig_combined_annual = make_subplots(
        rows=1, cols=num_counties, 
        shared_yaxes=True, 
        horizontal_spacing=0.08,
        subplot_titles=subplot_titles
    )

    # Identify month-end markers for each county
    month_ends_dfs = {}
    for county in config["counties"]:
        fips = county["fips"]
        df_merged = merged_dfs[fips]
        df_month_ends = df_merged.groupby(["year", df_merged["date"].dt.month]).tail(1).copy()
        month_ends_dfs[fips] = df_month_ends

    for year in years:
        for idx, county in enumerate(config["counties"]):
            fips = county["fips"]
            df_y_c = merged_dfs[fips][merged_dfs[fips]["year_str"] == year]
            df_pts_c = month_ends_dfs[fips][month_ends_dfs[fips]["year_str"] == year]
            
            fig_combined_annual.add_trace(
                go.Scatter(
                    x=df_y_c["cumulative_rain_year"], y=df_y_c["cumulative_dsci_year"], 
                    mode="lines", line=dict(color=year_colors[year]), 
                    name=year, legendgroup=year, showlegend=(idx == 0)
                ), 
                row=1, col=idx+1
            )
            fig_combined_annual.add_trace(
                go.Scatter(
                    x=df_pts_c["cumulative_rain_year"], y=df_pts_c["cumulative_dsci_year"], 
                    mode="markers", marker=dict(symbol="circle-open", size=5, color=year_colors[year], line=dict(width=1)), 
                    name=year, legendgroup=year, showlegend=False
                ), 
                row=1, col=idx+1
            )

    for idx in range(num_counties):
        col_str = str(idx + 1) if idx > 0 else ""
        fig_combined_annual.add_annotation(
            xref=f"x{col_str} domain", yref=f"y{col_str} domain",
            x=0.15, y=0.85,
            text="<b>DRY</b>",
            showarrow=False,
            font=dict(size=40, color="rgba(150, 150, 150, 0.2)"),
            textangle=-30
        )
        fig_combined_annual.add_annotation(
            xref=f"x{col_str} domain", yref=f"y{col_str} domain",
            x=0.85, y=0.15,
            text="<b>WET</b>",
            showarrow=False,
            font=dict(size=40, color="rgba(150, 150, 150, 0.2)"),
            textangle=-30
        )

    reset_args = {
        f"xaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 1)
    }
    reset_args.update({
        f"yaxis{i if i > 1 else ''}.autorange": True for i in range(1, num_counties + 1)
    })

    fig_combined_annual.update_layout(
        height=480, 
        template="plotly_white", 
        title=dict(
            text="Annual Cumulative Rain vs. Cumulative Drought Index (DSCI) Trajectories",
            y=0.94,
            x=0.5,
            xanchor="center",
            yanchor="top"
        ),
        margin=dict(t=65),
        legend=dict(
            groupclick="togglegroup",
            itemdoubleclick="toggleothers",
            itemclick="toggle",
            title_text="Year"
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1,
                y=0,
                xanchor="left",
                yanchor="bottom",
                showactive=False,
                buttons=[
                    dict(
                        label="Reset View",
                        method="update",
                        args=[
                            {"visible": [True] * len(fig_combined_annual.data)},
                            reset_args
                        ]
                    )
                ]
            )
        ]
    )
    fig_combined_annual.update_xaxes(title_text="Cumulative Precipitation (inches)")
    fig_combined_annual.update_yaxes(title_text="Cumulative DSCI", row=1, col=1)
    return attach_debounced_legend_listener(fig_combined_annual)


LEGEND_DEBOUNCED_POST_SCRIPT = """
(function() {
    var gd = (typeof arguments !== 'undefined' && arguments.length > 0 && arguments[0]) ? arguments[0] : null;
    if (!gd) {
        var scripts = document.getElementsByTagName('script');
        var currScript = scripts[scripts.length - 1];
        if (currScript && currScript.previousElementSibling && currScript.previousElementSibling.classList.contains('plotly-graph-div')) {
            gd = currScript.previousElementSibling;
        }
    }
    if (!gd) {
        var divs = document.querySelectorAll('.plotly-graph-div, .js-plotly-plot');
        if (divs.length > 0) gd = divs[divs.length - 1];
    }
    if (gd && gd.on && !gd._debouncedLegendAttached) {
        gd._debouncedLegendAttached = true;
        var clickTimer = null;
        var clickCount = 0;
        var lastGroup = null;
        var lastCurve = null;

        function performSingleClick(group, curveNumber) {
            if (!gd.data || gd.data.length === 0) return;
            var currentVisible = gd.data[curveNumber] ? gd.data[curveNumber].visible : true;
            var newVisible = (currentVisible === 'legendonly') ? true : 'legendonly';
            var update = {visible: []};
            for (var i = 0; i < gd.data.length; i++) {
                var trace = gd.data[i];
                if (group !== null && group !== undefined && group !== '') {
                    if (trace.legendgroup === group) {
                        update.visible.push(newVisible);
                    } else {
                        update.visible.push(trace.visible !== undefined ? trace.visible : true);
                    }
                } else {
                    if (i === curveNumber) {
                        update.visible.push(newVisible);
                    } else {
                        update.visible.push(trace.visible !== undefined ? trace.visible : true);
                    }
                }
            }
            Plotly.restyle(gd, update);
        }

        function performDoubleClick(group, curveNumber) {
            if (!gd.data || gd.data.length === 0) return;
            var otherVisible = false;
            for (var i = 0; i < gd.data.length; i++) {
                var trace = gd.data[i];
                var isMatch = (group !== null && group !== undefined && group !== '') ? (trace.legendgroup === group) : (i === curveNumber);
                if (!isMatch && trace.visible !== 'legendonly') {
                    otherVisible = true;
                    break;
                }
            }
            var update = {visible: []};
            for (var i = 0; i < gd.data.length; i++) {
                var trace = gd.data[i];
                var isMatch = (group !== null && group !== undefined && group !== '') ? (trace.legendgroup === group) : (i === curveNumber);
                if (otherVisible) {
                    update.visible.push(isMatch ? true : 'legendonly');
                } else {
                    update.visible.push(true);
                }
            }
            Plotly.restyle(gd, update);
        }

        function resetState() {
            clickCount = 0;
            lastGroup = null;
            lastCurve = null;
            clickTimer = null;
        }

        gd.on('plotly_legendclick', function(data) {
            var curveNumber = data.curveNumber;
            var group = (data.data && data.data[curveNumber]) ? data.data[curveNumber].legendgroup : null;

            if (clickTimer && (group !== lastGroup || (group === null && curveNumber !== lastCurve))) {
                clearTimeout(clickTimer);
                performSingleClick(lastGroup, lastCurve);
                resetState();
            }

            clickCount++;
            lastGroup = group;
            lastCurve = curveNumber;

            if (clickCount === 1) {
                var targetGroup = group;
                var targetCurve = curveNumber;
                clickTimer = setTimeout(function() {
                    performSingleClick(targetGroup, targetCurve);
                    resetState();
                }, 250);
            } else if (clickCount >= 2) {
                if (clickTimer) {
                    clearTimeout(clickTimer);
                }
                var targetGroup = group;
                var targetCurve = curveNumber;
                performDoubleClick(targetGroup, targetCurve);
                resetState();
            }

            return false;
        });

        gd.on('plotly_legenddoubleclick', function() {
            return false;
        });
    }
})();
"""

def attach_debounced_legend_listener(fig):
    import plotly.io as pio
    def _custom_repr_html_():
        return pio.to_html(fig, include_plotlyjs='cdn', full_html=False, post_script=LEGEND_DEBOUNCED_POST_SCRIPT)
    fig._repr_html_ = _custom_repr_html_
    return fig
