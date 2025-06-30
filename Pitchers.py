import streamlit as st
import pandas as pd
from scipy.stats import percentileofscore
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def format_pitcher_stat(stat, value):
    if pd.isnull(value):
        return "N/A"
    
    three_dp = ["BAVG", "BAbip"]
    two_dp = ["WHIP", "ERA"]
    one_dp = ["IP", "GO%", "FO%", "BB%", "SO%", "XBX%", "WP/BF", "SO/BB"]
    whole = ["ERA+"]

    if stat in three_dp:
        return f"{value:.3f}"
    elif stat in two_dp:
        return f"{value:.2f}"
    elif stat in one_dp:
        return f"{value:.1f}"
    elif stat in whole:
        return f"{round(value)}"
    else:
        return value


# ---------- Function: Compute percentiles ----------
def compute_percentiles(df, stats):
    filtered = df[(df["IP"] >= 3) & (df["BF"] >= 5)]
    percentiles = {}
    
    # Stats where lower is better (need inversion)
    invert_stats = ["ERA", "BB%", "BAbip", "WP/BF", "XBX%", "BAVG", "WHIP"]
    
    for stat in stats:
        if stat in df.columns and df[stat].dtype in ['float64', 'int64']:
            values = filtered[stat]
            if stat in invert_stats:
                percentiles[stat + "_pct"] = df[stat].apply(
                    lambda x: 100 - percentileofscore(values, x) if pd.notnull(x) else None
                )
            else:
                percentiles[stat + "_pct"] = df[stat].apply(
                    lambda x: percentileofscore(values, x) if pd.notnull(x) else None
                )
    return pd.concat([df, pd.DataFrame(percentiles)], axis=1)


# ---------- Load data ----------
data = pd.read_csv("pitchers.csv")

# ---------- Define stats to visualize ----------
stats_to_visualize = [
    "ERA", "WHIP", "SO%", "BB%", "GO%", "FO%", "BAbip", "XBX%", "SO/BB", "WP/BF", "BAVG"
]
available_stats = [stat for stat in stats_to_visualize if stat in data.columns]

# ---------- Compute percentiles ----------
data = compute_percentiles(data, available_stats)

# ---------- Table ----------
st.subheader("Pitchers")
st.write(data)

# ---------- Player selection ----------
player_names = data["Player"].unique()
selected_player = st.selectbox("Select a player", player_names)
player_data = data[data["Player"] == selected_player].iloc[0]

# ---------- Show non-percentile stats ----------
st.subheader("Stats")
excluded_columns = [stat for stat in data.columns if stat.endswith("_pct")] + available_stats
other_stats = {
    col: format_pitcher_stat(col, player_data[col])
    for col in player_data.index if col not in excluded_columns
}

other_stats_df = pd.DataFrame(other_stats.items(), columns=["Stat", "Value"])
st.dataframe(other_stats_df)

# ---------- Visual bar chart ----------
st.subheader("Percentile Rankings (Blue = Low, Red = High)")

def get_color(percentile):
    cmap = cm.get_cmap('bwr')  # blue-white-red
    norm = mcolors.Normalize(vmin=0, vmax=100)
    return mcolors.to_hex(cmap(norm(percentile)))

for stat in available_stats:
    percentile_col = stat + "_pct"
    if percentile_col in player_data and pd.notnull(player_data[percentile_col]):
        percentile = round(player_data[percentile_col])
        color = get_color(percentile)
        value_formatted = format_pitcher_stat(stat, player_data[stat])
        bar = f"""
        <div style="margin: 6px 0;">
            <strong>{stat}</strong> ({percentile}) <strong>({value_formatted})</strong>
            <div style="background-color: #eee; border-radius: 4px; overflow: hidden;">
                <div style="width: {percentile}%; background-color: {color}; padding: 4px 0;"></div>
            </div>
        </div>
        """
        st.markdown(bar, unsafe_allow_html=True)
    else:
        st.markdown(f"**{stat}**: Not enough IP or BF to calculate percentile")
