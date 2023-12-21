from openai import OpenAI
from service.config import Config


# client = OpenAI(api_key=Config.API_KEY,)
# template = "Write a short university(2 short paragraphs) letter from academic probation \
# and only use the following personal data enclosed in <>:"

print(Config.API_KEY)

def prompt(text):

    client = OpenAI(api_key=Config.API_KEY,)
    template = "Write a short university(2 short paragraphs) letter from academic probation \
    and only use the following personal data enclosed in <>:"


    user_detail =  {"role": "user","content": template + text,}
    

    chat_completion = client.chat.completions.create(
    messages=[ user_detail],
    model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content  
    return answer

