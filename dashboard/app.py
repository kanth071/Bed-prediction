# =========================================================
# AI HOSPITAL OPERATIONS INTELLIGENCE - COMPACT ENTERPRISE
# =========================================================

import streamlit as st
import pandas as pd
import os
import sys
import datetime
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.sidebar import render_sidebar
from dashboard.charts import (
    plot_advanced_forecast,
    plot_radial_occupancy,
    plot_sparkline,
    plot_utilization_heatmap,
    plot_staffing_trend
)
from dashboard.utils import (
    load_data,
    load_predictions,
    get_summary_metrics,
    get_live_activity_feed,
    get_smart_recommendations,
    get_resolved_history
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BedForecast",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open(os.path.join(os.path.dirname(__file__), "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =========================================================
# COMPONENT: COMPACT KPI CARD
# =========================================================

def render_kpi_compact(title, value, sublabel, status="Stable", color="blue", spark_data=None):
    chip_class = f"chip chip-{status.lower()}"
    st.markdown(
        f"""
        <div class="kpi-card-compact">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div class="kpi-label-compact">{title}</div>
                <div class="{chip_class}">{status}</div>
            </div>
            <div class="kpi-val">{value}</div>
            <div class="kpi-sublabel">{sublabel}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if spark_data is not None:
        fig = plot_sparkline(spark_data, 'Admissions', color=f"var(--neon-{color})")
        st.markdown('<div style="margin-top: -60px; margin-left: -15px; opacity: 0.25; pointer-events: none;">', unsafe_allow_html=True)
        st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# COMPONENT: COMPACT AI INSIGHT ROW
# =========================================================

def render_insight_compact(icon, text):
    st.markdown(
        f"""
        <div class="insight-row-compact">
            <span class="insight-icon-compact">{icon}</span>
            <span class="insight-text-compact">{text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN DASHBOARD APP
# =========================================================

def main():
    data = load_data()
    if data is None: return

    # Sidebar (Calibrated to 240px via CSS)
    selection, selected_sector, date_range = render_sidebar(data)
    
    # 1. Filter Data by Date
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range

    filtered_data = data[
        (data['Date'] >= pd.to_datetime(start_date)) &
        (data['Date'] <= pd.to_datetime(end_date))
    ]

    # 2. Filter Data by Sector
    if selected_sector != "All Units":
        filtered_data = filtered_data[filtered_data['service'] == selected_sector]

    metrics = get_summary_metrics(filtered_data)

    # 1. Header
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; margin-bottom:20px; border-bottom:1px solid var(--border-glass);">
            <div style="font-size:1.1rem; font-weight:800; letter-spacing:0.5px; color:var(--text-primary);">BEDFORECAST COMMAND CENTER <span style="color:var(--text-muted); font-weight:400; font-size:0.85rem;">| {selection.upper()} | {datetime.datetime.now().strftime("%d/%m/%Y")}</span></div>
            <div style="font-size:0.8rem; font-weight:700; color:var(--neon-blue); letter-spacing:1px;">AI CONFIDENCE: 94.2%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if selection == "Dashboard Overview":
        # ... (Dashboard Overview code remains same)
        # 2. TOP: KPI CARDS
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: render_kpi_compact("Total Admissions", f"{metrics['total_admissions']:,}", "Daily Patients", "Stable", "blue", filtered_data)
        with k2: render_kpi_compact("ICU Occupancy", f"{metrics['icu_load']:,}", "Beds Occupied", "Critical", "red")
        with k3: render_kpi_compact("Emergency Load", f"{metrics['emergency_load']:,}", "Current Cases", "Moderate", "orange")
        with k4: render_kpi_compact("General Demand", f"{metrics['general_load']:,}", "Ward Patients", "Stable", "green")
        with k5: render_kpi_compact("Utilization", f"{metrics['avg_occupancy']:.1f}%", "System Load", "Stable", "cyan")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. MIDDLE: FORECAST & ANALYTICS
        main_col, side_col = st.columns([2.8, 1.2])

        with main_col:
            st.markdown('<div class="section-header-compact">🔮 PREDICTIVE INTELLIGENCE <span class="prediction-badge" style="font-size:0.6rem;">14-DAY HORIZON</span></div>', unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            em_preds = load_predictions("emergency")
            icu_preds = load_predictions("icu")
            
            with f1: 
                if em_preds is not None: st.plotly_chart(plot_advanced_forecast(em_preds, title="Emergency Demand Forecast", height=280), use_container_width=True)
            with f2:
                if icu_preds is not None: st.plotly_chart(plot_advanced_forecast(icu_preds, title="ICU Occupancy Trend", height=280), use_container_width=True)

            st.markdown('<div class="section-header-compact">🏗️ CAPACITY DISTRIBUTION</div>', unsafe_allow_html=True)
            occ1, occ2, occ3 = st.columns(3)
            with occ1: st.plotly_chart(plot_radial_occupancy(76, "ICU Units", color="#ef4444", size=150), use_container_width=True)
            with occ2: st.plotly_chart(plot_radial_occupancy(metrics['avg_occupancy'], "Overall", color="#f59e0b", size=150), use_container_width=True)
            with occ3: st.plotly_chart(plot_radial_occupancy(68, "General Wards", color="#10b981", size=150), use_container_width=True)

        with side_col:
            st.markdown('<div class="section-header-compact">🚨 SYSTEM ALERTS</div>', unsafe_allow_html=True)
            st.markdown('<div style="background:rgba(239,68,68,0.05); border-left:2px solid var(--neon-red); padding:10px; border-radius:4px; margin-bottom:10px;"><div style="font-size:0.75rem; font-weight:700; color:var(--neon-red);">ICU CAPACITY ALERT</div><div style="font-size:0.65rem; color:var(--text-secondary);">Approaching safe threshold on Day 10.</div></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-header-compact">⏱️ ACTIVITY FEED</div>', unsafe_allow_html=True)
            feed = get_live_activity_feed()
            for item in feed[:5]:
                st.markdown(f'<div class="feed-compact"><span class="feed-time-compact">{item["time"]}</span> <span style="margin-left:5px; color:#fff;">{item["msg"]}</span></div>', unsafe_allow_html=True)

        # 4. BOTTOM: COMPACT AI INSIGHTS & RECS
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header-compact">🤖 AI RECOMMENDATION ENGINE</div>', unsafe_allow_html=True)
        
        i1, i2, i3, i4 = st.columns(4)
        with i1: render_insight_compact("📈", "Emergency demand +8%")
        with i2: render_insight_compact("⚠️", "ICU nearing threshold")
        with i3: render_insight_compact("✅", "General ward stable")
        with i4: render_insight_compact("👨‍⚕️", "Add 4 standby staff")

        st.markdown("<br>", unsafe_allow_html=True)
        
        recs = get_smart_recommendations()
        r1, r2, r3 = st.columns(3)
        for i, r in enumerate(recs):
            with [r1, r2, r3][i]:
                st.markdown(
                    f"""
                    <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:10px; padding:15px; height:120px; display:flex; flex-direction:column; justify-content:center;">
                    <div style="font-size:0.9rem; font-weight:800; color:var(--neon-cyan); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px;">{r['title']}</div>
                    <div style="font-size:0.8rem; color:var(--text-primary); line-height:1.5;">{r['desc']}</div>
                </div>
                    """,
                    unsafe_allow_html=True
                )

    elif selection == "General Analytics":
        st.markdown('<div class="section-header-compact">🏥 GENERAL WARD INTELLIGENCE</div>', unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        with k1: render_kpi_compact("General Demand", f"{metrics['general_load']:,}", "Active Patients", "Stable", "green")
        with k2: render_kpi_compact("Bed Availability", "42", "Free Beds", "High", "cyan")
        with k3: render_kpi_compact("Avg LOS", "4.2 Days", "Length of Stay", "Stable", "blue")

        st.markdown("<br>", unsafe_allow_html=True)
        
        gen_preds = load_predictions("general")
        if gen_preds is not None:
            st.plotly_chart(plot_advanced_forecast(gen_preds, title="General Ward Demand Forecast", height=400), use_container_width=True)

    elif selection == "ICU Analytics":
        st.markdown('<div class="section-header-compact">🏩 ICU CRITICAL CARE INTELLIGENCE</div>', unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        with k1: render_kpi_compact("ICU Occupancy", f"{metrics['icu_load']:,}", "Beds Occupied", "Critical", "red")
        with k2: render_kpi_compact("Ventilator Use", "18", "Active Units", "High", "orange")
        with k3: render_kpi_compact("Staff Ratio", "1:2", "Nurse-to-Patient", "Stable", "green")

        st.markdown("<br>", unsafe_allow_html=True)
        
        icu_preds = load_predictions("icu")
        if icu_preds is not None:
            st.plotly_chart(plot_advanced_forecast(icu_preds, title="ICU Occupancy Trend", height=400), use_container_width=True)

    elif selection == "Emergency Analytics":
        st.markdown('<div class="section-header-compact">🚑 EMERGENCY DEPARTMENT INTELLIGENCE</div>', unsafe_allow_html=True)
        
        k1, k2, k3 = st.columns(3)
        with k1: render_kpi_compact("Emergency Load", f"{metrics['emergency_load']:,}", "Current Cases", "Moderate", "orange")
        with k2: render_kpi_compact("Avg Wait Time", "18m", "To See Physician", "Stable", "blue")
        with k3: render_kpi_compact("Triage Count", "12", "In Processing", "Active", "cyan")

        st.markdown("<br>", unsafe_allow_html=True)
        
        em_preds = load_predictions("emergency")
        if em_preds is not None:
            st.plotly_chart(plot_advanced_forecast(em_preds, title="Emergency Demand Forecast", height=400), use_container_width=True)

    elif selection == "Bed Occupancy":
        # 1. TOP KPI STRIP (5 CARDS)
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: render_kpi_compact("ICU Occupancy", "88%", "22/25 Beds", "Critical", "red")
        with k2: render_kpi_compact("Emergency", "72%", "36/50 Beds", "Stable", "orange")
        with k3: render_kpi_compact("General Ward", "64%", "128/200 Beds", "Stable", "green")
        with k4: render_kpi_compact("Available Beds", "64", "System Wide", "High", "cyan")
        with k5: render_kpi_compact("Critical Alerts", "2", "Immediate Action", "Risk", "red")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. MAIN 3-PANEL LAYOUT
        left_p, center_p, right_p = st.columns([1, 2, 1])

        with left_p:
            st.markdown('<div class="section-header-compact">📟 REAL-TIME GAUGES</div>', unsafe_allow_html=True)
            st.plotly_chart(plot_radial_occupancy(88, "ICU", color="#ef4444", size=160), use_container_width=True)
            st.plotly_chart(plot_radial_occupancy(72, "EMERGENCY", color="#f59e0b", size=160), use_container_width=True)
            st.plotly_chart(plot_radial_occupancy(64, "GENERAL", color="#10b981", size=160), use_container_width=True)

        with center_p:
            st.markdown('<div class="section-header-compact">📈 OCCUPANCY DYNAMICS</div>', unsafe_allow_html=True)
            # Custom trend chart for occupancy
            occ_trend = filtered_data.copy()
            occ_trend['Threshold'] = 85
            fig_trend = px.line(occ_trend, x='Date', y=['Bed_Occupancy', 'Threshold'], 
                               template='plotly_dark', color_discrete_sequence=['#00d4ff', 'rgba(239, 68, 68, 0.5)'])
            fig_trend.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, xaxis=dict(tickformat='%d/%m/%Y'))
            st.plotly_chart(fig_trend, use_container_width=True)
            
            st.markdown('<div class="section-header-compact">🏗️ DEPARTMENT COMPARISON</div>', unsafe_allow_html=True)
            dept_comp = pd.DataFrame({
                'Dept': ['ICU', 'ER', 'GEN'],
                'Used': [22, 36, 128],
                'Total': [25, 50, 200]
            })
            fig_bar = px.bar(dept_comp, x='Dept', y=['Used', 'Total'], barmode='group', 
                             template='plotly_dark', color_discrete_sequence=['#00d4ff', 'rgba(255,255,255,0.1)'])
            fig_bar.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with right_p:
            st.markdown('<div class="section-header-compact">🕒 LIVE BED FEED</div>', unsafe_allow_html=True)
            feed_items = [
                {"msg": "ICU Bed #12 Occupied", "time": "2m ago", "type": "critical"},
                {"msg": "ER Capacity Increased", "time": "15m ago", "type": "info"},
                {"msg": "5 Beds Released (Gen)", "time": "32m ago", "type": "success"},
                {"msg": "Surge Beds Activated", "time": "45m ago", "type": "warning"},
                {"msg": "Unit B Cleaning Sync", "time": "1h ago", "type": "info"},
                {"msg": "Triage Overflow Alert", "time": "1h ago", "type": "critical"}
            ]
            for item in feed_items:
                color = "var(--neon-red)" if item['type'] == "critical" else "var(--text-secondary)"
                st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; margin-bottom:8px; border-left:2px solid {color};">
                        <div style="font-size:0.75rem; font-weight:700; color:var(--text-primary);">{item['msg']}</div>
                        <div style="font-size:0.65rem; color:var(--text-muted);">{item['time']}</div>
                    </div>
                """, unsafe_allow_html=True)

        # 3. BOTTOM ANALYTICS SECTION
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2 = st.columns([1.5, 2.5])
        
        with b_col1:
            st.markdown('<div class="section-header-compact">🤖 AI CAPACITY INSIGHTS</div>', unsafe_allow_html=True)
            insights = [
                "ICU predicted to reach 90% capacity by Day 10.",
                "Emergency load increasing steadily (+12% trend).",
                "General ward remains stable for next 48h.",
                "Opening 10 backup beds recommended for surge."
            ]
            for ins in insights:
                st.markdown(f'<div style="font-size:0.75rem; color:var(--text-secondary); margin-bottom:8px;">• {ins}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-header-compact">⚡ OPTIMIZATION RECS</div>', unsafe_allow_html=True)
            st.markdown("""
                <div style="background:rgba(0,212,255,0.05); border:1px solid var(--border-glass); padding:10px; border-radius:8px;">
                    <div style="font-size:0.75rem; font-weight:800; color:var(--neon-blue);">STAFFING PREDICTION</div>
                    <div style="font-size:0.7rem; color:var(--text-secondary); margin-top:4px;">Increase ICU nursing pool by 15% to handle predicted overflow.</div>
                </div>
            """, unsafe_allow_html=True)

        with b_col2:
            st.markdown('<div class="section-header-compact">🌡️ OCCUPANCY HEATMAP (PEAK HOURS)</div>', unsafe_allow_html=True)
            st.plotly_chart(plot_utilization_heatmap(filtered_data), use_container_width=True)

        # 4. ALERTS FOOTER - HIGH VISIBILITY GLOW BADGES
        st.markdown("<br>", unsafe_allow_html=True)
        a_col1, a_col2, a_col3, a_col4 = st.columns(4)
        
        def render_footer_alert(text, color_var, glow_color):
            st.markdown(f"""
                <div style="background:{glow_color}; border:1px solid {color_var}; padding:15px 10px; border-radius:10px; text-align:center; box-shadow: 0 0 15px {glow_color};">
                    <div style="font-size:0.85rem; color:#ffffff; font-weight:900; letter-spacing:1px; text-transform:uppercase;">{text}</div>
                </div>
            """, unsafe_allow_html=True)

        with a_col1: render_footer_alert("ICU OVERLOAD WARNING", "var(--neon-red)", "rgba(239, 68, 68, 0.2)")
        with a_col2: render_footer_alert("BED SHORTAGE RISK: HIGH", "var(--neon-red)", "rgba(239, 68, 68, 0.2)")
        with a_col3: render_footer_alert("HIGH INFLOW DETECTED", "var(--neon-orange)", "rgba(245, 158, 11, 0.2)")
        with a_col4: render_footer_alert("ER SURGE PREDICTION", "var(--neon-cyan)", "rgba(0, 212, 255, 0.2)")


    elif selection == "Risk Alerts":
        # 1. TOP OPERATIONAL HEADER
        header_l, header_r = st.columns([3, 1])
        with header_l:
            st.markdown(
                """
                <div style="display:flex; gap:15px; align-items:center;">
                    <div class="monitoring-badge"><span class="pulse-dot"></span> LIVE AI MONITORING ACTIVE</div>
                    <div style="font-size:0.7rem; color:var(--text-muted);">| &nbsp; CRITICAL: <span style="color:var(--neon-red); font-weight:800;">1</span></div>
                    <div style="font-size:0.7rem; color:var(--text-muted);">| &nbsp; HIGH: <span style="color:var(--neon-orange); font-weight:800;">1</span></div>
                    <div style="font-size:0.7rem; color:var(--text-muted);">| &nbsp; MODERATE: <span style="color:var(--neon-blue); font-weight:800;">1</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with header_r:
            st.markdown('<div style="text-align:right; font-size:0.65rem; color:var(--text-muted); font-weight:700;">NODE SECURE: PRIMARY CLOUD</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. MINI ANALYTICS STRIP
        st.markdown(
            """
            <div class="analytics-strip">
                <div style="font-size:0.65rem; color:var(--text-muted);">AVG RESPONSE: <span style="color:var(--text-primary);">8 MINS</span></div>
                <div style="font-size:0.65rem; color:var(--text-muted);">ALERTS TODAY: <span style="color:var(--text-primary);">12</span></div>
                <div style="font-size:0.65rem; color:var(--text-muted);">RESOLVED: <span style="color:var(--neon-green);">9</span></div>
                <div style="font-size:0.65rem; color:var(--text-muted);">UPTIME: <span style="color:var(--text-primary);">99.9%</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        main_alert_col, side_alert_col = st.columns([2.6, 1.4])

        with main_alert_col:
            st.markdown('<div class="section-header-compact">🤖 AI RISK ENGINE INSIGHTS</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="ai-insight-box" style="margin-bottom:10px; padding:10px;">
                    <div style="font-size:0.8rem; color:var(--text-primary); line-height:1.4;">
                        Emergency admissions expected to rise within the next <b>6 hours</b>. 
                        <span style="color:var(--neon-cyan);">Confidence: 94%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            from dashboard.utils import get_active_alerts
            alerts = get_active_alerts(filtered_data)
            
            for a in alerts:
                status_class = f"dot-{a['status'].lower()}"
                pulse_html = '<span class="pulse-dot"></span>' if a['status'] == 'Active' else ''
                st.markdown(
                    f"""
                    <div class="alert-card alert-glow-{a['glow']}" style="margin-bottom:8px; padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <div style="display:flex; gap:12px;">
                                <div style="font-size:1.2rem;">{a['icon']}</div>
                                <div>
                                    <div style="display:flex; align-items:center; gap:8px;">
                                        <span style="font-size:0.6rem; font-weight:800; color:var(--text-muted); letter-spacing:1px;">ALERT ID: {a['id']}</span>
                                        <span class="chip-compact chip-{a['type'].lower()}" style="font-size:0.55rem; padding:1px 6px;">{a['type']}</span>
                                    </div>
                                    <div style="font-weight:800; color:var(--text-primary); font-size:0.9rem; margin-top:2px;">{a['msg']}</div>
                                    <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">
                                        {a['desc']} | <span style="color:var(--neon-cyan); font-weight:700;">Occupancy: {a['occupancy']}</span>
                                    </div>
                                    <div style="margin-top:6px;">
                                        {" ".join([f'<span class="action-chip" style="font-size:0.6rem; margin-top:0;">{act}</span>' for act in a['actions']])}
                                    </div>
                                </div>
                            </div>
                            <div style="text-align:right;">
                                <div class="status-indicator" style="font-size:0.6rem;">{pulse_html}{a['status']}</div>
                                <div style="font-size:0.65rem; color:var(--neon-orange); font-weight:700; margin-top:5px;">Req. Response: {a['response_time']}</div>
                                <div style="font-size:0.65rem; font-weight:700; color:var(--text-secondary); margin-top:10px;">{a['trend']}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with side_alert_col:
            st.markdown('<div class="section-header-compact">🖥️ COMMAND STATUS</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:10px; padding:15px; margin-bottom:15px;">
                    <div style="text-align:center;">
                        <div style="color:var(--text-muted); font-size:0.65rem; text-transform:uppercase; letter-spacing:1px;">Global Risk Score</div>
                        <div style="color:var(--neon-red); font-size:1.8rem; font-weight:800; font-family: 'JetBrains Mono';">91%</div>
                        <div style="color:var(--text-secondary); font-size:0.65rem;">System Confidence: 94%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown('<div class="section-header-compact">🕒 ACTIVITY TIMELINE</div>', unsafe_allow_html=True)
            from dashboard.utils import get_resolved_history
            history = get_resolved_history()
            for h in history:
                st.markdown(
                    f"""
                    <div class="timeline-item">
                        <div class="timeline-dot" style="background:{h['dot']};"></div>
                        <div style="font-size:0.7rem; font-weight:800; color:var(--text-primary);">{h['msg']}</div>
                        <div style="display:flex; justify-content:space-between; margin-top:2px;">
                            <span style="font-size:0.6rem; color:var(--text-muted);">ID: {h['id']}</span>
                            <span style="font-size:0.6rem; color:var(--text-muted);">{h['time']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # 4. BOTTOM SECTION: FILLING SPACE (Removed as per user request)
        pass

    elif selection == "Resource Management":
        # 1. TOP KPI STRIP (4 CARDS)
        k1, k2, k3, k4 = st.columns(4)
        with k1: render_kpi_compact("Staff On Duty", f"{metrics['avg_staff']:.0f}", "Current Shift", "Stable", "blue")
        with k2: render_kpi_compact("Efficiency Score", "91%", "System Wide", "High", "green")
        with k3: render_kpi_compact("Emergency Pool", "12", "On Standby", "Ready", "cyan")
        with k4: render_kpi_compact("System Status", "Sync", "08:00 - 16:00", "Live", "orange")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. MAIN CENTER SECTION
        left_c, right_c = st.columns([2.5, 1.5])

        with left_c:
            st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none;">Staffing vs Patient Demand Trend</div>', unsafe_allow_html=True)
            st.plotly_chart(plot_staffing_trend(filtered_data), use_container_width=True)
            
            st.markdown('<br>', unsafe_allow_html=True)
            # Department Allocation Bars
            st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none;">Department Allocation Status</div>', unsafe_allow_html=True)
            depts = [("ICU", 92, "var(--status-red)"), ("Emergency", 84, "var(--accent-cyan)"), ("General", 61, "var(--accent-purple)")]
            for name, val, color in depts:
                st.markdown(f"""
                    <div style="margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-secondary); margin-bottom:4px;">
                            <span>{name}</span>
                            <span>{val}%</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.03); height:4px; border-radius:2px; width:100%;">
                            <div style="background:{color}; height:100%; width:{val}%; border-radius:2px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with right_c:
            # AI Insights (Only 2)
            st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none;">AI Insights</div>', unsafe_allow_html=True)
            insights = [
                {"msg": "Emergency staffing pressure increasing", "type": "High", "conf": "92%"},
                {"msg": "Recommend 3 standby nurses for ICU", "type": "Priority", "conf": "88%"}
            ]
            for ins in insights:
                st.markdown(f"""
                    <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:8px; padding:12px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:0.75rem; color:var(--accent-cyan); font-weight:700;">{ins['type']}</span>
                            <span style="font-size:0.65rem; color:var(--text-muted);">Conf: {ins['conf']}</span>
                        </div>
                        <div style="font-size:0.8rem; color:var(--text-primary); margin-top:5px;">{ins['msg']}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Staffing Alerts
            st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none;">Staffing Alerts</div>', unsafe_allow_html=True)
            alerts = [("ICU staffing shortage", "Critical"), ("Emergency overload risk", "High")]
            for msg, level in alerts:
                color = "var(--status-red)" if level == "Critical" else "var(--status-orange)"
                st.markdown(f"""
                    <div style="padding:10px; border-left:3px solid {color}; background:rgba(255,255,255,0.01); margin-bottom:8px;">
                        <div style="font-size:0.75rem; color:var(--text-primary);">{msg}</div>
                        <div style="font-size:0.65rem; color:{color}; font-weight:700;">{level} Priority</div>
                    </div>
                """, unsafe_allow_html=True)

            # Live Operational Feed
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none;">Live Operational Feed</div>', unsafe_allow_html=True)
            feed = [("2 nurses reassigned to ICU", "2m ago"), ("Shift handover in 42 mins", "Scheduled")]
            for msg, time in feed:
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-secondary); margin-bottom:6px;">
                        <span>• {msg}</span>
                        <span style="color:var(--text-muted);">{time}</span>
                    </div>
                """, unsafe_allow_html=True)

    elif selection.strip() == "AI Forecasting":
        # 1. SIMULATION ENGINE STATE
        st.markdown(
            """
            <div style="background:rgba(168, 85, 247, 0.1); border:1px solid rgba(168, 85, 247, 0.4); border-radius:10px; padding:12px 25px; margin-bottom:25px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:0.9rem; color:var(--accent-purple); font-weight:800; letter-spacing:0.5px;">🤖 AI PREDICTIVE ENGINE: <span style="color:#ffffff; font-weight:600; margin-left:10px;">Simulation Mode Active</span></div>
                <div class="monitoring-badge" style="background:rgba(168, 85, 247, 0.2); color:#ffffff; border-color:var(--accent-purple); font-weight:700;">LIVE MODELING</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        @st.fragment
        def render_simulation_engine():
            f_left, f_right = st.columns([2.2, 1.8])

            with f_right:
                st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none; font-size:0.85rem;">Capacity Simulation Controls</div>', unsafe_allow_html=True)
                with st.container(border=True):
                    sim_beds = st.slider("Additional Bed Units", 0, 50, 0, key="sim_beds_v3")
                    sim_staff = st.slider("Standby Nursing Pool", 0, 20, 0, key="sim_staff_v3")
                    c1, c2 = st.columns(2)
                    with c1: flu_outbreak = st.toggle("Flu Outbreak", key="sim_flu_v3")
                    with c2: er_spike = st.toggle("ER Surge Spike", key="sim_er_v3")
                    
                    base_peak = 72.4
                    surge = (15.5 if flu_outbreak else 0) + (19.2 if er_spike else 0)
                    mitigation = (sim_beds * 0.45) + (sim_staff * 0.25)
                    simulated_peak = min(100.0, max(0.0, base_peak + surge - mitigation))
                    
                    st.markdown('<hr style="margin:15px 0; border-color:rgba(255,255,255,0.1);">', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style="text-align:center;">
                            <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;">Mitigation Impact</div>
                            <div style="font-size:1.4rem; color:var(--accent-cyan); font-weight:900;">-{mitigation:.1f}% Reduction</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown('<br>', unsafe_allow_html=True)
                logic_msg = "Combined surge & mitigation modeled." if (flu_outbreak or er_spike) else "Baseline monitoring."
                st.markdown(f"""
                    <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:12px; padding:18px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <span style="font-size:0.75rem; color:#fff; font-weight:700;">AI Confidence</span>
                            <span style="font-size:1.1rem; color:var(--accent-cyan); font-weight:900;">{94.2 - (surge/6):.1f}%</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.05); height:6px; border-radius:3px; margin-bottom:15px;"><div style="background:var(--accent-cyan); width:{94.2 - (surge/6)}%; height:100%; border-radius:3px;"></div></div>
                        <div style="font-size:0.8rem; color:#e2e8f0; line-height:1.6;">{logic_msg}</div>
                    </div>
                """, unsafe_allow_html=True)

            with f_left:
                st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none; font-size:0.85rem;">Forecast Horizon</div>', unsafe_allow_html=True)
                horizon = st.select_slider("Horizon (Days)", options=[7, 14, 20], value=14, key="f_horizon_v3")
                
                peak_color = "#ff4b4b" if simulated_peak > 85 else "#ffa500" if simulated_peak > 75 else "#00ff9f"
                st.markdown(f"""
                    <div style="background:linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(0, 212, 255, 0.15) 100%); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:25px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:0.7rem; color:#94a3b8; text-transform:uppercase;">Peak Date</div>
                            <div style="font-size:1.6rem; color:#ffffff; font-weight:900;">{18 + (horizon-14)} May</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:0.7rem; color:#94a3b8; text-transform:uppercase;">Peak Load</div>
                            <div style="font-size:2.4rem; color:{peak_color}; font-weight:900;">{simulated_peak:.0f}%</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-header-compact" style="color:var(--text-secondary); text-transform:none; font-size:0.85rem;">Trend Analysis</div>', unsafe_allow_html=True)
                chart_data = filtered_data.head(horizon).copy()
                chart_data['Simulated_Load'] = (chart_data['Bed_Occupancy'] + (surge * 0.85) - (mitigation * 0.6)).clip(10, 100)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Simulated_Load'], fill='tozeroy', line=dict(color='#a855f7', width=3), fillcolor='rgba(168, 85, 247, 0.2)'))
                fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Bed_Occupancy'], line=dict(color='rgba(255,255,255,0.2)', width=2, dash='dot')))
                fig.update_layout(
                    template='plotly_dark', height=240, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(range=[0, 110], showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # BOTTOM SUMMARY
            st.markdown("<br>", unsafe_allow_html=True)
            r1, r2, r3, r4 = st.columns(4)
            calc_beds = max(0, int((simulated_peak - 70) * 0.6)) if simulated_peak > 70 else 0
            calc_staff = max(0, int(surge / 4.5))
            with r1: st.markdown(f"""<div style="background:rgba(168, 85, 247, 0.05); padding:15px; border-radius:10px;"><div style="font-size:0.6rem; color:#94a3b8;">BEDS</div><div style="font-size:1.2rem; color:#fff; font-weight:900;">+{calc_beds}</div></div>""", unsafe_allow_html=True)
            with r2: st.markdown(f"""<div style="background:rgba(0, 212, 255, 0.05); padding:15px; border-radius:10px;"><div style="font-size:0.6rem; color:#94a3b8;">STAFF</div><div style="font-size:1.2rem; color:#fff; font-weight:900;">+{calc_staff}</div></div>""", unsafe_allow_html=True)
            icu_color = "#ff4b4b" if surge > 10 else "#00ff9f"
            with r3: st.markdown(f'<div style="padding:15px;"><div style="font-size:0.6rem; color:#94a3b8;">ICU</div><div style="font-size:1rem; color:{icu_color}; font-weight:900;">{"SURGE" if surge > 10 else "STABLE"}</div></div>', unsafe_allow_html=True)
            er_color = "#ffa500" if er_spike else "#00ff9f"
            with r4: st.markdown(f'<div style="padding:15px;"><div style="font-size:0.6rem; color:#94a3b8;">ER</div><div style="font-size:1rem; color:{er_color}; font-weight:900;">{"SPIKE" if er_spike else "NORMAL"}</div></div>', unsafe_allow_html=True)

        render_simulation_engine()


    else:
        st.info(f"The '{selection}' section is currently being finalized.")

if __name__ == "__main__":
    main()
