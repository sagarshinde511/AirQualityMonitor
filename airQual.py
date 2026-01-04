import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_autorefresh import st_autorefresh

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=10 * 1000, key="refresh")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Air Quality Monitor",
    layout="wide"
)

# ---------------- DB CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students",
        port=3306
    )

# ---------------- FETCH DATA ----------------
def get_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

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

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(rows)

# ---------------- UI ----------------
st.title("🌫️ Air Quality Monitoring Dashboard")

try:
    df = get_data()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# ---------------- TABLE ----------------
st.subheader("📋 Live Sensor Data")
st.dataframe(df, use_container_width=True)

# ---------------- DATA PREP ----------------
df["DateT"] = pd.to_datetime(df["DateT"])

for col in ["GasRange", "DustValue", "Temp", "Humidity"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("DateT")

# ---------------- GRAPHS ----------------
st.subheader("📈 Sensor Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Gas Range & Dust Value**")
    st.line_chart(df.set_index("DateT")[["GasRange", "DustValue"]])

with col2:
    st.markdown("**Temperature & Humidity**")
    st.line_chart(df.set_index("DateT")[["Temp", "Humidity"]])

# ---------------- FOOTER ----------------
st.caption("🔄 Auto refresh every 10 seconds")
