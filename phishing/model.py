import joblib
import pandas as pd
from urllib.parse import urlparse

# Load the trained model
model_filename = 'models/random_forest_model.pkl'
model = joblib.load(model_filename)

# Extract features from URLs
def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    url_length = len(url)
    special_chars = sum([url.count(c) for c in ['@', '-', '_', '.', '/', ':']])
    subdomains = domain.count('.')
    https = 1 if parsed_url.scheme == 'https' else 0
    domain_length = len(domain)
    digits = sum(c.isdigit() for c in url)
    keywords = sum(1 for keyword in ['login', 'verify', 'bank', 'account'] if keyword in url.lower())
    return [url_length, special_chars, subdomains, https, domain_length, digits, keywords]

# Check if URL is phishing
def checkPhishing(url):
    features = extract_features(url)
    features = pd.DataFrame([features])
    is_phishing = model.predict(features)[0]
    print(f"Model Output: {is_phishing}")  # Print to verify output
    return is_phishing == 'good'  # If 'bad' represents phishing
