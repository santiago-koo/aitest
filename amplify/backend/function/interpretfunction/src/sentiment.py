from flask import Blueprint, request, jsonify
from comprehend import Comprehend

sentiement_bp = Blueprint('sentiement', __name__)

@sentiement_bp.route('/sentiment', methods=['POST'])
def get_sentiment():
  request_args = request.get_json()
  message = request_args['message']
  if message is not None:
    comprehend = Comprehend(message)
    language_code = comprehend.detect_language()
    sentiment = comprehend.detect_sentiment(language_code)
    return jsonify(data=sentiment)
  else:
    return jsonify(data='No message')
