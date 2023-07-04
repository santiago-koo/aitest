from flask import Blueprint, request, jsonify
from utils import detect_sentiment, detect_language

sentiement_bp = Blueprint('sentiement', __name__)

@sentiement_bp.route('/sentiment', methods=['POST'])
def get_sentiment():
  request_args = request.get_json()
  message = request_args['message']
  if message is not None:
    language_code = detect_language(message)
    sentiment = detect_sentiment(message, language_code)
    return jsonify(data=sentiment)
  else:
    return jsonify(data='No message')
