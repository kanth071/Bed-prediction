# =========================================================
# HOSPITAL BED DEMAND FORECASTING — COMPACT PREMIUM CHARTS
# =========================================================

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


CHART_THEME = "plotly_dark"
COLOR_SEQUENCE = ['#00d4ff', '#ff3e3e', '#ff9f1c', '#2ecc71', '#a855f7', '#06b6d4']

def plot_sparkline(data, column, color="#00d4ff"):
    """Create a minimalist sparkline for KPI cards."""
    fig = px.line(data.tail(15), x='Date', y=column, template=CHART_THEME)
    fig.update_traces(line=dict(color=color, width=2.5, shape='spline'))
    fig.update_xaxes(visible=False, tickformat='%d/%m/%Y')
    fig.update_yaxes(visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

def plot_radial_occupancy(value, title, color="#00d4ff", size=180):
    """Create a compact semi-circular gauge."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 11, 'color': '#94a3b8'}},
        number = {'font': {'size': 20, 'family': 'JetBrains Mono', 'color': 'white'}, 'suffix': '%'},
        gauge = {
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': color},
            'bgcolor': "rgba(255, 255, 255, 0.05)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 80], 'color': 'rgba(255, 255, 255, 0.02)'},
                {'range': [80, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
            ]
        }
    ))

    fig.update_layout(
        height=size,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': "Inter"}
    )
    return fig

def plot_advanced_forecast(predictions, title="Forecast", height=280):
    """Plot forecast with confidence bands (compact version)."""
    fig = go.Figure()

    # Confidence Interval
    fig.add_trace(go.Scatter(
        x=pd.concat([predictions['ds'], predictions['ds'][::-1]]),
        y=pd.concat([predictions['yhat_upper'], predictions['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(0, 212, 255, 0.05)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    ))

    # Forecast Line
    fig.add_trace(go.Scatter(
        x=predictions['ds'],
        y=predictions['yhat'],
        mode='lines',
        line=dict(color='#00d4ff', width=2.5, shape='spline'),
        name='AI Prediction'
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 13, 'color': 'white'}},
        template=CHART_THEME,
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=30, r=10, t=40, b=30),
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color='#64748b'), title="", tickformat='%d/%m/%Y'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', tickfont=dict(size=9, color='#64748b'), title=""),
        showlegend=False
    )
    return fig

def plot_utilization_heatmap(data):
    """Generate a heatmap (compact version)."""
    data['Month'] = data['Date'].dt.month_name()
    data['Day'] = data['Date'].dt.day_name()
    pivot = data.pivot_table(values='Bed_Occupancy', index='Day', columns='Month', aggfunc='mean')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(days_order)

    fig = px.imshow(pivot, color_continuous_scale='Blues', template=CHART_THEME)
    fig.update_layout(
        title={'text': "Occupancy Trends", 'font': {'size': 12}},
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(size=8), title=""),
        yaxis=dict(tickfont=dict(size=8), title="")
    )
    return fig

def plot_staffing_trend(data):
    """Clean enterprise staffing trend chart."""
    fig = go.Figure()
    
    # Admissions Trend (Cyan)
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Total_Admissions'],
        mode='lines', name='Patient Admissions',
        line=dict(color='#00d4ff', width=3, shape='spline'),
        hovertemplate='%{y:.0f} Admissions<extra></extra>'
    ))
    
    # Staff Count (Purple)
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Staff_Count'],
        mode='lines', name='Staff On Duty',
        line=dict(color='#a855f7', width=3, shape='spline'),
        hovertemplate='%{y:.0f} Staff<extra></extra>'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, color="#8b949e")),
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color='#484f58'), tickformat='%d/%m'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', tickfont=dict(size=10, color='#484f58'), rangemode='nonnegative')
    )
    return fig

