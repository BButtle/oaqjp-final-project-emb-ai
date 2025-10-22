# EmotionDetection/emotion_detection.py
import requests

def _empty_result():
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None
    }

def emotion_detector(text_to_analyze: str):
    # handle blank input
    if not text_to_analyze or not str(text_to_analyze).strip():
        return _empty_result()
    
    # Set the URL, header, and input json format
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}

    resp = requests.post(url, json=payload, headers=headers, timeout=30)

    # if service says 400, return all None
    if resp.status_code == 400:
        return _empty_result()

    data = resp.json()  

    emotions = {}
    if isinstance(data, dict) and "documentEmotion" in data:
        emotions = (data.get("documentEmotion", {}) or {}).get("emotion", {}) or {}
    if not emotions and "emotionPredictions" in data:
        preds = data.get("emotionPredictions") or []
        if isinstance(preds, list) and preds:
            first = preds[0] or {}
            if "emotion" in first:
                emotions = first.get("emotion", {}) or {}
            elif "emotionMentions" in first:
                mentions = first.get("emotionMentions") or []
                if isinstance(mentions, list) and mentions:
                    emotions = (mentions[0] or {}).get("emotion", {}) or {}

    # Extract required scores (with safe defaults)
    anger   = float(emotions.get("anger",   0.0))
    disgust = float(emotions.get("disgust", 0.0))
    fear    = float(emotions.get("fear",    0.0))
    joy     = float(emotions.get("joy",     0.0))
    sadness = float(emotions.get("sadness", 0.0))

    scores = {"anger": anger, "disgust": disgust, "fear": fear, "joy": joy, "sadness": sadness}
    dominant_emotion = max(scores, key=scores.get) if scores else "unknown"

    return {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant_emotion
    }


"""
*******
Task 6 ver
*******

import requests


def emotion_detector(text_to_analyze: str):
    
    #Calls the Watson NLP EmotionPredict service and returns:
    #{'anger': float, 'disgust': float, 'fear': float, 'joy': float, 'sadness': float,
    #'dominant_emotion': <name>}
    
    # Set the URL, header, and input json format
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    data = resp.json()  # parse JSON

    # Handle both common response shapes - see https://www.ibm.com/docs/en/watson-libraries?topic=catalog-emotion
    emotions = {}
    if isinstance(data, dict) and "documentEmotion" in data:
        emotions = (data.get("documentEmotion", {}) or {}).get("emotion", {}) or {}
    if not emotions and "emotionPredictions" in data:
        preds = data.get("emotionPredictions") or []
        if isinstance(preds, list) and preds:
            first = preds[0] or {}
            if "emotion" in first:
                emotions = first.get("emotion", {}) or {}
            elif "emotionMentions" in first:
                mentions = first.get("emotionMentions") or []
                if isinstance(mentions, list) and mentions:
                    emotions = (mentions[0] or {}).get("emotion", {}) or {}

    # Extract required scores (with safe defaults)
    anger = float(emotions.get("anger", 0.0))
    disgust = float(emotions.get("disgust", 0.0))
    fear = float(emotions.get("fear", 0.0))
    joy = float(emotions.get("joy", 0.0))
    sadness = float(emotions.get("sadness", 0.0))

    scores = {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness
    }

    dominant_emotion = max(scores, key=scores.get) if scores else "unknown"

    return {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant_emotion
    }
    """