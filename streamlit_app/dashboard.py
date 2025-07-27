import streamlit as st
import json
from datetime import datetime
import os
import pandas as pd
import plotly.express as px

VALIDATION_PATH = "great_expectations/validations/latest_validation.json"

def load_validation():
    if not os.path.exists(VALIDATION_PATH):
        st.error("Validation file not found.")
        return None
    with open(VALIDATION_PATH) as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="AI Data Quality Dashboard", layout="centered")
    st.title("📊 AI-Powered Data Quality Validation Results")

    validation = load_validation()
    if not validation:
        return

    st.markdown(f"**Dataset/Table**: `{validation['table']}`")
    st.markdown(f"**Timestamp**: `{validation['timestamp']}`")

    df = pd.DataFrame(validation["results"])
    df["expectation"] = df["expectation"].apply(lambda e: e if isinstance(e, str) else str(e))
    df["Status"] = df["success"].apply(lambda x: "✅ Pass" if x else "❌ Fail")

    st.subheader("Expectation Results")
    st.dataframe(df[["expectation", "Status"]], use_container_width=True)

    # Pie chart
    passed = df["success"].sum()
    failed = len(df) - passed
    fig = px.pie(values=[passed, failed], names=["Passed", "Failed"], title="Validation Summary")
    st.plotly_chart(fig)

    st.markdown("---")
    st.caption("Built with ❤️ using GPT + Great Expectations + Streamlit")

if __name__ == "__main__":
    main()
