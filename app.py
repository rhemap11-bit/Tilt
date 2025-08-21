import streamlit as st
from datetime import datetime

# --- Data ---
SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
SYMPTOM_EMOJIS = ["🌀","❤️‍🔥","😴","🤢","🧠💭","🤕","💦","🤲"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]
TRIGGER_EMOJIS = ["🧍","🌞","😰","🛌","💧","🧂❌"]

# --- Session state ---
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "selected_triggers" not in st.session_state:
    st.session_state.selected_triggers = []

st.subheader("Quick Log")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
heart_rate = st.number_input("Heart Rate", 40, 200, 70)

# Use a pastel range for the slider
severity = st.slider("Severity (1-10)", 1, 10, 5, key="severity")

blood_pressure = st.text_input("Blood Pressure (optional)")

# --- Symptoms ---
st.markdown("**Symptoms:**")
symptoms_display = [f"{SYMPTOM_EMOJIS[i]} {symptom}" for i, symptom in enumerate(SYMPTOMS)]
selected_symptoms = st.multiselect(
    "Select symptoms",
    options=symptoms_display,
    default=[f"{SYMPTOM_EMOJIS[i]} {s}" for i,s in enumerate(st.session_state.selected_symptoms)]
)
st.session_state.selected_symptoms = [s.split(" ",1)[1] for s in selected_symptoms]

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers ---
st.markdown("**Possible Triggers:**")
triggers_display = [f"{TRIGGER_EMOJIS[i]} {trigger}" for i, trigger in enumerate(TRIGGERS)]
selected_triggers = st.multiselect(
    "Select triggers",
    options=triggers_display,
    default=[f"{TRIGGER_EMOJIS[i]} {t}" for i,t in enumerate(st.session_state.selected_triggers)]
)
st.session_state.selected_triggers = [t.split(" ",1)[1] for t in selected_triggers]

what_helped = st.text_area("What Helped?")

# --- Save Quick Log ---
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
    st.write(new_entry)
    st.session_state.selected_symptoms.clear()
    st.session_state.selected_triggers.clear()


