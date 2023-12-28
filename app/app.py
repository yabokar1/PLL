import sys
# sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
import bcrypt
from flask import Flask, request, render_template, redirect, url_for
from app.utils.helper import anonymize_data, deanonymize_data
from app.model.message_model import Message
from app.model.user_model import User


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./login.html')


@app.route('/anonymize', methods=['POST'])
def anonymize():
    user_text = request.form['text']
    user_prompt = request.form['prompt']
    anonymize_text = anonymize_data(user_text,user_prompt)
    deanonymize_text = deanonymize_data(user_text,anonymize_text)
    print(anonymize_text)
    print(deanonymize_text)
    save_message(anonymize_text, deanonymize_text)


    return render_template('result.html', anonymized_text=anonymize_text, mapping_text=deanonymize_text)


def save_message(text_1, text_2):
    hash_anonymize = text_1.encode('utf-8')
    hash_deanonymize = text_2.encode('utf-8')
    hash_anonymize = bcrypt.hashpw(hash_anonymize, bcrypt.gensalt())
    hash_deanonymize = bcrypt.hashpw(hash_deanonymize, bcrypt.gensalt())
    message_table = Message()
    message_table.save(hash_anonymize, hash_deanonymize)



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
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    print(email)
    user_table = User()
    user = user_table.get_credentials(email)
    print(user)

    if user['email'] == email:
        return render_template('./main.html')
    else:
        return render_template('./login.html')



if __name__ == '__main__':
    app.run(debug=True)

