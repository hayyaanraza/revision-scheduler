import streamlit as st
import json
from datetime import datetime, timedelta

# Define file path for storing data
DATA_FILE = "study_log.json"

# Define chapter data by subject with hours
chapters = {
    "Physics": [
        {"name": "Mathematical Tools", "hours": 13},
        {"name": "Rectilinear motion", "hours": 8.5},
        {"name": "Projectile motion", "hours": 5.5},
        {"name": "Relative motion", "hours": 7},
        {"name": "Geometrical Optics and Ray Optics", "hours": 25},
        {"name": "Optical instruments", "hours": 5},
        {"name": "Newton's laws of motion", "hours": 11},
        {"name": "Friction", "hours": 5},
        {"name": "Work, Power and Energy", "hours": 10.5},
        {"name": "Circular motion", "hours": 10.5},
        {"name": "Center of mass", "hours": 12.5},
        {"name": "Rotational dynamics", "hours": 20},
        {"name": "Simple harmonic motion", "hours": 12},
        {"name": "Electrostatics", "hours": 28},
        {"name": "Conductors (Electrostatics)", "hours": 6.5},
        {"name": "Gravitation", "hours": 7.5},
        {"name": "Current electricity", "hours": 14},
        {"name": "Heat transfer", "hours": 8},
        {"name": "Capacitor/Capacitance", "hours": 12.5},
        {"name": "Electromagnetic forces", "hours": 11},
        {"name": "Magnetic effect of current", "hours": 10},
        {"name": "Magnetic properties of matter", "hours": 5.5},
        {"name": "Electromagnetic Induction", "hours": 17.5},
        {"name": "Alternating current", "hours": 7.5},
        {"name": "Electromagnetic waves", "hours": 5},
        {"name": "Bohr's model Atom St. Modern Phy-1", "hours": 8},
        {"name": "Photoelectric Effect", "hours": 7.5},
        {"name": "X ray Modern physics", "hours": 4},
        {"name": "Nuclear Physics", "hours": 10.5},
        {"name": "Wave on string", "hours": 13.5},
        {"name": "Sound waves", "hours": 15.5},
        {"name": "Wave Optics", "hours": 13.5},
        {"name": "Thermodynamics", "hours": 7.5},
        {"name": "Kinetic theory of gases", "hours": 4.5},
        {"name": "Calorimetry", "hours": 3},
        {"name": "Thermal expansion", "hours": 3.5},
        {"name": "Fluid mechanics", "hours": 12},
        {"name": "Viscosity", "hours": 2.5},
        {"name": "Elasticity Properties of solids", "hours": 3.5},
        {"name": "Surface tension", "hours": 4.5},
        {"name": "Semiconductors", "hours": 11},
        {"name": "Communication system", "hours": 3},
        {"name": "Error and measurement", "hours": 7.5},
    ],
    "Chemistry": [
        {"name": "Mole Concept", "hours": 6},
        {"name": "Atomic Structure", "hours": 14.5},
        {"name": "Gaseous State", "hours": 10.5},
        {"name": "Periodic Table", "hours": 7.5},
        {"name": "Chemical Bonding", "hours": 24},
        {"name": "Basic Inorganic Nomenclature", "hours": 1},
        {"name": "GIC", "hours": 4},
        {"name": "Hydrogen", "hours": 2},
        {"name": "Chemical Equilibrium", "hours": 5},
        {"name": "Ionic Equilibrium", "hours": 11.5},
        {"name": "Coordination Compounds", "hours": 13},
        {"name": "Electrochemistry", "hours": 12.5},
        {"name": "Metallurgy", "hours": 7.5},
        {"name": "Qualitative Analysis", "hours": 8},
        {"name": "Qualitative Analysis (Cation)", "hours": 4.5},
        {"name": "p Block (n& O family)", "hours": 7.5},
        {"name": "p Block (Group 17, 18)", "hours": 3},
        {"name": "Chemical Kinetics", "hours": 9.5},
        {"name": "Liquid Solution", "hours": 7},
        {"name": "Surface Chemistry", "hours": 5.5},
        {"name": "s Block Elements", "hours": 5},
        {"name": "Solid State", "hours": 8.5},
        {"name": "Thermodynamics", "hours": 10.5},
        {"name": "Thermochemistry", "hours": 4},
        {"name": "Redox Reaction and Equivalent Concept", "hours": 7},
        {"name": "The d and f Block Elements", "hours": 6.5},
        {"name": "The Boron and Carbon Family", "hours": 6},
        {"name": "Nuclear Chemistry", "hours": 3.5},
        {"name": "Miscellaneous concept", "hours": 1},
    ],
    "Maths": [
        {"name": "Sets", "hours": 3.5},
        {"name": "Fundamental of Maths", "hours": 6},
        {"name": "Ratio and Identities", "hours": 12.5},
        {"name": "Trigonometric Equation", "hours": 3},
        {"name": "Logarithm", "hours": 4},
        {"name": "Quadratic Equations", "hours": 12},
        {"name": "Function", "hours": 35},
        {"name": "Inverse Trigonometric Function", "hours": 4},
        {"name": "Progression and Series", "hours": 15},
        {"name": "Determinants", "hours": 4.5},
        {"name": "Matrices", "hours": 6},
        {"name": "Straight Lines", "hours": 14},
        {"name": "Circles", "hours": 12.5},
        {"name": "Limits", "hours": 17},
        {"name": "Continuity", "hours": 8},
        {"name": "Differentiability", "hours": 7.5},
        {"name": "Differentiation", "hours": 10},
        {"name": "Application of Derivatives", "hours": 22},
        {"name": "Parabola", "hours": 6},
        {"name": "Ellipse", "hours": 4.5},
        {"name": "Hyperbola", "hours": 3.5},
        {"name": "Indefinite Integration", "hours": 14.5},
        {"name": "Definite Integration", "hours": 14.5},
        {"name": "Area Under The Curves", "hours": 1.5},
        {"name": "Differential Equation", "hours": 3},
        {"name": "Vector and 3-D Geometry", "hours": 9.5},
        {"name": "Complex Number", "hours": 11},
        {"name": "Solution/Properties of Triangle", "hours": 4.5},
        {"name": "Binomial Theorem", "hours": 15},
        {"name": "Permutation and Combination", "hours": 11.5},
        {"name": "Probability", "hours": 6.5},
    ]
}

