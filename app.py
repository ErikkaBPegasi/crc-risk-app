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
# Fecha de nacimiento con selector de calendario
dob = st.date_input(
    "Fecha de nacimiento",
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today()
)
height_str = st.text_input("Altura (cm)", value="", placeholder="ej. 170")
weight_str = st.text_input("Peso (kg)", value="", placeholder="ej. 65")

# Parse inputs
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
ibd = st.checkbox("¿Alguna vez te han dicho que tienes inflamación crónica en el intestino (Crohn o colitis ulcerativa)?")
hered = st.checkbox("¿Te han dicho que tienes un síndrome hereditario que aumenta el riesgo de cáncer de colon (p.ej. Lynch)?")
hamart = st.checkbox("¿Tienes o te han dicho que tienes un síndrome de pólipos poco común (Peutz-Jeghers, Cowden)?")
fap = st.checkbox("¿Te han dicho que tienes muchos pólipos en el colon desde joven (poliposis familiar)?")

family_crc = st.checkbox("¿Algún familiar cercano tuvo cáncer de colon o recto?")
family_before_60 = False
if family_crc:
    family_before_60 = st.checkbox("¿Ese familiar fue diagnosticado antes de los 60 años?")

polyp10 = st.checkbox("¿Te han encontrado algún pólipo en los últimos 10 años?")
tmp_advanced = False
tmp_serrated = False
if polyp10:
    tmp_advanced = st.checkbox("¿Fueron pólipos grandes o con riesgo alto?")
    tmp_serrated = st.checkbox("¿Te han dicho que esos pólipos eran de tipo serrado?")

symptoms = st.checkbox("¿Has tenido sangre en las heces, cambios en el hábito intestinal o pérdida de peso sin explicación?")

# Compute outputs only when all inputs are provided
if dob and height_cm is not None and weight_kg is not None:
    age = calculate_age(dob)
    bmi = calculate_bmi(height_cm, weight_kg)
    st.markdown(f"**Edad**: {age} años | **IMC**: {bmi}")
    st.markdown("---")
    st.subheader("Resultado de la evaluación")

    # Validate age
    if age <= 0 or age > 120:
        st.error("Por favor ingresa una fecha de nacimiento válida.")
        st.stop()

    # 1. Hereditario / EII / Hamartomatosos / PAF
    if hered or ibd or hamart or fap:
        st.warning("**Riesgo Alto/Incrementado – Genético/EII**")
        st.markdown(
            """
            - Colonoscopia: cada 1–2 años (Lynch o hamartomatosos).
            - Colonoscopia: cada 1–5 años (EII, PAF).
            - Si no es posible: TSOMFi anual o TSOMFg bienal.
            """
        )

    # 2. Familiar con CCR\  
    elif family_crc:
        if family_before_60:
            st.info("**Riesgo Incrementado – Familiar <60 años**")
            st.markdown(
                """
                - Colonoscopia: iniciar a los 40 años o 10 años antes del caso familiar más joven.
                - Repetir cada 5 años.
                - Alternativa: TSOMFi anual o TSOMFg bienal.
                """
            )
        else:
            st.info("**Riesgo Incrementado – Familiar ≥60 años**")
            st.markdown(
                """
                - Colonoscopia: iniciar a los 50 años.
                - Repetir cada 5 años.
                - Alternativa: TSOMFi cada 2 años o TSOMFg bienal.
                """
            )

    # 3. Historial de pólipos\  
    elif polyp10:
        if tmp_advanced:
            st.warning("**Riesgo Alto – Adenomas Avanzados**")
            st.markdown(
                """
                - Colonoscopia: control en 3 años.
                - Interim: TSOMFi anual o TSOMFg bienal.
                """
            )
        elif tmp_serrated:
            st.warning("**Riesgo Alto – Poliposis Serrada**")
            st.markdown(
                """
                - Colonoscopia: vigilancia cada 3–5 años.
                - Evaluación genética.
                """
            )
        else:
            st.info("**Riesgo Intermedio – Historial de Pólipos**")
            st.markdown(
                """
                - Colonoscopia: control en 5 años.
                - Alternativa: TSOMFi anual o TSOMFg bienal.
                """
            )

    # 4. Síntomas\  
    elif symptoms:
        st.warning("**Síntomas presentes**: requiere evaluación médica inmediata.")

    # 5. Riesgo promedio <50\  
    elif age < 50:
        st.info("No se recomienda tamizaje <50 años sin otros factores de riesgo.")

    # 6. Riesgo promedio 50–75\  
    elif age <= 75:
        st.success("**Riesgo Promedio**: 50–75 años sin factores adicionales.")
        st.markdown(
            """
            Opciones de tamizaje:
            - TSOMFi cada 2 años
            - TSOMFg cada 2 años
            - Rectosigmoidoscopía cada 5 años
            - Colonoscopia cada 10 años
            - Colonoscopia Virtual (VCC) cada 5 años como alternativa no invasiva
            """
        )

    # 7. >75 años
    else:
        st.warning("No se recomienda tamizaje programático >75 años sin evaluación individualizada.")

    # Nota IMC
    if bmi >= 25:
        st.markdown("**Nota:** Tu IMC es elevado, factor de riesgo adicional para CCR.")
