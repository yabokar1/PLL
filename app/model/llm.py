import boto3
import json
from abc import ABC, abstractmethod
from app.config.setting import AppConfig
from app.config.constants import *

    
class LLM(ABC):
    @abstractmethod
    def response(self):
        pass

    @abstractmethod
    def generate_dataset(self):
        pass
    

class OpenAI(LLM):
    def __init__(self):
        self.client = OpenAI(api_key=AppConfig.API_KEY)
        self.context_response = CONTEXT_RESPONSE
        self.context_dataset = CONTEXT_DATASET
    
    def response(self, user_prompt, custom_entity):
        message = user_prompt + self.context_response + custom_entity
        chat_completion = self.user_details(message)
        model_response = chat_completion.choices[0].message.content
        return model_response  

    def generate_dataset(self, entity_dict):
        pll_entities = ""
        for key,value in entity_dict.items():
            pll_entities = pll_entities + key + ":" + value + " "
        message = self.context_dataset + pll_entities
        chat_completion = self.user_details(message)
        response = chat_completion.choices[0].message.content
        return response

    def user_details(self, message):
        user_detail =  {"role": "user","content": message}
        chat_completion = self.client.chat.completions.create(
            messages=[user_detail],
            model="gpt-4",
        )
        return chat_completion

    
    

class Llama(LLM):
    def __init__(self):
        self.endpoint_name = 'safegpt-model-endpoint'
        self.client = boto3.client("sagemaker-runtime")
              
    def response(self, user_prompt):
        extracted_text = ""
        payload = { "inputs": user_prompt, 
                    "parameters": {"max_new_tokens": 100, "top_p": 0.9, "temperature": 0.6, "return_full_text": False}
                }
        model_response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name, InferenceComponentName='meta-textgeneration-llama-2-7b-20240327-031345',
            ContentType="application/json",
            Body=json.dumps(payload),
        )
        
        model_response_body = model_response["Body"].read().decode("utf8")
        response_json = json.loads(model_response_body)
        return response_json
        
    def generate_dataset(self):
        pass


if __name__ == "__main__":
    pass