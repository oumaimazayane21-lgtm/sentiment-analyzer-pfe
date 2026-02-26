from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def simple_sentiment(text: str) -> str:
    t = text.lower()
    positive_words = ["love", "good", "great", "amazing", "excellent", "perfect", "like"]
    negative_words = ["bad", "hate", "worst", "awful", "terrible", "poor"]

    pos = sum(w in t for w in positive_words)
    neg = sum(w in t for w in negative_words)

    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    return "Neutral"


@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = None
    text = ""
if request.method == "POST":
        import time
        time.sleep(2)
        text = request.form.get("text", "")
        sentiment = simple_sentiment(text)
    
    html", sentiment=sentiment, text=text)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    return jsonify({"sentiment": simple_sentiment(text), "text": text})


if __name__ == "__main__":
    app.run(debug=True, port=5000)