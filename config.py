import os
import requests
from pathlib import Path
import streamlit as st

# Model configuration
MODEL_FILES = {
    "features.pkl": "1M7Z1VxwhKecCowpTNajY7a6N1nuw2P0M",
    "model.pkl": "1L3jE4j-MfrtOfdtULxG9T4zG1U_vQbe9",
    "random_forest_model.pkl": "1cNXP_0KPJ8bkQmcVI2AUKhWfhptwoV-7"
}

def download_file_from_google_drive(file_id, destination):
    """Download a file from Google Drive given its file ID"""
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    save_response_content(response, destination)

def get_confirm_token(response):
    """Get confirmation token for large files"""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    """Save the downloaded content to a file"""
    CHUNK_SIZE = 32768
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def check_and_download_models():
    """Check if models exist and download if missing"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    for filename, file_id in MODEL_FILES.items():
        file_path = models_dir / filename
        if not file_path.exists():
            try:
                with st.spinner(f"Downloading {filename}..."):
                    download_file_from_google_drive(file_id, file_path)
                    st.success(f"Downloaded {filename}")
            except Exception as e:
                st.error(f"Failed to download {filename}: {str(e)}")
                return False
    return True