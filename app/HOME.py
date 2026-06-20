import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from src.pipeline import run_pipeline

st.set_page_config(page_title="Recruiter Brain", layout="wide", page_icon="🧠")

if "results_df" not in st.session_state:
    st.session_state["results_df"] = None
if "selected" not in st.session_state:
    st.session_state["selected"] = None

st.title("🧠 Recruiter Brain")


st.markdown("""
### Explainable AI-Powered Talent Matching

Identify the most relevant candidates using semantic search,
career-fit analysis, hiring signals, and profile-quality screening.

Built to rank large candidate pools efficiently while maintaining
transparent recruiter-friendly explanations.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Candidate Pool", "100,000")
with col2:
    st.metric("Honeypot Traps", "~80")
with col3:
    st.metric("Ranking Runtime", "< 2 min")
with col4:
    df_count = len(st.session_state["results_df"]) if st.session_state["results_df"] is not None else 0
    st.metric("Last Run — Ranked", df_count)

st.divider()

st.markdown("### How it works")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("**1. Filter**")
    st.caption("Honeypot detection and hard filters remove invalid candidates.")
with c2:
    st.markdown("**2. Semantic Match**")
    st.caption("Embeddings compare experience against the JD's meaning, not keywords.")
with c3:
    st.markdown("**3. Career Fit**")
    st.caption("Domain signal evidence and red-flag penalties refine the score.")
with c4:
    st.markdown("**4. Availability**")
    st.caption("Behavioral signals down-weight unreachable candidates.")

st.divider()

st.markdown("### Run the Matching Engine")
col_a, col_b = st.columns([2, 1])
with col_a:
    sample_size = st.slider("Candidate sample size", 50, 2000, 200, step=50)
with col_b:
    top_n = st.slider("Top N (capped at 100 per competition rules)", 5, 100, 100, step=5)

if st.button("🚀 Run Matching Engine", use_container_width=True, type="primary"):
    with st.spinner("Running ranking pipeline..."):
        try:
            result_df = run_pipeline(
                candidates_path="data/candidates.jsonl",
                output_path="outputs/streamlit_output.csv",
                embeddings_path="data/candidate_embeddings.npy",
                ids_path="data/candidate_ids.npy",
                limit=sample_size,
                top_n=top_n,
            )
            st.session_state["results_df"] = result_df
            st.session_state["selected"] = None
            st.success(f"Done! Ranked top {len(result_df)} candidates. Go to **Ranking Results** in the sidebar to view them.")
        except FileNotFoundError as e:
            st.error(f"Missing file: {e}. Run precompute_embeddings.py first.")
        except Exception as e:
            import traceback

            st.error(f"Pipeline error: {e}")
            st.code(traceback.format_exc(),language="python")

st.info("👈 Use the sidebar to navigate to Job Description, Ranking Results, Stats, or About.")