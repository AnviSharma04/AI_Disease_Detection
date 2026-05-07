from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_file(filename):
    return pickle.load(open(os.path.join(BASE_DIR, "models", filename), "rb"))

diabetes_model  = load_file("diabetes_model.pkl")
diabetes_scaler = load_file("diabetes_scaler.pkl")
heart_model     = load_file("heart_model.pkl")
heart_scaler    = load_file("heart_scaler.pkl")
liver_model     = load_file("liver_model.pkl")
liver_scaler    = load_file("liver_scaler.pkl")
kidney_model    = load_file("kidney_model.pkl")
kidney_scaler   = load_file("kidney_scaler.pkl")
lung_model      = load_file("lung_model.pkl")
lung_scaler     = load_file("lung_scaler.pkl")


@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ── OLD ROUTE (predict all 5 at once) ─────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        f = request.form
        gender_val = int(f.get("gender", 0))

        diabetes_input = diabetes_scaler.transform(np.array([[
            float(f.get("gender", 0)), float(f.get("age", 0)),
            float(f.get("pregnancies", 0)), float(f.get("glucose", 0)),
            float(f.get("bp", 0)), float(f.get("skin_thickness", 0)),
            float(f.get("insulin", 0)), float(f.get("bmi", 0)),
            float(f.get("diabetes_pedigree", 0)), float(f.get("hba1c", 0)),
            float(f.get("family_history_diabetes", 0)), float(f.get("smoking", 0)),
            float(f.get("physical_activity", 0)), float(f.get("hypertension", 0)),
        ]]))

        heart_input = heart_scaler.transform(np.array([[
            float(f.get("age", 0)), float(f.get("sex", 0)),
            float(f.get("cp", 0)), float(f.get("trestbps", 0)),
            float(f.get("chol", 0)), float(f.get("fbs", 0)),
            float(f.get("restecg", 0)), float(f.get("thalach", 0)),
            float(f.get("exang", 0)), float(f.get("oldpeak", 0)),
            float(f.get("slope", 0)), float(f.get("ca", 0)),
            float(f.get("thal", 0)), float(f.get("smoking", 0)),
            float(f.get("heart_diabetes", 0)), float(f.get("bmi", 0)),
        ]]))

        liver_input = liver_scaler.transform(np.array([[
            float(f.get("age", 0)), float(f.get("total_bilirubin", 0)),
            float(f.get("direct_bilirubin", 0)), float(f.get("alkaline_phosphotase", 0)),
            float(f.get("alamine_aminotransferase", 0)), float(f.get("aspartate_aminotransferase", 0)),
            float(f.get("total_proteins", 0)), float(f.get("albumin", 0)),
            float(f.get("ag_ratio", 0)), 1 - gender_val, gender_val,
        ]]))

        kidney_input = kidney_scaler.transform(np.array([[
            float(f.get("age", 0)), float(f.get("bp_systolic", 0)),
            float(f.get("bp_diastolic", 0)), float(f.get("urea", 0)),
            float(f.get("creatinine", 0)), float(f.get("albumin", 0)),
        ]]))

        dt = f.get("disease_type", "none")
        tt = f.get("treatment_type", "none")
        lung_input = lung_scaler.transform(np.array([[
            float(f.get("age", 0)), float(f.get("lung_capacity", 0)),
            float(f.get("hospital_visits", 0)), int(f.get("sex", 0)),
            int(f.get("smoking", 0)),
            1 if dt=="bronchitis" else 0, 1 if dt=="copd" else 0,
            1 if dt=="lung_cancer" else 0, 1 if dt=="pneumonia" else 0,
            1 if tt=="surgery" else 0, 1 if tt=="therapy" else 0,
        ]]))

        results = {
            "Diabetes":      round(diabetes_model.predict_proba(diabetes_input)[0][1] * 100, 2),
            "Heart Disease": round(heart_model.predict_proba(heart_input)[0][1]    * 100, 2),
            "Liver Disease": round(liver_model.predict_proba(liver_input)[0][1]    * 100, 2),
            "Kidney Disease":round(kidney_model.predict_proba(kidney_input)[0][1]  * 100, 2),
            "Lung Disease":  round(lung_model.predict_proba(lung_input)[0][1]      * 100, 2),
        }
        highest = max(results, key=results.get)
        return render_template("result.html", results=results, highest=highest)

    except Exception as e:
        return f"<h2 style='font-family:sans-serif;padding:40px;color:#e8392a'>Error: {str(e)}</h2>"