# Define revision intervals
revision_intervals = {"O": 1, "R1": 7, "R2": 11}

# Load study log data from file
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save study log data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, default=str)

# Initialize study log
study_log = load_data()

# Function to calculate the next revision date based on revision type
def calculate_next_revision(last_revision_date, revision_type):
    interval = revision_intervals.get(revision_type, 11)  # Default to 11 days for R2 and beyond
    return last_revision_date + timedelta(days=interval)

# Log a study session
def log_study(chapter, study_date, revision_type):
    study_date_str = study_date.isoformat()  # Save as ISO format string for consistency
    if chapter not in study_log:
        study_log[chapter] = {
            "last_revision_date": study_date_str,
            "revision_type": revision_type,
            "revision_count": 1
        }
    else:
        study_log[chapter]["last_revision_date"] = study_date_str
        study_log[chapter]["revision_type"] = revision_type
        study_log[chapter]["revision_count"] += 1
    save_data(study_log)

# Streamlit UI
st.title("JEE Study Log Tracker")

subject = st.selectbox("Select Subject", list(chapters.keys()))
chapter_list = chapters[subject]
chapter_names = [ch["name"] for ch in chapter_list]
chapter = st.selectbox("Select Chapter", chapter_names)

today_date = datetime.now().date()
study_date = st.date_input("Select Study Date", today_date)
revision_type = st.selectbox("Select Revision Type", ["O", "R1", "R2"])

if st.button("Log Study Session"):
    log_study(chapter, study_date, revision_type)
    st.success(f"Logged study session for {chapter} on {study_date} with revision type {revision_type}")

st.header("Study Log")
if study_log:
    for ch, log in study_log.items():
        last_revision_date = datetime.fromisoformat(log["last_revision_date"]).date()
        days_since_revision = (today_date - last_revision_date).days
        st.write(f"Chapter: {ch}")
        st.write(f"Last Studied: {last_revision_date} ({days_since_revision} days ago)")
        st.write(f"Revision Type: {log['revision_type']}")
        st.write(f"Revisions Done: {log['revision_count']}")
else:
    st.write("No study sessions logged yet.")

st.header("Suggested Chapters for Revision")
for ch, log in study_log.items():
    last_revision_date = datetime.fromisoformat(log["last_revision_date"]).date()
    revision_type = log["revision_type"]
    next_revision_date = calculate_next_revision(last_revision_date, revision_type)
    days_until_revision = (next_revision_date - today_date).days
    
    if days_until_revision <= 0:
        st.write(f"{ch} (Due for {revision_type} revision)")
