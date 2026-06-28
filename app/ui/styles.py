GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
 
/* ===== RESET & BASE ===== */
html, body {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {
    background: #f8faff;
}
.block-container {
    padding-top: 1rem !important;
}
/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}
[data-testid="stSidebarContent"] {
    padding-top: 0rem;
}
 
/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #6366f1; border-radius: 3px; }
 
/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}
 
/* ===== METRICS ===== */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e8ecf4;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
[data-testid="metric-container"] label {
    color: #6b7280 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
 
/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #e8ecf4 !important;
}
 
/* ===== SLIDERS ===== */
.stSlider [data-baseweb="slider"] {
    margin-top: 8px;
}
.stSlider [data-testid="stThumbValue"] {
    color: #6366f1 !important;
}
 
/* ===== ALERTS ===== */
.stSuccess {
    background: rgba(16, 185, 129, 0.08) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 12px !important;
}
.stError {
    background: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 12px !important;
}
.stWarning {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-radius: 12px !important;
}
 
/* ===== SPINNER ===== */
.stSpinner {
    color: #6366f1 !important;
}
 
/* ===== DIVIDER ===== */
hr {
    border-color: #e8ecf4 !important;
    margin: 24px 0 !important;
}
 
/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: #f8faff !important;
    border-radius: 10px !important;
    border: 1px solid #e8ecf4 !important;
}
</style>
"""
 
SIDEBAR_CSS = """
<style>
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 20px 16px 16px 16px;
    border-bottom: 1px solid #e8ecf4;
    margin-bottom: 16px;
}
.sidebar-logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.sidebar-logo-text {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
}
.sidebar-status {
    padding: 12px 16px;
    margin-top: 16px;
}
.sidebar-status-title {
    font-size: 11px;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
}
.status-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #374151;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    flex-shrink: 0;
}
</style>
"""