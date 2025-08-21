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
HEADER_FONT = "'Fredoka One', cursive"
BODY_FONT = "'Quicksand', sans-serif"
ACCENT_COLORS = {
    "Quick Log": "#FFD6E0",
    "Daily Checklist": "#D4FFEA",
    "Trends": "#D4EAFF",
    "Notes": "#FFF3B0",
    "Doctor Export": "#E5D4FF",
    "Symptoms": "#FFB3C6",
    "Triggers": "#B0E0FF"
}
SYMPTOM_COLORS = ["#FFD6E0","#E5D4FF","#D4EAFF","#FFF3B0","#D4FFEA","#FFB3C6","#B0E0FF","#FFD6A5"]

SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]

# --- Accessibility ---
st.sidebar.header("Accessibility Settings")
large_text = st.sidebar.checkbox("Large Text Mode")
high_contrast = st.sidebar.checkbox("High Contrast Mode")
font_size = "20px" if large_text else "16px"
bg_color = "#000000" if high_contrast else "#FFF8F0"
text_color = "#ffffff" if high_contrast else "#000000"

# --- Global Styles ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@400;500&display=swap" rel="stylesheet">
<style>
body, h1, h2, h3, label, div {{
    font-family: {BODY_FONT};
    font-size: {font_size};
    color: {text_color};
    background-color: {bg_color};
}}
.section-header {{
    font-family: {HEADER_FONT};
    font-weight: 700;
    font-size: 28px;
    margin-bottom:5px;
}}
.pill {{
    display:inline-block;
    border-radius:20px;
    padding:8px 16px;
    margin:4px;
    font-weight:500;
}}
.section-box {{
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
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
st.markdown(f"<h1 style='text-align:center; color:{ACCENT_COLORS['Doctor Export']}; font-family:{HEADER_FONT}'>Tilt: POTS Tracker</h1>", unsafe_allow_html=True)

# --- Helper ---
def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# --- Quick Log ---
with st.expander("Quick Log", expanded=True):
    st.markdown(f"<div class='section-box' style='background-color:{ACCENT_COLORS['Quick Log']};'></div>", unsafe_allow_html=True)
    st.subheader("Quick Log")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
    heart_rate = st.number_input("Heart Rate", 40, 200, 70)
    blood_pressure = st.text_input("Blood Pressure (optional)")
    severity = st.slider("Severity (1-10)", 1, 10, 5)

    # --- Symptoms as checkbox-pills ---
    st.subheader("Symptoms")
    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    sym_cols = st.columns(4)
    for i, symptom in enumerate(SYMPTOMS):
        col = sym_cols[i % 4]
        selected = symptom in st.session_state.selected_symptoms
        checked = col.checkbox("", value=selected, key=f"symptom_cb_{i}")
        if checked and symptom not in st.session_state.selected_symptoms:
            st.session_state.selected_symptoms.append(symptom)
        elif not checked and symptom in st.session_state.selected_symptoms:
            st.session_state.selected_symptoms.remove(symptom)
        color = SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)] if symptom in st.session_state.selected_symptoms else "#F0F0F0"
        col.markdown(f"<span class='pill' style='background-color:{color}'>{symptom}</span>", unsafe_allow_html=True)

    other_symptoms = st.text_input("Other Symptoms (optional)")
    if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(other_symptoms)

    # --- Triggers as checkbox-pills ---
    st.subheader("Possible Triggers")
    if "selected_triggers" not in st.session_state:
        st.session_state.selected_triggers = []

    trig_cols = st.columns(3)
    for i, trigger in enumerate(TRIGGERS):
        col = trig_cols[i % 3]
        selected = trigger in st.session_state.selected_triggers
        checked = col.checkbox("", value=selected, key=f"trigger_cb_{i}")
        if checked and trigger not in st.session_state.selected_triggers:
            st.session_state.selected_triggers.append(trigger)
        elif not checked and trigger in st.session_state.selected_triggers:
            st.session_state.selected_triggers.remove(trigger)
        color = ACCENT_COLORS['Triggers'] if trigger in st.session_state.selected_triggers else "#F0F0F0"
        col.markdown(f"<span class='pill' style='background-color:{color}'>{trigger}</span>", unsafe_allow_html=True)

    what_helped = st.text_area("What Helped?")

# --- Daily Checklist ---
with st.expander("Daily Checklist"):
    st.markdown(f"<div class='section-box' style='background-color:{ACCENT_COLORS['Daily Checklist']};'></div>", unsafe_allow_html=True)
    st.subheader("Daily Checklist")
    meds = st.checkbox("Medications taken")
    hydration = st.number_input("Hydration (ml)", 0, 5000, 250)
    salt_intake = st.number_input("Salt Intake (g)", 0, 50, 1)
    compression_wear = st.checkbox("Compression wear")
    exercise_tolerance = st.checkbox("Exercise tolerance")

    if st.button("Save Daily Checklist", key="checklist_btn"):
        checklist_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "meds": meds,
            "hydration": hydration,
            "salt_intake": salt_intake,
            "compression_wear": compression_wear,
            "exercise_tolerance": exercise_tolerance
        }
        logs.append(checklist_entry)
        save_logs()
        st.success("Checklist saved!")

# --- Trends ---
with st.expander("Trends"):
    st.markdown(f"<div class='section-box' style='background-color:{ACCENT_COLORS['Trends']};'></div>", unsafe_allow_html=True)
    st.subheader("Trends")
    if logs:
        df = pd.DataFrame(logs)
        trend_cols = ["heart_rate","hydration","salt_intake","severity"]
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
    st.markdown(f"<div class='section-box' style='background-color:{ACCENT_COLORS['Notes']};'></div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='section-box' style='background-color:{ACCENT_COLORS['Doctor Export']};'></div>", unsafe_allow_html=True)
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

# --- Final Quick Log Save ---
if st.button("Add Quick Log Entry", key="final_log_btn"):
    new_entry = {
        "timestamp": timestamp,
        "posture": posture,
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "severity": severity,
        "symptoms": st.session_state.selected_symptoms.copy(),
        "triggers": st.session_state.selected_triggers.copy(),
        "what_helped": what_helped
    }
    logs.append(new_entry)
    save_logs()
    st.success("Quick Log added!")
    st.session_state.selected_symptoms.clear()
    st.session_state.selected_triggers.clear()


