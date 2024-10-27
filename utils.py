import os
import streamlit as st
from PIL import Image
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def display_logo():
    try:
        logo = Image.open("assets/medico_logo.png")
    except FileNotFoundError:
        st.error("Logo file not found. Please ensure the path is correct.")
        return
    
    st.markdown(
        """
        <style>
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 250px;
        }
        .logo-container img {
            max-width: 250px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image(logo, width=250)

def connect_db():
    try:
        db_url = urlparse(os.getenv('DATABASE_URL'))
        conn = psycopg2.connect(
            host=db_url.hostname,
            database=db_url.path[1:],
            user=db_url.username,
            password=db_url.password,
            port=db_url.port
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None