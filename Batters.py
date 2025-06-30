import streamlit as st
import pandas as pd
from scipy.stats import percentileofscore
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ---------- Function: Compute percentiles ----------
def compute_percentiles(df, stats):
    df = df[df["PA"] >=5]
    percentiles = {}
    for stat in stats:
            if stat in df.columns and df[stat].dtype in ['float64', 'int64']:
                values = df[stat]
                if stat == "SO%":
                    try:
                    # Invert SO% so lower is better
                        percentiles[stat + "_pct"] = values.apply(lambda x: 100 - percentileofscore(values, x))
                    except:
                        continue
                else:
                    try:
                        percentiles[stat + "_pct"] = values.apply(lambda x: percentileofscore(values, x))
                    except:
                        continue
    return pd.concat([df, pd.DataFrame(percentiles)], axis=1)

# ---------- Load data ----------
data = pd.read_csv("batters.csv")

# ---------- Define stats to visualize ----------
stats_to_visualize = ["AVG", "OBP", "SLG", "OPS", "HR", "BB%", "SO%", "ISO", "wOBA", "wRAA","wRC"]
available_stats = [stat for stat in stats_to_visualize if stat in data.columns]

# ---------- Compute percentiles ----------
data = compute_percentiles(data, available_stats)

#Table 
st.subheader("Batters")
st.write(data)
# ---------- Player selection ----------
player_names = data["Player"].unique()
selected_player = st.selectbox("Select a player", player_names)
player_data = data[data["Player"] == selected_player].iloc[0]

# ---------- Show non-percentile stats ----------
st.subheader("Stats")
excluded_columns = [stat for stat in data.columns if stat.endswith("_pct")] + available_stats
other_stats = {col: player_data[col] for col in player_data.index if col not in excluded_columns}
other_stats_df = pd.DataFrame(other_stats.items(), columns=["Stat", "Value"])
st.dataframe(other_stats_df)

# ---------- Visual bar chart with color gradient ----------
st.subheader("Percentile Rankings (Blue = Low, Red = High)")

def get_color(percentile):
    cmap = cm.get_cmap('bwr')  # blue-white-red
    norm = mcolors.Normalize(vmin=0, vmax=100)
    return mcolors.to_hex(cmap(norm(percentile)))

# Exclude HR from chart
visual_stats = [s for s in available_stats if s != "HR"]

for stat in visual_stats:
    percentile = round(player_data[stat + "_pct"])
    color = get_color(percentile)
    bar = f"""
    <div style="margin: 6px 0;">
        <strong>{stat}</strong> ({percentile}th)<strong> ({player_data[stat]})
        <div style="background-color: #eee; border-radius: 4px; overflow: hidden;">
            <div style="width: {percentile}%; background-color: {color}; padding: 4px 0;"></div>
        </div>
    </div>
    """
    st.markdown(bar, unsafe_allow_html=True)
