import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# --- Constants ---
LOG_FILE = Path("logs.json")
PASTEL_BG = "#fff0e5"
PASTEL_PINK = "#ffd6e0"
PASTEL_PURPLE = "#e5d4ff"
PASTEL_BLUE = "#d4eaff"

# --- Load logs ---
if LOG_FILE.exists():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
else:
    logs = []

# --- Page config ---
st.set_page_config(page_title="Tilt: POTS Tracker", layout="centered")
st.markdown(f"<h1 style='text-align:center; color:{PASTEL_PURPLE}'>Tilt: POTS Tracker</h1>", unsafe_allow_html=True)
st.markdown(f"<div style='background-color:{PASTEL_BG}; padding:15px; border-radius:20px'>", unsafe_allow_html=True)

# --- Quick Log ---
st.subheader("Quick Log")
col1, col2 = st.columns(2)
with col1:
    fatigue = st.slider("Fatigue (1-10)", 1, 10, 5)
with col2:
    heart_rate = st.number_input("Heart Rate", min_value=40, max_value=200, value=70)
symptoms = st.text_input("Symptoms")

if st.button("Add Log"):
    new_log = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fatigue": fatigue,
        "heart_rate": heart_rate,
        "symptoms": symptoms
    }
    logs.append(new_log)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f)
    st.success("Log added!")

# --- Trends ---
if logs:
    df = pd.DataFrame(logs)
    st.subheader("Trends")
    df_chart = df[["date", "fatigue", "heart_rate"]].copy()
    df_chart = df_chart.set_index("date")
    st.line_chart(df_chart, use_container_width=True)

    # --- Doctor Summary ---
    st.subheader("Doctor Summary")
    st.dataframe(df)
else:
    st.info("No logs yet. Add your first log above!")

st.markdown("</div>", unsafe_allow_html=True)
