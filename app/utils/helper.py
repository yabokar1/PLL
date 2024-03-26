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


def generate_entity_dict(user_text):
    user_text_list = user_text.split(' ')
    entity_dict = {}
    print(user_text_list)
    for index,item in enumerate(user_text_list):
        if item == 'name':
            name = user_text_list[index + 2] + " " + user_text_list[index + 3]
            entity_dict['<PERSON>'] = name
        if item == 'student':
            student_id = user_text_list[index + 3]
            entity_dict['<STUDENT_ID>'] = student_id
        if item == 'SIN':
            sin_id = user_text_list[index + 3]
            entity_dict['<SIN>'] = sin_id
        if item == 'passport':
            passport_id = user_text_list[index + 3]
            entity_dict['<PASSPORT_ID>'] = passport_id

    return entity_dict


def deanonymize_data(user_text, anonymized_text):
    
    anonymized_list = anonymized_text.split(' ')
    entity_dict = generate_entity_dict(user_text)

    for index, item in enumerate(anonymized_list):
        item = item.strip()

        # print(item, "after", sep='-')
        if item == '<PERSON>':
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<PERSON>'] 
        if item == '<PERSON>,\n\nWe':
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<PERSON>'] + ',We'
        if item == '<PERSON>,\n\nI':
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<PERSON>'] + ',I'
        if item == '<STUDENT_ID>,' or item == '<STUDENT_ID>':
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<STUDENT_ID>'] 
        if item == '<PASSPORT_ID>\n\n' or item == '<PASSPORT_ID>.\n\n' or item == '<PASSPORT_ID>' or item == '<PASSPORT_ID>.':
            print("YES PASSPORT")
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<PASSPORT_ID>'] 
        if item == '<SIN>':
            index = anonymized_list.index(item)
            anonymized_list[index] = entity_dict['<SIN>'] 
            
    anonymized_text = ' '.join(anonymized_list)
    print("The anonmyized text is " , anonymized_text)
    return anonymized_text



def anonymize_data(user_text,user_prompt):
    try:
        # First, analyze the text with the specified language
        analyze_response = requests.post(AppConfig.ANALYZE_URL, json={"text": user_text, 
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
            "text": user_text,
            "analyzer_results": analyze_response.json()
        })
        if anonymize_response.status_code != 200:
            return f"Error in anonymization: {anonymize_response.text}"
        anonymize_text = anonymize_response.json().get('text', 'No text returned from anonymization')
        response_text = prompt(anonymize_text,user_prompt)
        
        return response_text
        
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    


def presidio(user_text):
    try:
        # First, analyze the text with the specified language
        analyze_response = requests.post("http://172.17.0.2:3000/analyze", json={"text": user_text, 
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
        anonymize_response = requests.post('http://172.17.0.3:3000/anonymize', json={
            "text": user_text,
            "analyzer_results": analyze_response.json()
        })
        if anonymize_response.status_code != 200:
            return f"Error in anonymization: {anonymize_response.text}"
        anonymize_text = anonymize_response.json().get('text', 'No text returned from anonymization')
        return anonymize_text
        
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    

# 

def prompt(anonymize_text,user_prompt):

    template =  """ Dear <PERSON>,
    I hope this letter finds you well. We regret to inform you that based on your recent academic performance, you have been placed on academic probation. This decision has been made after careful review of your grades and progress during the previous semester. Our records indicate that your student ID is <STUDENT_ID>, and we would appreciate your immediate attention to rectify the situation. Academic probation is a serious matter, and we strongly encourage you to seek assistance from our academic advisors and support services to improve your standing. Please reach out to our office as soon as possible to schedule a meeting and discuss a plan for your academic success. We are confident that with the right support, you can overcome this setback and work towards achieving your full potential.
    Furthermore, we kindly request that you update your personal details with our office. In particular, we would appreciate it if you could provide us with your SIN id and passport number for documentation purposes. This will enable us to keep accurate records and assist you more effectively throughout your academic journey. Your cooperation in this matter is greatly appreciated.
    Once again, we understand that being on academic probation may be disheartening, but we are here to support you. Don't hesitate to seek help from our dedicated faculty and resources. Together, we can help you regain your academic standing and ensure your success at our university. """

    client = OpenAI(api_key=AppConfig.API_KEY,)
    message = user_prompt + template

    # message = user_prompt + "<PERSON>" + template 

    print(f'The user prompt is : {user_prompt}' )
    
    user_detail =  {"role": "user","content": message + anonymize_text,}
    
    chat_completion = client.chat.completions.create(
    messages=[ user_detail],
    model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content  
    return answer


