from flask import render_template, request, Flask
from joblib import load
from pandas import read_csv
from numpy import nan

# Global Variables
model_health_insurance = load("Models/health_insurance_model.joblib")
scaler_health_insurance = load("Models/health_insurance_scaler.joblib")
symptom_desc = read_csv("Datasets/symptom_desc.csv")
symptom_desc['Disease'] = symptom_desc['Disease'].apply(lambda x: x.lower())
symptom_desc = list(symptom_desc.values)
symptom_precaution = read_csv("Datasets/symptom_precaution.csv")
symptom_precaution['Disease'] = symptom_precaution['Disease'].apply(lambda x: x.lower())
symptom_precaution = list(symptom_precaution.values)

def get_symptom_description(symptom):
    symptom = symptom.lower()
    results = []
    for i in symptom_desc:
        for j in i:
            if symptom in str(j):
                results.append(list(i))

    return results


def get_symptom_precaution(symptom):
    symptom = symptom.lower()
    results = []
    for i in symptom_precaution:
        for j in i:
            if symptom in str(j):
                results.append(list(i))

    return results

# Initializing App
app = Flask(__name__)


# App routes and logic
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/credits")
def credits():
    return render_template("credits.html")


@app.route("/symptom_describer", methods=["POST", "GET"])
def symptom_describer():
    return render_template("symptom_describer.html")


@app.route("/symptom_curer", methods=["POST", "GET"])
def symptom_curer():
    if request.method == "POST":
        symptom = str(request.form["disease"]).lower()
        precuations = get_symptom_precaution(symptom)
        print(precuations)
        return render_template("symptom_curer.html", cures=precuations)
    
    else:
        return render_template("symptom_curer.html")


@app.route("/heath_insurance_predicter", methods=["GET", "POST"])
def health_insurance_predicter():
    if request.method == "POST":
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        region = request.form['region'].lower()
        gender = request.form['gender'].lower()
        smoker = request.form['smoker'].lower()
        region_se = 0
        region_sw = 0
        region_ne = 0
        region_nw = 0

        if region == "se":
            region_se = 1
        elif region == "sw":
            region_sw = 1
        elif region == "ne":
            region_ne = 1
        elif region == "nw":
            region_nw = 1

        if gender == "female":
            gender = 1
        else:
            gender = 0

        if smoker == "yes":
            smoker = 1
        else:
            smoker = 0

        data_to_predict = [[age, gender, bmi,
                            children, smoker, region_ne, region_nw, region_se, region_sw]]
        

        data_to_predict = scaler_health_insurance.transform(data_to_predict)
        prediction = model_health_insurance.predict(data_to_predict)
        money = int(prediction)
        print(money)
        return render_template("health_insurance_results.html", prediction=money)

    else:
        return render_template("health_insurance_predicter.html")



if __name__ == "__main__":
    app.run(debug=True)
