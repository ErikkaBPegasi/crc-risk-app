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
    "Herramienta para pacientes: responde tus datos para obtener tu estrategia de tamizaje según la Guía Argentina."
)

# Inputs
dob = st.date_input(
    "Fecha de nacimiento",
    value=None,
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today(),
    help="Selecciona tu fecha de nacimiento"
)
height_str = st.text_input("Altura (cm)", placeholder="Ej: 170", help="Mide tu altura sin zapatos")
weight_str = st.text_input("Peso (kg)", placeholder="Ej: 65", help="Ingresa tu peso actual")

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
ibd = st.checkbox("¿Tenés enfermedad intestinal inflamatoria como Crohn o colitis ulcerosa?")
hered = st.checkbox("¿Algún médico te dijo que tenés un síndrome hereditario como el de Lynch?")
hamart = st.checkbox("¿Te diagnosticaron un síndrome de pólipos hereditarios como Peutz-Jeghers o Cowden?")
fap = st.checkbox("¿Tenés diagnóstico de poliposis adenomatosa familiar (PAF)?")
fasha = st.checkbox("¿Tenés diagnóstico de poliposis adenomatosa familiar atenuada (PAFA)?")
serrated_synd = st.checkbox("¿Te diagnosticaron síndrome de poliposis serrada (múltiples pólipos serrados)?")

# 2. Antecedentes familiares
st.markdown("**2. Antecedentes familiares**")
family_crc = st.checkbox("¿Tenés un familiar directo (padre/madre/hermano/a/hijo/a) con cáncer colorrectal?")
family_before_60 = False
if family_crc:
    family_before_60 = st.checkbox("¿Ese familiar fue diagnosticado antes de los 60 años?")

# 3. Historial de pólipos en colon o recto
st.markdown("**3. Historial de pólipos**")
polyp10 = st.checkbox("Durante los últimos 10 años, ¿algún médico te dijo que tenías pólipos en el colon o el recto?")
advanced_poly = False
serrated = False
if polyp10:
    advanced_poly = st.checkbox("¿Alguno de esos pólipos fue grande (más de 1 cm) o de alto riesgo?")
    serrated = st.checkbox("¿Alguno de los pólipos era del tipo serrado?")

# 4. Síntomas actuales
st.markdown("**4. Síntomas actuales**")
symptoms = st.checkbox("¿Tenés sangrado por recto, cambios en el ritmo intestinal o pérdida de peso sin explicación?")

# Cálculo y resultados
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad:** {age} años   **IMC:** {bmi}")
    st.markdown("---")
    st.subheader("Resultados y estrategia de tamizaje")

    # Validar edad
    if age < 0 or age > 120:
        st.error("Fecha inválida.")
        st.stop()

    # 1. Riesgo Alto por condición específica
    if hered:
        st.warning("**Riesgo Alto: Lynch**")
        st.markdown(
            "- Colonoscopia cada 1–2 años\n- TSOMFi anual o TSOMFg bienal"
        )
    elif serrated_synd:
        st.warning("**Riesgo Alto: pólipos serrados**")
        st.markdown(
            "- Colonoscopia anual\n- Evaluación genética"
        )
    elif hamart:
        st.warning("**Riesgo Alto: síndrome hamartomatoso**")
        st.markdown(
            "- Colonoscopia cada 1–2 años\n- TSOMFi anual o TSOMFg bienal"
        )
    elif fap:
        st.warning("**Riesgo Alto: PAF**")
        st.markdown(
            "- Colonoscopia cada 1–5 años\n- TSOMFi anual o TSOMFg bienal"
        )
    elif fasha:
        st.warning("**Riesgo Alto: PAFA**")
        st.markdown(
            "- Colonoscopia cada 1–5 años\n- TSOMFi anual o TSOMFg bienal"
        )
    elif ibd:
        st.warning("**Riesgo Alto: EII**")
        st.markdown(
            "- Colonoscopia cada 1–5 años\n- TSOMFi anual o TSOMFg bienal"
        )

    # 2. Historial de pólipos específicos
    elif polyp10 and advanced_poly:
        st.warning("**Riesgo Alto: adenoma avanzado**")
        st.markdown(
            "- Colonoscopia de control a los 3 años\n- FIT o FOBT anual"
        )
    elif polyp10 and serrated:
        st.warning("**Riesgo Alto: pólipo serrado**")
        st.markdown(
            "- Colonoscopia de vigilancia cada 3–5 años\n- Evaluación genética"
        )
    elif polyp10:
        st.info("**Riesgo Intermedio: pólipos simples**")
        st.markdown(
            "- Colonoscopia de control a los 5 años\n- TSOMFi anual o TSOMFg bienal"
        )

    # 3. Síntomas urgentes
    elif symptoms:
        st.warning("**Síntomas:** derivar urgente para evaluacion medica")

    # 4. Antecedente familiar
    elif family_crc:
        if family_before_60:
            st.info("**Riesgo Incrementado:** familiar <60 años")
            st.markdown(
                "- Colonoscopia a los 40 años o 10 años antes\n- Repetir cada 5 años\n- TSOMFi anual o TSOMFg bienal"
            )
        else:
            st.info("**Riesgo Incrementado:** familiar ≥60 años")
            st.markdown(
                "- Colonoscopia a los 50 años\n- Repetir cada 5 años\n- TSOMFi cada 2 años o TSOMFg bienal"
            )

    # 5. Riesgo Promedio
    elif age < 50:
        st.info("Menos de 50 años sin factores de riesgo: no requiere tamizaje")
    elif age <= 75:
        st.success("**Riesgo Promedio (50–75 años)**")
        st.markdown(
            "- TSOMFi cada 2 años\n- TSOMFg cada 2 años\n- Rectosigmoidoscopía cada 5 años\n- Colonoscopia cada 10 años\n- VCC cada 5 años"
        )
    else:
        st.warning("Más de 75 años: evaluar caso a caso sin tamizaje rutinario")

    # Nota IMC
    if bmi >= 25:
        st.markdown("**Nota:** IMC elevado, factor de riesgo adicional")

# Disclaimer
st.markdown("---")
st.markdown(
    "**Aviso:** Esta herramienta tiene fines educativos e informativos y está adaptada a la guía \"Recomendaciones para el tamizaje de CCR en población de riesgo promedio en Argentina 2022\". No constituye una consulta médica ni reemplaza el consejo de un profesional de la salud. Te invitamos a usar esta información como base para conversar con tu médico sobre tu riesgo de cáncer colorrectal y las alternativas recomendadas en tu caso."
)
