import streamlit as st
import pandas as pd
from scipy.stats import norm

from src.data_loader import get_validated_dataset

# Page configuration
st.set_page_config(
    page_title="GamePulse | A/B Testing Analytics",
    page_icon="🎮",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return get_validated_dataset()

df = load_data()

# Dashboard heading
st.title("🎮 GamePulse")
st.subheader("Mobile Game A/B Testing & Player Retention Analytics")

st.markdown(
    """
    Analyze the impact of moving the first game gate
    from level 30 to level 40 on player engagement and retention.
    """
)

st.divider()

# Calculate key metrics
total_players = len(df)

gate_30_players = (df["version"] == "gate_30").sum()
gate_40_players = (df["version"] == "gate_40").sum()

day_1_retention = df["retention_1"].mean() * 100
day_7_retention = df["retention_7"].mean() * 100

# KPI section
st.subheader("Experiment Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Players",
    f"{total_players:,}"
)

col2.metric(
    "Gate 30 Players",
    f"{gate_30_players:,}"
)

col3.metric(
    "Gate 40 Players",
    f"{gate_40_players:,}"
)

col4.metric(
    "Overall Day-7 Retention",
    f"{day_7_retention:.2f}%"
)

st.divider()

# Retention overview
st.subheader("Overall Retention")

col1, col2 = st.columns(2)

col1.metric(
    "Day-1 Retention",
    f"{day_1_retention:.2f}%"
)

col2.metric(
    "Day-7 Retention",
    f"{day_7_retention:.2f}%"
)

# Experiment group distribution
st.subheader("Experiment Group Distribution")

group_distribution = (
    df["version"]
    .value_counts()
    .rename_axis("Experiment Group")
    .reset_index(name="Players")
)

st.bar_chart(
    group_distribution,
    x="Experiment Group",
    y="Players"
)

st.caption(
    "Dataset: Cookie Cats Mobile Game A/B Testing Dataset"
)

# Retention analysis by experiment group

st.divider()
st.subheader("Retention Performance by Experiment Group")

retention_by_group = df.groupby("version").agg(
    total_players=("userid", "count"),
    day_1_retained=("retention_1", "sum"),
    day_7_retained=("retention_7", "sum")
)

retention_by_group["Day-1 Retention (%)"] = (
    retention_by_group["day_1_retained"]
    / retention_by_group["total_players"] * 100
)

retention_by_group["Day-7 Retention (%)"] = (
    retention_by_group["day_7_retained"]
    / retention_by_group["total_players"] * 100
)

display_columns = [
    "total_players",
    "Day-1 Retention (%)",
    "Day-7 Retention (%)"
]

st.dataframe(
    retention_by_group[display_columns].round(2),
    use_container_width=True
)

# Retention comparison chart

st.subheader("Day-1 vs Day-7 Retention")

retention_chart = retention_by_group[
    ["Day-1 Retention (%)", "Day-7 Retention (%)"]
]

st.bar_chart(
    retention_chart,
    use_container_width=True
)

# Retention difference between experiment groups

day_1_difference = (
    retention_by_group.loc["gate_40", "Day-1 Retention (%)"]
    - retention_by_group.loc["gate_30", "Day-1 Retention (%)"]
)

day_7_difference = (
    retention_by_group.loc["gate_40", "Day-7 Retention (%)"]
    - retention_by_group.loc["gate_30", "Day-7 Retention (%)"]
)

st.subheader("Retention Impact: Gate 40 vs Gate 30")

col1, col2 = st.columns(2)

col1.metric(
    "Day-1 Retention Difference",
    f"{day_1_difference:.2f} pp",
    delta=f"{day_1_difference:.2f} pp"
)

col2.metric(
    "Day-7 Retention Difference",
    f"{day_7_difference:.2f} pp",
    delta=f"{day_7_difference:.2f} pp"
)

st.caption(
    "Negative values indicate lower retention in gate_40 "
    "compared with gate_30. Differences are measured in "
    "percentage points."
)
# Statistical significance testing

st.divider()
st.header("Statistical Significance Analysis")

alpha = 0.05

metrics = {
    "Day-1 Retention": "day_1_retained",
    "Day-7 Retention": "day_7_retained"
}

statistical_results = []

for metric_name, column in metrics.items():

    success_30 = int(retention_by_group.loc["gate_30", column])
    success_40 = int(retention_by_group.loc["gate_40", column])

    n_30 = int(retention_by_group.loc["gate_30", "total_players"])
    n_40 = int(retention_by_group.loc["gate_40", "total_players"])

    p_30 = success_30 / n_30
    p_40 = success_40 / n_40

    difference = p_40 - p_30

    # Pooled standard error for the hypothesis test
    pooled_p = (success_30 + success_40) / (n_30 + n_40)

    standard_error = (
        pooled_p * (1 - pooled_p) * (1 / n_30 + 1 / n_40)
    ) ** 0.5

    z_statistic = difference / standard_error
    p_value = 2 * norm.sf(abs(z_statistic))

    # 95% confidence interval using unpooled standard error
    ci_se = (
        p_30 * (1 - p_30) / n_30
        + p_40 * (1 - p_40) / n_40
    ) ** 0.5

    margin = norm.ppf(0.975) * ci_se

    lower_ci = difference - margin
    upper_ci = difference + margin

    statistical_results.append({
        "Metric": metric_name,
        "Z Statistic": z_statistic,
        "P-value": p_value,
        "95% CI Lower (pp)": lower_ci * 100,
        "95% CI Upper (pp)": upper_ci * 100,
        "Decision": (
            "Significant"
            if p_value < alpha
            else "Not Significant"
        )
    })

statistical_df = pd.DataFrame(statistical_results)

st.subheader("Hypothesis Testing Results")

st.dataframe(
    statistical_df.round(4),
    use_container_width=True,
    hide_index=True
)

# Business interpretation
st.subheader("Statistical Interpretation")

day_7_p_value = statistical_df.loc[
    statistical_df["Metric"] == "Day-7 Retention",
    "P-value"
].iloc[0]

day_7_difference = day_7_difference

if day_7_p_value < alpha and day_7_difference < 0:
    st.warning(
        "Day-7 retention is significantly lower in gate_40. "
        "The experiment provides evidence against moving "
        "the first gate from level 30 to level 40."
    )
elif day_7_p_value < alpha and day_7_difference > 0:
    st.success(
        "Day-7 retention is significantly higher in gate_40."
    )
else:
    st.info(
        "The Day-7 retention difference is not statistically "
        "significant at the 5% level."
    )

st.caption(
    "Two-sided two-proportion Z-test | Alpha = 0.05 | "
    "Difference calculated as gate_40 minus gate_30."
)

# Interactive player engagement analysis

st.divider()
st.header("Player Engagement Analytics")

selected_group = st.selectbox(
    "Select Experiment Group",
    ["All Groups", "gate_30", "gate_40"]
)

if selected_group == "All Groups":
    filtered_df = df.copy()
else:
    filtered_df = df[df["version"] == selected_group].copy()

st.write(f"Selected group: {selected_group}")
st.write(f"Number of players: {len(filtered_df):,}")

# Engagement summary

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Game Rounds",
    f"{filtered_df['sum_gamerounds'].mean():.2f}"
)

