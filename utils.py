import streamlit as st
from PIL import Image

def display_logo():
    # MediCo Logo (replace 'assets/medico_logo.png' with the correct path to your logo)
    try:
        logo = Image.open("assets/medico_logo.png")  # Correct path to your logo
    except FileNotFoundError:
        st.error("Logo file not found. Please ensure the path is correct.")
        return
    
    # Display the logo using st.image() for proper handling in Streamlit
    st.markdown(
        """
        <style>
        /* Make sure the logo is always displayed in a fixed size */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 250px;  /* Adjusted height */
        }

        .logo-container img {
            max-width: 250px;  /* Adjusted width to be larger */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Use st.image to ensure the image is properly loaded
    st.image(logo, width=250)  # Adjusted width for a larger logo
