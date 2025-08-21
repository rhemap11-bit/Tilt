import streamlit as st
from datetime import datetime

# --- Data ---
SYMPTOMS = ["Dizziness", "Heart Palpitations", "Fatigue", "Nausea",
            "Brain Fog", "Headache", "Sweating", "Tremors"]
TRIGGERS = ["Standing long", "Heat", "Stress", "Lack of sleep", "Dehydration", "Salt restriction"]

SYMPTOM_COLORS = ["🟪", "🟩", "🟦", "🟧", "🟨", "🟫", "🟩", "🟦"]  # just using emoji blocks for fun pastel look
TRIGGER_COLORS = ["🟦", "🟩", "🟧", "🟨", "🟪", "🟫"]

st.subheader("Quick Log")

# --- Basic Inputs ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
heart_rate = st.number_input("Heart Rate", 40, 200, 70)
blood_pressure = st.text_input("Blood Pressure (optional)")
severity = st.slider("Severity (1-10)", 1, 10, 5)

# --- Symptoms Multiselect ---
st.markdown("**Symptoms:**")
symptoms_with_colors = [f"{SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)]} {symptom}" for i, symptom in enumerate(SYMPTOMS)]
selected_symptoms = st.multiselect("Select symptoms", options=symptoms_with_colors)
selected_symptoms_clean = [s.split(" ", 1)[1] for s in selected_symptoms]  # remove emoji for storage

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms:
    selected_symptoms_clean.append(other_symptoms)

# --- Triggers Multiselect ---
st.markdown("**Possible Triggers:**")
triggers_with_colors = [f"{TRIGGER_COLORS[i % len(TRIGGER_COLORS)]} {trigger}" for i, trigger in enumerate(TRIGGERS)]
selected_triggers = st.multiselect("Select triggers", options=triggers_with_colors)
selected_triggers_clean = [t.split(" ", 1)[1] for t in selected_triggers]

# --- What Helped ---
what_helped = st.text_area("What Helped?")

# --- Save Entry ---
if st.button("Save Quick Log Entry"):
    new_entry = {
        "timestamp": timestamp,
        "posture": posture,
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "severity": severity,
        "symptoms": selected_symptoms_clean,
        "triggers": selected_triggers_clean,
        "what_helped": what_helped
    }
    st.success("Quick Log saved!")
    st.write(new_entry)  # for demonstration; replace with storage later