col2.metric(
    "Median Game Rounds",
    f"{filtered_df['sum_gamerounds'].median():.0f}"
)

col3.metric(
    "Maximum Game Rounds",
    f"{filtered_df['sum_gamerounds'].max():,}"
)

# Game rounds distribution

st.subheader("Game Rounds Distribution")

st.bar_chart(
    filtered_df["sum_gamerounds"]
    .value_counts()
    .sort_index()
    .head(50),
    use_container_width=True
)

st.caption(
    "Distribution shows the frequency of players by game rounds. "
    "The chart displays the first 50 distinct game-round values."
)

# Business recommendation panel

st.divider()
st.header("Business Recommendation")

st.markdown(
    """
    ### Experiment Objective

    Evaluate whether moving the first game gate from
    level 30 to level 40 improves player retention.
    """
)

# Retrieve Day-7 results
day7_result = statistical_df[
    statistical_df["Metric"] == "Day-7 Retention"
].iloc[0]

day7_p = day7_result["P-value"]
day7_lower = day7_result["95% CI Lower (pp)"]
day7_upper = day7_result["95% CI Upper (pp)"]

st.subheader("Final Experiment Decision")

if day7_p < 0.05 and day_7_difference < 0:

    st.error(
        "Recommendation: Retain gate_30.\n\n"
        "Gate_40 has significantly lower Day-7 retention "
        "than gate_30 in this experiment."
    )

elif day7_p < 0.05 and day_7_difference > 0:

    st.success(
        "Recommendation: Consider gate_40.\n\n"
        "Gate_40 has significantly higher Day-7 retention."
    )

else:

    st.warning(
        "Recommendation: No statistically significant "
        "Day-7 retention improvement was detected."
    )

st.markdown("### Key Business Findings")

st.write(
    f"- Day-1 retention difference: "
    f"{day_1_difference:.2f} percentage points."
)

st.write(
    f"- Day-7 retention difference: "
    f"{day_7_difference:.2f} percentage points."
)

st.write(
    f"- Day-7 statistical p-value: {day7_p:.4f}."
)

st.write(
    f"- Day-7 95% confidence interval: "
    f"[{day7_lower:.2f}, {day7_upper:.2f}] percentage points."
)

st.caption(
    "Recommendation is based on retention outcomes in this "
    "experiment. Other business metrics and experiment "
    "limitations should also be considered."
)

# Downloadable experiment reports

st.divider()
st.header("Download Experiment Reports")

st.write(
    "Export experiment retention metrics and statistical "
    "testing results for further analysis."
)

col1, col2 = st.columns(2)

# Retention report
retention_export = retention_by_group.reset_index()

col1.download_button(
    label="Download Retention Report",
    data=retention_export.to_csv(index=False),
    file_name="gamepulse_retention_report.csv",
    mime="text/csv",
    use_container_width=True
)

# Statistical report
col2.download_button(
    label="Download Statistical Report",
    data=statistical_df.to_csv(index=False),
    file_name="gamepulse_statistical_report.csv",
    mime="text/csv",
    use_container_width=True
)

