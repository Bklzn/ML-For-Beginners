import pickle
from flask import Flask, render_template, request
from pumpkin_input import build_input_row

app = Flask(__name__)

with open("pumpkin-model.pkl", "rb") as file:
    artifact = pickle.load(file)

ct = artifact["preprocessor"]
model = artifact["model"]
classes = artifact["classes"]
allowed = artifact["allowed"]


@app.route("/")
def home():
    return render_template("index.html", allowed=allowed)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        row = build_input_row(request.form.to_dict(), allowed)
    except ValueError as error:
        return render_template(
            "index.html", allowed=allowed, prediction_text=f"Invalid input: {error}"
        )

    encoded = ct.transform(row)
    prediction = model.predict(encoded)[0]
    probabilities = model.predict_proba(encoded)[0]

    label = classes[prediction]
    confidence = probabilities[prediction]

    return render_template(
        "index.html",
        allowed=allowed,
        prediction_text=f"Likely color: {label} ({confidence:.1%})",
    )


if __name__ == "__main__":
    app.run(debug=True)