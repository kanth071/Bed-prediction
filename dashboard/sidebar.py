# =========================================================
# PREMIUM ENTERPRISE SIDEBAR 
# =========================================================

import os
import streamlit as st
import pandas as pd

def render_sidebar(data):
    """Render the ultra-premium sidebar with custom navigation."""

    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    
    with st.sidebar.container():
        # Inject custom CSS for perfect column alignment in branding
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:nth-child(2) [data-testid="column"] {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3.2])
        
        with col1:
            if os.path.exists(logo_path):
                st.image(logo_path, use_column_width=True)
            else:
                st.markdown('<div style="width:55px; height:55px; background:rgba(255,255,255,0.05); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; border: 1px solid rgba(255,255,255,0.15);">🏥</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(
                """
                <div style="margin-left: -5px;">
                    <h1 style="color: #fff; font-size: 1.4rem; margin: 0; font-weight: 800; letter-spacing: 0.5px; line-height: 1;">BedForecast</h1>
                    <p style="color: #06b6d4; font-size: 0.65rem; margin: 0; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 2px;">Predictive Intelligence</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 2. CUSTOM NAVIGATION
    if "nav_state" not in st.session_state:
        st.session_state.nav_state = "Dashboard Overview"

    nav_items = [
        ("Dashboard Overview", "📊"),
        ("ICU Analytics", "🏩"),
        ("Emergency Analytics", "🚑"),
        ("General Analytics", "🏥"),
        ("Bed Occupancy", "🛏️"),
        ("Risk Alerts", "⚠️"),
        ("Resource Management", "👥"),
        ("AI Forecasting", "🔮")
    ]


    st.sidebar.markdown("<div style='color: #64748b; font-size: 0.7rem; font-weight: 700; margin-left: 30px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px;'>Navigation</div>", unsafe_allow_html=True)

    # Simplified button rendering for perfect horizontal alignment
    for item, icon in nav_items:
        label = f"{icon} &nbsp; {item}"
        
        # Use key to maintain state
        if st.sidebar.button(label, key=f"nav_{item}", use_container_width=True):
            if st.session_state.nav_state != item:
                st.session_state.nav_state = item
                st.rerun()




    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    # 3. GLOBAL FILTERS (Removed as per user request)
    # Defaulting internal state to maintain app compatibility
    selected_sector = "All Units"
    max_date = data['Date'].max().date()
    current_month_start = max_date.replace(day=1)
    date_range = (current_month_start, max_date)

    # Return state
    return st.session_state.nav_state, selected_sector, date_range
