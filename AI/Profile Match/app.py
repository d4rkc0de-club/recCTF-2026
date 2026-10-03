from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

FLAG = "d4rk{pr0f1le_m4tched_ez!!}"

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No profile data received."
            }), 400

        age = int(data["age"])
        height = int(data["height"])
        weight = int(data["weight"])
        month = int(data["month"])
        year = int(data["year"])

        profile = [[
            age,
            height,
            weight,
            month,
            year
        ]]

        prediction = float(model.predict(profile)[0])

        # Clamp tiny ML prediction errors.
        score = max(0.0, min(1.0, prediction))

        percentage = round(score * 100, 4)

        if score >= 0.9999:
            return jsonify({
                "success": True,
                "score": percentage,
                "access": True,
                "flag": FLAG
            })

        return jsonify({
            "success": True,
            "score": percentage,
            "access": False
        })

    except (ValueError, TypeError, KeyError):
        return jsonify({
            "success": False,
            "error": "Invalid profile parameters."
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": "Model evaluation failed."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5021,
        debug=False
    )