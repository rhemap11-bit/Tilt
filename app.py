import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os

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
    "Symptoms": "#FFD6E0",
    "Triggers": "#E5D4FF"
}

SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]

TRIGGERS = ["Standing for long periods","Heat exposure","Stress","Lack of sleep","Dehydration","Salt restriction"]

# --- Accessibility ---
st.sidebar.header("Accessibility Settings")
large_text = st.sidebar.checkbox("Large Text Mode")
high_contrast = st.sidebar.checkbox("High Contrast Mode")
font_size = "20px" if large_text else "16px"
bg_color = "#000000" if high_contrast else "#F9F5FF"
text_color = "#ffffff" if high_contrast else "#000000"

# --- Global Styles ---
st.markdown(f"""
<style>
body, h1, h2, h3, label, div {{
    font-family: {FUN_FONT};
    font-size: {font_size};
    color: {text_color};
}}
.reportview-container {{
    background-color: {bg_color};
}}
.sidebar .sidebar-content {{
    background-color: #E5D4FF;
}}
.section-header {{
    font-weight: 700;
    font-size: 24px;
    margin-bottom:5px;
}}
.small-text {{
    font-weight: 400;
    font-size:16px;
}}
</style>
""", unsafe_allow_html=True)

# --- Load Logs ---
if LOG_FILE.exists():
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
else:
    logs = []

# --- Page Config ---
st.set_page_config(page_title="Tilt: POTS Tracker", layout="centered")
st.markdown(f"<h1 style='text-align:center; color:#E5D4FF'>Tilt: POTS Tracker</h1>", unsafe_allow_html=True)

# --- Helper: Save Logs ---
def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# --- Quick Log ---
with st.expander("Quick Log", expanded=True):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Quick Log']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Quick Log")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
    heart_rate = st.number_input("Heart Rate", min_value=40, max_value=200, value=70)
    blood_pressure = st.text_input("Blood Pressure (optional)")
    hydration = st.number_input("Hydration (ml)", min_value=0, max_value=5000, value=250)
    salt_intake = st.number_input("Salt Intake (g)", min_value=0, max_value=50, value=1)
    severity = st.slider("Severity (1-10)", 1, 10, 5)

    # --- Symptoms Inline Checkboxes ---
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Symptoms']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Select Symptoms")
    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    cols = st.columns(4)
    for i, symptom in enumerate(SYMPTOMS):
        selected = symptom in st.session_state.selected_symptoms
        label = f"✅ {symptom}" if selected else f"🔹 {symptom}"
        if cols[i % 4].checkbox(label, key=f"symptom_{i}"):
            if not selected:
                st.session_state.selected_symptoms.append(symptom)
        else:
            if selected:
                st.session_state.selected_symptoms.remove(symptom)

    other_symptoms = st.text_input("Other Symptoms (optional)")
    if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(other_symptoms)

    # --- Possible Triggers ---
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Triggers']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Possible Triggers")
    if "selected_triggers" not in st.session_state:
        st.session_state.selected_triggers = []
    for trigger in TRIGGERS:
        checked = st.checkbox(trigger, value=trigger in st.session_state.selected_triggers)
        if checked:
            if trigger not in st.session_state.selected_triggers:
                st.session_state.selected_triggers.append(trigger)
        else:
            if trigger in st.session_state.selected_triggers:
                st.session_state.selected_triggers.remove(trigger)

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

# --- Daily Checklist ---
with st.expander("Daily Checklist"):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Daily Checklist']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Daily Checklist")
    meds = st.checkbox("Medications taken")
    water_goal = st.checkbox("Water goal met")
    compression_wear = st.checkbox("Compression wear")
    exercise_tolerance = st.checkbox("Exercise tolerance")

    if st.button("Save Daily Checklist", key="checklist_btn"):
        checklist_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "meds": meds,
            "water_goal": water_goal,
            "compression_wear": compression_wear,
            "exercise_tolerance": exercise_tolerance
        }
        logs.append(checklist_entry)
        save_logs()
        st.success("Checklist saved!")

# --- Trends ---
with st.expander("Trends"):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Trends']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Trends")
    if logs:
        df = pd.DataFrame(logs)
        trend_cols = ["heart_rate","hydration","severity"]
        for col in trend_cols:
            if col not in df.columns:
                df[col] = None
        df_chart = df[["timestamp"] + trend_cols].copy()
        df_chart['timestamp'] = pd.to_datetime(df_chart['timestamp'])
        df_chart = df_chart.set_index('timestamp')
        st.line_chart(df_chart)
    else:
        st.info("No data to show trends yet.")

# --- Notes ---
with st.expander("Notes"):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Notes']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Notes")
    note_text = st.text_area("Add a note")
    uploaded_file = st.file_uploader("Attach photo (optional)", type=["png","jpg","jpeg"])
    if st.button("Save Note", key="note_btn"):
        note_entry = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "note": note_text}
        if uploaded_file:
            path = UPLOAD_DIR / uploaded_file.name
            with open(path,"wb") as f:
                f.write(uploaded_file.getbuffer())
            note_entry["image"] = str(path)
        logs.append(note_entry)
        save_logs()
        st.success("Note saved!")

# --- Doctor Export ---
with st.expander("Doctor Export"):
    st.markdown(f"<div style='height:8px; background-color:{ACCENT_COLORS['Doctor Export']}; border-radius:4px;'></div>", unsafe_allow_html=True)
    st.subheader("Doctor Export")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Generate PDF", key="pdf_btn"):
        filtered_logs = [log for log in logs if 'timestamp' in log and start_date <= pd.to_datetime(log['timestamp']).date() <= end_date]
        if filtered_logs:
            pdf_file = BytesIO()
            with PdfPages(pdf_file) as pdf:
                for log in filtered_logs:
                    plt.figure(figsize=(6,2))
                    plt.text(0.5,0.5,str(log),fontsize=12)
                    plt.axis('off')
                    pdf.savefig()
                    plt.close()
            pdf_file.seek(0)
            st.download_button("Download PDF", data=pdf_file, file_name="Tilt_export.pdf")
        else:
            st.info("No logs in selected date range.")

