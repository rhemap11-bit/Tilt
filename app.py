import streamlit as st
from datetime import datetime
from streamlit_pills import pills


# --- Data ---
SYMPTOMS = ["Dizziness","Heart Palpitations","Fatigue","Nausea",
            "Brain Fog","Headache","Sweating","Tremors"]
TRIGGERS = ["Standing long","Heat","Stress","Lack of sleep","Dehydration","Salt restriction"]
SYMPTOM_COLORS = ["#FFD6E0","#E5D4FF","#D4EAFF","#FFF3B0","#D4FFEA","#FFB3C6","#B0E0FF","#FFD6A5"]
TRIGGER_COLORS = ["#B0E0FF","#D4FFEA","#FFD6A5","#FFF3B0","#E5D4FF","#FFD6E0"]

# --- Session state ---
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "selected_triggers" not in st.session_state:
    st.session_state.selected_triggers = []

# --- CSS for pills ---
st.markdown("""
<style>
.pill-checkbox {
    display:none;
}
.pill-label {
    display:inline-block;
    border-radius:20px;
    padding:8px 16px;
    margin:4px;
    font-weight:500;
    cursor:pointer;
    user-select:none;
    text-align:center;
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
cols = st.columns(4)
for i, symptom in enumerate(SYMPTOMS):
    col = cols[i % 4]
    selected = symptom in st.session_state.selected_symptoms
    color = "#8B5CF6" if selected else SYMPTOM_COLORS[i % len(SYMPTOM_COLORS)]
    checked = col.checkbox("", value=selected, key=f"symptom_{i}", help=symptom)
    if checked and symptom not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(symptom)
    elif not checked and symptom in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom)
    # draw styled pill
    col.markdown(f"<span class='pill-label' style='background-color:{color}'>{symptom}</span>", unsafe_allow_html=True)

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms and other_symptoms not in st.session_state.selected_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers as toggleable pills ---
st.markdown("**Possible Triggers:**")
cols = st.columns(3)
for i, trigger in enumerate(TRIGGERS):
    col = cols[i % 3]
    selected = trigger in st.session_state.selected_triggers
    color = "#1D4ED8" if selected else TRIGGER_COLORS[i % len(TRIGGER_COLORS)]
    checked = col.checkbox("", value=selected, key=f"trigger_{i}", help=trigger)
    if checked and trigger not in st.session_state.selected_triggers:
        st.session_state.selected_triggers.append(trigger)
    elif not checked and trigger in st.session_state.selected_triggers:
        st.session_state.selected_triggers.remove(trigger)
    col.markdown(f"<span class='pill-label' style='background-color:{color}'>{trigger}</span>", unsafe_allow_html=True)

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
    st.session_state.selected_symptoms.clear()
    st.session_state.selected_triggers.clear()


