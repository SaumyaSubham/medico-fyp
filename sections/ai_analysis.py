import streamlit as st
import os
import google.generativeai as genai
from utils import display_logo
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Configure the API key for Google Generative AI SDK
genai.configure(api_key=os.getenv("API_KEY"))

# Chatbot View for Text Analysis
def ai_analysis_view():
    # Check if the user is logged in
    if not st.session_state.get('logged_in', False):
        display_logo()
        st.warning("Please log in, sign up, or activate guest mode to use this service.")
        return

    # Display the logo
    display_logo()

    # Title with text and GIF inline, aligned to the left
    st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 30px;">
        <h1 style='font-size: 50px; color: white; margin: 0;'>Hi from <span style='color: #4CAF50;'>MediCo</span></h1>
        <img src="https://media.tenor.com/SNL9_xhZl9oAAAAi/waving-hand-joypixels.gif" style="width: 50px; height: 50px; margin-left: 5px;">
    </div>
    """,
    unsafe_allow_html=True
    )

    # Input for user symptoms or medical queries
    user_input = st.text_area("Describe your symptoms, medical query, or concerns:")

    if st.button("Get Assistance"):
        if user_input:
            # Placeholder for chatbot response while processing
            with st.spinner("Analyzing your input..."):
                response = analyze_text_with_gemini(user_input)

                if response:
                    st.subheader("Analysis Results")
                    st.write(f"**Gemini AI's Response:** {response}")
                else:
                    st.error("Failed to analyze the text. Please try again.")
        else:
            st.error("Please provide your symptoms or query.")

# Function to analyze text using Google Generative AI SDK
def analyze_text_with_gemini(user_input):
    try:
        # Generation model configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Load the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start the chat session with an empty history
        chat_session = model.start_chat(
            history=[]
        )

        # Send the user's input to the model and get the response
        response = chat_session.send_message(user_input)

        # Return the generated text from the response
        return response.text

    except Exception as e:
        st.error(f"Error analyzing text: {e}")
        return None

if __name__ == "__main__":
    ai_analysis_view()
