import streamlit as st
from datetime import datetime
from utils import display_logo
import os




def scheduler_page():
    # Check if the user is logged in
    if not st.session_state.get('logged_in', False):
        display_logo()
        st.warning("Please log in, sign up, or activate guest mode to use this service.")
        return

    # Display the logo at the top
    display_logo()
    st.subheader("Schedule a Medical Appointment")

    # List of doctors with their descriptions and image paths
    doctors = [
        {"name": "Dr. Rahul Mehta", "description": "A leading cardiologist with 15 years of experience, specializing in heart disease treatment. Expert in interventional cardiology, including angioplasty and pacemaker implantation. Renowned for research in heart failure management.", "image": "assets/doctor.png", "role": "Cardiologist"},
        {"name": "Dr. Ananya Basu", "description": "A renowned dermatologist with over 10 years of experience. She specializes in treating acne, psoriasis, and eczema, as well as cosmetic dermatology, including skin rejuvenation and laser treatments.", "image": "assets/doctor(1).png", "role": "Dermatologist"},
        {"name": "Dr. Priya Verma", "description": "A compassionate pediatrician with over 8 years of experience, specializing in child development and adolescent health. Known for her gentle approach and dedication to preventive care.", "image": "assets/doctor(2).png", "role": "Pediatrician"},
        {"name": "Dr. Amit Sinha", "description": "An accomplished neurologist with over 10 years of experience. He specializes in treating epilepsy, Parkinson’s disease, and strokes, and is skilled in neuroimaging and neurosurgical techniques.", "image": "assets/doctor(3).png", "role": "Neurologist"},
        {"name": "Dr. Neha Ahuja", "description": "A respected gynecologist with over 15 years of experience. She specializes in high-risk pregnancies, infertility treatments, and menstrual disorders, and advocates for women’s health awareness and education.", "image": "assets/doctor(4).png", "role": "Gynecologist"},
        {"name": "Dr. Vikram Nair", "description": "An orthopedic surgeon with over 12 years of experience. He specializes in joint replacements and sports injuries, and is skilled in minimally invasive surgery.", "image": "assets/doctor(5).png", "role": "Orthopedic surgeon"}
    ]

    # Doctor selection
    doctor_names = [doc['name'] for doc in doctors]
    selected_doctor = st.selectbox("Select Doctor", doctor_names)

    # Date and time selection
    date = st.date_input("Select Date", min_value=datetime.now().date())
    time = st.time_input("Select Time")

    # Confirm appointment
    if st.button("Confirm Appointment"):
        st.success(f"Appointment scheduled with {selected_doctor} on {date} at {time}")

    # Display doctors list below the appointment confirmation
    st.write("### Meet Our Doctors")

    # Loop through doctors in sets of 3 per row using Streamlit's columns
    for i in range(0, len(doctors), 3):
        cols = st.columns(3, gap="large")
        for idx, col in enumerate(cols):
            if i + idx < len(doctors):
                doctor = doctors[i + idx]
                with col:
                    col.image(doctor["image"], width=150, caption=f"{doctor['role']}", use_column_width=False)
                    col.markdown(f"<h4 style='text-align: center;'>{doctor['name']}</h4>", unsafe_allow_html=True)
                    col.write(doctor["description"])
                    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
