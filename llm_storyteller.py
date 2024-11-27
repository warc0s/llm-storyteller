import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="LLM StoryTeller",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #FF4B4B;
        color: white;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: white !important;
        background-color: #FF4B4B;
    }
    .story-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .story-text {
        color: #1E1E1E;
        font-size: 1.1rem;
        line-height: 1.6;
        font-family: 'Georgia', serif;
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
        outline_prompt = f"""Crea una historia en {language} con estas características:
        - Personaje principal: {main_character}
        - Personaje secundario: {secondary_character}
        - Ubicación: {location}
        - Acción clave: {key_action}
        - Estilo: {style}
        - Longitud: {length}

        Importante: NO uses formato markdown ni secciones como "Introducción", "Desarrollo", etc.
        Escribe la historia de forma natural y fluida, como si fuera un cuento tradicional.
        La historia debe ser coherente y cautivadora, manteniendo el interés del lector."""

        outline = call_llm(outline_prompt, outline_model, temperature)
        
        if outline:
            with st.spinner("✍️ Puliendo la narrativa..."):
                writing_prompt = f"""Mejora esta historia manteniendo su esencia:
                {outline}

                Importante:
                - Escribe de forma natural y fluida
                - NO uses formato markdown ni secciones
                - Mantén el estilo {style}
                - Asegúrate de que la historia fluya naturalmente
                - Evita mencionar explícitamente "introducción", "desarrollo" o "conclusión"
                """

                story = call_llm(writing_prompt, writing_model, temperature)
                
                if story:
                    with st.spinner("🔍 Dando los últimos toques..."):
                        review_prompt = f"""Revisa y mejora esta historia:
                        {story}

                        Importante:
                        - Mantén un estilo narrativo natural y fluido
                        - NO uses formato markdown ni secciones
                        - Asegura que la historia sea coherente y cautivadora
                        - Mejora la gramática y el estilo sin cambiar la esencia
                        - Evita cualquier formato especial o estructura visible"""

                        final_story = call_llm(review_prompt, review_model, temperature)
                        
                        if final_story:
                            st.subheader("📖 Tu Historia")
                            st.markdown(
                                f'<div class="story-container"><div class="story-text">{final_story}</div></div>',
                                unsafe_allow_html=True
                            )
                            
                            # Botón para descargar
                            st.download_button(
                                label="📥 Descargar Historia",
                                data=final_story,
                                file_name="mi_historia.txt",
                                mime="text/plain"
                            )
