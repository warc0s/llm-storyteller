# 📚 LLM StoryTeller - Create Engaging Stories with AI

![Project Banner](https://github.com/warc0s/llm-storyteller/blob/main/images/banner.png)

Welcome to **LLM StoryTeller**, an interactive web application that leverages Large Language Models (LLMs) to help you craft captivating stories effortlessly. Whether you're a student, writer, or enthusiast, LLM StoryTeller provides a seamless experience to generate, refine, and download your unique narratives.

Note: The application interface is in Spanish, but don’t worry! We will walk you through each step in detail in this README. The interface is intuitive, and with the included explanations and screenshots, you’ll find it easy to follow and understand the workflow. Here, you can see the main dashboard of the application:

![LLM StoryTeller Interface](https://github.com/warc0s/llm-storyteller/blob/main/images/dashboard.png)

---

### 🆕! Try It Online on Streamlit Cloud ☁️

Now, you can experience **LLM StoryTeller** directly on **Streamlit Cloud**, thanks to the integration of free models provided by OpenRouter. This version showcases the functionality of the interface with a simplified and accessible experience. Unlike the original `llm_storyteller.py` script designed for local use with your own machine models, this online version (`llm_storyteller_openrouter.py`) is optimized for public interaction and can be accessed at the following link:

[**LLM StoryTeller on Streamlit Cloud**](https://llm-storyteller.streamlit.app)

Explore the power of AI storytelling visually and intuitively. Try it out now and see how the interface seamlessly helps you craft your stories!

---

## Table of Contents

- [📖 About](#-about)
- [🚀 Features](#-features)
- [🔧 Installation](#-installation)
- [🛠️ Usage](#️-usage)
- [⚙️ Configuration](#️-configuration)
- [💡 How It Works](#-how-it-works)
- [📄 License](#-license)
- [📬 Contact](#-contact)

---

## 📖 About

LLM StoryTeller is a Streamlit-based application designed to assist users in creating engaging stories through the power of AI. Instead of simply requesting a story from an LLM, the application guides the language models through a structured three-step process: generating a detailed story outline, crafting the narrative, and refining it for grammar and coherence. This approach ensures higher-quality results compared to a single-step prompt. Additionally, the application is highly customizable, allowing you to select different models, adjust creativity levels, and tailor the story's style and length to your preferences.

To ensure the application functions correctly, you need to have two OpenAI-compatible language models running locally on your machine, configured to serve requests through an endpoint at **http://localhost:7860**. These models should be compatible with OpenAI's API format to handle prompts effectively. If you don't have these models or prefer a different setup, you can modify the `BASE_URL` and `AVAILABLE_MODELS` sections in the code to point to other endpoints or adjust the model names to match your setup.

---

## 🚀 Features

- **Guided Multi-Step Process**: Directs LLMs through outlining, writing, and reviewing to ensure higher-quality stories.
- **Model Compatibility**: Easily configure and run OpenAI-compatible models locally, such as Llama 1B or Qwen 1.5B.
- **Customizable Story Parameters**: Adjust creativity, choose narrative style, language, and story length.
- **Intuitive Interface**: Simple and responsive design with clear input fields for seamless interaction.
- **Downloadable Stories**: Save the final story as a text file with a single click.
- **Flexible Configuration**: Modify model endpoints and settings to fit your environment.

---

## 🔧 Installation

Follow these steps to set up LLM StoryTeller on your local machine:

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed. [Download Python](https://www.python.org/downloads/)
- **Streamlit**: Install Streamlit using pip.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/warc0s/llm-storyteller.git
   cd LLM-StoryTeller
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   streamlit run app.py
   ```

5. **Access the App**

   Open your browser and navigate to `http://localhost:8501`

---

## 🛠️ Usage

### 1. **Configure Settings**

Navigate to the sidebar to select models for each storytelling step, adjust the temperature for creativity, and set the language of your story.

![Configuration Sidebar](https://github.com/warc0s/llm-storyteller/blob/main/images/settings.png)

### 2. **Input Story Elements**

Fill in the main character, secondary character, location, key action, desired length, and narrative style.

![Input Fields](https://github.com/warc0s/llm-storyteller/blob/main/images/Story_Elements.png)

### 3. **Generate Story**

Click on the "✨ Generar Historia" button. The app will process your inputs through the selected models to create your story.

![Generate Button](https://github.com/warc0s/llm-storyteller/blob/main/images/button.png)

### 4. **Step-by-Step Story Generation**

As the story is being generated, you will see real-time updates for each of the three internal steps:
- **Outline Creation**: The app generates a structured story framework.
- **Story Writing**: The detailed narrative is crafted based on the outline.
- **Review and Refinement**: Grammar, coherence, and overall quality are polished.

Each step's progress is displayed with clear messages, giving you transparency and confidence in the process.

![Generation Steps](https://github.com/warc0s/llm-storyteller/blob/main/images/pasos.png)

### 5. **View and Download**

Once generated, your story will be displayed in a formatted container. You can download the final version as a `.txt` file by clicking on the button "📩 Descargar Historia".

![Generated Story](https://github.com/warc0s/llm-storyteller/blob/main/images/historia.png)

---

## ⚙️ Configuration

LLM StoryTeller offers various configuration options to tailor your storytelling experience:

### **Model Selection**

The application currently supports **Llama 1B** and **Qwen 1.5B**, optimized by default for these smaller models running on CPUs. These options ensure compatibility and performance in a lightweight setup. 

If you'd like to use other models or endpoints, you can customize the application by modifying the `BASE_URL` and `AVAILABLE_MODELS` variables in the `llm_storyteller.py` file. This allows you to adapt the app to your preferred models or configurations.

- **Outline Model**: Generates the story framework.
- **Writing Model**: Crafts the detailed narrative.
- **Review Model**: Enhances grammar and coherence.

![Model Selection](https://github.com/warc0s/llm-storyteller/blob/main/images/model_selection.png)

### **Temperature Adjustment**

Control the creativity of the generated content. Higher values yield more creative outputs, while lower values ensure consistency.

![Temperature Slider](https://github.com/warc0s/llm-storyteller/blob/main/images/temp_slider.png)

### **Language and Style**

The **Language** field is a flexible text box where you can input any language of your choice without restrictions. This input is directly included in the prompt sent to the LLM, ensuring your story is crafted in the specified language.

Additionally, select the desired narrative **Style** from predefined options such as Mystery, Science Fiction, Romance, Fantasy, and Comedy to tailor the tone and feel of your story.

![Language and Style](https://github.com/warc0s/llm-storyteller/blob/main/images/language_style.png)

---

## 💡 How It Works

To summarize, here’s a clear overview of how LLM StoryTeller works, as this structured approach has proven to be the most effective for generating high-quality stories, especially when using smaller models with limited parameters:

1. **Outline Generation**: The application begins by creating a structured framework based on your inputs. This ensures a clear direction and logical flow for the story.

2. **Story Writing**: The framework is expanded into a detailed and engaging narrative, incorporating the chosen language, style, and length specifications.

3. **Review and Refinement**: Finally, the story is polished for grammatical accuracy, coherence, and overall quality, ensuring the end result is compelling and well-written.

This step-by-step process is optimized for smaller models, ensuring they can perform effectively and deliver results comparable to larger models. By guiding the LLM through these structured phases and incorporating **prompt engineering techniques**, LLM StoryTeller maximizes the potential of the models, ensuring they generate stories of superior quality compared to a single-step prompt.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

If you encounter any issues or have suggestions to improve the application, feel free to reach out or open a pull request on GitHub. Your feedback is greatly appreciated!

- **LinkedIn**: [Marcos Garcia](https://www.linkedin.com/in/marcosgarest/)
- **GitHub**: [warc0s](https://github.com/warc0s)
