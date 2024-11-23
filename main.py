import os
import streamlit as st
from groq import Groq
from groq.types.chat import ChatCompletion

# Add tabs to the interface
tab1, tab2 = st.tabs(["Chat", "Help"])

with tab1:
    # Initialize session state for messages and selected model
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "model" not in st.session_state:
        st.session_state.model = "llama3-8b-8192"  # default model

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

with tab2:
    st.markdown("""
    # Groq Chat Interface

    A Streamlit-based chat interface for interacting with Groq's language models.

    ## Getting Started

    ### 1. Get Your Groq API Key
    1. Visit [Groq Console](https://console.groq.com/playground)
    2. Sign up or log in to your account
    3. Navigate to "API Keys" in the left sidebar
    4. Create a new API key
    5. Copy your API key (make sure to save it as it won't be shown again)

    ⚠️ **Important**: Keep your API key secure and never share it publicly.

    ## Usage

    1. Enter your Groq API key in the password field
    2. Select your preferred model from the dropdown
    3. Type your message in the text area
    4. Click "Send" to get a response
    5. Use "Clear Chat" to reset the conversation

    ## Features

    - Interactive chat interface with Groq's LLMs
    - Secure API key input
    - Chat history management
    - Full JSON response viewing
    - Clear chat functionality
    - Side-by-side display of chat and raw API responses

    ## Security Note

    The API key is handled securely through Streamlit's password input field and is not stored permanently.
    Always ensure you keep your API key confidential.
    """)