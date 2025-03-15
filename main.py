import os
import time
import tempfile
from malware.file_checker import checkFile
import streamlit as st
import pandas as pd
import plotly.express as px
from phishing.model import checkPhishing
from DB_and_login.login import display_login_form, check_login, logout
import DB_and_login.dashboard as dashboard

st.set_page_config(page_title="Sentinel Guard", layout="wide")

# ✅ Apply custom styles (Center headers + Blue theme)
st.markdown(
    """
    <style>
        /* Main Title */
        h1 {
            text-align: center;
            color: #BF00FF; /* Electric Purple */
            font-size: 2.8rem;
            font-weight: bold;
        }

        /* Subheaders */
        h2 {
            text-align: center;
            color: #FF007F; /* Bright Magenta */
            font-size: 2.2rem;
        }

        /* General text */
        body, p, label, span {
            color: #EAEAEA !important; /* Soft White */
        }

        /* Buttons - Neon Gradient */
        button {
            background: linear-gradient(135deg, #FF007F, #00BFFF) !important; /* Magenta to Blue */
            color: #FFFFFF !important;
            border-radius: 8px;
            padding: 12px 18px;
            border: none;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
            text-transform: uppercase;
        }
        button:hover {
            background: linear-gradient(135deg, #00BFFF, #FF007F) !important;
            transform: scale(1.07);
            box-shadow: 0px 0px 15px rgba(255, 0, 127, 0.8);
        }
        
        /* Input Fields */
        input, select, textarea {
            background-color: #222222 !important;
            color: #FFFFFF !important;
            border: 2px solid #00FFFF;
            padding: 10px;
            border-radius: 6px;
            transition: 0.3s;
        }
        input:focus, select:focus, textarea:focus {
            border-color: #FF007F !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0D0D0D !important;
        }

        /* Links */
        a {
            color: #00FFFF !important;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            color: #FF007F !important;
            text-decoration: underline;
        }
        #color of malware
        
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    # Ensure session state variables are initialized
    if 'pwd_correct' not in st.session_state:
        st.session_state['pwd_correct'] = False
    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ""
    if 'pwd' not in st.session_state:
        st.session_state['pwd'] = ""
    if 'uploaded_data' not in st.session_state:
        st.session_state['uploaded_data'] = None
    
    # Sidebar for navigation and login
    st.sidebar.title("Navigation & Login")
    # Display login form if not logged in
    if not st.session_state['pwd_correct'] and not st.session_state['form_submitted']:
        display_login_form()
    elif not st.session_state['pwd_correct'] and st.session_state["form_submitted"]:
        display_login_form()
        st.sidebar.error("Invalid username or password. Please try again.")
    else:
        st.sidebar.success("Login Successful! Welcome, user!")
    st.sidebar.markdown("---")
    # Allow navigation if logged in
    if st.session_state['pwd_correct']:
        selection = st.sidebar.radio("Go to", ["Dashboard", "Malware Detection", "Phishing Detection"])
        st.sidebar.markdown("---")
    else:
        selection = None
    
    
    # Display logout button if logged in
    if st.session_state['pwd_correct']:
        
        if st.sidebar.button("Logout"):
            logout()
            st.sidebar.write("You have been logged out.")
    
    # Main logic for navigation
    if st.session_state['pwd_correct']:
        if selection == "Dashboard":
            dashboard.dashboard()
            dashboard.plot()
            dashboard.showInformation()
            
        elif selection == "Malware Detection":
            st.title("Malware Detection")
            st.markdown("---")
            file = st.file_uploader("Upload a file to check for malwares:", accept_multiple_files=True, key="file_uploader")
            
            if file:
                with st.spinner("Analyzing..."):
                    for i in file:
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(i.getvalue())
                            temp_file_path = temp_file.name
                        
                        # Ensure the file is properly closed and checked
                        with open(temp_file_path, 'rb') as temp_file:
                            legitimate = checkFile(temp_file.name)
                        
                        # Retry deleting the file to handle access issues
                        retries = 5
                        while retries > 0:
                            try:
                                os.remove(temp_file_path)
                                break
                            except PermissionError:
                                time.sleep(0.5)
                                retries -= 1
                        
                        if legitimate:
                            st.markdown(f'<p class="legitimate">File {i.name} seems LEGITIMATE!</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<p class="malware">File {i.name} is probably MALWARE!!!</p>', unsafe_allow_html=True)
                    #st.write("Content for Malware Detection goes here...")
            dashboard.mal_info()        
        
        elif selection == "Phishing Detection":
            st.title("Phishing Detection")
            st.markdown("---")
            #st.write("Phishing attacks can trick you into revealing personal information. Use this tool to check if a URL might be a phishing attempt.")
            url = st.text_input("Enter a URL to check:", key="phishing_url", help="Enter the URL you want to check for phishing")
            if url:
                with st.spinner("Analyzing..."):
                    is_phishing = checkPhishing(url)
                    if is_phishing:
                        st.error(f"The URL {url} is likely a PHISHING attempt!!!")
                    else:
                        st.success(f"The URL {url} seems SAFE!")

            dashboard.phishing_info()
        
    else:
        st.write("Please log in to access the detection tools.")

if __name__ == "__main__":
    main()
