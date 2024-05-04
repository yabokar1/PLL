import sys
import bcrypt
from flask import Flask, request, render_template, redirect, url_for, jsonify
from app.utils.helper import *
from app.model.message import Message
from app.model.user import User
from app.config.setting import AppConfig
from flask_cors import CORS, cross_origin
import logging


app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def index():
    return render_template('./login.html')


@app.route('/anonymize', methods=['POST'])
def anonymize():
    user_data = request.get_json().get('secret')
    user_input = request.get_json().get('input')
    message = presidio_privacy_operation(user_data, user_input)
    # deanonymize_text = deanonymize_data(user_text,anonymize_text)
    response = {"message": message}
    return jsonify(response)
    

@app.route('/vault', methods=['POST'])
def store_vault():
    # TODO: Add request validation and store,encrypt in DB 
    vault_dict = request.get_json()
    return vault_dict



@app.route('/generate', methods=['POST'])
def generate_dataset():
    entities = request.get_json()["template"]
    response = openai_generate_dataset(entities)
    response = {"message": "" }
    return jsonify(response)
    


if __name__ == '__main__':
    app.run(debug=True)

