import streamlit as st
import requests
import json
import re

# Configuración de la página
st.set_page_config(
    page_title="LLM StoryTeller",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
    .main {
        padding: 2rem;
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #FF4B4B;
        color: white !important;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: white !important;
        background-color: #FF4B4B;
    }
    .stButton>button:active, .stButton>button:focus {
        color: white !important;
    }
    .story-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .story-text {
        color: #2C3E50;
        font-size: 1.2rem;
        line-height: 1;
        font-family: 'Crimson Text', 'Georgia', serif !important;
        text-align: justify;
        white-space: pre-wrap;
        letter-spacing: 0.3px;
        word-spacing: 1px;
        text-rendering: optimizeLegibility;
    }
    .story-text p {
        margin-bottom: 0.5rem;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
    }
    .story-text::first-letter {
        font-size: 3.5rem;
        font-weight: bold;
        float: left;
        line-height: 1;
        padding-right: 12px;
        color: #FF4B4B;
    }
    @media (max-width: 768px) {
        .story-container {
            padding: 1.5rem;
        }
        .story-text {
            font-size: 1.1rem;
            line-height: 1.6;
        }
    }
    .input-container {
        padding: 1rem;
        border-radius: 10px;
        margin: 0;
    }
    .custom-input {
        border: 1px solid #ddd !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
    }
    div.stMarkdown {
        background-color: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: transparent !important;
    }
    .sidebar .element-container {
        background-color: transparent !important;
    }
    .row-widget {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    .stTextInput > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("🌟 LLM StoryTeller")

st.info("""
**Información sobre el proceso:**
Cada paso del proceso creativo puede utilizar dos modelos de IA diferentes (Llama 1B o Qwen 1.5B)\n
Paso 1: Generación del guión de la historia. \n
Paso 2: Escritura como tal de la historia. \n
Paso 3: Mejora de gramática y coherencia general. 
""")

# Configuración de los endpoints
BASE_URL = "http://localhost:7860/v1"
AVAILABLE_MODELS = {
    "Llama 1B": "llama-3.2-1b-instruct",
    "Qwen 1.5B": "qwen2.5-1.5b-instruct"
}

def call_llm(prompt, model, temperature=0.7):
    """Función para llamar al LLM"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": AVAILABLE_MODELS[model],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": 2048
            }
        )
        result = response.json()
        if "choices" not in result or not result["choices"]:
            raise Exception("No se recibió una respuesta válida del modelo")
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error al llamar al modelo: {str(e)}")
        return None

def preprocess_story(text):
    """
    Elimina elementos markdown del texto antes de renderizarlo
    """
    import re
    # Eliminar símbolos markdown comunes
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)  # Eliminar headers (#, ##, etc)
    text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', text)  # Eliminar énfasis (* y _)
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Eliminar código inline
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # Eliminar bullets
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # Eliminar listas numeradas
    return text.strip()

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selección de modelos para cada paso
    st.subheader("Selección de Modelos")
    outline_model = st.selectbox("Modelo para Guión", AVAILABLE_MODELS.keys(), key="outline")
    writing_model = st.selectbox("Modelo para Escritura", AVAILABLE_MODELS.keys(), key="writing")
    review_model = st.selectbox("Modelo para Revisión", AVAILABLE_MODELS.keys(), key="review")
    
    # Configuración de temperatura
    st.subheader("Ajustes de Generación")
    temperature = st.slider(
        "Temperatura (Mayor = Mayor Creatividad)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controla la creatividad del modelo. Valores más altos = más creatividad, valores más bajos = más consistencia"
    )
    
    # Idioma
    language = st.text_input("Idioma de la Historia", "Español")

# Formulario principal
col1, col2 = st.columns(2)

with col1:
    main_character = st.text_input("Personaje Principal", 
                                 placeholder="ej. Luna, la exploradora",
                                 key="main_char")
    location = st.text_input("Lugar", 
                           placeholder="ej. Una ciudad submarina",
                           key="location")
    
with col2:
    secondary_character = st.text_input("Personaje Secundario",
                                      placeholder="ej. Max, el científico",
                                      key="sec_char")
    key_action = st.text_input("Acción Importante",
                              placeholder="ej. Descubrir un portal dimensional",
                              key="action")

# Selección de longitud y estilo
col3, col4 = st.columns(2)

with col3:
    length = st.selectbox(
        "Longitud de la Historia",
        ["Historia Breve (250 palabras)", 
         "Relato Mediano (500 palabras)",
         "Novela Corta (1000 palabras)"]
    )

with col4:
    style = st.selectbox(
        "Estilo Narrativo",
        ["Misterio", "Ciencia Ficción", "Romance", "Fantasía", "Comedia"]
    )

# Botón de generación fuera del formulario
generate = st.button("✨ Generar Historia")

if generate:
    with st.spinner("🎭 Creando el guión de la historia..."):
        outline_prompt = f"""Escribe un guión para una historia en {language} con estos elementos:
        - {main_character} (protagonista)
        - {secondary_character} (personaje secundario)
        - Ubicada en {location}
        - Centrada en {key_action}
        - Estilo {style}
        - Longitud {length}

        IMPORTANTE: Responde SOLO con el esquema de la historia. NO repitas estas instrucciones ni uses viñetas."""

        outline = call_llm(outline_prompt, outline_model, temperature)
        
        if outline:
            with st.spinner("✍️ Puliendo la narrativa..."):
                writing_prompt = f"""Aquí tienes el esquema de una historia:

{outline}

Escribe una historia basada en el esquema de manera detallada y cautivadora, considerando:
- Mantén el estilo {style}
- Incluye detalles sensoriales y emociones
- Usa diálogos naturales
- Longitud aproximada (MUY IMPORTANTE): {length}

IMPORTANTE: Responde SOLO con la historia final. NO repitas estas instrucciones ni el esquema original."""

                story = call_llm(writing_prompt, writing_model, temperature)
                
                if story:
                    with st.spinner("🔍 Dando los últimos toques..."):
                        review_prompt = f"""Aquí tienes una historia que necesita revisión:

{story}

Mejora esta historia manteniendo estos puntos clave:
- Estilo {style}
- Corrección de errores gramaticales y ortográficos
- Mejora de diálogos y descripciones
- Mantén la longitud similar !! MUY IMPORTANTE!! ({length})

IMPORTANTE: Responde SOLO con la versión final mejorada. NO repitas estas instrucciones ni la historia original."""

                        final_story = call_llm(review_prompt, review_model, temperature)
                        
                        if final_story:
                            st.subheader("📖 Tu Historia")
                            # Preprocesar la historia antes de mostrarla
                            cleaned_story = preprocess_story(final_story)
                            st.markdown(
                                f'<div class="story-container"><div class="story-text">{cleaned_story}</div></div>',
                                unsafe_allow_html=True
                            )
                            
                            # Botón para descargar
                            st.download_button(
                                label="📥 Descargar Historia",
                                data=final_story,
                                file_name="mi_historia.txt",
                                mime="text/plain"
                            )
