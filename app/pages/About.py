import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS

st.set_page_config(page_title="About", layout="wide", page_icon="ℹ️")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🧠</div>
        <div class="sidebar-logo-text">Recruiter Brain</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="padding: 40px 48px;">
    <h1 style="font-size: 28px; font-weight: 700; color: #111827; margin-bottom: 8px;">ℹ️ About Recruiter Brain</h1>
    <p style="font-size: 14px; color: #6b7280; margin-bottom: 32px;">Built for the Redrob Hackathon — Intelligent Candidate Discovery & Ranking Challenge</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    sections = [
        ("The Problem", "#ef4444", """
            Keyword-based hiring fails in a specific, predictable way. A candidate who lists
            "RAG, Pinecone, LLM" in their skills beats someone who actually shipped a
            recommendation system but described it in plain English. The dataset contains
            deliberate adversarial traps: keyword-stuffed profiles, logically impossible
            honeypot candidates, and behavioral near-duplicates.
        """),
        ("The Solution", "#6366f1", """
            Recruiter Brain ranks on meaning, not vocabulary. Semantic embeddings capture what
            candidates actually did — not just which words they used. Combined with rule-based
            honeypot detection, red-flag penalties for title-chasing and non-coding roles, and
            behavioral availability signals, the system surfaces genuinely relevant candidates.
        """),
        ("Compute Strategy", "#10b981", """
            CPU-only · No external API calls during ranking · Full 100K candidate embeddings
            precomputed offline once and cached to disk (.npy format) · Ranking step loads
            precomputed vectors and scores, completing in under 2 minutes · Honeypot rate
            well under 10% in top 100.
        """),
    ]

    for title, color, content in sections:
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e8ecf4;
            border-left: 4px solid {color};
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 12px;">{title}</div>
            <p style="font-size: 14px; color: #6b7280; line-height: 1.7; margin: 0;">{content}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Tech stack
    techs = [
        ("🐍", "Python", "Core language"),
        ("🤗", "Sentence-Transformers", "Semantic embeddings"),
        ("⚡", "scikit-learn", "Cosine similarity"),
        ("🔢", "NumPy", "Embedding storage"),
        ("🐼", "Pandas", "Data processing"),
        ("🎈", "Streamlit", "Frontend UI"),
    ]

    tech_rows = "".join([
        f'<div style="display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #f3f4f6;">'
        f'<div style="font-size:20px;">{icon}</div>'
        f'<div><div style="font-size:13px;font-weight:600;color:#111827;">{name}</div>'
        f'<div style="font-size:12px;color:#9ca3af;">{desc}</div></div>'
        f'</div>'
        for icon, name, desc in techs
    ])

    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 4px;">Tech Stack</div>
        {tech_rows}
    </div>
    """, unsafe_allow_html=True)

    # Performance
    metrics = [
        ("< 2 min", "Ranking Runtime"),
        ("100%", "CPU Only"),
        ("~80", "Honeypots Caught"),
        ("3.5 hrs", "Precomputation"),
    ]

    metrics_rows = "".join([
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f3f4f6;">'
        f'<div style="font-size:13px;color:#6b7280;">{label}</div>'
        f'<div style="font-size:14px;font-weight:700;color:#6366f1;">{value}</div>'
        f'</div>'
        for value, label in metrics
    ])

    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 4px;">Performance</div>
        {metrics_rows}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 16px;
        padding: 24px;
        margin-top: 16px;
        text-align: center;
    ">
        <div style="font-size: 15px; font-weight: 700; color: white; margin-bottom: 4px;">Shreya Chaturvedi</div>
        <div style="font-size: 13px; color: rgba(255,255,255,0.75);">1st Year CS Student · Solo Participant</div>
        <div style="margin-top: 12px;">
            <a href="https://github.com/Shreya-git-ai/Recruiter_Brain"
               style="color:white;font-size:13px;text-decoration:none;">
               🔗 GitHub Repository
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)