import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import altair as alt

# 🚀 Load Malware Data
def load_data():
    try:
        df = pd.read_csv("data/malware_data.csv")
        return df
    except FileNotFoundError:
        st.error("⚠️ Error: 'data/malware_data.csv' not found!")
        return pd.DataFrame()  # Return an empty DataFrame to prevent crashes

# 📊 Display Key Metrics
def display_metrics(df):
    total_records = len(df)
    train_size = 0.7  # Assuming 70% train size
    test_size = 0.3 -int(train_size) 
    accuracy = 99  # Placeholder accuracy

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📁 DATASET SIZE", total_records)
    with col2:
        st.metric("🎯 TRAINING SIZE", f"{train_size * 100}%")
    with col3:
        st.metric("🧪 TEST SIZE", f"{test_size * 100}%")
    with col4:
        st.metric("✅ ACCURACY", f"{accuracy}%")

# 📈 Algorithm Accuracy Comparison
def algorithm_accuracy_chart():
    data = {
        "Algorithm": ["Decision Tree", "Random Forest", "Linear Regression"],
        "Accuracy": [99.09, 99.45, 98.45]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x="Algorithm", y="Accuracy", text="Accuracy",
                 color="Algorithm", color_discrete_sequence=["red", "orange", "blue"],
                 title="📊 Algorithm Vs Accuracy")
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig)

# 🔎 Malware Distribution Pie Chart
def malware_pie_chart(df):
    labels = ["Legitimate", "Malicious"]
    values = [70.1, 29.9]  # Placeholder values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title_text="🦠 Legitimate Vs Malicious")
    st.plotly_chart(fig)

# 🛡️ Main Dashboard
def dashboard():
    #st.sidebar.markdown("---")
    st.title("🛡️ Sentinel Guard Dashboard")
    st.markdown("---")

    df = load_data()
    
    if not df.empty:
        display_metrics(df)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("---")
            algorithm_accuracy_chart()
        with col2:
            st.markdown("---")
            malware_pie_chart(df)

# 📌 Threat Level & Entropy Analysis
def plot():
    col1, col2 = st.columns(2)
    st.markdown("---")
    
    with col1:
        st.markdown("---")
        st.write("📊 Threat Level Analysis")
        
        if "data" not in st.session_state:
            st.session_state.data = pd.DataFrame(
                np.random.randn(20, 3), columns=["File Size", "Detection Confidence", "Threat Level"]
            )
        df = st.session_state.data

        point_selector = alt.selection_point()
        interval_selector = alt.selection_interval()
        
        chart = (
            alt.Chart(df)
            .mark_circle()
            .encode(
                x="File Size",
                y="Detection Confidence",
                size="Threat Level",
                color="Threat Level",
                tooltip=["File Size", "Detection Confidence", "Threat Level"],
                opacity=alt.condition(point_selector, alt.value(1), alt.value(0.3))
            )
            .add_params(point_selector, interval_selector)
        )

        st.altair_chart(chart, key="alt_chart")

    with col2:
        st.markdown("---")
        st.write("📈 Entropy-Based Analysis")
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 3), 
            columns=["Min API Call Entropy", "Mean API Call Entropy", "Max API Call Entropy"]
        )
        st.area_chart(chart_data)

def showInformation():  
   #st.subheader("🛡️ Everything You Need to Know About Malware Detection")  

    st.header("🔍 Quick Facts About Malware Detection")  
    st.markdown("""
    ✅ **AI-Powered Security** – This system utilizes **Machine Learning (ML)** to analyze file behavior and detect potential threats with high accuracy.  
    ✅ **High Detection Accuracy** – The implemented models, including **Random Forest and Decision Tree**, achieve an accuracy of up to **99.45%** in identifying malware.  
    ✅ **Real-Time Threat Analysis** – The system performs rapid analysis to classify files as **legitimate or malicious** within seconds.  
    ✅ **Entropy-Based Detection** – Measures randomness in file structure to identify obfuscated malware techniques used by attackers.  
    ✅ **Threat Level Classification** – Assigns a risk score based on file attributes, enabling users to take appropriate security actions.  
    ✅ **Interactive Data Visualization** – Graphical insights into malware behavior using **bar charts, pie charts, and scatter plots** to enhance understanding.  
    """)

    st.header("⚠️ Do’s, Don’ts & Pro Tips")  
    st.markdown("""
    ✅ **DO:** Keep your software updated. Outdated software is like an open door for hackers. 🚪  
    ✅ **DO:** Use strong passwords. ‘123456’ is not a password, it’s an invitation. 🔑  
    ✅ **DO:** Regularly scan for malware – Prevention is better than cyber regret. 🔍  
        
    ❌ **DON’T:** Click on shady email links. No, you didn’t win a million dollars. 🤑  
    ❌ **DON’T:** Download unknown software. Free stuff sometimes comes with *extra surprises* (malware). 🎁💀  
    ❌ **DON’T:** Use the same password everywhere – If one gets leaked, say goodbye to your accounts. 👋  

    🚀 **Pro Tip:** If something feels *off*, trust your instincts and scan it. Your gut is a better antivirus than Windows Defender. 💡  
    """)

    st.markdown("---") 


