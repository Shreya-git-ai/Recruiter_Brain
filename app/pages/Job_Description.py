import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from src.semantic_score import JD_FOCUS_TEXT

st.set_page_config(
    page_title="Job Description",
    layout="wide",
    page_icon="📄"
)

st.title("📄 Target Job Description")

st.caption(
    "All candidates are ranked against this role."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Domain", "AI / ML")

with col2:
    st.metric("Focus", "Semantic Search")

with col3:
    st.metric("Role Type", "Senior Engineer")

st.divider()

st.markdown("### 🎯 Key Signals Considered")

st.info("""
• NLP and Language Technologies

• Search, Retrieval, and Ranking Systems

• Recommendation System Experience

• Production Machine Learning Deployments

• Strong Software Engineering Fundamentals

• Candidate Quality and Consistency Signals
""")

st.divider()

st.markdown("### ⚙️ Evaluation Pipeline")

st.markdown("""
**Filter Candidates**
→ **Profile Quality Checks**
→ **Semantic Matching**
→ **Career Fit Analysis**
→ **Hiring Signal Evaluation**
→ **Final Ranking**
""")

st.divider()

st.markdown("### 📑 Matching Criteria")

st.text_area(
    "Job Description",
    JD_FOCUS_TEXT,
    height=450,
    disabled=True
)