import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Smart Water Tank Simulator",
    page_icon="💧",
    layout="wide"
)

# ===============================
# HEADER
# ===============================

st.title("💧 Smart Water Tank Simulation Dashboard")
st.caption("Engineering Simulation System for Water Distribution Tank")

st.markdown("---")

# ===============================
# SIDEBAR CONTROL PANEL
# ===============================

st.sidebar.title("⚙️ Control Panel")

radius = st.sidebar.slider("Tank Radius (meter)", 0.5, 5.0, 2.0)
height = st.sidebar.slider("Tank Height (meter)", 1.0, 10.0, 5.0)

inlet_flow = st.sidebar.slider("Inlet Flow Rate (m³/min)", 0.1, 10.0, 2.0)
outlet_flow = st.sidebar.slider("Outlet Flow Rate (m³/min)", 0.1, 10.0, 1.0)

simulation_time = st.sidebar.slider("Simulation Time (minutes)", 10, 200, 60)

# ===============================
# TANK CALCULATION
# ===============================

tank_volume = np.pi * radius**2 * height
fill_time = tank_volume / inlet_flow
empty_time = tank_volume / outlet_flow

# ===============================
# KPI DASHBOARD
# ===============================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tank Volume", f"{tank_volume:.2f} m³")
col2.metric("Fill Time", f"{fill_time:.2f} min")
col3.metric("Empty Time", f"{empty_time:.2f} min")
col4.metric("Net Flow", f"{inlet_flow-outlet_flow:.2f} m³/min")

st.markdown("---")

# ===============================
# SIMULATION ENGINE
# ===============================

time = np.linspace(0, simulation_time, 200)

net_flow = inlet_flow - outlet_flow

volume = net_flow * time
volume = np.clip(volume, 0, tank_volume)

water_height = volume / (np.pi * radius**2)

# ===============================
# HEIGHT GRAPH
# ===============================

st.subheader("📈 Water Level vs Time")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=time,
    y=water_height,
    mode="lines",
    line=dict(width=4),
    name="Water Height"
))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Time (minutes)",
    yaxis_title="Water Height (m)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# TANK VISUALIZATION
# ===============================

st.subheader("💧 Tank Water Level Visualization")

fill_percentage = (volume[-1] / tank_volume) * 100

fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fill_percentage,
    title={'text': "Tank Fill Level (%)"},
    gauge={
        'axis': {'range': [0,100]},
        'bar': {'thickness':0.4},
        'steps':[
            {'range':[0,30],'color':"red"},
            {'range':[30,70],'color':"orange"},
            {'range':[70,100],'color':"green"}
        ],
    }
))

fig2.update_layout(height=400)

st.plotly_chart(fig2, use_container_width=True)

# ===============================
# TANK OPTIMIZATION ANALYSIS
# ===============================

st.subheader("🧠 Tank Capacity Optimization")

daily_need = st.number_input("Daily Water Demand (m³)", 10.0, 1000.0, 200.0)

recommended = daily_need * 0.25

st.success(f"Recommended Tank Volume ≈ **{recommended:.2f} m³**")

if tank_volume < recommended:
    st.warning("⚠️ Tank capacity may be too small.")
else:
    st.success("✅ Tank capacity is sufficient.")

# ===============================
# FOOTER
# ===============================

st.markdown("---")

st.caption(f"Simulation Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Engineering Modeling & Simulation System")