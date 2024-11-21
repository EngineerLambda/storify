import base64
from PIL import Image
import io
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import tempfile
import gtts
import os


st.header("Storify with LangChain - Generate Stories from Images")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# ai system prompt
SYSTEM_PROMPT = """
You are a creative storyteller. Your task is to craft detailed, imaginative, and engaging stories based on a provided image and the user's specific guidelines. Always aim for vivid descriptions and immersive narratives.
"""

# using streamlit native session state to manage state memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "system_message" not in st.session_state:
    st.session_state.system_message = SystemMessage(content=SYSTEM_PROMPT)

uploaded_image = st.file_uploader("Upload an image (e.g., .jpg, .png)")

# user has to always see the image
if uploaded_image:
    pil_image = Image.open(uploaded_image)
    st.image(pil_image, caption="Uploaded Image", use_column_width=True)

    buffered = io.BytesIO()

    if pil_image.mode == "RGBA":
        pil_image = pil_image.convert("RGB")

    pil_image.save(buffered, format="JPEG")

    # encode the image to Base64 to meet langchain's reqs
    image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")


# managing (format to display) all user + ai messages
for message, kind in st.session_state.chat_history:
    with st.chat_message(kind):
        st.markdown(message)

# user prompt
user_prompt = st.chat_input("Provide story guidelines here")

# this function handles the process of generating and tweaking the generated story
def generate_or_tweak_story(system_message, image_data, user_input, history, tweak=False):
    messages = []

    if not tweak:
        messages.append(system_message)

    # update chat history to the message list
    for past_message, kind in history:
        if kind == "user":
            messages.append(HumanMessage(content=past_message))
        elif kind == "assistant":
            messages.append(AIMessage(content=past_message))

    # Add the new user input for tweaking or creating
    if tweak:
        messages.append(
            HumanMessage(content=f"Tweak the previous story as follows: {user_input}")
        )
    else:
        # New user input and image for generating a story
        messages.append(
            HumanMessage(
                content=[
                    {"type": "text", "text": user_input},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ]
            )
        )

    response = llm.invoke(messages)
    return response.content


# Handle Story Generation
if user_prompt and uploaded_image:
    try:
        # Add user input to the chat history
        st.session_state.chat_history.append((user_prompt, "user"))

        # Generate the story
        with st.spinner("Generating story..."):
            story = generate_or_tweak_story(
                st.session_state.system_message,
                image_data,
                user_prompt,
                st.session_state.chat_history,
            )

        # Add AI response to the chat history
        st.session_state.chat_history.append((story, "assistant"))

        # Display AI response
        st.chat_message("assistant").markdown(story)

    except Exception as e:
        st.error(f"Error generating story: {e}")
else:
    if not uploaded_image:
        st.warning("Please upload an image.")
    if not user_prompt:
        st.info("Enter your story guidelines.")
        

# Preparing text and audio files from llm output
st.sidebar.header("Download Options")
st.sidebar.info("Kindly make sure that the story you want to download is the last message before the files (audio and text) are prepared before downloadinf them. Thanks.")

# Ensure there's a final story to download
if st.session_state.chat_history:
    final_story = st.session_state.chat_history[-1][0]  # obtains the last message

    # making sure users are aware of the file prep process
    with st.sidebar.status("Preparing documents") as status:
        
        # prep text file
        text_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        status.update(label="Preparing text document...")
        with open(text_file.name, "w") as f:
            f.write(final_story)
        status.update(label="Text document ready!")

        # txt download btn
        st.sidebar.download_button(
            label="Download as Text",
            data=open(text_file.name, "rb"),
            file_name="story.txt",
            mime="text/plain",
        )
        os.unlink(text_file.name)  # remove file from storage

        # prep audio file
        if "audio_file_path" not in st.session_state:
            st.session_state.audio_file_path = None

        # generate audio if not already done
        if st.session_state.audio_file_path is None:
            try:
                status.update(label="Preparing audio file...")
                tts = gtts.gTTS(final_story, lang='en')

                audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(audio_file.name)

                status.update(label="Audio file ready!")
                st.session_state.audio_file_path = audio_file.name

            except Exception as e:
                status.update(label="Error occurred while preparing audio.")
                st.sidebar.error(f"Error generating audio: {e}")
        
        # audio file btn
        if st.session_state.audio_file_path:
            st.sidebar.download_button(
                label="Download as Audio",
                data=open(st.session_state.audio_file_path, "rb"),
                file_name="story.mp3",
                mime="audio/mpeg",
            )
