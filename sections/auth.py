import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import bcrypt
import os
from utils import display_logo
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",  # Or your PostgreSQL server's address
            database=os.getenv("MyDB"),
            user=os.getenv("MyDB_USER"),  # Replace with your DB username
            password=os.getenv("MyDB_PASS"),  # Replace with your DB password
            port=os.getenv("MyDB_PORT")  # Or the port you're using
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Create user table if it doesn't exist
def create_user_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        st.error(f"Error creating users table: {e}")

# Function to add a new user to the database
def add_user(username, password):
    conn = connect_db()
    if conn:
        create_user_table(conn)
        try:
            cur = conn.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
            conn.commit()
            cur.close()
            st.success(f"Account created for {username}")
        except Exception as e:
            st.error(f"Error adding user: {e}")
        finally:
            conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = connect_db()
    if conn:
        create_user_table(conn)
        try:
            cur = conn.cursor()
            cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            if result:
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Logged in as {username}")
                else:
                    st.error("Incorrect password")
            else:
                st.error("Username not found")
            cur.close()
        except Exception as e:
            st.error(f"Error authenticating user: {e}")
        finally:
            conn.close()

def login_page():
    # Display the logo
    display_logo()

    st.title("Choose Authentication Method")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
   
    
    # Use option_menu for authentication options with icons
    option = option_menu(
    menu_title= None,  # Optional title
    options=["Login", "Signup", "Guest Mode"],  # Menu options
    icons=["person", "person-plus", "person-circle"],  # Corresponding icons
    default_index=0,  # Default selected option
    styles={
        "container": {"padding": "0px", "background-color": "#2c2f33"},  # Darker background
        "icon": {"color": "white", "font-size": "18px"},  # Icons styling
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "color": "#4CAF50"},
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    }
    )

    if option == "Login":
        login_form()
    elif option == "Signup":
        signup_form()
    else:
        guest_mode()

def login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        authenticate_user(username, password)

def signup_form():
    st.subheader("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if password == confirm_password:
            add_user(username, password)
        else:
            st.error("Passwords do not match")

def guest_mode():
    st.session_state['logged_in'] = True
    st.session_state['username'] = "Guest"
    st.success("Guest mode activated! You have limited access.")
