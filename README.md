# 📚 LLM StoryTeller

![Project Banner](https://github.com/warc0s/llm-storyteller/blob/main/images/banner.png)

Welcome to **LLM StoryTeller**, an interactive web application that leverages Large Language Models (LLMs) to help you craft captivating stories effortlessly. Whether you're a student, writer, or enthusiast, LLM StoryTeller provides a seamless experience to generate, refine, and download your unique narratives.

![LLM StoryTeller Interface](https://github.com/warc0s/llm-storyteller/blob/main/images/dashboard.png)

---

## Table of Contents

- [📖 About](#-about)
- [🚀 Features](#-features)
- [🔧 Installation](#-installation)
- [🛠️ Usage](#️-usage)
- [📸 Screenshots](#-screenshots)
- [⚙️ Configuration](#️-configuration)
- [💡 How It Works](#-how-it-works)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📬 Contact](#-contact)

---

## 📖 About

LLM StoryTeller is a Streamlit-based application designed to assist users in creating engaging stories through the power of AI. By integrating multiple language models, it guides you through generating a story outline, writing the narrative, and refining it for grammar and coherence. The application is highly customizable, allowing you to choose different models, adjust creativity levels, and tailor the story's style and length to your preferences.

![About Section](path/to/about_image.png)

---

## 🚀 Features

- **Multi-Step Story Generation**: Breaks down the storytelling process into outlining, writing, and reviewing.
- **Model Selection**: Choose between different LLMs (e.g., Llama 1B, Qwen 1.5B) for each step.
- **Customizable Parameters**: Adjust temperature settings to control creativity and select language, style, and length.
- **User-Friendly Interface**: Intuitive design with clear input fields and responsive layout.
- **Downloadable Output**: Easily download your final story in text format.
- **Responsive Design**: Optimized for both desktop and mobile devices.

![Features Overview](path/to/features_image.png)

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

![Installation Steps](path/to/installation_image.png)

---

## 🛠️ Usage

### 1. **Configure Settings**

Navigate to the sidebar to select models for each storytelling step, adjust the temperature for creativity, and set the language of your story.

![Configuration Sidebar](path/to/sidebar_image.png)

### 2. **Input Story Elements**

Fill in the main character, secondary character, location, key action, desired length, and narrative style.

![Input Fields](path/to/input_fields_image.png)

### 3. **Generate Story**

Click on the "✨ Generate Story" button. The app will process your inputs through the selected models to create your story.

![Generate Button](path/to/generate_button_image.png)

### 4. **View and Download**

Once generated, your story will be displayed in a formatted container. You can download the final version as a `.txt` file.

![Generated Story](path/to/generated_story_image.png)

![Download Button](path/to/download_button_image.png)

---

## 📸 Screenshots

### **Home Page**

![Home Page](path/to/home_page_image.png)

### **Configuration Sidebar**

![Configuration Sidebar](path/to/configuration_sidebar_image.png)

### **Story Generation Process**

![Story Generation](path/to/story_generation_image.png)

### **Final Story Output**

![Final Story](path/to/final_story_image.png)

---

## ⚙️ Configuration

LLM StoryTeller offers various configuration options to tailor your storytelling experience:

### **Model Selection**

Choose different models for each step:

- **Outline Model**: Generates the story framework.
- **Writing Model**: Crafts the detailed narrative.
- **Review Model**: Enhances grammar and coherence.

![Model Selection](path/to/model_selection_image.png)

### **Temperature Adjustment**

Control the creativity of the generated content. Higher values yield more creative outputs, while lower values ensure consistency.

![Temperature Slider](path/to/temperature_slider_image.png)

### **Language and Style**

Specify the language of the story and select the desired narrative style from options like Mystery, Science Fiction, Romance, Fantasy, and Comedy.

![Language and Style](path/to/language_style_image.png)

---

## 💡 How It Works

LLM StoryTeller operates through a three-step process:

1. **Outline Generation**: Creates a structured framework based on user inputs.
2. **Story Writing**: Expands the outline into a detailed narrative.
3. **Review and Refinement**: Enhances the story for grammatical accuracy and coherence.

Each step utilizes different language models to ensure a high-quality output.

![Workflow Diagram](path/to/workflow_diagram.png)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For any inquiries or support, feel free to reach out:

- **Linkedin**: [Marcos Garcia](https://www.linkedin.com/in/marcosgarest/)
- **GitHub**: [warc0s](https://github.com/warc0s)
