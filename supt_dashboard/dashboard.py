import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

# Placeholder/demo data until live NOAA/USGS feed wired
x = [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")]
y = [0.1]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="ΔΦ Drift"))

fig.update_layout(
    title="SUPT ψ-Fold Dashboard (Main Build)",
    xaxis_title="Date/Time (UTC)",
    yaxis_title="ΔΦ Drift",
)

# ✅ Always write to root as index.html
pio.write_html(fig, file="index.html", auto_open=False)
print("✅ Dashboard written to index.html")
