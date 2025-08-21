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

# --- Symptoms Multiselect ---
st.markdown("**Symptoms:**")
symptoms_display = [f"{SYMPTOM_EMOJIS[i]} {symptom}" for i, symptom in enumerate(SYMPTOMS)]

# Multiselect — no default needed here
selected_symptoms = st.multiselect(
    "Select symptoms",
    options=symptoms_display
)

# Save clean symptom names without emojis
st.session_state.selected_symptoms = [s.split(" ", 1)[1] for s in selected_symptoms]

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers Multiselect ---
st.markdown("**Possible Triggers:**")
triggers_display = [f"{TRIGGER_EMOJIS[i]} {trigger}" for i, trigger in enumerate(TRIGGERS)]
selected_triggers = st.multiselect(
    "Select triggers",
    options=triggers_display
)
st.session_state.selected_triggers = [t.split(" ", 1)[1] for t in selected_triggers]
