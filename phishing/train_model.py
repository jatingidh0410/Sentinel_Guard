import pandas as pd
import numpy as np
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load the dataset
def load_phishing_dataset(csv_path):
    df = pd.read_csv(csv_path)
    return df

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

# Prepare the dataset
def prepare_dataset(df):
    X = np.array([extract_features(url) for url in df['URL']])
    y = df['Label']
    return X, y

# Load data
df = load_phishing_dataset('data/phishing_site_urls.csv')

# Prepare data
X, y = prepare_dataset(df)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42) #, class_weight='balanced'
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='bad')
recall = recall_score(y_test, y_pred, pos_label='bad')
f1 = f1_score(y_test, y_pred, pos_label='bad')

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")

# Save the trained model to a file
model_filename = 'models/random_forest_model.pkl'
joblib.dump(model, model_filename)
print(f"Model saved to {model_filename}")

# Load the model
loaded_model = joblib.load(model_filename)

# Use the loaded model for predictions
# url = "http://example-phishing-site.com"
# features = extract_features(url)
# features = pd.DataFrame([features])
# is_phishing = loaded_model.predict(features)[0]
# print(f"The URL {url} is likely {'a phishing attempt' if is_phishing == 'bad' else 'safe'}")
