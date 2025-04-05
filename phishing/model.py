import joblib
import pandas as pd
from urllib.parse import urlparse
import os
from pathlib import Path
import sys

# Constants
MODEL_FILENAME = 'random_forest_model.pkl'
MODEL_DIR = 'models'
FEATURE_NAMES = [
    'url_length', 
    'special_chars', 
    'subdomains',
    'https', 
    'domain_length', 
    'digits', 
    'keywords'
]
PHISHING_KEYWORDS = ['login', 'verify', 'bank', 'account', 'secure', 'update']

class PhishingDetector:
    def __init__(self):
        self.model = self._load_model()
        self._verify_model_labels()
    
    def _load_model(self):
        """Safely load the trained model with error handling"""
        try:
            model_path = Path(__file__).parent.parent / MODEL_DIR / MODEL_FILENAME
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")

            model = joblib.load(model_path)
            
            if not hasattr(model, 'predict'):
                raise ValueError("Loaded object is not a valid scikit-learn model")
                
            print(f"Successfully loaded model from {model_path}")
            return model
            
        except Exception as e:
            print(f"Error loading model: {str(e)}", file=sys.stderr)
            return None
    
    def _verify_model_labels(self):
        """Verify and print model's class labels for debugging"""
        if self.model and hasattr(self.model, 'classes_'):
            print(f"Model class labels: {self.model.classes_}")
    
    def extract_features(self, url):
        """Extract phishing detection features from URL"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            features = [
                len(url),  # Longer URLs more suspicious
                sum(url.count(c) for c in ['@','-','_','.','/',':','?','=']),  # More special chars = more suspicious
                domain.count('.'),  # More subdomains = more suspicious
                1 if parsed_url.scheme == 'https' else 0,  # HTTPS is safer
                len(domain),  # Longer domains more suspicious
                sum(c.isdigit() for c in url),  # More digits more suspicious
                sum(1 for kw in PHISHING_KEYWORDS if kw in url.lower())  # More keywords more suspicious
            ]
            
            if len(features) != len(FEATURE_NAMES):
                raise ValueError(f"Expected {len(FEATURE_NAMES)} features, got {len(features)}")
                
            return features
            
        except Exception as e:
            print(f"Feature extraction failed: {str(e)}", file=sys.stderr)
            raise
    
    def check_phishing(self, url):
        """
        Check if URL is phishing
        Returns: False if safe, True if phishing (reversed logic for better intuition)
        """
        try:
            if self.model is None:
                return self._fallback_check(url)
                
            features = self.extract_features(url)
            features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
            
            # Get both prediction and probability for better confidence
            prediction = self.model.predict(features_df)[0]
            proba = self.model.predict_proba(features_df)[0] if hasattr(self.model, 'predict_proba') else None
            
            # Debug information
            print("\nURL:", url)
            print("Features:", dict(zip(FEATURE_NAMES, features)))
            print("Prediction:", prediction)
            if proba is not None:
                print("Probability:", {k: f"{v:.2%}" for k, v in zip(self.model.classes_, proba)})
            
            # Handle different label formats and return True for phishing, False for safe
            if isinstance(prediction, str):
                return prediction.lower() in ['phishing', 'bad', 'malicious']
            else:  # numeric
                # Assuming higher number means more likely phishing
                return prediction >= 1 if len(self.model.classes_) > 1 else prediction > 0.5
                
        except Exception as e:
            print(f"Phishing check failed for {url}: {str(e)}", file=sys.stderr)
            return False  # Default to safe if error occurs
    
    def _fallback_check(self, url):
        """Basic heuristics when model isn't available"""
        url_lower = url.lower()
        suspicious = (
            len(url) > 75 or  # Long URLs
            sum(c.isdigit() for c in url) > 5 or  # Many numbers
            any(kw in url_lower for kw in PHISHING_KEYWORDS) or  # Suspicious keywords
            not url.startswith('https') or  # Not HTTPS
            url.count('.') > 3  # Many subdomains
        )
        return suspicious

# Initialize detector
phishing_detector = PhishingDetector()

# Public interface
def checkPhishing(url):
    """Public interface for phishing detection
    Returns: True if phishing, False if safe
    """
    return phishing_detector.check_phishing(url)

# Test cases when run directly
if __name__ == "__main__":
    test_urls = [
        ("https://www.google.com", False),  # Safe
        ("https://www.paypal.com/login", False),  # Legitimate login
        ("http://fake-paypal-login.com/secure/update", True),  # Phishing
        ("https://example.com/verify?account=123", True),  # Suspicious
        ("http://long.subdomain.chain.suspicious-site.com/login.php", True)  # Phishing
    ]
    
    print("Starting phishing detection tests...\n")
    for url, expected in test_urls:
        print("="*50)
        result = checkPhishing(url)
        status = "PASS" if result == expected else "FAIL"
        print(f"\nTest {status}: {url}")
        print(f"Expected: {'PHISHING' if expected else 'SAFE'}")
        print(f"Actual: {'PHISHING' if result else 'SAFE'}")