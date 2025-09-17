import re
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

# Function to extract features from password
def extract_features(password):
    length = len(password)
    digits = len(re.findall(r"\d", password))
    upper = len(re.findall(r"[A-Z]", password))
    lower = len(re.findall(r"[a-z]", password))
    special = len(re.findall(r"[^A-Za-z0-9]", password))
    return [length, digits, upper, lower, special]

# Sample dataset (passwords + labels: weak=0, strong=1)
passwords = ["12345", "password", "helloWorld1", "P@ssw0rd!", "Admin123!", "aB1!xyz"]
labels = [0, 0, 1, 1, 1, 1]

X = [extract_features(p) for p in passwords]
y = labels

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")
print("✅ Model trained and saved!")
