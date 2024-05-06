from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
from .tools import extract_json

def generate_resume(template, resume_content, job_description, tone, language, API_KEY):
    client = OctoAI(api_key=API_KEY,)
    
    completion = client.text_gen.create_chat_completion(
        max_tokens=10000,
        messages=[
            ChatMessage(
                content=f"{template}",
                role="system"
            ),
            ChatMessage(
                content=f"{resume_content}\n{job_description}\n{tone}\n{language}",
                role="user"
            )
        ],
        model="mixtral-8x22b-instruct",
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9
    )

    return extract_json(completion.choices[0].message.content)