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
    Esta herramienta evalúa tu perfil de riesgo según las Guías Argentinas de tamizaje.
    Contesta las preguntas para recibir la estrategia de tamizaje recomendada.
    """
)

# Inputs
dob = st.date_input(
    "Fecha de nacimiento", min_value=datetime(1900,1,1), max_value=datetime.today()
)
height_str = st.text_input("Altura (cm)", value="")
weight_str = st.text_input("Peso (kg)", value="")

# Parse height & weight
height_cm = None
weight_kg = None
if height_str:
    try:
        height_cm = float(height_str)
    except ValueError:
        st.error("Altura no válida")
if weight_str:
    try:
        weight_kg = float(weight_str)
    except ValueError:
        st.error("Peso no válido")

# Risk factor checkboxes
ibd = st.checkbox("Inflamación crónica del intestino (Crohn o colitis)")
family_crc = st.checkbox("Familiar cercano con cáncer de colon o recto")
hered = st.checkbox("Síndrome hereditario de riesgo (p.ej. Lynch)")
advanced_adenoma = st.checkbox("Adenomas avanzados previamente detectados")
fap = st.checkbox("Poliposis adenomatosa familiar (PAF)")
polyp10 = st.checkbox("¿Te han encontrado un pólipo en el colon o recto en los últimos 10 años?")

# Only show serrated if a polyp was found
tmp_serrated = False
if polyp10:
    tmp_serrated = st.checkbox("¿Te han dicho que esos pólipos son de tipo serrado o múltiples?")

# Symptom check
symptoms = st.checkbox(
    "Has tenido sangre en las heces, cambios en el hábito intestinal o pérdida de peso sin explicación?"
)

# Compute outputs
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad**: {age} años | **IMC**: {bmi}")
    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    # Validate age
    if age <= 0:
        st.error("Selecciona una fecha anterior a hoy.")
        st.stop()

    # 1. High-risk hereditary or IBD
    if hered or ibd or fap:
        st.warning("**Riesgo Incrementado – Hereditario/EII**")
        st.markdown(
            """
            - Colonoscopia: cada 1–2 años (Lynch) o cada 1–5 años (EII).
            - Si no es posible: TSOMFi anual o TSOMFg bienal.
            """
        )

    # 2. Family CRC (non-syndromic)
    elif family_crc:
        st.info("**Riesgo Incrementado – Familiar**")
        st.markdown(
            """
            - Colonoscopia: iniciar a los 40 años o 10 años antes del familiar más joven.
            - Repetir cada 5 años.
            - Alternativa: TSOMFi anual o TSOMFg bienal.
            """
        )

    # 3. Post-polyp detection
    elif polyp10:
        # Further classify by serrated
        if tmp_serrated:
            st.warning("**Riesgo Incrementado – Poliposis Serrada**")
            st.markdown(
                """
                - Colonoscopia de vigilancia cada 3–5 años.
                - Evaluación genética si es necesario.
                """
            )
        else:
            st.info("**Historial de Pólipos**")
            st.markdown(
                """
                - Colonoscopia de control en 3 años.
                - Entre controles: TSOMFi anual o TSOMFg bienal.
                """
            )

    # 4. Symptoms
    elif symptoms:
        st.warning("**Síntomas presentes**: requiere evaluación médica inmediata.")

    # 5. Average risk under 50
    elif age < 50:
        st.info("No se recomienda tamizaje si tienes menos de 50 años sin otros factores de riesgo.")

    # 6. Average risk 50–75
    elif age <= 75:
        st.success("**Riesgo Promedio**: 50–75 años sin factores adicionales.")
        st.markdown(
            """
            Opciones de tamizaje:
            - TSOMFi cada 2 años
            - TSOMFg cada 2 años
            - Rectosigmoidoscopía cada 5 años
            - Colonoscopia cada 10 años
            """
        )

    # 7. Over 75
    else:
        st.warning("No se recomienda tamizaje programático >75 años sin evaluación individual.")

    # BMI note
    if bmi >= 25:
        st.markdown("**Nota:** Tu IMC es elevado, factor de riesgo adicional.")
