import streamlit as st
from PIL import Image
from utils import display_logo

def about_page():
    
    # Display the logo
    display_logo()

    # Description of MediCo
    st.markdown("""
    ## What MediCo Brings for Us
    
    MediCo is an advanced AI-powered healthcare platform designed to provide accurate medical insights and support for individuals seeking reliable online healthcare. 
    Whether it's diagnosing health conditions, monitoring regular check-ups, or ensuring medication adherence, MediCo offers personalized health analysis and recommendations through cutting-edge AI technology.
    
    ### Key Features:
    - **AI Analysis**: Upload medical images for detailed AI-driven analysis.
    - **User Profiles**: Manage your medical history and track analysis results.
    - **Appointment Scheduling**: Schedule consultations with medical professionals directly from the platform.
    
    MediCo is your trusted companion for managing your health with modern technology.
    """)

# Call the page function
about_page()
