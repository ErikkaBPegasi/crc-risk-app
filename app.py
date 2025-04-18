import streamlit as st
from datetime import datetime

# Helper functions
def calculate_age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

# App layout
st.title("Evaluación de Riesgo para Tamizaje de Cáncer Colorrectal")
st.markdown("""
Esta herramienta te ayuda a evaluar tu riesgo para cáncer colorrectal basado en recomendaciones actuales.
Por favor completa los siguientes datos:
""")

# Input fields
dob = st.date_input("Fecha de nacimiento")
height_cm = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
weight_kg = st.number_input("Peso (kg)", min_value=30, max_value=200, step=1)

ibd = st.checkbox("¿Tienes enfermedad inflamatoria intestinal (Crohn o colitis ulcerativa)?")
family_crc = st.checkbox("¿Tienes un familiar de primer grado con cáncer colorrectal?")
hereditary_syndrome = st.checkbox("¿Tienes un síndrome hereditario conocido como el síndrome de Lynch?")
family_before_60 = st.checkbox("¿Ese familiar fue diagnosticado antes de los 60 años?")

# Output results
if dob and height_cm and weight_kg:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)

    st.markdown(f"**Edad**: {age} años")
    st.markdown(f"**Índice de Masa Corporal (IMC)**: {bmi}")

    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    if ibd:
        st.warning("Riesgo alto: Se recomienda colonoscopia cada 1-2 años con vigilancia endoscópica especializada.")
    elif hereditary_syndrome:
        st.warning("Riesgo alto: Iniciar colonoscopia a los 20-25 años o antes según antecedentes familiares.")
    elif family_crc and family_before_60:
        st.info("Riesgo moderado: Iniciar colonoscopia a los 40 años o 10 años antes del diagnóstico familiar, cada 5 años.")
    elif family_crc:
        st.info("Riesgo Incrementado: Colonoscopia periódica segun evaluacion medica.")
