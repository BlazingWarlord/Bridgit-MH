import streamlit as st
import time
import os
import google.generativeai as genai
import requests
import json

st.title("Meet Bridgit")
st.header("Your AI Mental Health Companion")

headers = {
    "Content-Type": "application/json",
    "x-apikey": "66fe8addf368d41ba1577f2e"
}

# Initialize history in session state
if "hist" not in st.session_state:
    st.session_state.hist = []

# Function for bot response
def bot_reply(user_message):
    genai.configure(api_key='AIzaSyBDBFgNWh6U2QGX9I4kiZWnZt7iXseKJeg')

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You are Bridgit, a mental health specialist aimed to help people between ages 10-100 with their mental health issues. You must help out the patient until they say they are satisfied with the session",
    )

    chat_session = model.start_chat(
    history=st.session_state.hist
    )

    response = chat_session.send_message(user_message)

    st.session_state.hist.append({"role": "user", "parts": [user_message]})
    st.session_state.hist.append({"role": "model", "parts": [response.text]})

    return f"Bridgit: {response.text}"

# Initialize the user's credits if not already set
if "credits" not in st.session_state:
    st.session_state["credits"] = 100

st.sidebar.header(f"Credits: {st.session_state['credits']}") 

st.sidebar.write("""
Disclaimer Note

            The information provided by this generative AI chatbot is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider with any questions regarding your health.
            
            Please be aware that the chatbot may sometimes provide inaccurate or counter-intuitive information. It should only be considered as a preliminary resource and not as a definitive guide. Always verify any health-related information with a qualified professional.
            
            By using this chatbot, you acknowledge its limitations and agree not to rely solely on its responses for making health decisions. In case of emergencies or urgent health issues, please seek immediate assistance from a healthcare professional or emergency services.
            """)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("You: "):
    if st.session_state['credits'] > 0:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        st.session_state['credits'] -= 5
        
        response = bot_reply(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        save = requests.post("https://bridgitchatstore-f2d7.restdb.io/rest/chatdata", headers=headers, data = json.dumps({"user": prompt,"bridgit": response}))
        
                             
    else:
        st.error('Looks like you are out of credits... ', icon="🚨")
