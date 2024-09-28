# import streamlit as st
# from streamlit_option_menu import option_menu
# from sections.about import about_page
# from sections.auth import login_page
# from sections.ai_analysis import ai_analysis_view
# from sections.profile import profile_page
# from sections.appointment import scheduler_page
# import base64

# # Set Page Configurations (Optional)
# # st.set_page_config(page_title="MediCo", layout="centered")

# # Read the MediCo logo and convert it to base64
# file_path = "assets/medico_logo(3).png"
# with open(file_path, "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode()

# # Sidebar logo display with round border
# st.sidebar.markdown(
#     f"""
#     <style>
#     .sidebar-logo img {{
#         border-radius: 50%;
#         border: 3px solid #4CAF50; /* Optional: Add a border color */
#         display: block;
#         margin-left: auto;
#         margin-right: auto;
#     }}
#     </style>
#     <div class="sidebar-logo">
#         <img src="data:image/png;base64,{encoded_string}" alt="MediCo Logo" style="width: 150px;">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Streamlit App Sidebar Navigation
# st.sidebar.title("MediCo")
# menu = st.sidebar.selectbox(
#     "Select a page",
#     ["About", "Login", "AI Assistant", "User Profile", "Schedule Appointment"]
# )

# # Custom CSS to fix the cursor issue and prevent contenteditable in the dropdown
# st.markdown(
#     """
#     <style>
#     .stSelectbox div[contenteditable="true"] {
#         caret-color: transparent !important;
#     }

#     /* Set cursor to pointer for the dropdown */
#     .stSelectbox div {
#         cursor: pointer !important;
#     }

#     /* Override Streamlit's internal styling that turns dropdown into contenteditable */
#     .stSelectbox [contenteditable="true"] {
#         pointer-events: none !important;
#         caret-color: transparent !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Centralized Placeholder for Page Content
# content_placeholder = st.container()

# # Navigation Logic with Single Placeholder
# def render_page(menu_selection):
#     content_placeholder.empty()  # Clear previous content
#     with content_placeholder:
#         if menu_selection == "About":
#             about_page()
#         elif menu_selection == "Login":
#             login_page()
#         elif menu_selection == "AI Assistant":
#             ai_analysis_view()
#         elif menu_selection == "User Profile":
#             profile_page()
#         elif menu_selection == "Schedule Appointment":
#             scheduler_page()

# # Render the selected page
# render_page(menu)



import streamlit as st
from streamlit_option_menu import option_menu
from sections.about import about_page
from sections.auth import login_page
from sections.ai_analysis import ai_analysis_view
from sections.profile import profile_page
from sections.appointment import scheduler_page
import base64

# Set Page Configurations (Optional)
# st.set_page_config(page_title="MediCo", layout="centered")

def display_sidebar_logo():
    file_path = "assets/medico_logo(3).png"  # Adjust the path to your logo file
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.sidebar.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{encoded_string}" alt="MediCo Logo" style="
                width:130px; 
                height:130px; 
                border-radius:50%; 
                border: 4px solid #4CAF50;
                margin-bottom: 20px;  /* Space between logo and menu */
            ">
        </div>
        """,
        unsafe_allow_html=True
    )

# Call the function to display the logo
display_sidebar_logo()

# Sidebar Navigation
with st.sidebar:
    menu = option_menu(
        menu_title="MediCo",  # Menu title
        options=["About", "Login", "AI Assistant", "User Profile", "Schedule Appointment"],  # Options
        default_index=0,  # Start on the first option
        icons=["info-circle", "person", "robot", "person", "calendar"],  # FontAwesome Unicode icons
        styles={
            "container": {"padding": "5px", "background-color": "#333"},
            "nav-link": {
                "font-size": "16px",
                "margin": "10px 0",
                "padding": "10px",
                "border-radius": "4px",
                "color": "#f0f0f0",
                "--hover-color": "#4CAF50",
            },
            "nav-link-selected": {
                "background-color": "#4CAF50",
                "color": "white",
                "font-weight": "bold",
                "border-radius": "8px",
            },
        },
    )
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 330px;
        min-width: 330px;
        max-width: 330px;
        background-color: #333;  /* Dark sidebar */
    }
    /* Lock cursor to default within the sidebar */
    .css-1d391kg {
        cursor: default !important;
    }
    /* Prevent col-resize on hover */
    div[data-testid="stSidebar"] {
        cursor: default !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Centralized Placeholder for Page Content
content_placeholder = st.container()

# Navigation Logic with Single Placeholder
def render_page(menu_selection):
    content_placeholder.empty()  # Clear previous content
    with content_placeholder:
        if menu_selection == "About":
            about_page()
        elif menu_selection == "Login":
            login_page()
        elif menu_selection == "AI Assistant":
            ai_analysis_view()
        elif menu_selection == "User Profile":
            profile_page()
        elif menu_selection == "Schedule Appointment":
            scheduler_page()

# Render the selected page
render_page(menu)









