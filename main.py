import os
import streamlit as st
from groq import Groq
from groq.types.chat import ChatCompletion

# Initialize session state for messages and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "llama3-8b-8192"  # default model

# Add title and API key input
st.title("Groq Chat Interface")
api_key = st.text_input("Enter your Groq API Key:", type="password")

# Add clear button after initialization
if st.button("Clear Chat"):
    st.session_state.messages = []

# Only proceed if API key is provided
if api_key:
    client = Groq(api_key=api_key)
    
    try:
        # Fetch available models
        models = client.models.list()
        model_names = [model.id for model in models.data]
        
        # Create model selector
        selected_model = st.selectbox(
            "Select Model:",
            model_names,
            index=model_names.index(st.session_state.model) if st.session_state.model in model_names else 0
        )
        st.session_state.model = selected_model
        
        # Get user input
        user_input = st.text_area("Enter your message:", "Explain the importance of fast language models")
        
        # Create columns for side-by-side display
        col1, col2 = st.columns(2)
        
        if st.button("Send"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful assistant."
                    },
                    *st.session_state.messages
                ],
                model=selected_model,  # Use selected model
            )
            
            # Add assistant response to history
            assistant_response = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Display chat history in left column
            with col1:
                st.subheader("Chat")
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        st.write("You:", message["content"])
                    else:
                        st.write("Assistant:", message["content"])
            
            # Display raw JSON in right column
            with col2:
                st.subheader("Raw JSON Response")
                st.json(chat_completion.model_dump())
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("Please enter your Groq API key to continue.")