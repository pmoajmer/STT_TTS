import streamlit as st
from gtts import gTTS
import os
import tempfile
import base64
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_icon="👽")
st.title("Speech to Speech :red[Assistant]")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
instruction = "You are a helpful assistant for Q/A tasks. Respond to user's question in just Urdu language. Keep the answer short and concise. Don't give incomplete answer."
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.2, "max_output_tokens":200},
                              system_instruction=instruction)

def text_to_speech(text, lang='ur'):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts = gTTS(text=text, lang=lang, tld="co.in", slow=False)
        tts.save(fp.name)
        return fp.name

def get_audio_player(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

with st.spinner("Converting speech to text..."):
    text = speech_to_text(language="ur", just_once=True, key="STT")

if text:
    st.chat_message("user", avatar="human.png").write(text)
    
    with st.chat_message("assistant", avatar="bot.png"):
        try:
            response = st.session_state.chat.send_message(text)
            st.write(response.text)
            text_to_speak = (response.text).translate(str.maketrans('', '', '#*_')) # Removing special chars
            audio_file = text_to_speech(text_to_speak)    # Generate TTS audio file
            audio_player = get_audio_player(audio_file)  # Create an audio player
            st.markdown(audio_player, unsafe_allow_html=True)
            os.remove(audio_file)  # Clean up the temporary audio file
        except Exception as e:
            st.error(f"An error occured {e}")
else:
    st.info("Please click 'Start Recording' and speak something!")
