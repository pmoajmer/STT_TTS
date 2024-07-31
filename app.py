import streamlit as st
import os
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_icon="👽")
st.title("Google Gemini :red[Assistant]")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
instruction = "You are a helpful assistant for Q/A tasks. Respond to user's question in just Urdu language. Keep the answer concise."
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.5}, system_instruction=instruction)


if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

with st.spinner("Converting speech to text..."):
    text = speech_to_text(language="ur", just_once=True, key="STT")

if text:
    st.chat_message("user").write(text)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(text)
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occured {e}")
else:
    st.info("Please speak something to generate answer!")
