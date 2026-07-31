import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Australian Crime Analytics Dashboard",
    layout="wide"
)


# -----------------------------
# Load dataset
# -----------------------------

DATA_FILE = Path(
    "data/processed/offenders_clean.csv"
)


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)

    return df


df = load_data()

def shorten_offence_name(name):
    if not isinstance(name, str):
        return name

    normalized_name = name.strip()

    replacements = {
        "01 Homicide and related offences(e)": "Homicide",
        "02 Acts intended to cause injury(f)": "Acts causing injury",
        "03 Sexual assault and related offences(g)": "Sexual assault",
        "04 Dangerous/negligent acts(h)": "Dangerous acts",
        "08 Theft(i)(j)": "Theft",
        "10 Illicit drug offences(l)": "Drug offences",
        "13 Public order offences(m)": "Public order",
        "15 Offences against justice(n)(o)": "Justice offences",
    }

    return replacements.get(normalized_name, normalized_name)


# -----------------------------
# Dashboard Header
# -----------------------------

st.title(
    "Australian Crime Analytics Dashboard"
)

st.markdown("### Description")
st.markdown(
    """
    Analysis of Australian offender statistics using
    ABS data from 2008–09 to 2024–25.
    
    The dashboard explores crime trends, offence categories,
    and long-term changes in offender counts and rates.
    """
)
st.markdown("---")
st.subheader("Key Findings")

st.write(
"""
- Total offender counts have declined over the long term.
- Acts intended to cause injury remain the largest offence category.
- Theft and public order offences show significant decreases since 2008.
- Some offence categories, including weapons and assault-related offences,
  have increased over the same period.
"""
)

st.markdown("---")
st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

latest_year = df["Year"].max()

latest_total = (
    df[df["Year"] == latest_year]
    ["Offender_Count"]
    .sum()
)

highest_category = (
    df[df["Year"] == latest_year]
    .groupby("Offence_Category")
    ["Offender_Count"]
    .sum()
    .idxmax()
)

highest_category_label = shorten_offence_name(highest_category)


with col1:
    st.metric(
        "Latest Year",
        latest_year
    )

with col2:
    st.metric(
        "Total Offenders",
        f"{latest_total:,.0f}"
    )

with col3:
    st.metric(
        "Highest Category",
        highest_category_label
    )

with col4:
    first_year = df["Year"].min()

    first_total = (
        df[df["Year"] == first_year]
        ["Offender_Count"]
        .sum()
    )

    change = (
        (latest_total-first_total)
        /
        first_total
        *
        100
    )

    st.metric(
        "Change Since 2008",
        f"{change:.1f}%"
    )

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header(
    "Dashboard Filters"
)

years = sorted(
    df["Year"].unique()
)

selected_years = st.sidebar.multiselect(
    "Select Years",
    years,
    default=years,
    help="Choose one or more years to display on the dashboard"
)

categories = sorted(
    df["Offence_Category"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Offence Categories",
    categories,
    default=categories,
    help="Choose one or more offence categories to display on the dashboard"
)


filtered_df = df[
    (df["Year"].isin(selected_years))
    &
    (df["Offence_Category"].isin(selected_categories))
]


st.markdown("---")
st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Selected Offenders",
        f"{filtered_df['Offender_Count'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Offence Categories",
        filtered_df["Offence_Category"].nunique()
    )

with col3:
    st.metric(
        "Years Analysed",
        len(selected_years)
    )
# -----------------------------
# Data Preview
# -----------------------------

st.markdown("---")
st.subheader("Dataset Preview")

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_crime_data.csv",
    mime="text/csv"
)

st.dataframe(
    filtered_df.head(50),
    width="stretch"
)
#------------------------------
# Charts and Graphs
#------------------------------
col1, col2 = st.columns(2)
# Offender Trend Over Time
with col1: 
    yearly_totals = (
        filtered_df
        .groupby("Year", as_index=False)["Offender_Count"]
        .sum()
    )


    fig = px.line(
        yearly_totals,
        x="Year",
        y="Offender_Count",
        markers=True,
        title="Overall Offender Trend"
    )

    fig.update_layout(
        xaxis_title="Financial Year",
        yaxis_title="Offender Count"
    )



    st.plotly_chart(
        fig,
        width="stretch"
    )

