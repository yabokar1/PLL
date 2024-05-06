from openai import OpenAI
from app.config.setting import AppConfig
import requests
import json
import boto3
import re
from sagemaker import Session
from sagemaker.jumpstart.estimator import JumpStartEstimator
from sagemaker.s3 import S3Uploader
from app.utils.recognizer import (
student_id_recognizer,
faculty_id_recognizer,
sin_recognizer,
medical_records_recognizer,
passport_id_recognizer,
)


def create_entity_text(anonymize_text, user_text):
    user_text_list = user_text.split()
    anonymize_list = anonymize_text.split()
    entity_str = ""
    for index,item in enumerate(anonymize_list):
        if item == "<PERSON>":
            entity_str += f"<NAME>:{user_text_list[index]}  {user_text_list[index + 1]},"
        elif item.startswith("<") and item.endswith(">") and item != user_text_list[index+1]:
            if index < len(user_text_list) - 2:
                entity_str += f"{item}:{user_text_list[index + 1]},"
            else:
                entity_str += f"{item}:{user_text_list[index + 1]}"
    return entity_str


def create_entity_dict(user_text):
    user_text_list = user_text.split(',')
    entity_dict = {}
    for item in user_text_list:
        item_list = item.split(":")
        entity_dict[item_list[0]] = item_list[1]
    return entity_dict
        

def deanonymize(user_text, anonymized_text):
    entity_dict = create_entity_dict(user_text)
    deanonymized_text = anonymized_text.replace('<NAME>', entity_dict['<NAME>'])\
                                       .replace('<STUDENT_ID>', entity_dict['<STUDENT_ID>'])\
                                       .replace('<PASSPORT_ID>', entity_dict['<PASSPORT_ID>'])\
                                       .replace('<SIN>', entity_dict['<SIN>'])
    return deanonymized_text

def privacy_operation(anonmyized_data, user_input):
    try:
        if not anonmyized_data:
            # anonymize_text = llama_anonmyization(user_input)
            anonymize_text = presidio_anonmyization(anonmyized_data, user_input)
            return anonymize_text 
        else:
            anonmyized_response = openai_response(anonmyized_data, user_input)
            deanonmyized_response = deanonymize(anonmyized_data, anonmyized_response)
            response = "----------Anonmyized Response:" + anonmyized_response + "----------Deanonmyized Response:" + deanonmyized_response
            return response
            
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

def llama_anonmyization(user_text):
    extracted_text = ""
    payload = { "inputs": user_text, 
                 "parameters": {"max_new_tokens": 100, "top_p": 0.9, "temperature": 0.6, "return_full_text": False}
               }
    
    endpoint_name = 'jumpstart-dft-meta-textgeneration-l-20240503-170416'
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, InferenceComponentName='meta-textgeneration-llama-2-7b-20240503-170418',
        ContentType="application/json",
        Body=json.dumps(payload),
    )

    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    decoded_output = response[0]['generated_text']
    pattern = r"Expected Output: '(.*?)'"
    match = re.search(pattern, decoded_output)
    if match:
        extracted_text = match.group(1) 
        print("Extracted Part:", extracted_text)
    else:
        print("No match found")
    return extracted_text


def presidio_anonmyization(anonymize_text, user_text):
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

    anonymize_response = requests.post(AppConfig.ANONYMIZE_URL, json={
        "text": user_text,
        "analyzer_results": analyze_response.json()
    })
    if anonymize_response.status_code != 200:
        return f"Error in anonymization: {anonymize_response.text}"
    anonymize_text = anonymize_response.json().get('text', 'No text returned from anonymization')
    entity_text = create_entity_text(anonymize_text, user_text)
    return entity_text




