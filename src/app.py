from flask import Flask, request, render_template
import requests
from open_api import open_ai_request

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
        if item == '<US_BANK_NUMBER>' or item == '<US_PASSPORT>':
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

    try:
        # First, analyze the text with the specified language
        analyze_response = requests.post(analyze_url, json={"text": text, "language": "en"})
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
        response_text = open_ai_request(anonymize_text)
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

