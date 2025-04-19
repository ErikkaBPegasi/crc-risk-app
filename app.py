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
st.title("Evaluación de riesgo para tamizaje de cáncer colorrectal")
st.markdown(
    "Herramienta para pacientes: responde tus datos y condiciones para obtener la estrategia de tamizaje según las Guías Argentinas."
)

# Inputs
# Fecha de nacimiento: iniciar vacío y abrir calendario
dob = st.date_input(
    "Fecha de nacimiento",
    value=None,
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today(),
    help="Haz clic para seleccionar tu fecha de nacimiento"
)
height_str = st.text_input(
    "Altura (cm)",
    placeholder="Ej: 170",
    help="Mide tu altura sin zapatos"
)
weight_str = st.text_input(
    "Peso (kg)",
    placeholder="Ej: 65",
    help="Ingresa tu peso actual"
)

# Parse numeric inputs
height_cm = None
weight_kg = None
if height_str:
    try:
        height_cm = float(height_str)
    except:
        st.error("Altura inválida.")
if weight_str:
    try:
        weight_kg = float(weight_str)
    except:
        st.error("Peso inválido.")

# 1. Antecedentes personales de salud
st.markdown("**1. Antecedentes personales de salud**")
ibd = st.checkbox(
    "¿Tienes enfermedad intestinal crónica (Crohn o colitis ulcerativa)?",
    help="Inflamación del intestino diagnosticada por un médico"
)
hered = st.checkbox(
    "¿Te diagnosticaron un síndrome hereditario como Lynch?",
    help="Síndrome genético que aumenta el riesgo de varios cánceres"
)

# 2. Antecedentes familiares
st.markdown("**2. Antecedentes familiares**")
family_crc = st.checkbox(
    "¿Tienes un familiar de primer grado con cáncer colorrectal?",
    help="Padre, madre, hermano/a o hijo/a"
)
family_before_60 = False
if family_crc:
    family_before_60 = st.checkbox(
        "¿Ese familiar fue diagnosticado antes de los 60 años?",
        help="El año en que se detectó el cáncer puede influir en tu riesgo"
    )

# 3. Historial de pólipos en colon o recto
st.markdown("**3. Historial de pólipos**")
polyp10 = st.checkbox(
    "¿Te encontraron pólipos en colon o recto en los últimos 10 años?",
    help="Pólipo: pequeño bulto en el revestimiento interno del colon o recto"
)
advanced_poly = False
serrated = False
serrated_synd = False
fap = False
fasha = False
hamart = False
if polyp10:
    advanced_poly = st.checkbox(
        "¿Algún pólipo era grande (>1 cm) o con alto riesgo?",
        help="Los pólipos grandes o atípicos tienen más probabilidad de volverse malignos"
    )
    serrated = st.checkbox(
        "¿Algún pólipo era del tipo serrado?",
        help="Forma serrada en tejido premaligno identificado en colonoscopía"
    )
    if serrated:
        serrated_synd = st.checkbox(
            "¿Te diagnosticaron síndrome de poliposis serrada (múltiples pólipos serrados)?",
            help="Conjunto de múltiples pólipos serrados"
        )
    fap = st.checkbox(
        "¿Tienes diagnóstico de PAF (poliposis adenomatosa familiar)?",
        help="Mutación que genera muchos pólipos en colon"
    )
    fasha = st.checkbox(
        "¿Tienes diagnóstico de PAFA (poliposis familiar atenuada)?",
        help="Variante con menos pólipos que PAF"
    )
    hamart = st.checkbox(
        "¿Tienes diagnóstico de síndrome de pólipos hereditario (Peutz‑Jeghers, Cowden, etc.)?",
        help="Síndromes con crecimiento de pólipos no cancerosos"
    )

# 4. Síntomas actuales
st.markdown("**4. Síntomas**")
symptoms = st.checkbox(
    "¿Has tenido sangrado rectal, cambios en el hábito intestinal o pérdida de peso inexplicada?",
    help="Estos síntomas pueden indicar la necesidad de colonoscopía urgente"
)