def train():
    model_id = "meta-textgeneration-llama-2-7b"
    session = Session()
    estimator = JumpStartEstimator(
        model_id=model_id,
        environment={"accept_eula": "true"},
        disable_output_compression=True,
        hyperparameters={
            "instruction_tuned": "False",
            "epoch": "5",
            "max_input_length": "1024",
            "per_device_train_batch_size": "4",
            "lora_dropout": "0.1",
            "learning_rate": "0.0002",
            "lora_alpha": "64",
            "validation_split_ratio": "0.2",
            "lora_r": "16",
            "add_input_output_demarcation_key": "True",
            "chat_dataset": "False",
            "enable_fsdp": "True",
            "int8_quantization": "False", 
        },
        sagemaker_session=session,
    )

    output_bucket = "trainingpll"
    train_data_location = f"s3://{output_bucket}"
    estimator.fit({"training": train_data_location})
    predictor = estimator.deploy()
    return predictor
    
def deploy(estimator):
    predictor = estimator.deploy()
    
    
def openai_config(context,user_prompt=""):
    client = OpenAI(api_key=AppConfig.OPEN_API_KEY,)  
    message = user_prompt + context  
    user_detail =  {"role": "user","content": message}
    return client, user_detail

def openai_response(anonymize_text,user_prompt):

    
    context = """and only use the following personal data enclosed in <> such as <NAME>. For example do not know Saorise but replace with <NAME>
                 Make sure the letter does not have personal data such as Name, SIN, Phone number and 
                 replace mentioned information with <NAME> <STUDENT_ID> <SIN> <PHONE>""" 
    # client = OpenAI(api_key=AppConfig.API_KEY,)
    # message = user_prompt + context
    
    
    client, user_detail =  openai_config(context,user_prompt)

    # user_detail =  {"role": "user","content": message + anonymize_text,}
    user_detail["content"] = user_detail["content"] + anonymize_text
    chat_completion = client.chat.completions.create(
    messages=[ user_detail],
    model="gpt-4",
    )
    answer = chat_completion.choices[0].message.content  
    return answer


def openai_generate_dataset(entities_dict):
    input_str = ""
    format_str = ""
    output_str = ""
    for item in entities_dict:
       entities_list =  item.values()
       for index, entity in enumerate(entities_list):
           entity = entity.replace(" ", "_").replace("\r", "").replace(" ", "")
           if index % 2 == 0:
               format_str += f"<{entity.upper()}>:{entity.upper()}, "
               output_str += f"<{entity.upper()}>:"
           else:
               output_str += entity + " "   
           input_str +=  entity + " "
    
    input_str += " has not met their academic goals in psychology. The university is set to issue a direct academic probation letter" 
    sample_text = f"\"text\": ### Task: Anonymize the personal information in the following text and output in the specified format. ### Input: '{input_str}' ### Format: '{format_str}'  ### Expected Output: {output_str}"

    context = f"""  Generate 10 data points similar to the following format for only these dataset features ${format_str}, but the personal identifiers should be different and unique for all data points and should have 
                    variations while keeping the structure the same. Make sure all the personal identifiers are different for all the data points that will be generated. Refer from these examples and don't include 
                    Data Point 1: or any Data Point N in the response and include the dataset between {{}}
                    between dataset responses:
                    {
                        {sample_text}
                    }
               """
    
    client, user_detail = openai_config(context)
    chat_completion = client.chat.completions.create(messages=[ user_detail], model="gpt-4")
    answer = chat_completion.choices[0].message.content
    json_data = json_formatter(answer)
    response = write_to_s3(AppConfig.OUTPUT_FILE, json_data)
    return response
    
def json_formatter(data):
    json_list = re.findall(r'{.+?}',data, re.DOTALL)
    json_list = [item.replace("\n", "") for item in json_list]
    json_items = [json.loads(item) for item in json_list]
    return json_items
    
def write_to_s3(filename, data):
    try:
        with open('output.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        s3 = boto3.client('s3', aws_access_key_id=AppConfig.AWS_ACCESS_KEY_ID, aws_secret_access_key=AppConfig.AWS_SECRET_ACCESS_KEY)
        s3.upload_file(filename, AppConfig.S3_BUCKET_NAME, filename)
        return 'File uploaded successfully!'
    except Exception as e:
        return str(e)
            
            

    
                 
    
    
    
    


