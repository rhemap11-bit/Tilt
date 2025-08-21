import streamlit as st
from datetime import datetime

# --- Sample data ---
SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]
SYMPTOM_COLORS = ["#FFD6E0","#E5D4FF","#D4EAFF","#FFF3B0","#D4FFEA","#FFB3C6","#B0E0FF","#FFD6A5"]

# --- Initialize session state ---
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []

if "selected_triggers" not in st.session_state:
    st.session_state.selected_triggers = []

# --- Quick Log Section ---
st.markdown("""
<style>
.pill {
    display:inline-block;
    border-radius:20px;
    padding:8px 16px;
    margin:4px;
    cursor:pointer;
    font-weight:500;
    user-select:none;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Quick Log")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
heart_rate = st.number_input("Heart Rate", 40, 200, 70)
blood_pressure = st.text_input("Blood Pressure (optional)")
severity = st.slider("Severity (1-10)", 1, 10, 5)

# --- Symptoms as toggleable pills ---
st.markdown("**Symptoms:**")
for i, symptom in enumerate(SYMPTOMS):
    color = SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)]
    if symptom in st.session_state.selected_symptoms:
        color = "#8B5CF6"  # darker when selected
    pill_html = f"""
    <span class='pill' style='background-color:{color}' 
        onclick="document.getElementById('{symptom}').click()">{symptom}</span>
    <input type="checkbox" id="{symptom}" style="display:none;" 
        {'checked' if symptom in st.session_state.selected_symptoms else ''}>
    """
    clicked = st.markdown(pill_html, unsafe_allow_html=True)
    # Using st.checkbox hidden to store state
    if st.checkbox("", key=f"hidden_symptom_{i}", value=(symptom in st.session_state.selected_symptoms)):
        if symptom not in st.session_state.selected_symptoms:
            st.session_state.selected_symptoms.append(symptom)
    else:
        if symptom in st.session_state.selected_symptoms:
            st.session_state.selected_symptoms.remove(symptom)

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers as toggleable pills ---
st.markdown("**Possible Triggers:**")
for i, trigger in enumerate(TRIGGERS):
    color = "#B0E0FF"  # pastel default
    if trigger in st.session_state.selected_triggers:
        color = "#1D4ED8"  # darker when selected
    pill_html = f"""
    <span class='pill' style='background-color:{color}' 
        onclick="document.getElementById('trig_{i}').click()">{trigger}</span>
    <input type="checkbox" id="trig_{i}" style="display:none;" 
        {'checked' if trigger in st.session_state.selected_triggers else ''}>
    """
    clicked = st.markdown(pill_html, unsafe_allow_html=True)
    if st.checkbox("", key=f"hidden_trigger_{i}", value=(trigger in st.session_state.selected_triggers)):
        if trigger not in st.session_state.selected_triggers:
            st.session_state.selected_triggers.append(trigger)
    else:
        if trigger in st.session_state.selected_triggers:
            st.session_state.selected_triggers.remove(trigger)

what_helped = st.text_area("What Helped?")

# --- Quick Log Save Button ---
if st.button("Save Quick Log Entry"):
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
    st.success("Quick Log saved!")
    st.session_state.selected_symptoms.clear()
    st.session_state.selected_triggers.clear()

# --- Daily Checklist ---
with st.expander("Daily Checklist"):
    st.markdown(f"<div class='section-box' style='background-color:{SECTION_COLORS['Daily Checklist']};'></div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='section-box' style='background-color:{SECTION_COLORS['Trends']};'></div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='section-box' style='background-color:{SECTION_COLORS['Notes']};'></div>", unsafe_allow_html=True)
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
    st.markdown(f"<div class='section-box' style='background-color:{SECTION_COLORS['Doctor Export']};'></div>", unsafe_allow_html=True)
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


