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
ibd = st.checkbox("¿Tenés enfermedad intestinal inflamatoria como Crohn o colitis ulcerosa?", help="Estas enfermedades aumentan el riesgo de cáncer colorrectal y requieren vigilancia especial.")
hered = st.checkbox("¿Algún médico te dijo que tenés un síndrome hereditario como el de Lynch?", help="El síndrome de Lynch es una condición genética que aumenta el riesgo de cáncer colorrectal y otros tipos de cáncer.")
hamart = st.checkbox("¿Te diagnosticaron un síndrome de pólipos hereditarios como Peutz-Jeghers o Cowden?")
fap = st.checkbox("¿Tenés diagnóstico de poliposis adenomatosa familiar (PAF)?")
fasha = st.checkbox("¿Tenés diagnóstico de poliposis adenomatosa familiar atenuada (PAFA)?")
serrated_synd = st.checkbox("¿Te diagnosticaron síndrome de poliposis serrada (múltiples pólipos serrados)?")

# 2. Antecedentes familiares
st.markdown("**2. Antecedentes familiares**")
family_crc = st.checkbox("¿Tenés un familiar directo (padre/madre/hermano/a/hijo/a) con cáncer colorrectal?", help="El riesgo aumenta si un familiar cercano tuvo cáncer colorrectal, especialmente si fue antes de los 60 años.")
family_before_60 = False
if family_crc:
    family_before_60 = st.checkbox("¿Ese familiar fue diagnosticado antes de los 60 años?")

# 3. Historial de pólipos en colon o recto
st.markdown("**3. Historial de pólipos**")
polyp10 = st.checkbox("Durante los últimos 10 años, ¿algún médico te dijo que tenías pólipos en el colon o el recto?", help="Los pólipos pueden ser precursores del cáncer colorrectal, por eso es importante informar si fueron detectados.")
advanced_poly = False
serrated = False
resected = False
if polyp10:
    advanced_poly = st.checkbox("¿Alguno de esos pólipos fue grande (más de 1 cm) o de alto riesgo?")
    serrated = st.checkbox("¿Alguno de los pólipos era del tipo serrado?")
    resected = st.checkbox("¿Te realizaron una resección o extirpación de esos pólipos o adenomas?")

# Evaluación de síntomas (fuera del bloque de riesgo)
symptoms = st.checkbox("¿Tenés sangrado por recto, cambios en el ritmo intestinal o pérdida de peso sin explicación?")

# Evaluación de riesgo y recomendaciones
if dob and height_cm and weight_kg:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)

    st.markdown(f"**Edad:** {age} años | **IMC:** {bmi}")
    st.markdown("---")
    st.subheader("Estrategia de tamizaje recomendada")

    if hered:
        st.warning("Riesgo Alto: Síndrome de Lynch")
        st.markdown("Colonoscopia cada 1–2 años.")
    elif ibd:
        st.warning("Riesgo Alto: Enfermedad Inflamatoria Intestinal")
        st.markdown("Colonoscopia cada 1–5 años.")
    elif fap or fasha:
        st.warning("Riesgo Alto: Poliposis Adenomatosa Familiar")
        st.markdown("Colonoscopia cada 1–2 años.")
    elif hamart:
        st.warning("Riesgo Alto: Síndrome hamartomatoso")
        st.markdown("Colonoscopia cada 1–2 años.")
    elif serrated_synd:
        st.warning("Riesgo Alto: Poliposis serrada")
        st.markdown("Colonoscopia anual.")
    elif polyp10 and advanced_poly and resected:
        st.warning("Riesgo Alto: Adenoma avanzado resecado")
        st.markdown("Colonoscopia a los 3 años + FIT anual.")
    elif polyp10 and serrated and resected:
        st.warning("Riesgo Alto: Pólipo serrado resecado")
        st.markdown("Colonoscopia cada 3–5 años + evaluación genética.")
    elif polyp10 and resected:
        st.info("Riesgo Intermedio: Pólipos simples resecados")
        st.markdown("Colonoscopia a los 5 años.")
    elif family_crc:
        if family_before_60:
            st.info("Riesgo Incrementado: Familiar <60 años")
            st.markdown("Colonoscopia a los 40 años o 10 años antes del caso + repetir cada 5 años.")
        else:
            st.info("Riesgo Incrementado: Familiar ≥60 años")
            st.markdown("Colonoscopia a los 50 años + repetir cada 5 años.")
    elif 50 <= age <= 75:
        st.success("Riesgo Promedio")
        st.markdown("""
        **Tu médico puede ayudarte a revisar las siguientes opciones disponibles de tamizaje, considerando la disponibilidad de las pruebas con tu prestador de salud:**

        - ✅ **Test de sangre oculta inmunoquímico (TSOMFi)** cada 2 años *(recomendado como primera opción)*
        - 🟡 **Test con guayaco (TSOMFg)** cada 2 años *(si no se dispone de TSOMFi)*
        - 🔍 **Colonoscopia** cada 10 años
        - 📹 **Videocolonoscopía (VCC)** cada 5 años
        - 🔬 **Rectosigmoidoscopía (RSC)** cada 5 años *(sola o combinada con TSOMFi anual)*
        - 🧭 **Colonoscopia virtual** *(solo si no se dispone de las anteriores)*
        """)
    elif age < 50:
        st.info("Menor de 50 años sin factores: no requiere tamizaje")
    elif age > 75:
        st.info("Mayor de 75 años: evaluar caso a caso")

    # Nota sobre IMC
    if bmi >= 25:
        st.markdown("**Nota:** IMC elevado: factor de riesgo adicional.")
        st.markdown("Para mejorar tu salud y reducir riesgos, el IMC recomendado es entre 18.5 y 24.9. Consultá con un profesional para orientación nutricional y cambios sostenibles.")

    # Síntomas aparte
    if symptoms:
        st.markdown("---")
        st.warning("**Atención:** Presentás síntomas clínicos (sangrado, cambios intestinales o pérdida de peso sin causa aparente). Se recomienda evaluación médica con colonoscopia inmediata.")

# Disclaimer
st.markdown("---")
st.markdown("""**Aviso:** Esta herramienta tiene fines educativos e informativos y está adaptada a la guía \"Recomendaciones para el tamizaje de CCR en población de riesgo promedio en Argentina 2022\". No constituye una consulta médica ni reemplaza el consejo de un profesional de la salud. Te invitamos a usar esta información como base para conversar con tu médico sobre tu riesgo de cáncer colorrectal y las alternativas recomendadas en tu caso.  
📄 [Accedé a la guía oficial del Instituto Nacional del Cáncer](https://bancos.salud.gob.ar/sites/default/files/2023-09/recomendaciones-para-el-tamizaje-organizado-cancer-colorrectal-poblacion-de-riesgo-promedio-argentina.pdf)""")
