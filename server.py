"""
Flask web app for Watson NLP emotion detection.
Exposes two routes:
- "/" renders the UI (templates/index.html).
- "/emotionDetector" accepts text (GET/POST) and returns a formatted result string.
"""
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET"])
def index():
    """Render the main page"""
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """Accept text from GET/POST, run emotion detection, return formatted result"""
    text = ""
    if request.method == "GET":
        text = (request.args.get("textToAnalyze") or request.args.get("text") or "").strip()
    else:
        if request.is_json:
            j = request.get_json(silent=True) or {}
            text = (j.get("textToAnalyze") or j.get("text") or "").strip()
        if not text:
            text = (request.form.get("textToAnalyze") or request.form.get("text") or "").strip()

    result = emotion_detector(text)

    # Task 7 >> show message when function signals invalid input
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    anger   = result.get("anger", 0.0)
    disgust = result.get("disgust", 0.0)
    fear    = result.get("fear", 0.0)
    joy     = result.get("joy", 0.0)
    sadness = result.get("sadness", 0.0)
    dom     = result.get("dominant_emotion", "unknown")

    formatted = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. The dominant emotion is {dom}."
    )
    return formatted, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    