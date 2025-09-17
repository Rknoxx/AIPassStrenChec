from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, re, math, hashlib, requests, secrets, string

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load ML model
model = joblib.load("model.pkl")

# --- Feature extraction ---
def extract_features(password):
    length = len(password)
    digits = len(re.findall(r"\d", password))
    upper = len(re.findall(r"[A-Z]", password))
    lower = len(re.findall(r"[a-z]", password))
    special = len(re.findall(r"[^A-Za-z0-9]", password))
    return [length, digits, upper, lower, special]

# --- Entropy calculation ---
def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password): pool += 10
    if re.search(r"[^A-Za-z0-9]", password): pool += 32
    if pool == 0: return 0
    return round(len(password) * math.log2(pool), 2)

# --- Strength classification ---
def classify_strength(entropy):
    if entropy < 28: return "Weak ❌"
    elif entropy < 36: return "Medium ⚠️"
    elif entropy < 60: return "Strong 💪"
    else: return "Very Strong 🔥"

# --- Suggestions ---
def generate_suggestions(password):
    suggestions = []
    if len(password) < 8: suggestions.append("Use at least 8 characters 📏")
    if not re.search(r"[A-Z]", password): suggestions.append("Add uppercase letters 🔠")
    if not re.search(r"[a-z]", password): suggestions.append("Add lowercase letters 🔡")
    if not re.search(r"\d", password): suggestions.append("Add numbers 🔢")
    if not re.search(r"[^A-Za-z0-9]", password): suggestions.append("Add special characters like @#$% 🔒")
    if not suggestions: suggestions.append("Great! Your password looks strong ✅")
    return suggestions

# --- HIBP breach check ---
def check_pwned(password):
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    if res.status_code != 200:
        return "Error checking breach database"
    hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return f"⚠️ Found in breaches ({count} times)"
    return "✅ Not found in known breaches"

# --- Secure password generator ---
def generate_password(length=14):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- API Routes ---
@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.json
    password = data.get("password", "")
    print("Checking password:", password)  # Debug

    features = [extract_features(password)]
    model_prediction = model.predict(features)[0]

    entropy = calculate_entropy(password)
    strength = classify_strength(entropy)
    suggestions = generate_suggestions(password)
    breach_status = check_pwned(password)

    return jsonify({
        "password": password,
        "entropy": entropy,
        "strength": strength,
        "ml_prediction": "Strong" if model_prediction == 1 else "Weak",
        "suggestions": suggestions,
        "breach_status": breach_status
    })

@app.route("/generate_password", methods=["GET"])
def get_generated_password():
    pwd = generate_password(14)
    print("Generated password:", pwd)  # Debug
    return jsonify({"generated_password": pwd})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