# Cálculo y resultados
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad:** {age} años   **IMC:** {bmi}")
    st.markdown("---")
    st.subheader("Estrategia de tamizaje recomendada")

    # Validar edad
    if age < 0 or age > 120:
        st.error("Fecha inválida.")
        st.stop()

    # Riesgo Alto GLOBAL: hered, EII, PAF, PAFA, hamart, serrada-synd
    if hered or ibd or (polyp10 and (serrated_synd or fap or fasha or hamart)):
        st.warning("**Riesgo Alto**: seguimiento especializado necesario.")
        st.markdown(
            """
- Colonoscopia anual (poliposis serrada).
- Colonoscopia cada 1–2 años (síndrome de Lynch o hamartomatosos).
- Colonoscopia cada 1–5 años (EII).
- Colonoscopia cada 1–5 años (PAF/PAFA).
- Alternativa: TSOMFi anual o TSOMFg bienal.

**Nota:** La frecuencia puede ajustarse según tu situación clínica tras evaluación médica.
"""
        )

    # Riesgo Incrementado: antecedentes familiares
    elif family_crc:
        if family_before_60:
            st.info("**Riesgo Incrementado (familiar <60 años)**")
            st.markdown(
                """
- Iniciar colonoscopia a los 40 años o 10 años antes que tu familiar.
- Repetir cada 5 años.
- Alternativa: TSOMFi anual o TSOMFg bienal.

**Nota:** Ajusta los intervalos según consejo profesional.
"""
            )
        else:
            st.info("**Riesgo Incrementado (familiar ≥60 años)**")
            st.markdown(
                """
- Iniciar colonoscopia a los 50 años.
- Repetir cada 5 años.
- Alternativa: TSOMFi cada 2 años o TSOMFg bienal.

**Nota:** Ajusta los intervalos según consejo profesional.
"""
            )

    # Historial de pólipos sin alto riesgo
    elif polyp10:
        if advanced_poly:
            st.warning("**Riesgo Alto (adenoma avanzado)**")
            st.markdown(
                """
- Colonoscopia de control a los 3 años.
- FIT/FOBT anual o bienal.

**Nota:** Revisa tu programa de seguimiento con tu médico.
"""
            )
        elif serrated:
            st.warning("**Riesgo Alto (pólipo serrado)**")
            st.markdown(
                """
- Colonoscopia de vigilancia cada 3–5 años.
- Evaluación genética.

**Nota:** Consulta para personalizar tu frecuencia.
"""
            )
        else:
            st.info("**Riesgo Intermedio (pólipos simples)**")
            st.markdown(
                """
- Colonoscopia de control a los 5 años.
- Alternativa: TSOMFi anual o TSOMFg bienal.

**Nota:** Puedes ajustar la frecuencia previo acuerdo médico.
"""
            )

    # Síntomas urgentes
    elif symptoms:
        st.warning("**Síntomas**: derivar urgente para colonoscopia.")

    # Riesgo Promedio: edad 50-75
    elif age < 50:
        st.info("Menos de 50 años sin factores: no se recomienda tamizaje.")
    elif age <= 75:
        st.success("**Riesgo Promedio (50–75 años)**")
        st.markdown(
            """
Opciones de tamizaje:
- TSOMFi cada 2 años
- TSOMFg cada 2 años
- Rectosigmoidoscopía cada 5 años
- Colonoscopia cada 10 años
- VCC cada 5 años (alternativa no invasiva)

**Nota:** Ajusta según tu contexto clínico tras consulta.
"""
        )
    else:
        st.warning(
            ">75 años: evaluar caso a caso, sin tamizaje rutinario."
        )

    # Nota IMC
    if bmi >= 25:
        st.markdown("**Nota:** IMC elevado, factor de riesgo adicional.")