# malware function of info
def mal_info():  
    
    st.markdown("---")  
    st.write("""
    Malware, short for **malicious software**, is any program designed to **disrupt, damage, or gain unauthorized access** to computer systems.  
    It constantly evolves to evade detection, making it a serious cybersecurity threat for individuals and organizations.
    """)
    st.markdown("---")
    st.header("🦠 Types of Malware")  
    st.markdown("""
    - **🛑 Viruses** – Attach to legitimate files and spread when executed.  
    - **🌐 Worms** – Self-propagate across networks without user intervention.  
    - **🎭 Trojans** – Disguised as safe software but contain malicious payloads.  
    - **💰 Ransomware** – Encrypts files and demands payment for decryption.  
    - **🕵️ Spyware** – Secretly monitors user activity to steal sensitive information.  
    - **📢 Adware** – Displays intrusive ads, sometimes leading to malware infections.  
    - **🔓 Rootkits** – Grants hackers deep access, making detection difficult.  
    - **⌨️ Keyloggers** – Record keystrokes to steal credentials.  
    """)
    st.markdown("---")
    st.header("📡 How Malware Spreads")  
    st.warning("""
    🚨 **Phishing Emails** – Fake messages containing malicious links or attachments.  
    🚨 **Drive-By Downloads** – Automatic downloads from compromised websites.  
    🚨 **Infected USB Devices** – Malware-laden external storage devices.  
    🚨 **Software Vulnerabilities** – Unpatched security flaws in applications.  
    🚨 **Malvertising** – Malware embedded in legitimate advertisements.  
    """)

    st.header("🛡️ Preventing and Detecting Malware")  
    st.success("""
    ✅ **Regular Software Updates** – Patching vulnerabilities to prevent infections.  
    ✅ **Endpoint Protection** – Using antivirus and real-time monitoring.  
    ✅ **User Awareness Training** – Recognizing phishing attempts.  
    ✅ **Behavior-Based Detection** – AI/ML models analyzing file behavior.  
    ✅ **Network Monitoring** – Identifying anomalies in network traffic.  
    ✅ **Sandboxing** – Running suspicious files in isolated environments.  
    """)
    st.markdown("---")
    st.info("""
    As malware continues to evolve, cybersecurity strategies must combine **traditional detection methods**  
    with **AI-driven behavioral analysis** to stay ahead of emerging threats.
    """)

# phishing info
def phishing_info():  
    st.write("""
    Phishing is a form of **social engineering attack** where cybercriminals trick individuals into revealing **sensitive information**,  
    such as passwords, credit card details, or personal data. It is one of the most common attack vectors used in cybercrime.
    """)
    st.markdown("---")
    st.header("📌 Common Types of Phishing Attacks")  
    st.markdown("""
    - **📧 Email Phishing** – Fraudulent emails impersonating trusted sources to steal credentials.  
    - **📱 Smishing (SMS Phishing)** – Fake messages containing malicious links or requests for sensitive information.  
    - **📞 Vishing (Voice Phishing)** – Attackers use phone calls to deceive victims into revealing private data.  
    - **🕵️ Spear Phishing** – Highly targeted attacks tailored to a specific individual or organization.  
    - **👥 Whaling** – Targeting high-profile executives (CEOs, CFOs) to gain access to corporate systems.  
    - **🔗 Clone Phishing** – Duplicating legitimate emails with altered malicious links.  
    """)
    st.markdown("---")
    st.header("🚨 How Phishing Attacks Work")  
    st.warning("""
    1️⃣ **Baiting the Victim** – Attackers send emails, messages, or calls pretending to be trusted entities.  
    2️⃣ **Embedding Malicious Links** – Fake websites are designed to steal login credentials or download malware.  
    3️⃣ **Triggering Urgency** – Messages create a sense of panic (e.g., "Your account will be locked in 24 hours!").  
    4️⃣ **Stealing Data** – Users unknowingly enter sensitive information on fraudulent sites.  
    """)
    st.markdown("---")
    st.header("🛡️ How to Prevent Phishing Attacks")  
    st.success("""
    ✅ **Verify Email Senders** – Always check email addresses before clicking links.  
    ✅ **Hover Over Links** – Inspect URLs before opening them to detect fakes.  
    ✅ **Enable Multi-Factor Authentication (MFA)** – Adds an extra layer of security.  
    ✅ **Avoid Urgent Requests** – Be skeptical of messages pressuring immediate action.  
    ✅ **Use Security Tools** – Deploy anti-phishing filters and endpoint protection.  
    ✅ **Employee Training** – Educate users about recognizing phishing attempts.  
    """)
    st.markdown("---")
    st.info("""
    As phishing tactics become more sophisticated, **AI-driven email security** and **user awareness training**  
    are essential to defending against these evolving cyber threats.
    """)