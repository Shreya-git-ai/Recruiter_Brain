import streamlit as st

st.set_page_config(
    page_title="About",
    layout="wide",
    page_icon="ℹ️"
)

st.title("ℹ️ About Recruiter Brain")

st.markdown("""
### Explainable AI Talent Intelligence

Recruiter Brain is an AI-powered candidate ranking system designed
to identify the most relevant candidates for a target role using
semantic search, hiring signals, profile-quality screening, and
explainable scoring.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.success("""
### Semantic Matching

Uses transformer embeddings to understand
candidate relevance based on meaning rather
than keyword overlap.
""")

with col2:
    st.success("""
### Explainable Rankings

Every ranked candidate includes concise,
human-readable reasoning for recruiter review.
""")

col3, col4 = st.columns(2)

with col3:
    st.info("""
### Profile Quality Analysis

Detects suspicious profiles, keyword stuffing,
and inconsistencies that can affect ranking quality.
""")

with col4:
    st.info("""
### Scalable Architecture

Precomputed embeddings enable efficient
CPU-only ranking over large candidate pools.
""")

st.divider()

st.markdown("### ⚙️ System Pipeline")

st.markdown("""
Candidate Loading

→ Hard Filters

→ Profile Quality Checks

→ Semantic Matching

→ Career Fit Scoring

→ Hiring Signal Analysis

→ Score Aggregation

→ Reasoning Generation

→ Final Ranking
""")

st.divider()

st.markdown("### 🛠 Technology Stack")

st.code(
"""
Python
Sentence Transformers
Scikit-Learn
NumPy
Pandas
Streamlit
"""
)

st.caption(
    "Built for the Redrob Intelligent Candidate Discovery & Ranking Challenge."
)