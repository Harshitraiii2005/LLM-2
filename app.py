from flask import Flask, render_template, request
from flow import nlp_pipeline, predict_sentiment

app = Flask(__name__)


best_model = None
vectorizer_name = None
vectorizer_X = None

SENTIMENT_MAP = {
    0: "Negative ",
    1: "Neutral ",
    2: "Positive "
}


@app.route("/", methods=["GET", "POST"])
def index():
    global best_model, vectorizer_name, vectorizer_X

    prediction = None
    news_text = ""

    if request.method == "POST":
        news_text = request.form["news_text"]

        if best_model is None:
            return render_template(
                "index.html",
                prediction=None,
                news_text=news_text,
                message="Please retrain the pipeline first!"
            )

        # Predict sentiment
        pred_label = predict_sentiment(
            news_text,
            best_model,
            vectorizer_name,
            vectorizer_X
        )

        prediction = SENTIMENT_MAP.get(pred_label, "Unknown")

    return render_template(
        "index.html",
        prediction=prediction,
        news_text=news_text
    )




@app.route("/retrain", methods=["POST"])
def retrain():
    global best_model, vectorizer_name, vectorizer_X

    # Retrain the pipeline
    best_model, vectorizer_name, vectorizer_X = nlp_pipeline("Dataset/Product_Reviews.csv")
    return render_template("index.html", prediction=None, news_text="", message="Pipeline retrained successfully!")


if __name__ == "__main__":
    app.run(debug=True, port=9070)
