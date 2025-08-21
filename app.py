import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os

# --- Constants ---
LOG_FILE = Path("logs.json")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# --- Palette & Font ---
PASTEL_BG = "#f9f5ff"
FUN_FONT = "Comic Sans MS, cursive, sans-serif"

EXPANDER_COLORS = {
    "Quick Log": "#fff3b0",       # yellow
    "Daily Checklist": "#d4ffea", # green
    "Trends": "#d4eaff",          # blue
    "Notes": "#ffd6e0",           # pink
    "Doctor Export": "#e5d4ff"    # purple
}

SYMPTOM_COLORS = ["#ffd6e0", "#e5d4ff", "#d4eaff", "#fff3b0", "#d4ffea", "#ffd6e0", "#e5d4ff", "#d4eaff"]

# --- Sidebar Accessibility ---
st.sidebar.header("Accessibility Settings")
large_text = st.sidebar.checkbox("Large Text Mode")
high_contrast = st.sidebar.checkbox("High Contrast Mode")

font_size = "22px" if large_text else "16px"
bg_color = "#000000" if high_contrast else PASTEL_BG
text_color = "#ffffff" if high_contrast else "#000000"

st.markdown(f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
        font-family: {FUN_FONT};
        font-size: {font_size};
    }}
    h1, h2, h3 {{
        font-family: {FUN_FONT};
    }}
    div.stButton > button {{
        border-radius: 20px;
        padding: 10px 20px;
        margin: 5px;
        font-size: {font_size};
        color: #000000;
    }}
    div.stCheckbox > label {{
        border-radius: 15px;
        padding: 8px 12px;
        margin: 4px;
        background-color: #ffd6e0;
        color: #000000;
    }}
    textarea, input, select {{
        font-size: {font_size};
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
st.markdown(f"<h1 style='text-align:center; color:#e5d4ff'>Tilt: POTS Tracker</h1>", unsafe_allow_html=True)

# --- Quick Log ---
with st.expander("Quick Log", expanded=True):
    st.markdown(f"<div style='background-color:{EXPANDER_COLORS['Quick Log']}; border-radius:15px; padding:15px;'>", unsafe_allow_html=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
    heart_rate = st.number_input("Heart Rate", min_value=40, max_value=200, value=70)
    blood_pressure = st.text_input("Blood Pressure (optional)")
    hydration = st.number_input("Hydration (ml)", min_value=0, max_value=5000, value=250)
    salt_intake = st.number_input("Salt Intake (g)", min_value=0, max_value=50, value=1)
    severity = st.slider("Severity (1-10)", 1, 10, 5)

    # Symptoms
    st.subheader("Select Symptoms")
    common_symptoms = ["Dizziness", "Heart Palpitations", "Fatigue", "Nausea",
                       "Brain Fog", "Headache", "Sweating", "Tremors"]

    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    cols = st.columns(4)
    for i, symptom in enumerate(common_symptoms):
        color = SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)]
        selected = symptom in st.session_state.selected_symptoms
        style = f"background-color:{color}; border:{'3px solid #000' if selected else '1px solid #000'}; border-radius:15px; padding:10px 15px; margin:5px;"
        if cols[i % 4].button(symptom, key=f"symptom_{i}", help="Click to toggle symptom"):
            if selected:
                st.session_state.selected_symptoms.remove(symptom)
            else:
                st.session_state.selected_symptoms.append(symptom)

    if st.session_state.selected_symptoms:
        st.markdown("**Selected Symptoms:** " + ", ".join(st.session_state.selected_symptoms))

    other_symptoms = st.text_input("Other Symptoms (optional)")
    if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(other_symptoms)

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
            "what_helped": what_helped
        }
        logs.append(new_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
        st.success("Log added!")
        st.session_state.selected_symptoms.clear()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Daily Checklist ---
with st.expander("Daily Checklist"):
    st.markdown(f"<div style='background-color:{EXPANDER_COLORS['Daily Checklist']}; border-radius:15px; padding:15px;'>", unsafe_allow_html=True)
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
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
        st.success("Checklist saved!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Trends ---
with st.expander("Trends"):
    st.markdown(f"<div style='background-color:{EXPANDER_COLORS['Trends']}; border-radius:15px; padding:15px;'>", unsafe_allow_html=True)
    if logs:
        df = pd.DataFrame(logs)
        trend_cols = ["heart_rate", "hydration", "severity"]
        for col in trend_cols:
            if col not in df.columns:
                df[col] = None
        df_chart = df[["timestamp"] + trend_cols].copy()
        df_chart['timestamp'] = pd.to_datetime(df_chart['timestamp'])
        df_chart = df_chart.set_index('timestamp')
        st.line_chart(df_chart)
    else:
        st.info("No data to show trends yet.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Notes ---
with st.expander("Notes"):
    st.markdown(f"<div style='background-color:{EXPANDER_COLORS['Notes']}; border-radius:15px; padding:15px;'>", unsafe_allow_html=True)
    note_text = st.text_area("Add a note")
    uploaded_file = st.file_uploader("Attach photo (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Save Note", key="note_btn"):
        note_entry = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "note": note_text}
        if uploaded_file:
            path = UPLOAD_DIR / uploaded_file.name
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            note_entry["image"] = str(path)
        logs.append(note_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
        st.success("Note saved!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Doctor Export ---
with st.expander("Doctor Export"):
    st.markdown(f"<div style='background-color:{EXPANDER_COLORS['Doctor Export']}; border-radius:15px; padding:15px;'>", unsafe_allow_html=True)
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Generate PDF", key="pdf_btn"):
        filtered_logs = [log for log in logs if 'timestamp' in log and start_date <= pd.to_datetime(log['timestamp']).date() <= end_date]
        if filtered_logs:
            pdf_file = BytesIO()
            with PdfPages(pdf_file) as pdf:
                for log in filtered_logs:
                    plt.figure(figsize=(6, 2))
                    plt.text(0.5, 0.5, str(log), fontsize=12)
                    plt.axis('off')
                    pdf.savefig()
                    plt.close()
            pdf_file.seek(0)
            st.download_button("Download PDF", data=pdf_file, file_name="Tilt_export.pdf")
        else:
            st.info("No logs in selected date range.")
    st.markdown("</div>", unsafe_allow_html=True)
