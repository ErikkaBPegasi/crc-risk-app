import streamlit as st
from datetime import datetime
from io import BytesIO
# from fpdf import FPDF  # Desactivado temporalmente para evitar error

# Helper functions
def calculate_age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

# def generar_pdf(edad, imc, resumen):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="Resultado de evaluación para cáncer colorrectal", ln=1, align="C")
#     pdf.ln(10)
#     pdf.cell(200, 10, txt=f"Edad: {edad} años", ln=1)
#     pdf.cell(200, 10, txt=f"IMC: {imc}", ln=1)
#     pdf.ln(5)
#     pdf.multi_cell(0, 10, resumen)
#
#     buffer = BytesIO()
#     pdf.output(buffer)
#     buffer.seek(0)
#     return buffer

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
st.caption("Luego de ingresar tus datos, hacé clic en 'Evaluar riesgo' para ver tu recomendación.")

# Parse numeric inputs
age = None
bmi = None
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

if dob and height_str and weight_str:
    try:
        height_cm = float(height_str)
        weight_kg = float(weight_str)
        age = calculate_age(dob)
        bmi = calculate_bmi(height_cm, weight_kg)
        st.markdown(f"**Edad:** {age} años | **IMC:** {bmi}")
    except:
        st.error("Por favor ingresá valores válidos para altura y peso.")

# 1. Antecedentes personales de salud
st.markdown("**1. Antecedentes personales de salud**")
ibd = st.toggle("¿Tenés enfermedad intestinal inflamatoria como Crohn o colitis ulcerosa?", value=False)
hered = st.toggle("¿Algún médico te dijo que tenés un síndrome hereditario como el de Lynch?", value=False)
hamart = st.toggle("¿Te diagnosticaron un síndrome de pólipos hereditarios como Peutz-Jeghers o Cowden?", value=False)
fap = st.toggle("¿Tenés diagnóstico de poliposis adenomatosa familiar (PAF)?", value=False)
fasha = st.toggle("¿Tenés diagnóstico de poliposis adenomatosa familiar atenuada (PAFA)?", value=False)
serrated_synd = st.toggle("¿Te diagnosticaron síndrome de poliposis serrada (múltiples pólipos serrados)?", value=False)

# 2. Antecedentes familiares
st.markdown("**2. Antecedentes familiares**")
family_crc = st.toggle("¿Tenés un familiar directo (padre/madre/hermano/a/hijo/a) con cáncer colorrectal?", value=False)
family_before_60 = False
if family_crc:
    family_before_60 = st.toggle("¿Ese familiar fue diagnosticado antes de los 60 años?", value=False)

# 3. Historial de pólipos en colon o recto
st.markdown("**3. Historial de pólipos**")
polyp10 = st.toggle("Durante los últimos 10 años, ¿algún médico te dijo que tenías pólipos en el colon o el recto?", value=False)
advanced_poly = False
serrated = False
resected = False
if polyp10:
    advanced_poly = st.toggle("¿Alguno de esos pólipos fue grande (más de 1 cm) o de alto riesgo?", value=False)
    serrated = st.toggle("¿Alguno de los pólipos era del tipo serrado?", value=False)
    resected = st.toggle("¿Te realizaron una resección o extirpación de esos pólipos o adenomas?", value=False)

# Evaluación de síntomas (fuera del bloque de riesgo)
symptoms = st.toggle("¿Tenés sangrado por recto, cambios en el ritmo intestinal o pérdida de peso sin explicación?", value=False)

