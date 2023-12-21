# import sys
# sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
from flask import Flask, request, render_template
import requests
# from app.service.api import prompt
from app.utils.helper import anonymize, deanonymize
# from app.model.message_model import Message
# from app.model.user_model import User
from app.utils.recognizer import (
student_id_recognizer,
faculty_id_recognizer,
sin_recognizer,
medical_records_recognizer,
passport_id_recognizer,
)
 

app = Flask(__name__)

@app.route('/')
def index():
    # Renders the HTML form page
    return render_template('./main.html')

# def mapping(user_text,anonymized_text):
#     user_list = user_text.split(' ')
#     anonymized_list = anonymized_text.split(' ')
#     mapping_dict = dict()
#     for index,item in enumerate(anonymized_list):
#         if item == '<PERSON>':
#             mapping_dict[item] = f'{user_list[index]} {user_list[index + 1]}'
#         if item == '<STUDENT_ID>':
#              mapping_dict[item] = f'{user_list[index + 1]}'

    
#     print(anonymized_list)
#     print(user_list)
#     print(mapping_dict)
#     return mapping_dict



@app.route('/anonymize', methods=['POST'])
def updated_anonymize():
    user_text = request.form['text']
    anonymize_response = anonymize(user_text)
    deanonymize_response = deanonymize(user_text,anonymize_response)
    print(anonymize_response)
    print(deanonymize_response)
    return render_template('result.html', anonymized_text=anonymize_response, mapping_text=deanonymize_response)


# @app.router('/sign-up', methods=['POST'])
# def signup():
#     user_text = request.form['text']
#     User.save(user_text)


# @app.router('login', methods=['POST'])
# def login():
#     user_text = request.form['text']
#     User.get_user_by_credentials(user_text)






# @app.route('/anonymize', methods=['POST'])
# def anonymize():
#     user_text = request.form['text']
#     anonymized_text, mapping_text = call_presidio(user_text)
   
#     return render_template('result.html', anonymized_text=anonymized_text, mapping_text=mapping_text)
    

# def call_presidio(text):
#     analyze_url = 'http://localhost:5001/analyze'  # Presidio Analyzer URL
#     anonymize_url = 'http://localhost:5002/anonymize'  # Presidio Anonymizer URL


#     try:
#         # First, analyze the text with the specified language
#         analyze_response = requests.post(analyze_url, json={"text": text, "language": "en", "ad_hoc_recognizers": [
#                 student_id_recognizer, 
#                 faculty_id_recognizer, 
#                 sin_recognizer, 
#                 medical_records_recognizer,
#                 passport_id_recognizer 
#             ]})
#         if analyze_response.status_code != 200:
#             return f"Error in analysis: {analyze_response.text}"

#         # Then, anonymize the text using the analysis results
#         anonymize_response = requests.post(anonymize_url, json={
#             "text": text,
#             "analyzer_results": analyze_response.json()
#         })
#         if anonymize_response.status_code != 200:
#             return f"Error in anonymization: {anonymize_response.text}"
        
#         anonymize_text = anonymize_response.json().get('text', 'No text returned from anonymization')
#         response_text = prompt(anonymize_text)
#         mapping_text = response_text[:]
#         mapping_dict = mapping(text,anonymize_text)
      
#         for item in mapping_dict:
#            print(item, mapping_dict[item])
#            mapping_text = mapping_text.replace(item, mapping_dict[item])

#         print(mapping_text)

      
#         return response_text, mapping_text
#     except requests.exceptions.RequestException as e:
#         return f"Request failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)

