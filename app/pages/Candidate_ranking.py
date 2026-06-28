import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
 
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
 
import streamlit as st
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS
from app.ui.components import candidate_card, explanation_panel, stat_card
from app.ui.utils import load_results
 
st.set_page_config(page_title="Candidate Rankings", layout="wide", page_icon="🏆")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
 
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🧠</div>
        <div class="sidebar-logo-text">Recruiter Brain</div>
    </div>
    """, unsafe_allow_html=True)
 
# Always read fresh from absolute path CSV
df = load_results()
 
if "selected" not in st.session_state:
    st.session_state["selected"] = None
 
st.markdown("""
<div style="padding: 40px 48px 24px 48px;">
    <h1 style="font-size: 28px; font-weight: 700; color: #111827; margin-bottom: 8px;">🏆 Candidate Rankings</h1>
    <p style="font-size: 14px; color: #6b7280;">AI-ranked shortlist with explainable scoring</p>
</div>
""", unsafe_allow_html=True)
 
if df is None:
    st.markdown("""
    <div style="padding: 0 48px;">
        <div style="
            background: white;
            border: 1px solid #e8ecf4;
            border-radius: 20px;
            padding: 60px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">🎯</div>
            <div style="font-size: 20px; font-weight: 600; color: #111827; margin-bottom: 8px;">No results yet</div>
            <div style="font-size: 14px; color: #9ca3af;">Go to the Home page and run the matching engine first</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
 
# ── Quick stats bar ───────────────────────────────────────────────────────────
st.markdown("<div style='padding: 0 48px 16px 48px;'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(stat_card(str(len(df)), "Candidates Ranked", "🏆"), unsafe_allow_html=True)
with c2:
    st.markdown(stat_card(f"{df['score'].max():.3f}", "Top Score", "⭐"), unsafe_allow_html=True)
with c3:
    st.markdown(stat_card(f"{df['score'].mean():.3f}", "Avg Score", "📊"), unsafe_allow_html=True)
with c4:
    high = len(df[df["score"] >= 0.7])
    st.markdown(stat_card(str(high), "High Fit (≥0.70)", "🎯"), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Filters ───────────────────────────────────────────────────────────────────
st.markdown("<div style='padding: 0 48px 16px 48px;'>", unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 2, 1])
with f1:
    search = st.text_input("🔍 Search by candidate ID", placeholder="CAND_XXXXXXX")
with f2:
    score_filter = st.slider("Min score filter", 0.0, 1.0, 0.0, step=0.05)
with f3:
    st.markdown("<br>", unsafe_allow_html=True)
    csv_data = df.to_csv(index=False)
    st.download_button("⬇ Export CSV", csv_data, "ranked_candidates.csv", "text/csv", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
 
# ── Apply filters ─────────────────────────────────────────────────────────────
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[filtered_df["candidate_id"].str.contains(search, case=False, na=False)]
if score_filter > 0:
    filtered_df = filtered_df[filtered_df["score"] >= score_filter]
 
# ── Candidate list + explanation panel ───────────────────────────────────────
col_main, col_right = st.columns([2.2, 1])
 
with col_main:
    st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background: #f8faff;
        border: 1px solid #e8ecf4;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div style="font-size: 13px; font-weight: 600; color: #374151;">
            Showing {len(filtered_df)} of {len(df)} candidates
        </div>
        <div style="font-size: 13px; color: #9ca3af;">
            Top score: <strong style="color: #6366f1;">{df['score'].max():.3f}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    for _, row in filtered_df.iterrows():
        is_top3 = row["rank"] <= 3
        st.markdown(
            candidate_card(row["rank"], row["candidate_id"], row["score"], row["reasoning"], is_top3),
            unsafe_allow_html=True,
        )
        if st.button("View Details →", key=f"rank_btn_{row['candidate_id']}"):
            st.session_state["selected"] = row.to_dict()
            st.rerun()
 
    st.markdown("</div>", unsafe_allow_html=True)
 
with col_right:
    st.markdown("<div style='padding-right: 48px;'>", unsafe_allow_html=True)
    st.markdown(explanation_panel(st.session_state.get("selected")), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)