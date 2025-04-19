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
    "Esta herramienta evalúa tu perfil de riesgo según las Guías Argentinas de tamizaje. Contesta las preguntas para recibir la estrategia de tamizaje recomendada."
)

# Inputs
dob = st.date_input(
    "Fecha de nacimiento",
    value=None,
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today()
)
height_str = st.text_input(
    "Altura (cm)",
    value="",
    placeholder="ej. 170"
)
weight_str = st.text_input(
    "Peso (kg)",
    value="",
    placeholder="ej. 65"
)

# Parse numeric inputs
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

# Risk factors
ibd = st.checkbox("¿Te han dicho que tienes Crohn o colitis ulcerativa?")
hered = st.checkbox("¿Tienes un síndrome hereditario (por ejemplo, Lynch)?")
hamart = st.checkbox("¿Te diagnosticaron Peutz-Jeghers, Cowden u otro síndrome hamartomatoso?")
fap = st.checkbox("¿Tienes o tuviste poliposis adenomatosa familiar (PAF)?")

family_crc = st.checkbox("¿Algún familiar de primer grado tuvo cáncer colorrectal?")
family_before_60 = False
if family_crc:
    family_before_60 = st.checkbox("¿Fue diagnosticado antes de los 60 años?")

polyp10 = st.checkbox("¿Te encontraron algún pólipo en los últimos 10 años?")
tmp_advanced = False
tmp_serrated = False
if polyp10:
    tmp_advanced = st.checkbox("¿Ese pólipo fue grande o de alto riesgo?")
    tmp_serrated = st.checkbox("¿Era de tipo serrado?")

symptoms = st.checkbox("¿Tienes sangrado rectal, cambios en el hábito intestinal o pérdida de peso inexplicada?")

# Evaluation
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad**: {age} años | **IMC**: {bmi}")
    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    if age <= 0 or age > 120:
        st.error("Fecha de nacimiento inválida.")
        st.stop()

    # 1. Genetic / EII / Hamartomatous / PAF
    if hered or ibd or hamart or fap:
        st.warning("**Riesgo Alto** (Genético, EII o hamartomatosos)")
        st.markdown(
            """
- Colonoscopia: cada 1–2 años (Lynch, hamartomatosos).
- Colonoscopia: cada 1–5 años (EII, PAF).
- Alternativa: TSOMFi anual o TSOMFg bienal.
            """
        )

    # 2. Family history
    elif family_crc:
        if family_before_60:
            st.info("**Riesgo Incrementado** (Familiar <60 años)")
            st.markdown(
                """
- Iniciar colonoscopia a los 40 años o 10 años antes del caso familiar.
- Repetir cada 5 años.
- Alternativa: TSOMFi anual o TSOMFg bienal.
                """
            )
        else:
            st.info("**Riesgo Incrementado** (Familiar ≥60 años)")
            st.markdown(
                """
- Iniciar colonoscopia a los 50 años.
- Repetir cada 5 años.
- Alternativa: TSOMFi cada 2 años o TSOMFg bienal.
                """
            )

    # 3. Polyp history
    elif polyp10:
        if tmp_advanced:
            st.warning("**Riesgo Alto** (Adenoma avanzado)")
            st.markdown(
                """
- Colonoscopia: control en 3 años.
- FIT/FOBT anual o bienal entre controles.
                """
            )
        elif tmp_serrated:
            st.warning("**Riesgo Alto** (Poliposis serrada)")
            st.markdown(
                """
- Colonoscopia: vigilancia cada 3–5 años.
- Evaluación genética.
                """
            )
        else:
            st.info("**Riesgo Intermedio** (Historial de pólipos)")
            st.markdown(
                """
- Colonoscopia: control en 5 años.
- Alternativa: FIT anual o FOBT bienal.
                """
            )

    # 4. Symptoms
    elif symptoms:
        st.warning("**Síntomas**: requiere evaluación médica urgente.")

    # 5. Average risk <50
    elif age < 50:
        st.info("No se recomienda tamizaje <50 años sin factores adicionales.")

    # 6. Average risk 50–75
    elif age <= 75:
        st.success("**Riesgo Promedio** (50–75 años)")
        st.markdown(
            """
Opciones de tamizaje:
- TSOMFi cada 2 años
- FOBT (TSOMFg) cada 2 años
- Rectosigmoidoscopía (RSC) cada 5 años
- Colonoscopia cada 10 años
- Colonoscopia Virtual (VCC) cada 5 años (alternativa no invasiva)
            """
        )

    # 7. >75 años
    else:
        st.warning(
            ">75 años: evaluar caso a caso, sin tamizaje rutinario."
        )

    if bmi >= 25:
        st.markdown("**Nota:** IMC elevado, factor de riesgo adicional.")
