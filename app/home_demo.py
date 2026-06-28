import warnings
warnings.filterwarnings("ignore")
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
 
import streamlit as st
from app.ui.styles import GLOBAL_CSS, SIDEBAR_CSS
 
st.set_page_config(page_title="Recruiter Brain — Demo", layout="wide", page_icon="🧠")
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
<div style="padding: 80px 48px; text-align: center;">
    <div style="font-size: 48px; margin-bottom: 16px;">🧠</div>
    <div style="font-size: 24px; font-weight: 700; color: #111827; margin-bottom: 8px;">Recruiter Brain</div>
    <div style="font-size: 15px; color: #6b7280; margin-bottom: 24px;">
        Please navigate to <strong>HOME</strong> from the sidebar to run the pipeline and see results.
    </div>
</div>
""", unsafe_allow_html=True)