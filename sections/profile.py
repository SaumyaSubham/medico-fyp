import streamlit as st
import psycopg2
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
            database=os.getenv("MyDB"),  #Your DataBase Name
            user=os.getenv("MyDB_USER"),  # Replace with your DB username
            password=os.getenv("MyDB_PASS"),  # Replace with your DB password
            port=os.getenv("MyDB_PORT")  # Or the port you're using
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Create appointment table if it doesn't exist
def create_appointment_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                doctor VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Scheduled'
            )
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        st.error(f"Error creating appointments table: {e}")

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
    # Display the logo
    display_logo()

    # Ensure the user is logged in
    if 'username' in st.session_state:
        username = st.session_state['username']
        
        # Display basic user profile information
        st.subheader(f"User Profile: {username}")
        st.text("Name: John Doe")  # You can fetch this dynamically later if needed
        st.text("Email: johndoe@example.com")  # Same for email
        st.text("Medical History: Asthma, Hypertension")
        st.text("Prescriptions: XYZ Medication")

        # Fetch and display the user's appointment history/schedule
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
            st.info("No appointment history or upcoming appointments.")

        # Logout option
        if st.button("Logout"):
            st.session_state.clear()  # Clear the session state to log out
            st.success("You have logged out!")
    else:
        st.warning("Please login to view your profile.")
