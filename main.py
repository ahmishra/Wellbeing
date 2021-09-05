# Imports
from flask import render_template, request, Flask
from joblib import load
from pandas import read_csv








# Initializing App
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"








# Global Variables
model_health_insurance = load("Models/health_insurance_model.joblib")
scaler_health_insurance = load("Models/health_insurance_scaler.joblib")
pipeline_diabetes = load("Models/diabetes_pipeline.joblib")
symptom_desc = read_csv("Datasets/symptom_desc.csv").drop_duplicates()
symptom_desc['Disease'] = symptom_desc['Disease'].apply(lambda x: x.lower())
symptom_desc = list(symptom_desc.values)
symptom_precaution = read_csv("Datasets/symptom_precaution.csv").drop_duplicates()
symptom_precaution['Disease'] = symptom_precaution['Disease'].apply(lambda x: x.lower())
symptom_precaution = list(symptom_precaution.values)
foodsncals = list(read_csv("Datasets/foodsncals.csv").drop_duplicates().values)


















foods = []
# Initilazing Foods
for i in foodsncals:
    foods.append({
        "name":i[0].lower(),
        "serving":i[1],
        "cals":i[2],
        "cals_raw":int(i[2].split()[0])
    })
# Helper functions
def get_symptom_description(symptom):
    """
    Gets symptom's description given the symptom
    """

    symptom = symptom.lower()
    results = []
    for i in symptom_desc:
        for j in i:
            if symptom in str(j):
                results.append(list(i))

    return results
def get_symptom_precaution(symptom):
    """
    Gets symptom's cure(s) given the symptom
    """

    symptom = symptom.lower()
    results = []
    for i in symptom_precaution:
        for j in i:
            if symptom in str(j):
                results.append(list(i))

    return results



def get_food_cals(food):
    """
    Gets the calories of food given the food
    """

    results = []

    if type(food) == str:
        food = food.lower()
        for i in foods:
            if food == i['name']:
                results.append(i)
    else:
        for j in food:
            j = j.lower()
            for i in foods:
                if j == i['name']:
                    results.append(i)

    return results




# Home page
@app.route("/")
def home():
    """
    Home Page
    """

    return render_template("index.html")


# Credits Page
@app.route("/credits")
def credits():
    """
    Credits Page
    """

    return render_template("credits.html")










# Symptom Describer
@app.route("/symptom_describer", methods=["POST", "GET"])
def symptom_describer():
    """
    Symptom Description Page
    """

    if request.method == "POST":
        symptom = str(request.form["disease"]).lower()
        description = get_symptom_description(symptom)
        return render_template("symptom_describer.html", description=description)

    else:
        return render_template("symptom_describer.html")


# Symptom Curer
@app.route("/symptom_curer", methods=["POST", "GET"])
def symptom_curer():
    """
    Symptom Cure(s) Page
    """

    if request.method == "POST":
        symptom = str(request.form["disease"]).lower()
        precuations = get_symptom_precaution(symptom)
        return render_template("symptom_curer.html", cures=precuations)
    
    else:
        return render_template("symptom_curer.html")

















# Diabetes predicter and logic
@app.route("/diabetes_predicter", methods=["POST", "GET"])
def diabetes_predicter():
    """
    Predicts Diabetes
    """

    if request.method == "POST":
        pregnancies = int(request.form["pregnancies"])
        glucose = float(request.form["glucose"])
        diastolic_bp = float(request.form["diastolic_bp"])
        skinthick = float(request.form["skinthick"])
        insulin = int(request.form["insulin"])
        bmi = float(request.form["bmi"])
        diabetes_pedigree = float(request.form["diabetes_pedigree"])
        age = int(request.form["age"])

        data_to_predict = [[pregnancies, glucose, diastolic_bp, skinthick, insulin, bmi, diabetes_pedigree, age]]
        prediction = int(pipeline_diabetes.predict(data_to_predict)[0])
        print(prediction)
        return render_template("diabetes_results.html", prediction=prediction)
    else:
        return render_template("diabetes_predicter.html")


# Health Insurance and logic
@app.route("/heath_insurance_predicter", methods=["GET", "POST"])
def health_insurance_predicter():
    """
    Predicts calue of health insurance
    """
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






















# BMI Calculator
@app.route("/bmicalculator", methods=["POST", "GET"])
def bmi_calculator():
    bmi = None

    if request.method == "POST":
        age = float(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        bmi = round(weight/(height*height)*10000, 2)

    return render_template("bmi_calculator.html", bmi=bmi)


# Calorie Calculator
@app.route("/calcalc", methods=["POST", "GET"])
def calorie_calc():
    results = None
    summed_cals = []
    expected_cals = 0

    if request.method == "POST":
        edible = request.form["edible"]
        expected_cals = int(request.form["calories"])
        edible = [x.strip() for x in edible.split(',')]
        if len(edible) == 1:
            edible = edible[0]
        
        results = get_food_cals(edible)

        if len(results) > 1:
            for i in results:
                summed_cals.append(i['cals_raw'])
        
    return render_template("cal_calc.html", results=results, summed_cals=sum(summed_cals), cals_left=expected_cals-sum(summed_cals), expected_cals=expected_cals) 


















# Running App
if __name__ == "__main__":
    app.run(debug=True)
