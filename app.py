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
