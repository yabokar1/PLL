from openai import OpenAI
from config import Config




def open_ai_request(text):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=Config.API_KEY,
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Write a short university(2 short paragraphs) letter for academic probation and only use the following personal data enclosed in <>:" + text,
              
        }
    ],
    model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content
    # print(text)
    return answer

