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
Esta herramienta te ayuda a evaluar tu riesgo para cáncer colorrectal basado en las recomendaciones vigentes en Argentina.
Dirigida a personas de riesgo promedio, sin antecedentes personales ni familiares de CCR o síndromes hereditarios conocidos.
""")

# Input fields
# Allow dates back to 1900-01-01 to accommodate older birth dates
dob = st.date_input(
    "Fecha de nacimiento",
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today()
)
height_cm = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
weight_kg = st.number_input("Peso (kg)", min_value=30, max_value=200, step=1)

# Risk factor checkboxes
ibd = st.checkbox("¿Tienes enfermedad inflamatoria intestinal (Crohn o colitis ulcerativa)?")
family_crc = st.checkbox("¿Tienes un familiar de primer grado con cáncer colorrectal?")
hereditary_syndrome = st.checkbox("¿Tienes un síndrome hereditario conocido como el síndrome de Lynch?")
family_before_60 = st.checkbox("¿Ese familiar fue diagnosticado antes de los 60 años?")
polyp_checkbox = st.checkbox("¿Te han dicho en los últimos 10 años que tenías un pólipo en el colon o recto? (Un pólipo es un pequeño crecimiento que se desarrolla en el interior del colon o recto.)")
advanced_adenoma = st.checkbox("¿Te han extirpado previamente pólipos o adenomas avanzados?")
fap = st.checkbox("¿Tienes diagnóstico de poliposis adenomatosa familiar (PAF)?")
serrated_polyps = st.checkbox("¿Te han diagnosticado poliposis serrada o pólipos múltiples?")
other_hereditary = st.checkbox("¿Tienes antecedentes familiares de otros síndromes genéticos (Peutz-Jeghers, Cowden, etc.)?")
symptoms = st.checkbox("¿Tienes síntomas como sangrado rectal, cambios recientes en el hábito intestinal, o pérdida de peso sin causa conocida?")

# Output results
if dob and height_cm and weight_kg:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)

    st.markdown(f"**Edad**: {age} años")
    st.markdown(f"**Índice de Masa Corporal (IMC)**: {bmi}")

    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    # Validate date of birth before other checks
    if age <= 0:
        st.error("Fecha de nacimiento inválida. Por favor selecciona una fecha anterior a hoy.")
        st.stop()

    # High-risk exclusions
    if ibd or hereditary_syndrome or family_crc or advanced_adenoma or fap or serrated_polyps or other_hereditary:
        st.warning("Tu perfil indica un riesgo elevado. Se recomienda derivación a consulta médica especializada para seguimiento individualizado.")
    elif polyp_checkbox:
        st.info("Historial de pólipos: Consulta médica recomendada para evaluación personalizada y posible colonoscopia.")
    elif symptoms:
        st.warning("Síntomas presentes: Se recomienda evaluación médica inmediata para descartar patología activa.")
    elif age < 50:
        st.info("Actualmente no se recomienda tamizaje si tienes menos de 50 años y no presentas factores de riesgo adicionales.")
    elif age <= 75:
        st.success("Riesgo promedio: Iniciar tamizaje con test de sangre oculta en materia fecal inmunoquímico (TSOMFi) cada 2 años o colonoscopia cada 10 años.")
    else:
        st.warning("No se recomienda tamizaje programático en mayores de 75 años, salvo evaluación médica individualizada.")

    # Additional note
    if bmi >= 25:
        st.markdown("**Nota:** Tu IMC sugiere sobrepeso, lo cual puede ser un factor de riesgo adicional para cáncer colorrectal.")

