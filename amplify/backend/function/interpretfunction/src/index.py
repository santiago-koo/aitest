import boto3
import awsgi
import os
from flask_cors import CORS
from flask import Flask, jsonify, request

BASE_ROUTE = "/sentiment"
COMPREHEND_CLIENT = boto3.client('comprehend', region_name=os.getenv('REGION'))

app = Flask(__name__)
CORS(app)

def detect_language(text):
  response = COMPREHEND_CLIENT.detect_dominant_language(Text=text)
  dominant_language = sorted(response['Languages'], key=lambda language: language['Score'])
  return dominant_language[0]['LanguageCode']

def detect_sentiment(text):
  language_code = detect_language(text)
  response = COMPREHEND_CLIENT.detect_sentiment(Text=text, LanguageCode=language_code)
  return {'recomendedSentiment': response['Sentiment'], 'sentiments': response['SentimentScore']}

@app.route(BASE_ROUTE, methods=['POST'])
def get_sentiment():
  request_args = request.get_json()
  message = request_args['message']
  if message is not None:
    sentiment = detect_sentiment(message)
    return jsonify(data=sentiment)
  else:
    return jsonify(data='No message')

def handler(event, context):
  return awsgi.response(app, event, context)
