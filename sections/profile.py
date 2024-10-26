import streamlit as st
import psycopg2
import os
import datetime
from utils import display_logo
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("MyDB_HOST"),  # Your PostgreSQL server's address
            database=os.getenv("MyDB"),  # Your DB name
            user=os.getenv("MyDB_USER"),  # Your DB username
            password=os.getenv("MyDB_PASS"),  # Your DB password
            port=os.getenv("MyDB_PORT"),  # Your DB port
            sslmode="require"
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Create user profile table if it doesn't exist
def create_user_profile_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                email VARCHAR(255),
                medical_history TEXT,
                prescriptions TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        st.error(f"Error creating user_profiles table: {e}")

# Create appointments table if it doesn't exist
def create_appointments_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                doctor VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Scheduled',
                FOREIGN KEY (username) REFERENCES user_profiles (username) ON DELETE CASCADE
            )
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        st.error(f"Error creating appointments table: {e}")

# Function to fetch user profile information
def fetch_user_profile(username):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT name, email, medical_history, prescriptions, last_updated
                FROM user_profiles
                WHERE username = %s
            """, (username,))
            profile = cur.fetchone()
            cur.close()
            
            # Ensure five elements by filling in None for any missing values
            if profile is None:
                return ("", "", "", "", None)
            return profile + (None,) * (5 - len(profile))
        except Exception as e:
            st.error(f"Error fetching user profile: {e}")
            return None
        finally:
            conn.close()
    return None

# Function to insert or update user profile information
def update_user_profile(username, name, email, medical_history, prescriptions):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_profiles (username, name, email, medical_history, prescriptions, last_updated)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (username) DO UPDATE
                SET medical_history = EXCLUDED.medical_history, prescriptions = EXCLUDED.prescriptions
            """, (username, name, email, medical_history, prescriptions))
            conn.commit()
            cur.close()
            st.success("Profile updated successfully!")
        except Exception as e:
            st.error(f"Error updating profile: {e}")
        finally:
            conn.close()

# Function to check if the user can update name and email
def can_update_name_email(last_updated):
    if last_updated:
        days_passed = (datetime.datetime.now() - last_updated).days
        return days_passed >= 20
    return True

# Function to fetch user's appointment history
def fetch_user_appointments(username):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT appointment_date, appointment_time, doctor, status 
                FROM appointments 
                WHERE username = %s 
                ORDER BY appointment_date, appointment_time ASC
            """, (username,))
            appointments = cur.fetchall()
            cur.close()
            return appointments
        except Exception as e:
            st.error(f"Error fetching appointments: {e}")
            return []
        finally:
            conn.close()
    return []

# Profile Page to display user information and appointment history
def profile_page():
    # Connect to the database and create the necessary tables
    conn = connect_db()
    if conn:
        create_user_profile_table(conn)
        create_appointments_table(conn)  # Make sure this line is here
        conn.close()

    # Display the logo
    display_logo()

    if 'username' in st.session_state:
        username = st.session_state['username']

        # Fetch user profile data
        profile = fetch_user_profile(username)

        if profile and len(profile) == 5:
            name, email, medical_history, prescriptions, last_updated = profile
        else:
            st.info("No profile information found or incomplete data. Please update your details.")
            name, email, medical_history, prescriptions, last_updated = "", "", "", "", None

        # Check if the user can update name and email
        allow_name_email_update = can_update_name_email(last_updated)

        # Profile form for updating details
        st.subheader(f"User Profile: {username}")
        name = st.text_input("Name", value=name, disabled=not allow_name_email_update)
        email = st.text_input("Email", value=email, disabled=not allow_name_email_update)
        medical_history = st.text_area("Medical History", value=medical_history)
        prescriptions = st.text_area("Prescriptions", value=prescriptions)

        # Notify user when they can update name and email
        if not allow_name_email_update:
            days_left = 20 - (datetime.datetime.now() - last_updated).days
            st.info(f"You can update your name and email in {days_left} days.")

        # Save profile data
        if st.button("Update Profile"):
            update_user_profile(username, name, email, medical_history, prescriptions)

        # Fetch and display the user's appointment history
        appointments = fetch_user_appointments(username)
        if appointments:
            st.subheader("Appointment Schedule/History")
            for appointment in appointments:
                appointment_date, appointment_time, doctor, status = appointment
                if status == 'Scheduled':
                    st.markdown(f"**Upcoming Appointment**: {appointment_date} at {appointment_time} with Dr. {doctor} - Status: {status}")
                else:
                    st.markdown(f"**Past Appointment**: {appointment_date} at {appointment_time} with Dr. {doctor} - Status: {status}")
        else:
            st.info("You have no appointments scheduled.")

        if st.button("Logout"):
            st.session_state.clear()
            st.success("You have logged out!")
    else:
        st.warning("Please login to view your profile.")
