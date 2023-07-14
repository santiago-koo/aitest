from flask import Blueprint, request, jsonify
import boto3
import os

cognito_auth_bp = Blueprint('cognito_auth', __name__)

client = boto3.client("cognito-idp", region_name=os.getenv('REGION'))
client_id = os.getenv('AWS_COGNITO_CLIENT_ID')

@cognito_auth_bp.route('/session/signin', methods=['POST'])
def sign_in():
  request_args = request.get_json()
  username = request_args['email']
  password = request_args['password']

  try:
    initiate_auth_response = client.initiate_auth(
      ClientId=client_id,
      AuthFlow="USER_PASSWORD_AUTH",
      AuthParameters={"USERNAME": username, "PASSWORD": password},
    )

    return jsonify(data=initiate_auth_response)
  except client.exceptions.NotAuthorizedException as e:
    print(str(e))
    return jsonify(data='Incorrect username or password.')


@cognito_auth_bp.route('/session/signup', methods=['POST'])
def sign_up():
  request_args = request.get_json()
  username = request_args['email']
  password = request_args['password']

  sign_up_response = client.sign_up(
    ClientId=client_id,
    Username=username,
    Password=password
  )
  
  return jsonify(data=sign_up_response)

@cognito_auth_bp.route('/session/confirmsignup', methods=['POST'])
def confirm_sign_up():
  request_args = request.get_json()
  username = request_args['email']
  confirmation_code = request_args['confirmation_code']

  confirm_sign_up_response = client.confirm_sign_up(
    ClientId=client_id,
    Username=username,
    ConfirmationCode=confirmation_code,
  )

  return jsonify(data=confirm_sign_up_response)