# ── NEW ROUTE (predict single disease) ────────────────────────────────────────
@app.route("/predict_single", methods=["POST"])
def predict_single():
    try:
        f = request.form
        disease = f.get("disease")

        if disease == "diabetes":
            inp = diabetes_scaler.transform(np.array([[
                float(f.get("gender", 0)), float(f.get("age", 0)),
                float(f.get("pregnancies", 0)), float(f.get("glucose", 0)),
                float(f.get("bp", 0)), float(f.get("skin_thickness", 0)),
                float(f.get("insulin", 0)), float(f.get("bmi", 0)),
                float(f.get("diabetes_pedigree", 0)), float(f.get("hba1c", 0)),
                float(f.get("family_history_diabetes", 0)), float(f.get("smoking", 0)),
                float(f.get("physical_activity", 0)), float(f.get("hypertension", 0)),
            ]]))
            prob = diabetes_model.predict_proba(inp)[0][1]
            label = "Diabetes"

        elif disease == "heart":
            inp = heart_scaler.transform(np.array([[
                float(f.get("age", 0)), float(f.get("sex", 0)),
                float(f.get("cp", 0)), float(f.get("trestbps", 0)),
                float(f.get("chol", 0)), float(f.get("fbs", 0)),
                float(f.get("restecg", 0)), float(f.get("thalach", 0)),
                float(f.get("exang", 0)), float(f.get("oldpeak", 0)),
                float(f.get("slope", 0)), float(f.get("ca", 0)),
                float(f.get("thal", 0)), float(f.get("smoking", 0)),
                float(f.get("heart_diabetes", 0)), float(f.get("bmi", 0)),
            ]]))
            prob = heart_model.predict_proba(inp)[0][1]
            label = "Heart Disease"

        elif disease == "liver":
            gender_val = int(f.get("gender", 0))
            inp = liver_scaler.transform(np.array([[
                float(f.get("age", 0)), float(f.get("total_bilirubin", 0)),
                float(f.get("direct_bilirubin", 0)), float(f.get("alkaline_phosphotase", 0)),
                float(f.get("alamine_aminotransferase", 0)), float(f.get("aspartate_aminotransferase", 0)),
                float(f.get("total_proteins", 0)), float(f.get("albumin", 0)),
                float(f.get("ag_ratio", 0)), 1 - gender_val, gender_val,
            ]]))
            prob = liver_model.predict_proba(inp)[0][1]
            label = "Liver Disease"

        elif disease == "kidney":
            inp = kidney_scaler.transform(np.array([[
                float(f.get("age", 0)), float(f.get("bp_systolic", 0)),
                float(f.get("bp_diastolic", 0)), float(f.get("urea", 0)),
                float(f.get("creatinine", 0)), float(f.get("albumin", 0)),
            ]]))
            prob = kidney_model.predict_proba(inp)[0][1]
            label = "Kidney Disease"

        elif disease == "lung":
            dt = f.get("disease_type", "none")
            tt = f.get("treatment_type", "none")
            inp = lung_scaler.transform(np.array([[
                float(f.get("age", 0)), float(f.get("lung_capacity", 0)),
                float(f.get("hospital_visits", 0)), int(f.get("sex", 0)),
                int(f.get("smoking", 0)),
                1 if dt=="bronchitis" else 0, 1 if dt=="copd" else 0,
                1 if dt=="lung_cancer" else 0, 1 if dt=="pneumonia" else 0,
                1 if tt=="surgery" else 0, 1 if tt=="therapy" else 0,
            ]]))
            prob = lung_model.predict_proba(inp)[0][1]
            label = "Lung Disease"

        else:
            return "<h2 style='padding:40px;color:red'>Unknown disease type</h2>"

        score = round(prob * 100, 2)
        results = {label: score}
        return render_template("result_single.html", disease=label, score=score, results=results)

    except Exception as e:
        return f"<h2 style='font-family:sans-serif;padding:40px;color:#e8392a'>Error: {str(e)}</h2>"


if __name__ == "__main__":
    app.run(debug=True)