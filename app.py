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

# --- CSS for pastel theme and fonts ---
st.markdown("""
<style>
/* Section background colors */
.quicklog-section { background-color: #F8E1F4; padding: 16px; border-radius: 12px; margin-bottom: 16px; }
.dailycheck-section { background-color: #E1F0F8; padding: 16px; border-radius: 12px; margin-bottom: 16px; }
.trends-section { background-color: #E8E1F8; padding: 16px; border-radius: 12px; margin-bottom: 16px; }

/* Multiselect pastel background */
div[data-baseweb="select"] > div { background-color: #FDE1F8 !important; border-radius: 12px; }

/* Text input / text area pastel background */
input, textarea { background-color: #E1F0F8 !important; border-radius: 8px; color: black; }

/* Slider track pastel */
.css-1f7k2ku .stSlider>div>div>div { background-color: #E8E1F8 !important; }

/* Headers */
.section-header { font-family: 'Comic Neue', cursive; font-weight: bold; font-size: 24px; color: black; padding: 8px; }
.subtext { font-family: 'Comic Neue', cursive; font-size: 16px; color: black; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# --- Quick Log Section ---
st.markdown('<div class="quicklog-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Quick Log</div>', unsafe_allow_html=True)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
posture = st.selectbox("Posture", ["Sitting", "Standing", "Lying"])
heart_rate = st.number_input("Heart Rate", 40, 200, 70)
blood_pressure = st.text_input("Blood Pressure (optional)")
severity = st.slider("Severity (1-10)", 1, 10, 5)

# --- Symptoms ---
st.markdown('<div class="subtext">Symptoms:</div>', unsafe_allow_html=True)
symptoms_display = [f"{SYMPTOM_EMOJIS[i]} {symptom}" for i, symptom in enumerate(SYMPTOMS)]
selected_symptoms = st.multiselect("Select symptoms", options=symptoms_display)
st.session_state.selected_symptoms = [s.split(" ", 1)[1] for s in selected_symptoms]

other_symptoms = st.text_input("Other Symptoms (optional)")
if other_symptoms:
    st.session_state.selected_symptoms.append(other_symptoms)

# --- Triggers ---
st.markdown('<div class="subtext">Possible Triggers:</div>', unsafe_allow_html=True)
triggers_display = [f"{TRIGGER_EMOJIS[i]} {trigger}" for i, trigger in enumerate(TRIGGERS)]
selected_triggers = st.multiselect("Select triggers", options=triggers_display)
st.session_state.selected_triggers = [t.split(" ", 1)[1] for t in selected_triggers]

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
    st.write(new_entry)  # replace with storage later
    st.session_state.selected_symptoms.clear()
    st.session_state.selected_triggers.clear()

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)


