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
st.markdown(
    """
    Esta herramienta te ayuda a evaluar tu riesgo para cáncer colorrectal basado en las recomendaciones vigentes en Argentina.
    Dirigida a personas de riesgo promedio, sin antecedentes personales ni familiares de CCR o síndromes hereditarios conocidos.
    """
)

# Input fields
dob = st.date_input(
    "Fecha de nacimiento",
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today()
)

height_str = st.text_input("Altura (cm)", value="")
weight_str = st.text_input("Peso (kg)", value="")

# Parse height and weight
height_cm = None
weight_kg = None
if height_str:
    try:
        height_cm = float(height_str)
    except ValueError:
        st.error("Por favor ingresa un número válido para la altura.")
if weight_str:
    try:
        weight_kg = float(weight_str)
    except ValueError:
        st.error("Por favor ingresa un número válido para el peso.")

# Risk factor checkboxes
ibd = st.checkbox("¿Tienes enfermedad inflamatoria intestinal (Crohn o colitis ulcerativa)?")
family_crc = st.checkbox("¿Tienes un familiar de primer grado con cáncer colorrectal?")
hereditary_syndrome = st.checkbox("¿Tienes un síndrome hereditario conocido como el síndrome de Lynch?")
advanced_adenoma = st.checkbox("¿Te han extirpado previamente pólipos o adenomas avanzados?")
fap = st.checkbox("¿Tienes diagnóstico de poliposis adenomatosa familiar (PAF)?")
serrated_polyps = st.checkbox("¿Te han diagnosticado poliposis serrada o pólipos múltiples?")
other_hereditary = st.checkbox("¿Tienes antecedentes familiares de otros síndromes genéticos (Peutz-Jeghers, Cowden, etc.)?")
polyp_checkbox = st.checkbox("¿Te han dicho en los últimos 10 años que tenías un pólipo en el colon o recto? (Un pólipo es un pequeño crecimiento en el colon o recto.)")
symptoms = st.checkbox("¿Tienes síntomas como sangrado rectal, cambios recientes en el hábito intestinal, o pérdida de peso sin causa conocida?")

# Compute outputs
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)

    st.markdown(f"**Edad**: {age} años")
    st.markdown(f"**Índice de Masa Corporal (IMC)**: {bmi}")
    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    # Validate logical age
    if age <= 0:
        st.error("Fecha de nacimiento inválida. Selecciona una fecha anterior a hoy.")
        st.stop()

    # Risk stratification
    if any([ibd, hereditary_syndrome, family_crc, advanced_adenoma, fap, serrated_polyps, other_hereditary]):
        st.warning(
            "**Riesgo incrementado**: Antecedentes personales o familiares fuertes (CCR, Lynch, PAF/PAFA, poliposis hamartomatosa o serrada, EII)."
            " Se recomienda derivación a consulta médica especializada."
        )
        # Estrategia de tamizaje para riesgo incrementado
        st.markdown(
            """
            Estrategia de tamizaje recomendada para riesgo incrementado:
            - Colonoscopia cada 5 años, iniciando a los 40 años o 10 años antes de la edad del caso familiar más joven.
            - Para EII: colonoscopia de vigilancia según función de riesgo (entre 1-5 años).
            - En caso de sospecha de síndrome hereditario (Lynch): colonoscopia cada 1-2 años a partir de los 20-30 años según gen.
            """
        )
    elif polyp_checkbox:
        st.info("**Historial de pólipos**: Consulta médica y posible colonoscopia.")
    elif symptoms:
        st.warning("**Síntomas presentes**: Evaluación médica inmediata.")
    elif age < 50:
        st.info("No se recomienda tamizaje si tienes menos de 50 años sin factores de riesgo adicionales.")
    elif age <= 75:
        st.success("**Riesgo promedio**: Personas de 50–75 años sin antecedentes ni factores de riesgo fuertes.")
        st.markdown(
            """
            Opciones de tamizaje recomendadas:
            - Test de sangre oculta en materia fecal inmunoquímico (TSOMFi)
            - Test de sangre oculta en materia fecal con guayaco (TSOMFg)
            - Rectosigmoidoscopía flexible (RSC)
            - Videocolonoscopía (VCC)
            """
        )
    else:
        st.warning("No se recomienda tamizaje programático en mayores de 75 años salvo evaluación individualizada.")

    # BMI note
    if bmi >= 25:
        st.markdown("**Nota:** Tu IMC sugiere sobrepeso, un factor de riesgo adicional para CCR.")
