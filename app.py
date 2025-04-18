import streamlit as st
from datetime import datetime

# Helper functions
def calculate_age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

# Layout
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
height_cm = None; weight_kg = None
if height_str:
    try: height_cm = float(height_str)
    except: st.error("Altura no válida")
if weight_str:
    try: weight_kg = float(weight_str)
    except: st.error("Peso no válido")

# Risk questions
ibd = st.checkbox("Enfermedad inflamatoria intestinal (Crohn o colitis ulcerativa)")
family_crc = st.checkbox("Familiar 1° grado con cáncer colorrectal")
hered = st.checkbox("Síndrome hereditario (Lynch)")
advanced_adenoma = st.checkbox("Antecedente de adenomas avanzados")
fap = st.checkbox("Poliposis adenomatosa familiar (PAF)")
serrated = st.checkbox("Poliposis serrada o múltiple")
other_syndromes = st.checkbox("Otros síndromes genéticos (Peutz-Jeghers, Cowden, etc.)")
polyp10 = st.checkbox("Pólipo detectado en últimos 10 años")
symptoms = st.checkbox("Síntomas (sangrado, cambio de hábito, pérdida de peso)")

# Compute
if dob and height_cm and weight_kg:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad**: {age} años | **IMC**: {bmi}")
    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    # Invalid age
    if age <= 0:
        st.error("Fecha inválida")
        st.stop()

    # Branches
    # 1. High-risk hereditary/inflammatory
    if hered or ibd or fap or serrated or other_syndromes:
        st.warning("**Riesgo Incrementado**: factores hereditarios o EII detectados.")
        st.markdown(
            """
            Estrategia de tamizaje para riesgo incrementado:
            - Colonoscopia cada 1–2 años (Lynch) o cada 1–5 años (EII) según genotipo y duración.
            - Colonoscopia cada 5 años si PAF/PAFA o poliposis múltiple.
            - Considerar TSOMFi anual o TSOMFg bienal si colonoscopia no disponible.
            """
        )
    # 2. Family CRC w/o genetic syndrome
    elif family_crc:
        st.info("**Antecedente Familiar**: familiar 1° grado con CCR.")
        st.markdown(
            """
            Estrategia de tamizaje para riesgo familiar:
            - Iniciar colonoscopia a los 40 años o 10 años antes que diagnóstico del familiar.
            - Repetir cada 5 años.
            - TSOMFi anual o TSOMFg bienal como alternativa.
            """
        )
    # 3. Advanced adenoma history
    elif advanced_adenoma or polyp10:
        st.info("**Historial de Pólipos/Adenomas** detectados.")
        st.markdown(
            """
            Estrategia de tamizaje post-adenoma:
            - Colonoscopia de control en 3 años (adenomas avanzados).
            - TSOMFi anual o TSOMFg bienal entre colonoscopias.
            """
        )
    # 4. Symptoms
    elif symptoms:
        st.warning("**Síntomas** presentes, requiere evaluación médica inmediata.")
    # 5. Average risk age <50
    elif age < 50:
        st.info("No se recomienda tamizaje antes de 50 años sin otros factores de riesgo.")
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
        st.markdown("**Nota:** IMC elevado, factor de riesgo adicional.")
