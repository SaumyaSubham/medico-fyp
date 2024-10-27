import streamlit as st
from streamlit_option_menu import option_menu
import bcrypt
from utils import display_logo, connect_db

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
    display_logo()

    st.title("Choose Authentication Method")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
   
    option = option_menu(
    menu_title= None,
    options=["Login", "Signup", "Guest Mode"],
    icons=["person", "person-plus", "person-circle"],
    default_index=0,
    styles={
        "container": {"padding": "0px", "background-color": "#2c2f33"},
        "icon": {"color": "white", "font-size": "18px"},
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

if __name__ == "__main__":
    login_page()