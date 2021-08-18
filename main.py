from flask import render_template, request, Flask
from joblib import load

model_health_insurance = load("Models/health_insurance_model.joblib")
scaler_health_insurance = load("Models/health_insurance_scaler.joblib")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/credits")
def credits():
    return render_template("credits.html")


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
