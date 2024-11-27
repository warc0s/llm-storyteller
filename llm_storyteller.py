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
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .story-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("🌟 LLM StoryTeller")
st.markdown("### Crea historias únicas con la ayuda de la IA")

# Configuración de los endpoints
BASE_URL = "http://localhost:7860/v1"
AVAILABLE_MODELS = {
    "Llama 1B": "llama-1b",
    "Qwen 1.5B": "qwen-1.5b"
}

def call_llm(prompt, model, temperature=0.7):
    """Función para llamar al LLM"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": AVAILABLE_MODELS[model],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
        )
        return response.json()["choices"][0]["message"]["content"]
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
    
    # Configuración de creatividad
    st.subheader("Ajustes de Generación")
    creativity = st.select_slider(
        "Nivel de Creatividad",
        options=["Baja", "Media", "Alta"],
        value="Media"
    )
    temperature = {"Baja": 0.3, "Media": 0.7, "Alta": 0.9}[creativity]
    
    # Idioma
    language = st.text_input("Idioma de la Historia", "Español")

# Formulario principal
with st.form("story_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        main_character = st.text_input("Personaje Principal", placeholder="ej. Luna, la exploradora")
        location = st.text_input("Lugar", placeholder="ej. Una ciudad submarina")
        
    with col2:
        secondary_character = st.text_input("Personaje Secundario", placeholder="ej. Max, el científico")
        key_action = st.text_input("Acción Importante", placeholder="ej. Descubrir un portal dimensional")

    # Selección de longitud y estilo
    col3, col4 = st.columns(2)
    
    with col3:
        length = st.selectbox(
            "Longitud de la Historia",
            ["Historia Breve (500 palabras)", 
             "Relato Mediano (1000 palabras)",
             "Novela Corta (2000 palabras)"]
        )
    
    with col4:
        style = st.selectbox(
            "Estilo Narrativo",
            ["Misterio", "Ciencia Ficción", "Romance", "Fantasía", "Comedia"]
        )

    generate = st.form_submit_button("✨ Generar Historia")

if generate:
    with st.spinner("🎭 Creando el guión de la historia..."):
        # Prompt para el guión
        outline_prompt = f"""Como guionista experto, crea un esquema detallado para una historia en {language} con las siguientes características:
        - Personaje principal: {main_character}
        - Personaje secundario: {secondary_character}
        - Ubicación: {location}
        - Acción clave: {key_action}
        - Estilo: {style}
        - Longitud aproximada: {length}
        
        El esquema debe incluir:
        1. Introducción de personajes y escenario
        2. Desarrollo del conflicto principal
        3. Puntos de giro importantes
        4. Resolución y conclusión
        
        Mantén el esquema conciso pero informativo."""

        outline = call_llm(outline_prompt, outline_model, temperature)
        if outline:
            st.subheader("📝 Guión")
            st.text_area("", outline, height=200)

            with st.spinner("✍️ Escribiendo la historia..."):
                # Prompt para la escritura
                writing_prompt = f"""Como escritor creativo, desarrolla una historia en {language} basada en el siguiente guión:
                {outline}
                
                Consideraciones:
                - Mantén el estilo {style}
                - Desarrolla los personajes de {main_character} y {secondary_character}
                - Ambienta vívidamente la historia en {location}
                - Incorpora naturalmente la acción: {key_action}
                - Ajusta la longitud a {length}
                
                Escribe de manera cautivadora y mantén la coherencia narrativa."""

                story = call_llm(writing_prompt, writing_model, temperature)
                if story:
                    with st.spinner("🔍 Revisando y mejorando..."):
                        # Prompt para la revisión
                        review_prompt = f"""Como editor experto, revisa y mejora la siguiente historia en {language}:
                        {story}
                        
                        Enfócate en:
                        1. Coherencia narrativa y continuidad
                        2. Desarrollo de personajes
                        3. Ritmo y fluidez
                        4. Gramática y estilo
                        5. Impacto emocional
                        
                        Proporciona la versión mejorada manteniendo la esencia original."""

                        final_story = call_llm(review_prompt, review_model, temperature)
                        if final_story:
                            st.subheader("📖 Historia Final")
                            st.markdown(f'<div class="story-container">{final_story}</div>', unsafe_allow_html=True)
                            
                            # Botón para descargar
                            st.download_button(
                                label="📥 Descargar Historia",
                                data=final_story,
                                file_name="mi_historia.txt",
                                mime="text/plain"
                            )
