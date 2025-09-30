import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

CSV_FILE = "solar_data.csv"
MODEL_FILE = "solar_model.joblib"

print("Loading data from", CSV_FILE)
df = pd.read_csv(CSV_FILE)

print("Preview of raw CSV:")
print(df.head(10))

# --- Drop rows without weather data ---
df = df.dropna(subset=["clouds", "temp", "humidity"])

print("After cleaning, rows left:", len(df))
print(df.tail())

# Features (X) and Target (y)
X = df[["clouds", "temp", "humidity"]]
y = df["energy_Wh"]

if len(df) >= 2:
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    print("✅ Model trained and saved to", MODEL_FILE)
else:
    from sklearn.dummy import DummyRegressor
    dummy = DummyRegressor(strategy="mean")
    dummy.fit([[0,0,0]], [0])
    joblib.dump(dummy, MODEL_FILE)
    print("⚠️ Not enough clean rows, saved dummy model.")

