import boto3
import os

class Comprehend():
    def __init__(self, text):
       self.text = text
       self.aws_comprehend_client = boto3.client('comprehend', region_name=os.getenv('REGION'))

    def detect_language(self):
       response = self.aws_comprehend_client.detect_dominant_language(Text=self.text)
       dominant_language = sorted(response['Languages'], key=lambda language: language['Score'])

       return dominant_language[0]['LanguageCode']
    
    def detect_sentiment(self, language_code):
       response = self.aws_comprehend_client.detect_sentiment(Text=self.text, LanguageCode=language_code)
       
       return {'recomendedSentiment': response['Sentiment'], 'sentiments': response['SentimentScore']}
