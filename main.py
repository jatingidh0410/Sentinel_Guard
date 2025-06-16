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
from dark_mode import theme_toggle
from config import check_and_download_models

# Set page config (must be first Streamlit command)
st.set_page_config(page_title="Sentinel Guard", layout="wide")

# Custom CSS for malware detection results
st.markdown("""
<style>
    .legitimate {
        color: #00FF00 !important;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .malware {
        color: #FF0000 !important;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # First check and download models if needed
    if not check_and_download_models():
        st.error("Failed to download required model files. The app cannot continue.")
        st.stop()
        
    # Apply theme toggle (must be before any other content)
    theme_toggle()
    
    # Initialize session state variables
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
    if not st.session_state['pwd_correct']:
        if st.session_state["form_submitted"]:
            display_login_form()
            st.sidebar.error("Invalid username or password. Please try again.")
        else:
            display_login_form()
    else:
        st.sidebar.success(f"Login Successful! Welcome, {st.session_state['username']}!")
    
    st.sidebar.markdown("---")
    
    # Allow navigation if logged in
    if st.session_state['pwd_correct']:
        selection = st.sidebar.radio("Go to", ["Dashboard", "Malware Detection", "Phishing Detection"])
        st.sidebar.markdown("---")
        
        # Display logout button
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()  # Refresh the page to show login form
    else:
        selection = None
    
    # Main content area
    if st.session_state['pwd_correct']:
        if selection == "Dashboard":
            dashboard.dashboard()
            dashboard.plot()
            dashboard.showInformation()
            
        elif selection == "Malware Detection":
            st.title("Malware Detection")
            st.markdown("---")
            file = st.file_uploader("Upload a file to check for malware:", 
                                  accept_multiple_files=True, 
                                  key="file_uploader",
                                  help="Upload one or more files to scan for potential malware")
            
            if file:
                with st.spinner("Analyzing..."):
                    for i in file:
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(i.getvalue())
                            temp_file_path = temp_file.name
                        
                        try:
                            legitimate = checkFile(temp_file_path)
                            
                            if legitimate:
                                st.markdown(f'<p class="legitimate">✓ File {i.name} seems LEGITIMATE!</p>', 
                                            unsafe_allow_html=True)
                            else:
                                st.markdown(f'<p class="malware">⚠️ File {i.name} is probably MALWARE!!!</p>', 
                                           unsafe_allow_html=True)
                        finally:
                            # Ensure the temporary file is deleted
                            try:
                                os.unlink(temp_file_path)
                            except:
                                pass

            dashboard.mal_info()   
                        
        elif selection == "Phishing Detection":
            st.title("Phishing Detection")
            st.markdown("---")
            
            url = st.text_input("Enter a URL to check:", 
                               key="phishing_url", 
                               placeholder="https://example.com",
                               help="Enter the URL you want to check for phishing")
            
            if st.button("Check URL"):
                if url:
                    with st.spinner("Analyzing..."):
                        is_phishing = checkPhishing(url)
                        if is_phishing:
                            st.error(f"⚠️ The URL {url} is likely a PHISHING attempt!!!")
                        else:
                            st.success(f"✓ The URL {url} seems SAFE!")
                else:
                    st.warning("Please enter a URL to check")

            dashboard.phishing_info()
        
    else:
        st.info("Please log in to access the detection tools.")

if __name__ == "__main__":
    main()