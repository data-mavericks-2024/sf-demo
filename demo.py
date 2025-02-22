import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit app title

st.title("Pivot Chart Generator")

# File upload

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    required_columns = {"Territory", "Pharmacy", "Product", "Week", "Units"}

    if not required_columns.issubset(df.columns):
        st.error(
            f"Missing required columns: {required_columns - set(df.columns)}"
        )
    else:
        # Filters
        #territory = st.selectbox("Select Territory", df["Territory"].unique())
        territories = st.multiselect("Select Territories", df["Territory"].unique(), default=df["Territory"].unique())
        pharmacy = st.selectbox("Select Pharmacy", df["Pharmacy"].unique())

        # Filter data
        #filtered_df = df[
        #    (df["Territory"] == territory) & (df["Pharmacy"] == pharmacy)
        #]
        filtered_df = df[df["Territory"].isin(territories) & (df["Pharmacy"] == pharmacy)]

        # Pivot Table
        pivot_df = filtered_df.pivot_table(
            values="Units",
            index="Week",
            columns="Product",
            aggfunc="sum",
            fill_value=0,
        ).reset_index()

        # Create Chart
        fig = px.line(
            pivot_df,
            x="Week",
            y=pivot_df.columns[1:],
            title="Pivot Chart",
            markers=True,
        )

        # Show Chart
        st.plotly_chart(fig)
