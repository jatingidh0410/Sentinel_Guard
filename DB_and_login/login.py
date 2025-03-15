import streamlit as st

# Initialize session state
if all(key not in st.session_state.keys() for key in ('username', 'pwd', 'pwd_correct', 'form_submitted')):
    st.session_state['username'] = ""
    st.session_state['pwd'] = ""
    st.session_state['pwd_correct'] = False
    st.session_state['form_submitted'] = False

# Function to check login credentials
def check_login():
    st.session_state['form_submitted'] = True

    # Validate username and password
    if (
        st.session_state["username"] in st.secrets["passwords"]
        and st.session_state["pwd"] == st.secrets["passwords"][st.session_state["username"]]
    ):
        st.session_state['pwd_correct'] = True
        st.session_state['pwd'] = ""
        st.session_state['username'] = ""
    else:
        st.session_state['pwd_correct'] = False

# Function to display login form
def display_login_form():
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Login Page</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Please enter your credentials to proceed.</p>", unsafe_allow_html=True)

    # Center the form
    form_placeholder = st.empty()
    with form_placeholder.container():
        with st.form("login_form"):
            st.text_input("Username", key="username", placeholder="Enter your username")
            st.text_input("Password", type="password", key="pwd", placeholder="Enter your password")
            st.form_submit_button("Login", on_click=check_login)




# Function to handle logout
def logout():
    
    st.session_state['pwd_correct'] = False
    st.session_state['form_submitted'] = False
    st.session_state['username'] = ""
    st.session_state['pwd'] = ""




# def display_login_form():
#     with st.sidebar:
#         st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Login</h3>", unsafe_allow_html=True)
#         st.markdown("<p style='text-align: center;'>Enter your credentials to proceed.</p>", unsafe_allow_html=True)

#         # Sidebar form
#         with st.form("login_form"):
#             st.text_input("Username", key="username", placeholder="Enter your username")
#             st.text_input("Password", type="password", key="pwd", placeholder="Enter your password")
#             st.form_submit_button("Login", on_click=check_login)
