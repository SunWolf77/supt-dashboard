import os
import requests
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

# ======================
# 1. NOAA Solar Wind API
# ======================
def fetch_noaa():
    try:
        url = "https://services.swpc.noaa.gov/json/ace/solar_wind.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        times = [datetime.utcfromtimestamp(p["time_tag"]/1000) for p in data[-50:]]
        values = [float(p.get("density", 0)) for p in data[-50:]]
        return times, values
    except Exception as e:
        print(f"NOAA fetch failed, fallback to stub: {e}")
        return [datetime.utcnow()], [0.1]

# =====================
# 2. USGS Earthquakes
# =====================
def fetch_usgs():
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        times = [datetime.utcfromtimestamp(f["properties"]["time"]/1000) for f in data["features"]]
        mags = [f["properties"]["mag"] for f in data["features"]]
        return times, mags
    except Exception as e:
        print(f"USGS fetch failed, fallback to stub: {e}")
        return [datetime.utcnow()], [0.0]

# ==========================
# 3. Build Plotly Dashboard
# ==========================
def build_dashboard():
    noaa_t, noaa_v = fetch_noaa()
    usgs_t, usgs_m = fetch_usgs()

    fig = go.Figure()

    # NOAA ΔΦ Drift proxy
    fig.add_trace(go.Scatter(
        x=noaa_t, y=noaa_v,
        mode="lines+markers",
        name="NOAA ΔΦ Drift",
        line=dict(color="orange")
    ))

    # USGS Earthquake stress
    fig.add_trace(go.Scatter(
        x=usgs_t, y=usgs_m,
        mode="markers",
        name="USGS Earthquakes",
        marker=dict(color="red", size=10, symbol="x")
    ))

    # Layout
    fig.update_layout(
        title=f"SUϕT Dashboard — Live NOAA + USGS<br><sub>Updated {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</sub>",
        xaxis_title="Time (UTC)",
        yaxis_title="ΔΦ Drift / Magnitude",
        template="plotly_dark"
    )

    # Ensure site folder exists
    os.makedirs("site", exist_ok=True)
    output_path = os.path.join("site", "index.html")
    pio.write_html(fig, file=output_path, auto_open=False)
    print(f"✅ Dashboard written to {output_path}")

if __name__ == "__main__":
    build_dashboard()
