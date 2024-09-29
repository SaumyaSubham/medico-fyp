![MediCo Logo](assets/medico_logo(3).png)

# MediCo: AI-Powered Healthcare Platform

## Overview

MediCo is an AI-powered healthcare platform built to bridge the gap between patients and healthcare providers. It provides an intuitive, user-friendly interface where users can interact with a medical AI chatbot, schedule appointments with doctors, and manage their medical history—all in one platform. At the heart of MediCo is the real-time AI chatbot, powered by the Google Gemini API, which enables users to describe their symptoms or ask medical-related queries and receive intelligent responses. The chatbot can suggest possible diagnoses, provide medical advice, or recommend appropriate specialists, making it a valuable tool for preliminary symptom analysis and self-diagnosis. Beyond AI-based assistance, MediCo provides a robust appointment management system where users can browse a list of available doctors, view their profiles, and book appointments based on their health needs. Users also have access to their medical history and prescriptions, allowing for a more personalized healthcare experience.
MediCo is designed to be secure, offering protected user authentication for data privacy. The platform also supports guest mode for limited access, ensuring new users can explore its functionality before creating an account. This makes MediCo a versatile solution for anyone looking to manage their healthcare needs efficiently from the comfort of their home.

**Ready to experience the future of healthcare? Visit MediCo now!**

[https://medico-web.onrender.com/](https://medico-web.onrender.com/) \
**Please note:** While the AI chatbot offers insights and suggestions, it is not a substitute for professional medical advice. Always consult with a qualified healthcare professional for any medical concerns.

## Features

* **AI-Powered Real-Time Chatbot:** Gain medical insights, symptom analysis, and personalized health recommendations powered by the Google Gemini API.
* **Appointment Scheduling:** Schedule appointments with doctors, view appointment history, and receive appointment reminders to stay on top of your healthcare needs.
* **User Authentication:** Secure login, signup, and guest mode for limited access ensure the platform meets your needs.
* **Doctor Listing and Management:** Browse and choose from a curated list of specialists aligned with your health concerns.
* **Profile Management:** Update your medical history, prescriptions, and personal details for a comprehensive healthcare profile.

## Installation

**1. Clone the Repository**

```bash
git clone [https://github.com/your-username/medico.git](https://github.com/your-username/medico.git)
cd medico
```

**2. Create a Virtual Environment**

- Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**   

```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

For securing your passwords or API or other credentials,
Create a .env file in the project root directory and add the following lines, replacing the placeholders with your actual values:   

```.env
MyDB=your_database_name
MyDB_USER=your_database_user
MyDB_PASS=your_database_password
MyDB_PORT=your_PORT
API_KEY=your_api_key
```

**5. Set Up PostgreSQL Database**

Ensure PostgreSQL is installed and running on your machine. Create the necessary tables by running the application once.

**6. Run the Application**

```bash
streamlit run app.py
```
## Usage
MediCo offers a range of features to simplify your healthcare experience:

- User Authentication: Log in if you have an existing account, sign up for a new account to create a full-fledged profile, or use the guest mode to explore the platform's basic functionalities.
- AI Chatbot: Interact with the intelligent AI chatbot to receive real-time symptom analysis through the Google Gemini API.
- Appointment Management: Schedule appointments with doctors, view past and upcoming appointments, and receive automated reminders to stay organized.
- User Profile: Manage your personal information, medical history, and prescriptions in one convenient location.

## Project Structure

```bash
MediCo/
├── assets/                    # Images and static assets
├── .env                       # Environment variables
├── sections/                  # Application sections like auth, profile, AI analysis
├── utils/                     # Utility functions
├── app.py                     # Main application entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Project README file
```


## Technologies Used
- Frontend: Streamlit
- Backend: PostgreSQL, Python
- AI Integration: Google Gemini API
- Deployment: Streamlit Cloud or other hosting services

## Contributions
We welcome contributions to MediCo! Feel free to open a pull request to add features, improve the platform's functionality, or enhance its user experience.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
