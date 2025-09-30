import joblib
import requests

MODEL_FILE = "solar_model.joblib"

# === Load model ===
model = joblib.load(MODEL_FILE)

# === Example input (replace with real-time weather API) ===
clouds = 40       # %
temp = 28         # °C
humidity = 90     # %

# Features (must match training order!)
X_pred = [[clouds, temp, humidity]]

# === Prediction ===
y_pred = model.predict(X_pred)[0]

# Prevent negative outputs
y_pred = max(0, y_pred)

print(f"Predicted tomorrow’s energy: {y_pred:.2f} Wh")

# === Push to Blynk ===
BLYNK_TOKEN = "ytpOhl7Q9tC_uqDTgR1oowYcezftR9NM"
url = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}&V9={y_pred:.2f}"
resp = requests.get(url, timeout=10)

print("Blynk response:", resp.text)