# Botón para evaluar riesgo
if st.button("Evaluar riesgo"):
    if age and bmi:
        st.markdown(f"**Edad:** {age} años | **IMC:** {bmi}")
        st.markdown("---")
        st.subheader("Estrategia de tamizaje recomendada")

        resumen = ""

        if hered:
            st.warning("Riesgo Alto: Síndrome de Lynch")
            st.markdown("Colonoscopia cada 1–2 años.")
            resumen = "Riesgo alto debido a síndrome de Lynch. Se recomienda colonoscopia cada 1–2 años."
        elif ibd:
            st.warning("Riesgo Alto: Enfermedad Inflamatoria Intestinal")
            st.markdown("Colonoscopia cada 1–5 años.")
            resumen = "Riesgo alto por enfermedad inflamatoria intestinal. Colonoscopia entre 1–5 años."
        elif fap or fasha:
            st.warning("Riesgo Alto: Poliposis Adenomatosa Familiar")
            st.markdown("Colonoscopia cada 1–2 años.")
            resumen = "Riesgo alto por poliposis adenomatosa familiar. Colonoscopia cada 1–2 años."
        elif hamart:
            st.warning("Riesgo Alto: Síndrome hamartomatoso")
            st.markdown("Colonoscopia cada 1–2 años.")
            resumen = "Riesgo alto por síndrome hamartomatoso. Colonoscopia cada 1–2 años."
        elif serrated_synd:
            st.warning("Riesgo Alto: Poliposis serrada")
            st.markdown("Colonoscopia anual.")
            resumen = "Riesgo alto por poliposis serrada. Colonoscopia anual."
        elif polyp10 and advanced_poly and resected:
            st.warning("Riesgo Alto: Adenoma avanzado resecado")
            st.markdown("Colonoscopia a los 3 años + FIT anual.")
            resumen = "Riesgo alto por adenoma avanzado resecado. Colonoscopia a los 3 años + FIT anual."
        elif polyp10 and serrated and resected:
            st.warning("Riesgo Alto: Pólipo serrado resecado")
            st.markdown("Colonoscopia cada 3–5 años + evaluación genética.")
            resumen = "Riesgo alto por pólipo serrado resecado. Colonoscopia 3–5 años + genética."
        elif polyp10 and resected:
            st.info("Riesgo Intermedio: Pólipos simples resecados")
            st.markdown("Colonoscopia a los 5 años.")
            resumen = "Riesgo intermedio por pólipos simples. Colonoscopia a los 5 años."
        elif family_crc:
            if family_before_60:
                st.info("Riesgo Incrementado: Familiar <60 años")
                st.markdown("Colonoscopia a los 40 años o 10 años antes del caso + repetir cada 5 años.")
                resumen = "Riesgo incrementado: antecedente familiar <60 años. Colonoscopia temprana."
            else:
                st.info("Riesgo Incrementado: Familiar ≥60 años")
                st.markdown("Colonoscopia a los 50 años + repetir cada 5 años.")
                resumen = "Riesgo incrementado: familiar ≥60 años. Colonoscopia desde los 50."
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
            resumen = "📝 Resumen: Aunque no se detectaron factores de riesgo adicionales, cumplís con los criterios de edad (50–75 años). Se recomienda continuar con el tamizaje de acuerdo con las opciones disponibles con tu prestador de salud."
        elif age < 50:
            st.info("Menor de 50 años sin factores: no requiere tamizaje")
            resumen = "Actualmente no cumplís criterios para tamizaje por edad."
        elif age > 75:
            st.info("Mayor de 75 años: evaluar caso a caso")
            resumen = "Por tu edad, se recomienda evaluar caso a caso con tu médico tratante."

        # IMC nota
        if bmi >= 25:
            st.markdown(f"**Nota:** IMC elevado ({bmi}): factor de riesgo adicional.")
            st.markdown("Para mejorar tu salud y reducir riesgos, el IMC recomendado es entre 18.5 y 24.9. Consultá con un profesional para orientación nutricional.")

        # Síntomas
        if symptoms:
            st.warning("**Atención:** Presentás síntomas clínicos. Se recomienda consulta médica inmediata.")

        # Mostrar resumen
        if resumen:
            st.markdown("---")
            st.markdown(f"📋 **Resumen final:** {resumen}")

# Disclaimer
st.markdown("---")
st.markdown("""**Aviso:** Esta herramienta tiene fines educativos e informativos y está adaptada a la guía \"Recomendaciones para el tamizaje de CCR en población de riesgo promedio en Argentina 2022\". No constituye una consulta médica ni reemplaza el consejo de un profesional de la salud. Te invitamos a usar esta información como base para conversar con tu médico sobre tu riesgo de cáncer colorrectal y las alternativas recomendadas en tu caso.  
📄 [Accedé a la guía oficial del Instituto Nacional del Cáncer](https://bancos.salud.gob.ar/sites/default/files/2023-09/recomendaciones-para-el-tamizaje-organizado-cancer-colorrectal-poblacion-de-riesgo-promedio-argentina.pdf)""")
