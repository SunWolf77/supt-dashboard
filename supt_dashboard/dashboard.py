import os
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

# Example data (replace with NOAA/USGS later)
x = [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")]
y = [0.1]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="ΔΦ Drift"))

# Ensure ./site exists
os.makedirs("site", exist_ok=True)

# Always write to ./site/index.html
output_path = os.path.join("site", "index.html")
pio.write_html(fig, file=output_path, auto_open=False)

print(f"✅ Dashboard written to {output_path}")
