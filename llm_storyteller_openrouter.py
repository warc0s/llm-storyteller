import streamlit as st
import requests
import json
import re
from openai import OpenAI

# Configuración de la página
st.set_page_config(
    page_title="LLM StoryTeller",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenRouter client
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
        default_headers={
            "HTTP-Referer": "https://github.com/luisalvarez246/LLM_StoryTeller",
            "X-Title": "LLM StoryTeller",
        }
    )
except Exception as e:
    st.error(f"Error al inicializar el cliente OpenAI: {str(e)}")
    st.stop()

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

# Diccionario para mapear nombres amigables a IDs de modelos
MODEL_DISPLAY_NAMES = {
    "Llama 3.2 3B": "meta-llama/llama-3.2-3b-instruct:free",
    "Mistral 7B": "mistralai/mistral-7b-instruct:free",
    "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct:free",
    "Gemma 2 9B": "google/gemma-2-9b-it:free"
}

def call_llm(prompt, selected_model, temperature=0.7):
    try:
        # Crear lista de modelos de fallback (máximo 3 en total incluyendo el principal)
        all_models = list(MODEL_DISPLAY_NAMES.values())
        models = [selected_model]  # El modelo principal
        
        # Añadir solo 2 modelos más para fallback
        for model in all_models:
            if model != selected_model and len(models) < 3:
                models.append(model)

        completion = client.chat.completions.create(
            model=selected_model,
            headers={
                "HTTP-Referer": "https://github.com/luisalvarez246/LLM_StoryTeller",
                "X-Title": "LLM StoryTeller"
            },
            extra_body={
                "models": models
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error al generar la historia: {str(e)}")
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
    model_display_names = list(MODEL_DISPLAY_NAMES.keys())
    
    outline_display_model = st.selectbox(
        "Modelo para Guión", 
        model_display_names,
        key="outline"
    )
    outline_model = MODEL_DISPLAY_NAMES[outline_display_model]
    
    writing_display_model = st.selectbox(
        "Modelo para Escritura", 
        model_display_names,
        key="writing"
    )
    writing_model = MODEL_DISPLAY_NAMES[writing_display_model]
    
    review_display_model = st.selectbox(
        "Modelo para Revisión", 
        model_display_names,
        key="review"
    )
    review_model = MODEL_DISPLAY_NAMES[review_display_model]

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
        - Género: {style}
        - Tono: {style}

        IMPORTANTE: Responde SOLO con el esquema de la historia. NO repitas estas instrucciones ni uses viñetas."""

        outline = call_llm(outline_prompt, outline_model, temperature)
        
        if outline:
            with st.spinner("✍️ Puliendo la narrativa..."):
                writing_prompt = f"""Basándote en el siguiente esquema, escribe una historia en {language} que sea cautivadora y bien estructurada:

{outline}

Asegúrate de:
- Desarrollar bien los personajes
- Crear descripciones vívidas
- Mantener un ritmo narrativo coherente
- Usar diálogos naturales cuando sea apropiado
- Mantener el tono {style} y el género {style}

IMPORTANTE: Responde SOLO con la historia final. NO repitas estas instrucciones ni el esquema original."""

                story = call_llm(writing_prompt, writing_model, temperature)
                
                if story:
                    with st.spinner("🔍 Dando los últimos toques..."):
                        review_prompt = f"""Revisa y mejora la siguiente historia en {language}, manteniendo su esencia pero mejorando:

{story}

Enfócate en:
- Mejorar la fluidez y coherencia
- Pulir el lenguaje y las descripciones
- Asegurar que mantiene el tono {style}
- Verificar que sigue siendo fiel al género {style}

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
