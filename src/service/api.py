from openai import OpenAI
from service.config import Config


# client = OpenAI(api_key=Config.API_KEY,)
# template = "Write a short university(2 short paragraphs) letter from academic probation \
# and only use the following personal data enclosed in <>:"

print(Config.API_KEY)

def prompt(text):

    client = OpenAI(api_key=Config.API_KEY,)
    template = "Write a short university letter from university (York University) to a student, informing them of failing in a subject and their inability to attend any courses and use a similar template to this 'Dear Student's Name,I hope this letter finds you in good health. It is with a heavy heart that I must inform you of your failure to meet the academic standards required at York University. This decision has been made after careful consideration of your overall academic performance. As a consequence, in line with our academic policies, you will be unable to enroll in any courses for the upcoming semester. This period should be used to reflect on your academic goals and strategies for improvement. York University is committed to supporting its students, and we encourage you to take this time to focus on your academic development. Please feel free to reach out to me or the university's student support services for further guidance and assistance. We are here to help you navigate this challenging phase and prepare for a successful return to your studies.Sincerely,York University' and use the following personal data enclosed in <>:"

    user_detail =  {"role": "user","content": template + text,}

    chat_completion = client.chat.completions.create(
    messages=[ user_detail],
    model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content  
    return answer

