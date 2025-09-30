# solar_predict.py
import requests
import csv
import os
from datetime import datetime
import json
import time

# === CONFIG ===
BLYNK_TOKEN = "ytpOhl7Q9tC_uqDTgR1oowYcezftR9NM"   # replace with your ESP32 Blynk token
BLYNK_BASE = "https://blynk.cloud/external/api"
BLYNK_VPIN = "V8"   # ESP32 writes today's total energy here

OPENWEATHER_API_KEY = "b4e6cf0e40fed32abdbfde5f870942f9"   # OpenWeatherMap API key
CITY = "Kolkata,IN"                                        # your city
CSV_FILE = "solar_data.csv"

LOG_INTERVAL = 3  # seconds between logs (set to 300 for every 5 min)

# === FUNCTIONS ===
def read_blynk_energy():
    url = f"{BLYNK_BASE}/get?token={BLYNK_TOKEN}&{BLYNK_VPIN}"
    r = requests.get(url, timeout=10)
    txt = r.text.strip()
    try:
        if txt.startswith("["):   # sometimes Blynk returns ["value"]
            val = json.loads(txt)[0]
        else:
            val = float(txt)
    except Exception:
        raise RuntimeError(f"Can't parse Blynk response: {txt}")
    return float(val)

def read_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    r = requests.get(url, timeout=10)
    data = r.json()

    clouds = data["clouds"]["all"]          # %
    temp = data["main"]["temp"]             # °C
    humidity = data["main"]["humidity"]     # %
    return clouds, temp, humidity

def log_data():
    energy = read_blynk_energy()
    clouds, temp, humidity = read_weather()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Read {energy:.3f} Wh, Clouds={clouds}%, Temp={temp}°C, Hum={humidity}%")

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "energy_Wh", "clouds", "temp", "humidity"])
        writer.writerow([date, round(energy, 3), clouds, temp, humidity])

    print("✅ Appended to:", os.path.abspath(CSV_FILE))

# === MAIN LOOP ===
if __name__ == "__main__":
    print("📊 Solar logger started. Press CTRL+C to stop.")
    while True:
        try:
            log_data()
        except Exception as e:
            print("❌ ERROR:", e)
        time.sleep(LOG_INTERVAL)

