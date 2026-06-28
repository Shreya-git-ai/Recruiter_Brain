import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
 
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
 
import streamlit as st
from src.pipeline import run_pipeline
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS
from app.ui.components import (
    hero_section, feature_card, pipeline_step,
    tech_badge, candidate_card, explanation_panel,
    stat_card, section_header,
)
from app.ui.utils import detect_dataset_paths, load_results, STREAMLIT_OUTPUT_CSV
 
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Recruiter Brain", layout="wide", page_icon="🧠")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
 
# ── Dataset detection (absolute paths) ───────────────────────────────────────
candidates_path, embeddings_path, ids_path, MAX_SAMPLE, IS_DEMO = detect_dataset_paths()
 
# ── Session state init ────────────────────────────────────────────────────────
if "results_df" not in st.session_state:
    st.session_state["results_df"] = load_results()
if "selected" not in st.session_state:
    st.session_state["selected"] = None
 
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🧠</div>
        <div class="sidebar-logo-text">Recruiter Brain</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div class="sidebar-status">
        <div class="sidebar-status-title">System Status</div>
        <div class="status-item"><div class="status-dot"></div>Embeddings Ready</div>
        <div class="status-item"><div class="status-dot"></div>Pipeline Ready</div>
        <div class="status-item"><div class="status-dot"></div>CPU Optimised</div>
        <div class="status-item"><div class="status-dot"></div>Explainable AI Enabled</div>
    </div>
    """, unsafe_allow_html=True)
 
# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(hero_section(IS_DEMO), unsafe_allow_html=True)
 
# ── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown(section_header("Core Capabilities", "What makes Recruiter Brain different", "🛠️"), unsafe_allow_html=True)
st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(feature_card("🔍", "Semantic Search", "Understand career meaning, not just keywords. Surface Tier-5 plain-language candidates."), unsafe_allow_html=True)
with c2:
    st.markdown(feature_card("📈", "Career Intelligence", "Evaluate growth, skills and career trajectories with ML scoring."), unsafe_allow_html=True)
with c3:
    st.markdown(feature_card("🧠", "Explainable AI", "Built-in reasoning with strong, specific explanations per candidate."), unsafe_allow_html=True)
with c4:
    st.markdown(feature_card("🎯", "Recruiter Focused", "Built for recruiting workflows with availability signals."), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Stats ─────────────────────────────────────────────────────────────────────
df = st.session_state["results_df"]
 
st.markdown(section_header("Platform Overview", "Live metrics from last pipeline run", "📊"), unsafe_allow_html=True)
st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(stat_card("100,000+", "Candidates Processed", "👥"), unsafe_allow_html=True)
with s2:
    avg = f"{df['score'].mean():.3f}" if df is not None else "—"
    st.markdown(stat_card(avg, "Avg Match Score", "⚡"), unsafe_allow_html=True)
with s3:
    st.markdown(stat_card("< 2 min", "Ranking Runtime", "⏱️"), unsafe_allow_html=True)
with s4:
    ranked = str(len(df)) if df is not None else "—"
    st.markdown(stat_card(ranked, "Last Run — Ranked", "🏆"), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Run Engine ────────────────────────────────────────────────────────────────
st.markdown(section_header("Run Matching Engine", "Configure and launch the full ranking pipeline", "🚀"), unsafe_allow_html=True)
st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns([2, 2, 1])
with col_a:
    sample_size = st.slider("Candidate sample size", 10, MAX_SAMPLE, min(200, MAX_SAMPLE), step=10)
with col_b:
    top_n = st.slider("Top N results (max 100)", 5, 100, 20, step=5)
with col_c:
    st.markdown("<br>", unsafe_allow_html=True)
    run_clicked = st.button("🚀 Run Pipeline", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
 
if run_clicked:
    with st.spinner("Running pipeline — filtering, scoring, ranking..."):
        try:
            # STREAMLIT_OUTPUT_CSV is ABSOLUTE path from utils.py
            run_pipeline(
                candidates_path=candidates_path,
                output_path=STREAMLIT_OUTPUT_CSV,
                embeddings_path=embeddings_path,
                ids_path=ids_path,
                limit=sample_size,
                top_n=top_n,
            )
            # Reload from freshly-written CSV
            fresh_df = load_results()
            st.session_state["results_df"] = fresh_df
            st.session_state["selected"] = None
            n = len(fresh_df) if fresh_df is not None else 0
            st.success(f"✅ Done — ranked top {n} candidates from {sample_size:,} sample. See results below or go to **Candidate Rankings** page.")
            st.rerun()
        except FileNotFoundError as e:
            st.error(f"Missing file: {e}")
        except Exception as e:
            st.error(f"Pipeline error: {e}")
 
# ── Top Candidates Preview ────────────────────────────────────────────────────
df = st.session_state["results_df"]
 
if df is not None:
    st.markdown(section_header("Top Ranked Candidates", "Top 5 results — go to Candidate Rankings for full list", "⚡"), unsafe_allow_html=True)
    st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
    col_main, col_right = st.columns([2.2, 1])
 
    with col_main:
        for _, row in df.head(5).iterrows():
            is_top3 = row["rank"] <= 3
            st.markdown(
                candidate_card(row["rank"], row["candidate_id"], row["score"], row["reasoning"], is_top3),
                unsafe_allow_html=True,
            )
            if st.button("View Details →", key=f"home_btn_{row['candidate_id']}"):
                st.session_state["selected"] = row.to_dict()
                st.rerun()
 
    with col_right:
        st.markdown(explanation_panel(st.session_state.get("selected")), unsafe_allow_html=True)
 
    st.markdown("</div>", unsafe_allow_html=True)
 
# ── How It Works ──────────────────────────────────────────────────────────────
st.markdown(section_header("How It Works", "Step-by-step pipeline overview", "🔄"), unsafe_allow_html=True)
st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
steps = [
    ("🕵️", "Honeypot Detection", "Remove fake & quality-gaming profiles"),
    ("🔎", "Hard Filters", "Apply strict JD requirements"),
    ("🧬", "Semantic Matching", "Match by meaning, not keywords"),
    ("📊", "Career Fit", "Evaluate growth & trajectory"),
    ("📡", "Recruiter Signals", "Layer availability & location signals"),
    ("🏆", "Final Ranking", "Surface the best candidates"),
]
cols = st.columns(6)
for i, (col, (icon, title, desc)) in enumerate(zip(cols, steps), start=1):
    with col:
        st.markdown(pipeline_step(str(i), icon, title, desc, "#6366f1"), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Tech Stack ────────────────────────────────────────────────────────────────
st.markdown(section_header("Built With", "Modern AI technologies under the hood", "⚙️"), unsafe_allow_html=True)
st.markdown("<div style='padding: 0 48px 40px 48px;'>", unsafe_allow_html=True)
techs = ["🐍 Python", "🤗 Sentence Transformers", "⚡ Scikit-Learn", "🐼 Pandas", "🔢 NumPy", "🎈 Streamlit"]
cols = st.columns(len(techs))
for col, tech in zip(cols, techs):
    with col:
        st.markdown(tech_badge(tech), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    padding: 32px 48px;
    border-top: 1px solid #e8ecf4;
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="font-size: 13px; color: #9ca3af;">
        🧠 <strong style="color: #374151;">Recruiter Brain</strong> — Smarter Hiring. Better Talent. Stronger Teams.
    </div>
    <div style="font-size: 12px; color: #d1d5db;">Built for Redrob Hackathon 2024</div>
</div>
""", unsafe_allow_html=True)