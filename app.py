import streamlit as st
from datetime import datetime

SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]

# --- Session state ---
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "selected_triggers" not in st.session_state:
    st.session_state.selected_triggers = []

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
    color:black;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Quick Log")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
heart_rate = st.number_input("Heart Rate", 40, 200, 70)
blood_pressure = st.text_input("Blood Pressure (optional)")
severity = st.slider("Severity (1-10)", 1, 10, 5)

# --- Symptoms ---
st.markdown("**Symptoms:**")
cols = st.columns(4)
for i, symptom in enumerate(SYMPTOMS):
    col = cols[i % 4]
    selected = symptom in st.session_state.selected_symptoms
    color = "#FFD6E0" if not selected else "#8B5CF6"
    checked = col.checkbox(symptom, value=selected, key=f"symptom_{i}")
    if checked and symptom not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(symptom)
    elif not checked and symptom in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom)

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers ---
st.markdown("**Possible Triggers:**")
cols = st.columns(3)
for i, trigger in enumerate(TRIGGERS):
    col = cols[i % 3]
    selected = trigger in st.session_state.selected_triggers
    color = "#B0E0FF" if not selected else "#1D4ED8"
    checked = col.checkbox(trigger, value=selected, key=f"trigger_{i}")
    if checked and trigger not in st.session_state.selected_triggers:
        st.session_state.selected_triggers.append(trigger)
    elif not checked and trigger in st.session_state.selected_triggers:
        st.session_state.selected_triggers.remove(trigger)

what_helped = st.text_area("What Helped?")

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
