# Storify by Lambda - Generate Stories from Images

Welcome to **Storify**! This app allows users to generate creative stories based on their inputs and download the results in multiple formats, including text and audio. The app leverages machine learning for story generation and text-to-speech for audio output, all integrated seamlessly into a user-friendly interface built with Streamlit.

## Project Workflow

### 1. **User Input**:
- The user begins by uploading an image or providing instructions for the type of story they want, like; "Generate a fantasy story."

- The app accepts user input in two forms: 
  - **Image input**: The user can upload an image to guide the story generation.
  - **Text input**: The user can provide specific instructions or guidelines to shape the story.

### 2. **Story Generation**:
- Once the user has uploaded an image or entered a text prompt, the app uses **Google's generative AI model** via LangChain to create a story.
- The story is then displayed in the app's main interface.
  
### 3. **Text-to-Speech**:
- The app also provides the ability to convert the generated text into an audio file using **Google's Text-to-Speech API (gTTS)**.
- The audio is created in real-time based on the generated story, and users can download the audio in MP3 format.

### 4. **Download Options**:
- Users can download both the **text version** of the story as a `.txt` file and the **audio version** as an `.mp3` file.
- The app uses **Streamlit's sidebar** to display the download options, ensuring a seamless user experience.
---

## Installation Guide

### Prerequisites

Before you can run this app locally, you will need the following:

- **Python 3.7+**: Make sure Python is installed on your machine.
- **Streamlit**: The app is built using Streamlit for a smooth web interface.
- **LangChain**: To interface with Google's generative AI for story creation.
- **gTTS**: For generating audio from the story text.

### 1. **Clone the Repository**

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/EngineerLambda/storify
cd storify
```

### 2. **Install Dependencies**

Use `pip` to install all the required dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- `streamlit` for the web interface
- `gTTS` for text-to-speech conversion
- `langchain` and `langchain_core` for integrating with AI models
- `langchain_google_genai` to access google's model.

### 3. **Set up API Keys**

You will need an API key for Google's generative AI model. To get this:
- Go to the [Google Cloud Console](https://console.cloud.google.com/) or [Google For Developers](https://developers.google.com/)
- Create a project and enable the API you need (Gemini).
- Obtain your API key and add it to a `.env` file in the root directory.

Example `.env` file:

```plaintext
GOOGLE_API_KEY=your-google-api-key-here
```

### 4. **Run the App Locally**

Once everything is set up, you can run the app locally with:

```bash
streamlit run app.py
```

This will open the app in your default web browser.

---

## App Features

- **Generate Stories**: Users can upload an image and provide a text prompt to generate creative stories.
- **Text-to-Speech**: Convert the generated story into an audio file and download it as an MP3.
- **Download Options**: Download the story in both **text** and **audio** formats.
- **Real-Time Feedback**: Status updates provide real-time feedback while preparing the text and audio files.

---

## Demo Video showing key features
First demo video

https://github.com/user-attachments/assets/c72e3405-e95b-4fe3-a02b-1d3ef18ebaad

Improvement was made to improve the overall app latency and memory usage<br>
I made sure the user can select the story they like best and click a checker, before file preparation starts. That way, the files are only created when needed, and the user can freely choose any story even if they have generated a new one they don't like.<br>
I am also streaming the AI response now to make sure the user gets the messages as they come instead of waiting for the entire thing to be ready.

New video demo
---

## Deploy the App Live

If you’d like to take this app live, you can deploy it on platforms like [Streamlit Cloud](https://streamlit.io/cloud) or [Heroku](https://www.heroku.com/).

To deploy on Streamlit Cloud:
1. Push your repository to GitHub.
2. Log in to Streamlit Cloud and link your GitHub repository.
3. Configure the deployment settings (e.g., add environment variables for the API key).
4. Click "Deploy".

Once deployed, you'll have a live demo where users can interact with your app without running it locally. This is the link to the one I have deployed with streamlit cloud: https://storify-lambda.streamlit.app/
---


## Important Notes

- Make sure the `.env` file is configured correctly with your **Google API key** before running the app.
- If you encounter issues with generating the story or audio, check your API key and ensure you have internet access, as the AI and TTS functionalities require cloud access.

---

Thank you for exploring **Storify**! We hope it sparks your creativity and provides endless storytelling fun!