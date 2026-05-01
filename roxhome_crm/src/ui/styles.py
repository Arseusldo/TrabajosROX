import streamlit as st

def inject_global_styles():
    st.markdown(
        """
        <style>
        :root {
            --bg-sidebar:#1E2F4F;
            --primary:#7A1230;
            --soft:#F4F6FA;
            --card:#FFFFFF;
            --ok:#1FA971;
            --warn:#F39C12;
            --danger:#C0392B;
            --text:#1F2937;
        }
        .stApp {background: var(--soft);}
        [data-testid="stSidebar"] {background: var(--bg-sidebar);}
        [data-testid="stSidebar"] * {color: #F4F7FF !important;}
        .main .block-container{padding-top:1.2rem;padding-bottom:1.5rem;max-width:1300px;}
        .rh-card {
            background:var(--card); border-radius:14px; padding:16px 18px; 
            box-shadow:0 6px 18px rgba(16,24,40,.08); border:1px solid #E5E7EB;
        }
        .rh-kpi-title{font-size:.8rem;color:#6B7280;margin-bottom:6px;}
        .rh-kpi-value{font-size:1.55rem;font-weight:700;color:var(--text);}
        .rh-chip{display:inline-block;padding:4px 10px;border-radius:14px;font-size:.76rem;font-weight:600;}
        .chip-ok{background:#EAF8F2;color:var(--ok);} .chip-warn{background:#FFF4E5;color:var(--warn);} .chip-danger{background:#FDECEC;color:var(--danger);} .chip-neutral{background:#EEF2F7;color:#475467;}
        .stButton>button {background:var(--primary);color:white;border-radius:10px;border:none;padding:.5rem .95rem;font-weight:600;}
        .stButton>button:hover {filter:brightness(1.05);}
        .stDataFrame, .stTable {background:white;border-radius:12px;}
        div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input, .stDateInput input, .stTextArea textarea {
            border-radius:10px !important;
        }
        @media (max-width: 900px){
          .main .block-container{padding-left:.8rem;padding-right:.8rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
