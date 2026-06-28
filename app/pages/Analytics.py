import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS
from app.ui.components import stat_card

st.set_page_config(page_title="Analytics", layout="wide", page_icon="📊")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🧠</div>
        <div class="sidebar-logo-text">Recruiter Brain</div>
    </div>
    """, unsafe_allow_html=True)

from app.ui.utils import load_results

df = load_results()

if df is not None:
    st.session_state["results_df"] = df

st.markdown("""
<div style="padding: 40px 48px 24px 48px;">
    <h1 style="font-size: 28px; font-weight: 700; color: #111827; margin-bottom: 8px;">📊 Analytics Overview</h1>
    <p style="font-size: 14px; color: #6b7280;">Pipeline performance and ranking quality insights</p>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.markdown("""
    <div style="padding: 0 48px;">
        <div style="background:white;border:1px solid #e8ecf4;border-radius:20px;padding:60px;text-align:center;">
            <div style="font-size:48px;margin-bottom:16px;">📊</div>
            <div style="font-size:20px;font-weight:600;color:#111827;margin-bottom:8px;">No data yet</div>
            <div style="font-size:14px;color:#9ca3af;">Run the matching engine from the Home page first</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Stats row
    st.markdown("<div style='padding: 0 48px;'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(stat_card(len(df), "Candidates Ranked", "🏆"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card(f"{df['score'].max():.3f}", "Top Score", "⭐"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card(f"{df['score'].median():.3f}", "Median Score", "📊"), unsafe_allow_html=True)
    with c4:
        st.markdown(stat_card(f"{df['score'].min():.3f}", "Min Score", "📉"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='padding: 24px 48px;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div style="background:white;border:1px solid #e8ecf4;border-radius:16px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:16px;">
            <div style="font-size:16px;font-weight:600;color:#111827;margin-bottom:16px;">Score Distribution</div>
        """, unsafe_allow_html=True)
        chart_df = df[["rank", "score"]].set_index("rank")
        st.bar_chart(chart_df, color="#6366f1")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:white;border:1px solid #e8ecf4;border-radius:16px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:16px;">
            <div style="font-size:16px;font-weight:600;color:#111827;margin-bottom:16px;">Score Breakdown</div>
        """, unsafe_allow_html=True)
        high = len(df[df["score"] >= 0.7])
        mid = len(df[(df["score"] >= 0.5) & (df["score"] < 0.7)])
        low = len(df[df["score"] < 0.5])

        for label, count, color in [("High Fit (≥0.7)", high, "#10b981"), ("Medium Fit (0.5-0.7)", mid, "#f59e0b"), ("Lower Fit (<0.5)", low, "#ef4444")]:
            pct = int(count / len(df) * 100) if len(df) > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:13px;color:#374151;">{label}</span>
                    <span style="font-size:13px;font-weight:600;color:{color};">{count} ({pct}%)</span>
                </div>
                <div style="background:#f3f4f6;border-radius:6px;height:8px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Full table
    st.markdown("""
    <div style="background:white;border:1px solid #e8ecf4;border-radius:16px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="font-size:16px;font-weight:600;color:#111827;margin-bottom:16px;">Full Ranking Table</div>
    """, unsafe_allow_html=True)
    st.dataframe(df[["rank", "candidate_id", "score"]], use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)