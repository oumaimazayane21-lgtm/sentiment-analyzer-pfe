from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

def vader_analyze(text: str):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    # percentages (0..100)
    pos_pct = round(scores["pos"] * 100, 1)
    neu_pct = round(scores["neu"] * 100, 1)
    neg_pct = round(scores["neg"] * 100, 1)

    # compound to percent (0..100) just for UI bar
    compound_pct = round((compound + 1) / 2 * 100, 1)

    return {
        "label": label,
        "scores": scores,
        "pos_pct": pos_pct,
        "neu_pct": neu_pct,
        "neg_pct": neg_pct,
        "compound": compound,
        "compound_pct": compound_pct,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        result = vader_analyze(text)

    return render_template("index.html", result=result, text=text)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    result = vader_analyze(text)
    return jsonify({"text": text, **result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)