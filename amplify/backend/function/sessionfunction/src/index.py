import awsgi
from flask_cors import CORS
from flask import Flask
from cognito_auth import cognito_auth_bp

def create_app():
  app = Flask(__name__)
  CORS(app)
  
  # Blueprints
  app.register_blueprint(cognito_auth_bp)

  return app

def handler(event, context):
  app = create_app()
  return awsgi.response(app, event, context)
