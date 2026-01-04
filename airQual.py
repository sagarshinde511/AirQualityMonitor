import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=10 * 1000, key="refresh")  # 10 seconds

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Air Quality Monitor",
    layout="wide"
)

# ---------------- DATABASE ENGINE ----------------
engine = create_engine(
    "mysql+pymysql://u263681140_students:testStudents@123:82.180.143.66/u263681140_students"
)

# ---------------- FETCH DATA ----------------
def get_data():
    query = """
    SELECT 
        id,
        DateT,
        GasRange,
        DustValue,
        Temp,
        Humidity
    FROM AirQualityMonitor
    ORDER BY DateT DESC
    LIMIT 100
    """
    return pd.read_sql(query, engine)

# ---------------- UI ----------------
st.title("🌫️ Air Quality Monitoring Dashboard")

try:
    df = get_data()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Live Sensor Data")
st.dataframe(df, use_container_width=True)

# ---------------- PREPARE DATA ----------------
df["DateT"] = pd.to_datetime(df["DateT"])
df = df.sort_values("DateT")

# Convert values to numeric for plotting
for col in ["GasRange", "DustValue", "Temp", "Humidity"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------- GRAPHS ----------------
st.subheader("📈 Sensor Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Gas Range & Dust Value**")
    st.line_chart(
        df.set_index("DateT")[["GasRange", "DustValue"]]
    )

with col2:
    st.markdown("**Temperature & Humidity**")
    st.line_chart(
        df.set_index("DateT")[["Temp", "Humidity"]]
    )

# ---------------- FOOTER ----------------
st.caption("🔄 Auto-refresh every 10 seconds | Data from AirQualityMonitor table")

