from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "diabetes-app-secret-key")

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


def api(method, path, **kwargs):
    """Helper to call the FastAPI backend."""
    try:
        r = requests.request(method, f"{API_BASE}{path}", timeout=10, **kwargs)
        return r
    except requests.exceptions.ConnectionError:
        return None


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        data = request.form.to_dict()
        patient_id = data.pop("patient_id")

        # Build the nested payload the API expects
        # Convert hyphenated aliases
        alias_map = {
            "glyburide_metformin": "glyburide-metformin",
            "glipizide_metformin": "glipizide-metformin",
            "glimepiride_pioglitazone": "glimepiride-pioglitazone",
            "metformin_rosiglitazone": "metformin-rosiglitazone",
            "metformin_pioglitazone": "metformin-pioglitazone",
        }
        features = {}
        for k, v in data.items():
            api_key = alias_map.get(k, k)
            try:
                features[api_key] = int(v)
            except (ValueError, TypeError):
                features[api_key] = v

        payload = {"patient_id": patient_id, "features": features}
        r = api("POST", "/patients", json=payload)

        if r is None:
            flash("Cannot reach API server.", "error")
        elif r.status_code == 201 or r.status_code == 200:
            flash(f"Patient {patient_id} saved successfully!", "success")
            return redirect(url_for("patient_detail", patient_id=patient_id))
        elif r.status_code == 409:
            flash("A patient with that ID already exists.", "error")
        else:
            flash(f"Error: {r.json().get('detail', 'Unknown error')}", "error")

    return render_template("new_patient.html")


@app.route("/patients/<patient_id>")
def patient_detail(patient_id):
    r = api("GET", f"/patients/{patient_id}")
    if r is None:
        flash("Cannot reach API server.", "error")
        return redirect(url_for("dashboard"))
    if r.status_code == 404:
        flash("Patient not found.", "error")
        return redirect(url_for("lookup"))
    patient = r.json()
    return render_template("patient_detail.html", patient=patient)


@app.route("/patients/<patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    if request.method == "POST":
        data = request.form.to_dict()
        alias_map = {
            "glyburide_metformin": "glyburide-metformin",
            "glipizide_metformin": "glipizide-metformin",
            "glimepiride_pioglitazone": "glimepiride-pioglitazone",
            "metformin_rosiglitazone": "metformin-rosiglitazone",
            "metformin_pioglitazone": "metformin-pioglitazone",
        }
        updates = {}
        for k, v in data.items():
            if v != "":
                api_key = alias_map.get(k, k)
                try:
                    updates[api_key] = int(v)
                except ValueError:
                    updates[api_key] = v

        r = api("PUT", f"/patients/{patient_id}", json=updates)
        if r is None:
            flash("Cannot reach API server.", "error")
        elif r.status_code == 200:
            flash("Patient updated successfully.", "success")
            return redirect(url_for("patient_detail", patient_id=patient_id))
        else:
            flash(f"Update failed: {r.json().get('detail', 'Unknown error')}", "error")

    r = api("GET", f"/patients/{patient_id}")
    if r is None or r.status_code == 404:
        flash("Patient not found.", "error")
        return redirect(url_for("lookup"))
    patient = r.json()
    return render_template("edit_patient.html", patient=patient)


@app.route("/patients/<patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    r = api("DELETE", f"/patients/{patient_id}")
    if r is None:
        flash("Cannot reach API server.", "error")
    elif r.status_code == 200:
        flash(f"Patient {patient_id} deleted.", "success")
    else:
        flash(f"Delete failed: {r.json().get('detail', 'Unknown error')}", "error")
    return redirect(url_for("lookup"))


@app.route("/patients/<patient_id>/predict", methods=["POST"])
def predict(patient_id):
    r = api("POST", f"/patients/{patient_id}/predict")
    if r is None:
        flash("Cannot reach API server.", "error")
        return redirect(url_for("patient_detail", patient_id=patient_id))
    if r.status_code != 200:
        flash(f"Prediction failed: {r.json().get('detail', 'Unknown error')}", "error")
        return redirect(url_for("patient_detail", patient_id=patient_id))
    result = r.json()
    return render_template("prediction_result.html", result=result, patient_id=patient_id)


@app.route("/lookup")
def lookup():
    return render_template("lookup.html")


@app.route("/lookup/search")
def lookup_search():
    pid = request.args.get("patient_id", "").strip()
    if not pid:
        flash("Please enter a patient ID.", "error")
        return redirect(url_for("lookup"))
    return redirect(url_for("patient_detail", patient_id=pid))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
