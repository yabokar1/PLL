import sys
# sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
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
    print("Entered")
    print(request.get_json())
    user_data = request.get_json().get('secret')
    user_input = request.get_json().get('input')
    print(user_data)
    print(user_input)
    message = privacy_operation(user_data, user_input)
    # deanonymize_text = deanonymize_data(user_text,anonymize_text)
    print(message)
    response = {"message": message}
    return jsonify(response)
    

@app.route('/vault', methods=['POST'])
def store_vault():
    # TODO: Add request validation and store,encrypt in DB 
    vault_dict = request.get_json()
    print(vault_dict)
    return vault_dict



@app.route('/generate', methods=['POST'])
def generate_dataset():
    print(type(request.get_json()))
    print(request.get_json())
    entities = request.get_json()["template"]
    response = openai_generate_dataset(entities)
    print(response)

    response = {"message": "" }
    return jsonify(response)
    


  

def save_message(text_1, text_2, text_3):
    hash_anonymize = text_1.encode('utf-8')
    hash_deanonymize = text_2.encode('utf-8')
    hash_prompt = text_2.encode('utf-8')
    hash_anonymize = bcrypt.hashpw(hash_anonymize, bcrypt.gensalt())
    hash_deanonymize = bcrypt.hashpw(hash_deanonymize, bcrypt.gensalt())
    hash_prompt = bcrypt.hashpw(hash_prompt, bcrypt.gensalt())
    message_table = Message()
    message_table.save(hash_anonymize,hash_deanonymize,hash_prompt)



@app.route('/registration')
def registration():
    return render_template('./registration.html')

@app.route('/sign-up', methods=['POST'])
def signup():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    user_table = User()
    user_table.save(firstname,lastname,email,password)
    return render_template('./main.html')


@app.route('/home', methods=['POST'])
def login():
    email = request.form['email']
    # include password in the credential check
    password = request.form['password']
    # password = password.encode('utf-8')
    # password = bcrypt.hashpw(password, bcrypt.gensalt())
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("The email is ", email)
    app.logger.info("The password is ", password)
    app.logger.info("The setting user is", AppConfig.USER)
    app.logger.info("The setting password is", AppConfig.PASSWORD)

    user_table = User()
    user = user_table.get_credentials(email)
    app.logger.info("The user table is", user['email'] )

    if user['email'] == email:
        app.logger.info("Entered In")
        return render_template('./main.html')
    else:
        return render_template('./login.html')
    # return render_template('./main.html')



if __name__ == '__main__':
    app.run(debug=True)

