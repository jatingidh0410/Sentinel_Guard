import streamlit as st

dark_mode_css = """
<style>
    /* Dark Mode Styles */
    :root {
        --primary-color: #BF00FF;
        --secondary-color: #FF007F;
        --accent-color: #00FFFF;
    }
    
    /* Base styles */
    body, .main, .block-container, .stApp {
        background-color: #121212 !important;
        color: #EAEAEA !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0D0D0D !important;
    }
    
    /* All text elements */
    body, .main, [data-testid="stSidebar"], .block-container, 
    p, h1, h2, h3, h4, h5, h6, div, span, label, a, 
    .stRadio, .stSelectbox, .stTextInput, .stTextArea, 
    .stButton, .stFileUploader, .stNumberInput, 
    .stSlider, .stCheckbox, .stDateInput, .stTimeInput {
        color: #EAEAEA !important;
    }
    
    /* Input fields */
    .stTextInput input, input, select, textarea {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 2px solid var(--accent-color) !important;
    }
</style>
"""

light_mode_css = """
<style>
    /* Light Mode Styles */
    :root {
        --primary-color: #6A0DAD;
        --secondary-color: #D10068;
        --accent-color: #007BFF;
    }
    
    /* Base styles */
    body, .main, .block-container, .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8F8F8 !important;
    }
    
    /* All text elements */
    body, .main, [data-testid="stSidebar"], .block-container, 
    p, h1, h2, h3, h4, h5, h6, div, span, label, a, 
    .stRadio, .stSelectbox, .stTextInput, .stTextArea, 
    .stButton, .stFileUploader, .stNumberInput, 
    .stSlider, .stCheckbox, .stDateInput, .stTimeInput {
        color: #111111 !important;
    }
    
    /* Input fields */
    .stTextInput input, input, select, textarea {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 2px solid var(--accent-color) !important;
    }
</style>
"""

def theme_toggle():
    # Initialize session state for theme if not exists
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True  # Default to dark mode
    
    # Theme toggle radio button
    mode = st.sidebar.radio(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.dark_mode else 1,  # Set index based on current mode
        horizontal=True,
        label_visibility="visible"
    )
    
    # Custom styling for the toggle
    st.markdown("""
    <style>
        /* Theme toggle container */
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            background-color: transparent !important;
            border: 1px solid var(--border-color, #666) !important;
            padding: 5px 10px !important;
            border-radius: 8px !important;
            margin-bottom: 15px !important;
        }
        
        /* Radio button labels */
        [data-testid="stSidebar"] .stRadio label {
            margin-bottom: 0 !important;
            padding: 5px 10px !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Apply the selected theme
    if mode == "Dark":
        st.session_state.dark_mode = True
        st.markdown(dark_mode_css, unsafe_allow_html=True)
    else:
        st.session_state.dark_mode = False
        st.markdown(light_mode_css, unsafe_allow_html=True)