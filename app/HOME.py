import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from src.pipeline import run_pipeline

st.set_page_config(page_title="Recruiter Brain", layout="wide", page_icon="🧠")

# Detect whether full dataset or demo dataset is available
if os.path.exists("data/candidates.jsonl") and os.path.exists("data/candidate_embeddings.npy"):
    DEFAULT_CANDIDATES_PATH = "data/candidates.jsonl"
    DEFAULT_EMBEDDINGS_PATH = "data/candidate_embeddings.npy"
    DEFAULT_IDS_PATH = "data/candidate_ids.npy"
    MAX_SAMPLE = 2000
else:
    DEFAULT_CANDIDATES_PATH = "data/candidates_demo.jsonl"
    DEFAULT_EMBEDDINGS_PATH = "data/candidate_embeddings_demo.npy"
    DEFAULT_IDS_PATH = "data/candidate_ids_demo.npy"
    MAX_SAMPLE = 200

if "results_df" not in st.session_state:
    st.session_state["results_df"] = None
if "selected" not in st.session_state:
    st.session_state["selected"] = None

st.title("🧠 Recruiter Brain")
st.caption("Explainable candidate ranking, built for the Redrob Hackathon")

if DEFAULT_CANDIDATES_PATH.endswith("_demo.jsonl"):
    st.caption("⚠️ Running on a demo sample dataset (full 100K dataset not bundled with this deployment).")

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
    sample_size = st.slider("Candidate sample size", 10, MAX_SAMPLE, min(200, MAX_SAMPLE), step=10)
with col_b:
    top_n = st.slider("Top N (capped at 100 per competition rules)", 5, 100, min(20, MAX_SAMPLE), step=5)

if st.button("🚀 Run Matching Engine", use_container_width=True, type="primary"):
    with st.spinner("Running ranking pipeline..."):
        try:
            result_df = run_pipeline(
                candidates_path=DEFAULT_CANDIDATES_PATH,
                output_path="outputs/streamlit_output.csv",
                embeddings_path=DEFAULT_EMBEDDINGS_PATH,
                ids_path=DEFAULT_IDS_PATH,
                limit=sample_size,
                top_n=top_n,
            )
            st.session_state["results_df"] = result_df
            st.session_state["selected"] = None
            st.success(f"Done! Ranked top {len(result_df)} candidates. Go to **Ranking Results** in the sidebar to view them.")
        except FileNotFoundError as e:
            st.error(f"Missing file: {e}")
        except Exception as e:
            st.error(f"Pipeline error: {e}")

st.info("👈 Use the sidebar to navigate to Job Description, Ranking Results, Stats, or About.")