import streamlit as st 
import datetime
from utils import display_logo, connect_db

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
            return profile
        except Exception as e:
            st.error(f"Error fetching user profile: {e}")
            return None
        finally:
            conn.close()
    return None

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

def can_update_name_email(last_updated):
    if last_updated:
        days_passed = (datetime.datetime.now() - last_updated).days
        return days_passed >= 20
    return True

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

def profile_page():
    conn = connect_db()
    if conn:
        create_user_profile_table(conn)
        create_appointments_table(conn)
        conn.close()

    display_logo()

    if 'username' in st.session_state:
        username = st.session_state['username']

        profile = fetch_user_profile(username)

        if profile:
            name, email, medical_history, prescriptions, last_updated = profile
        else:
            st.info("No profile information found. Please update your details.")
            name, email, medical_history, prescriptions, last_updated = "", "", "", "", None

        allow_name_email_update = can_update_name_email(last_updated)

        st.subheader(f"User Profile: {username}")
        name = st.text_input("Name", value=name, disabled=not allow_name_email_update)
        email = st.text_input("Email", value=email, disabled=not allow_name_email_update)
        medical_history = st.text_area("Medical History", value=medical_history)
        prescriptions = st.text_area("Prescriptions", value=prescriptions)

        if not allow_name_email_update:
            days_left = 20 - (datetime.datetime.now() - last_updated).days
            st.info(f"You can update your name and email in {days_left} days.")

        if st.button("Update Profile"):
            update_user_profile(username, name, email, medical_history, prescriptions)

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

if __name__ == "__main__":
    profile_page()