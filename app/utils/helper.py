from openai import OpenAI
from app.config.setting import AppConfig
import requests
from app.utils.recognizer import (
student_id_recognizer,
faculty_id_recognizer,
sin_recognizer,
medical_records_recognizer,
passport_id_recognizer,
)

def mapping(user_text,anonymized_text):
    user_list = user_text.split(' ')
    anonymized_list = anonymized_text.split(' ')
    mapping_dict = dict()
    for index,item in enumerate(anonymized_list):
        if item == '<PERSON>':
            mapping_dict[item] = f'{user_list[index]} {user_list[index + 1]}'
        if item == '<STUDENT_ID>':
             mapping_dict[item] = f'{user_list[index + 1]}'

    
    # print(anonymized_list)
    # print(user_list)
    # print(mapping_dict)
    return mapping_dict



def anonymize(text):
    # analyze_url = 'http://localhost:5001/analyze'  # Presidio Analyzer URL
    # anonymize_url = 'http://localhost:5002/anonymize'  # Presidio Anonymizer URL
    try:
        # First, analyze the text with the specified language
        analyze_response = requests.post(AppConfig.ANALYZE_URL, json={"text": text, 
        "language": "en", "ad_hoc_recognizers": [
                student_id_recognizer, 
                faculty_id_recognizer, 
                sin_recognizer, 
                medical_records_recognizer,
                passport_id_recognizer 
            ]})
        if analyze_response.status_code != 200:
            return f"Error in analysis: {analyze_response.text}"

        # Then, anonymize the text using the analysis results
        anonymize_response = requests.post(AppConfig.ANONYMIZE_URL, json={
            "text": text,
            "analyzer_results": analyze_response.json()
        })
        if anonymize_response.status_code != 200:
            return f"Error in anonymization: {anonymize_response.text}"
        
        return anonymize_response
        
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    

def deanonymize(user_text,anonymize_text):

    anonymize_text = anonymize_text.json().get('text', 'No text returned from anonymization')
    response_text = prompt(anonymize_text)
    mapping_text = response_text[:]
    mapping_dict = mapping(user_text,anonymize_text)
    
    for item in mapping_dict:
        # print(item, mapping_dict[item])
        mapping_text = mapping_text.replace(item, mapping_dict[item])

    # print(mapping_text)



def call_presidio(text):
    analyze_url = 'http://localhost:5001/analyze'  # Presidio Analyzer URL
    anonymize_url = 'http://localhost:5002/anonymize'  # Presidio Anonymizer URL


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
        #    print(item, mapping_dict[item])
           mapping_text = mapping_text.replace(item, mapping_dict[item])

        # print(mapping_text)

      
        return response_text, mapping_text
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    

def prompt(text):

    client = OpenAI(api_key=AppConfig.API_KEY,)
    template = "Write a short university(2 short paragraphs) letter from academic probation \
    and only use the following personal data enclosed in <>:"


    user_detail =  {"role": "user","content": template + text,}
    

    chat_completion = client.chat.completions.create(
    messages=[ user_detail],
    model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content  
    return answer

    

