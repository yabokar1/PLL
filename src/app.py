from flask import Flask, request, render_template
import requests
from service.api import prompt

app = Flask(__name__)

@app.route('/')
def index():
    # Renders the HTML form page
    return render_template('./main.html')

def mapping(user_text,anonymized_text):
    user_list = user_text.split(' ')
    anonymized_list = anonymized_text.split(' ')
    mapping_dict = dict()
    for index,item in enumerate(anonymized_list):
        if item == '<PERSON>':
            mapping_dict[item] = f'{user_list[index]} {user_list[index + 1]}'
        if item == '<STUDENT_ID>':
             mapping_dict[item] = f'{user_list[index + 1]}'

    
    print(anonymized_list)
    print(user_list)
    print(mapping_dict)
    return mapping_dict

@app.route('/anonymize', methods=['POST'])
def anonymize():
    user_text = request.form['text']
    anonymized_text, mapping_text = call_presidio(user_text)
   
    return render_template('result.html', anonymized_text=anonymized_text, mapping_text=mapping_text)
    

def call_presidio(text):
    analyze_url = 'http://localhost:5001/analyze'  # Presidio Analyzer URL
    anonymize_url = 'http://localhost:5002/anonymize'  # Presidio Anonymizer URL

    student_id_recognizer = {
        "name": "student_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "student_id_pattern", "regex": r"\b\d{9}\b", "score": 0.9}
        ],
        "context": ["student", "id", "number"],
        "supported_entity": "STUDENT_ID"
    }

    # Faculty ID Recognizer
    faculty_id_recognizer = {
        "name": "faculty_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "faculty_id_pattern", "regex": r"\b1\d{8}\b", "score": 0.85}
        ],
        "context": ["faculty", "id", "number"],
        "supported_entity": "FACULTY_ID"
    }

    # SIN Recognizer
    sin_recognizer = {
        "name": "sin_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "sin_pattern", "regex":r"\b\d{3}-\d{3}-\d{3}\b", "score": 0.8}
        ],
        "context": ["social", "insurance", "number", "SIN"],
        "supported_entity": "SIN"
    }

    # Medical Records Recognizer
    medical_records_recognizer = {
        "name": "medical_records_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "medical_records_pattern", "regex": r"\b\d{6,10}\b", "score": 0.7}
        ],
        "context": ["medical", "record", "number"],
        "supported_entity": "MEDICAL_RECORD"
    }

    passport_id_recognizer = {
        "name": "passport_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "passport_id_pattern", "regex": r"\b[A-Z]{1,2}\d{5,9}\b", "score": 0.8}
        ],
        "context": ["passport", "id", "number"],
        "supported_entity": "PASSPORT_ID"
    }

    try:
        # First, analyze the text with the specified language
        analyze_response = requests.post(analyze_url, json={"text": text, "language": "en", "ad_hoc_recognizers": [
                student_id_recognizer, 
                faculty_id_recognizer, 
                sin_recognizer, 
                medical_records_recognizer,
                passport_id_recognizer 
            ]})
        if analyze_response.status_code != 200:
            return f"Error in analysis: {analyze_response.text}"

        # Then, anonymize the text using the analysis results
        anonymize_response = requests.post(anonymize_url, json={
            "text": text,
            "analyzer_results": analyze_response.json()
        })
        if anonymize_response.status_code != 200:
            return f"Error in anonymization: {anonymize_response.text}"
        
        anonymize_text = anonymize_response.json().get('text', 'No text returned from anonymization')
        response_text = prompt(anonymize_text)
        mapping_text = response_text[:]
        mapping_dict = mapping(text,anonymize_text)
      
        for item in mapping_dict:
           print(item, mapping_dict[item])
           mapping_text = mapping_text.replace(item, mapping_dict[item])

        print(mapping_text)

      
        return response_text, mapping_text
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)

