import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Lead Scoring Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/output/scored_leads.csv")

df = load_data()

st.title("AI Lead Scoring Dashboard")
st.markdown(
    """
    This dashboard displays ranked biotech/pharma leads based on
    role fit, scientific intent, funding readiness, and location signals.
    """
)

st.sidebar.header("Filters")

min_score = st.sidebar.slider(
    "Minimum Propensity Score",
    min_value=0,
    max_value=100,
    value=50
)

filtered_df = df[df["propensity_score"] >= min_score]

st.subheader("Ranked Leads")

display_columns = [
    "name",
    "title",
    "company",
    "person_location",
    "company_hq",
    "propensity_score"
]

st.dataframe(
    filtered_df[display_columns]
        .sort_values("propensity_score", ascending=False),
    use_container_width=True
)

st.subheader("Score Breakdown (Per Lead)")

selected_name = st.selectbox(
    "Select a lead to inspect",
    filtered_df["name"].unique()
)

selected_row = filtered_df[filtered_df["name"] == selected_name].iloc[0]

st.json(selected_row["score_breakdown"])