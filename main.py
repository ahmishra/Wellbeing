from flask import render_template, url_for, redirect, request, Flask
from joblib import load
import numpy as np

model_health_insurance = load("Models/health_insurance_model.joblib")
converter_health_insurance = load("Models/health_insurance_converter.joblib")
scaler_covid = load("Models/covid19_scaler.joblib")
model_covid = load("Models/covid19_model.joblib")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/credits")
def credits():
    return render_template("credits.html")


if __name__ == "__main__":
    app.run(debug=True)
