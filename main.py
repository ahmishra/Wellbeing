from flask import render_template, url_for, redirect, request, Flask
from joblib import load
import numpy as np
from scipy.sparse import data

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

@app.route("/covid_predicter", methods=["POST", "GET"])
def covid_predicter():
    if request.method == "POST":
        cough = request.form['cough'].lower()
        fever = request.form['fever'].lower()
        sore_throat = request.form['throat'].lower()
        short_breath = request.form['breath'].lower()
        headache = request.form['headache'].lower()
        above_60 = request.form['60'].lower()
        malefemale = request.form['malefemale'].lower()

        if cough == "yes":
            cough = 1
        elif cough == "no":
            cough = 0
        
        if fever == "yes":
            fever = 1
        elif fever == "no":
            fever = 0

        if sore_throat == "yes":
            sore_throat = 1
        elif sore_throat == "no":
            sore_throat = 0

        if short_breath == "yes":
            short_breath = 1
        elif short_breath == "no":
            short_breath = 0

        if headache == "yes":
            headache = 1
        elif headache == "no":
            headache = 0

        if above_60 == "yes":
            above_60 = 1
        elif above_60 == "no":
            above_60 = 0

        if malefemale == "female":
            malefemale = 1
        elif malefemale == "male":
            malefemale = 0

        data_to_predict = [[cough, fever, sore_throat, short_breath, headache, above_60, malefemale]]
        data_to_predict = scaler_covid.fit_transform(data_to_predict)
        prediction = model_covid.predict(data_to_predict)
        return render_template("covid_prediction_results.html", prediction=prediction)
    else:
        return render_template("covid_predicter.html")



if __name__ == "__main__":
    app.run(debug=True)
