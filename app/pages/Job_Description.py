import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from src.semantic_score import JD_FOCUS_TEXT
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS

st.set_page_config(page_title="Job Description", layout="wide", page_icon="📄")
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
    <div style="margin-bottom: 32px;">
        <h1 style="font-size: 28px; font-weight: 700; color: #111827; margin-bottom: 8px;">📄 Job Description</h1>
        <p style="font-size: 14px; color: #6b7280;">All candidates are ranked against this role using semantic matching</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #f3f4f6;">
            <div style="
                background: linear-gradient(135deg, #6366f1, #4f46e5);
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
            ">Senior AI Engineer</div>
            <div style="font-size: 13px; color: #6b7280;">Founding Team · Redrob AI · Pune/Noida, India</div>
        </div>
        <h3 style="font-size: 16px; font-weight: 600; color: #374151; margin-bottom: 12px;">AI Summary</h3>
        <p style="font-size: 14px; color: #6b7280; line-height: 1.7; margin-bottom: 0;">
            Senior AI Engineer role at a Series A startup building talent intelligence. 
            Requires 5-9 years applied ML/AI experience at product companies (not pure consulting/research), 
            hands-on with production embeddings, vector DBs, hybrid search, and ranking/retrieval evaluation 
            frameworks (NDCG, MRR). Must be actively coding, India-based, and available.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <h3 style="font-size: 16px; font-weight: 600; color: #374151; margin-bottom: 16px;">Matching Criteria Used</h3>
    """, unsafe_allow_html=True)

    st.text_area("Semantic embedding query", JD_FOCUS_TEXT, height=300, disabled=True, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    requirements = [
        ("✅ Required", "#10b981", [
            "5-9 yrs experience",
            "Production embeddings",
            "Vector DB / hybrid search",
            "NDCG / MRR eval frameworks",
            "Active hands-on coder",
            "India-based preferred",
            "NLP / IR background",
        ]),
        ("❌ Disqualifiers", "#ef4444", [
            "Pure research only",
            "Pure consulting only",
            "18+ months no coding",
            "Title-chasing pattern",
            "CV/robotics, no NLP",
        ]),
    ]

    for title, color, items in requirements:
        items_html = "".join([
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:13px;color:#374151;">'
            f'<div style="width:6px;height:6px;border-radius:50%;background:{color};flex-shrink:0;"></div>'
            f'{item}</div>'
            for item in items
        ])
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e8ecf4;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 13px; font-weight: 600; color: {color}; margin-bottom: 14px;">{title}</div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)