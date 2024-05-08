from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
from .tools import extract_json
import json, nltk
from rake_nltk import Rake

def extract_keywords(job_description):
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    r = Rake()
    r.extract_keywords_from_text(job_description)
    keywords_dict = {}
    for rating, keyword in r.get_ranked_phrases_with_scores():
        if rating > 5:
            keywords_dict.update({keyword: rating})
    return json.dumps(keywords_dict)

def generate_resume(template, resume_content, job_description,
    tone, language, API_KEY, key_words):
    client = OctoAI(api_key=API_KEY,)
    
    completion = client.text_gen.create_chat_completion(
        max_tokens=10000,
        messages=[
            ChatMessage(
                content=f"{template}",
                role="system"
            ),
            ChatMessage(
                content=f"""
                User Resume:
                {resume_content}
                Job Description:
                {job_description}
                Job Description Keywords and Ratings in Dict Format:
                {key_words}
                Tone to be applied:
                {tone}
                Language of the new resume:
                {language}""",
                role="user"
            )
        ],
        model="mixtral-8x22b-instruct",
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9
    )

    return extract_json(completion.choices[0].message.content)