# Top Offence Categories
with col2:
    top_categories = (
    filtered_df
    .groupby("Offence_Category", as_index=False)
    .agg(Offender_Count=("Offender_Count", "sum"))
    .sort_values("Offender_Count", ascending=False)
    )

    fig = px.bar(
        top_categories,
        x="Offender_Count",
        y="Offence_Category",
        orientation="h",
        title="Top Offence Categories"
    )
    fig.update_layout(
        xaxis_title="Offender Count",
        yaxis_title="",
        yaxis=dict(
            autorange="reversed"
        )
    )
    st.plotly_chart(
        fig,
        width="stretch"
    )

col1, col2 = st.columns(2)
# Offender Rate Trend

with col1: 
    yearly_rates = (
        filtered_df
        .groupby("Year", as_index=False)["Offender_Rate"]
        .mean()
    )

    fig = px.line(
        yearly_rates,
        x="Year",
        y="Offender_Rate",
        markers=True,
        title="Average Offender Rate"
    )

    fig.update_layout(
        xaxis_title="Financial Year",
        yaxis_title="Average Rate"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# Year-over-Year Change
with col2:
    yearly_change = yearly_totals.copy()

    yearly_change["Change"] = (
        yearly_change["Offender_Count"]
        .diff()
    )

    fig = px.bar(
        yearly_change,
        x="Year",
        y="Change",
        title="Year-over-Year Change"
    )

    fig.update_layout(
        xaxis_title="Financial Year",
        yaxis_title="Change in Offenders"
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

category_distribution = (
    filtered_df
    .groupby("Offence_Category", as_index=False)
    .agg(Offender_Count=("Offender_Count", "sum"))
    .sort_values("Offender_Count", ascending=False)
)

fig = px.treemap(
    category_distribution,
    path=["Offence_Category"],
    values="Offender_Count",
    title="Offence Category Distribution"
)

st.plotly_chart(
    fig,
    width="stretch"
)

#-----------------------------
# Key Findings
#-----------------------------

st.subheader("Key Findings")

# Highest offence category

highest_category = (
    filtered_df
    .groupby(
        "Offence_Category"
    )["Offender_Count"]
    .sum()
    .idxmax()
)

highest_value = (
    filtered_df
    .groupby(
        "Offence_Category"
    )["Offender_Count"]
    .sum()
    .max()
)
st.write(
    f"""
    **Highest offending category:** 
    {highest_category}

    Total offenders:
    {highest_value:,.0f}
    """
)

# Largest increase/decrease

category_change = (
    filtered_df
    .groupby(["Offence_Category", "Year"], as_index=False)
    .agg(Offender_Count=("Offender_Count", "sum"))
)

category_change = category_change.sort_values(
    by=["Offence_Category", "Year"]
)


category_change["Change"] = (
    category_change
    .groupby("Offence_Category")
    ["Offender_Count"]
    .diff()
)

largest_change = (
    category_change
    .dropna()
    .sort_values(
        "Change"
    )
)


largest_decline = largest_change.iloc[0]

largest_growth = (
    largest_change
    .iloc[-1]
)

st.write(
    f"""
    **Largest increase:**

    {largest_growth['Offence_Category']}
    
    Change:
    +{largest_growth['Change']:,.0f} offenders


    **Largest decline:**

    {largest_decline['Offence_Category']}
    
    Change:
    {largest_decline['Change']:,.0f} offenders
    """
)

# Overall trend

start_total = (
    yearly_totals
    .iloc[0]["Offender_Count"]
)

end_total = (
    yearly_totals
    .iloc[-1]["Offender_Count"]
)

percentage_change = (
    (end_total - start_total)
    /
    start_total
    *
    100
)

st.write(
    f"""
    **Overall trend:**

    Offender numbers changed by 
    {percentage_change:.1f}% 
    between 
    {yearly_totals.iloc[0]['Year']} 
    and 
    {yearly_totals.iloc[-1]['Year']}.
    """
)