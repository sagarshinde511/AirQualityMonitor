import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_autorefresh import st_autorefresh

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=10 * 1000, key="data_refresh")  # 10 seconds

# ---------------- DB CONNECTION ----------------
def get_data():
    conn = mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students"
    )

    query = """
    SELECT 
        id,
        DateT,
        GasRnqge,
        DustValue,
        Temp,
        Humidity
    FROM AirQualityMonitor
    ORDER BY DateT DESC
    LIMIT 100
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Air Quality Monitor", layout="wide")

st.title("🌫️ Air Quality Monitoring Dashboard")

df = get_data()

# ---------------- TABLE ----------------
st.subheader("📋 Sensor Data")
st.dataframe(df, use_container_width=True)

# ---------------- GRAPH ----------------
st.subheader("📈 Sensor Trends")

df["DateT"] = pd.to_datetime(df["DateT"])
df = df.sort_values("DateT")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(
        df.set_index("DateT")[["GasRnqge", "DustValue"]]
    )

with col2:
    st.line_chart(
        df.set_index("DateT")[["Temp", "Humidity"]]
    )

# ---------------- FOOTER ----------------
st.caption("🔄 Auto refresh every 10 seconds")
