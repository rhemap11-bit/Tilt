import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# --- Setup ---
LOG_FILE = Path("logs.json")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# --- Palette & Fonts ---
FUN_FONT = "Comic Sans MS, cursive, sans-serif"
ACCENT_COLORS = {
    "Quick Log": "#FFD6E0",
    "Daily Checklist": "#D4FFEA",
    "Trends": "#D4EAFF",
    "Notes": "#FFF3B0",
    "Doctor Export": "#E5D4FF",
}
SYMPTOM_COLORS = ["#FFD6E0","#E5D4FF","#D4EAFF","#FFF3B0","#D4FFEA","#FFD6E0","#E5D4FF","#D4EAFF"]

SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]

# --- Accessibility ---
st.sidebar.header("Accessibility Settings")
large_text = st.sidebar.checkbox("Large Text Mode")
high_contrast = st.sidebar.checkbox("High Contrast Mode")
font_size = "20px" if large_text else "16px"
bg_color = "#000000" if high_contrast else "#F9F5FF"
text_color = "#ffffff" if high_contrast else "#000000"

# --- Styles ---
st.markdown(f"""
<style>
body, h1, h2, h3, label, div {{
    font-family: {FUN_FONT};
    font-size: {font_size};
    color: {text_color};
}}
.section-header {{
    font-weight: 700;
    font-size: 24px;
    margin-bottom:5px;
}}
.pill {{
    display:inline-block;
    border-radius:20px;
    padding:8px 16px;
    margin:4px;
    cursor:pointer;
    font-weight:500;
}}
</style>
""", unsafe_allow_html=True)

# --- Load Logs ---
if LOG_FILE.exists():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
else:
    logs = []

st.set_page_config(page_title="Tilt: POTS Tracker", layout="centered")
st.markdown(f"<h1 style='text-align:center; color:{ACCENT_COLORS['Doctor Export']}'>Tilt: POTS Tracker</h1>", unsafe_allow_html=True)

# --- Helper ---
def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# --- Quick Log ---
with st.expander("Quick Log", expanded=True):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Quick Log']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Quick Log")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
    heart_rate = st.number_input("Heart Rate", 40, 200, 70)
    blood_pressure = st.text_input("Blood Pressure (optional)")
    hydration = st.number_input("Hydration (ml)", 0, 5000, 250)
    salt_intake = st.number_input("Salt Intake (g)", 0, 50, 1)
    severity = st.slider("Severity (1-10)", 1, 10, 5)

    # --- Symptoms as multi-select pills ---
    st.subheader("Symptoms")
    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    cols = st.columns(4)
    for i, symptom in enumerate(SYMPTOMS):
        color = SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)]
        selected = symptom in st.session_state.selected_symptoms
        bg = color if selected else "#F0F0F0"
        if cols[i % 4].button(symptom, key=f"symptom_{i}", help="Click to select/deselect"):
            if selected:
                st.session_state.selected_symptoms.remove(symptom)
            else:
                st.session_state.selected_symptoms.append(symptom)
        # Hack: manually apply color via markdown
        if selected:
            st.markdown(f"<span class='pill' style='background-color:{color}'>{symptom}</span>", unsafe_allow_html=True)

    other_symptoms = st.text_input("Other Symptoms (optional)")
    if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(other_symptoms)

    # --- Triggers as pills ---
    st.subheader("Possible Triggers")
    if "selected_triggers" not in st.session_state:
        st.session_state.selected_triggers = []

    cols = st.columns(3)
    for i, trigger in enumerate(TRIGGERS):
        color = "#FFD6E0" if trigger not in st.session_state.selected_triggers else "#FFB3C6"
        selected = trigger in st.session_state.selected_triggers
        if cols[i % 3].button(trigger, key=f"trigger_{i}"):
            if selected:
                st.session_state.selected_triggers.remove(trigger)
            else:
                st.session_state.selected_triggers.append(trigger)

    what_helped = st.text_area("What Helped?")

    if st.button("Add Log", key="log_btn"):
        new_entry = {
            "timestamp": timestamp,
            "posture": posture,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "hydration": hydration,
            "salt_intake": salt_intake,
            "severity": severity,
            "symptoms": st.session_state.selected_symptoms.copy(),
            "triggers": st.session_state.selected_triggers.copy(),
            "what_helped": what_helped
        }
        logs.append(new_entry)
        save_logs()
        st.success("Log added!")
        st.session_state.selected_symptoms.clear()
        st.session_state.selected_triggers.clear()
