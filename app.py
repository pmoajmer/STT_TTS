import streamlit as st
import os
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="Chatbot", page_icon="🤖")
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
        response = st.session_state.chat.send_message(text, stream=True)
        final_output = st.write_stream(response.text)





# api_key = st.text_input("Enter your API key", key="api_key", type="password")
# if api_key:
#     client = Groq(api_key=api_key)

#     if audio_bytes:
#         with st.spinner("Transcribing..."):
#             file_path = "temp_audio.mp3"
#             with open(file_path, "wb") as f:
#                 f.write(audio_bytes)

#             transcript = speech_to_text(file_path)
#             if transcript:
#                 st.session_state["messages"].append({"role": "user", "content": transcript})
#                 st.chat_message("user").write(transcript)

#                 os.remove(file_path)

#             with st.chat_message("assistant"):
#                 with st.spinner("Generating response..."):
#                     response = get_response(transcript)
#                     st.write(response)
#                 st.session_state["messages"].append({"role": "assistant", "content": response})
