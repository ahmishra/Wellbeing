from flask import render_template, url_for, flash, redirect, request, Flask
from joblib import load
import numpy as np

model = load("Models/health_insurance_model.joblib")
converter = load("Models/health_insurance_converter.joblib")
scaler = load("Models/health_insurance_scaler.joblib")

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
