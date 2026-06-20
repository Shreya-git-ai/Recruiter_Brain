import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Stats & Graphs",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Ranking Analytics")

df = st.session_state.get("results_df", None)

if df is None:
    st.warning(
        "No results yet. Run the matching engine from the Home page first."
    )

else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Candidates Ranked", len(df))

    with col2:
        st.metric(
            "Top Score",
            f"{df['score'].max():.3f}"
        )

    with col3:
        st.metric(
            "Median Score",
            f"{df['score'].median():.3f}"
        )

    st.divider()

    st.markdown("### 📈 Score Distribution")

    chart_data = (
        df[["rank", "score"]]
        .set_index("rank")
    )

    st.bar_chart(chart_data)

    st.divider()

    st.markdown("### 📉 Top Candidate Trend")

    top20 = df.head(min(20, len(df)))

    st.line_chart(
        top20.set_index("rank")["score"]
    )

    st.divider()

    st.markdown("### 📋 Ranked Candidate Table")

    st.dataframe(
        df[["rank", "candidate_id", "score"]],
        use_container_width=True,
        hide_index=True,
    )