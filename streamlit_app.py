import streamlit as st
import time
import os
import google.generativeai as genai

st.title("Meet Bridgit")
st.header("Your AI Mental Health Companion")



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
    history=[
    ]
    )

    response = chat_session.send_message(user_message)

    return f"Bridgit: {response.text}"

# Initialize the user's credits if not already set
if "credits" not in st.session_state:
    st.session_state["credits"] = 100

st.sidebar.header(f"Credits: {st.session_state['credits']}") 


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
    
        response = bot_reply(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error('Looks like you are out of credits... ', icon="🚨")
