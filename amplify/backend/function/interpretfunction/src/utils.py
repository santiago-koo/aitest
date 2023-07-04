import boto3
import os

COMPREHEND_CLIENT = boto3.client('comprehend', region_name=os.getenv('REGION'))

def detect_language(text):
  response = COMPREHEND_CLIENT.detect_dominant_language(Text=text)
  dominant_language = sorted(response['Languages'], key=lambda language: language['Score'])
  return dominant_language[0]['LanguageCode']

def detect_sentiment(text, language_code):
  response = COMPREHEND_CLIENT.detect_sentiment(Text=text, LanguageCode=language_code)
  return {'recomendedSentiment': response['Sentiment'], 'sentiments': response['SentimentScore']}
