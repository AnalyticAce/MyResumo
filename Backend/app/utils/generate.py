from openai import ChatCompletion, OpenAI
import json, nltk
from rake_nltk import Rake

class ResumeGenerator:
    def __init__(self, 
            API_KEY: str, job_description: str, 
            model_name: str = "gpt-3.5-turbo",
            presence_penalty=0, temperature=0.1, 
            top_p=0.9
        ) -> None:
        self.client = OpenAI(api_key=API_KEY)
        self.job_description = job_description
        self.model_name = model_name
        self.presence_penalty = presence_penalty
        self.temperature = temperature
        self.top_p = top_p

    def extract_json(self, text: str) -> dict:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        try:
            json.loads(json_text)
        except json.JSONDecodeError:
            return None
        return json_text

    def extract_keywords(self) -> str:
        try:
            libs = ["punkt", "stopwords", "tokenizers/punkt", "corpora/stopwords"]
            nltk.data.find(libs[2])
        except LookupError:
            nltk.download(libs[0])
        try:
            nltk.data.find(libs[3])
        except LookupError:
            nltk.download(libs[1])
        r = Rake()
        r.extract_keywords_from_text(self.job_description)
        keywords_dict = {}
        for rating, keyword in r.get_ranked_phrases_with_scores():
            if rating > 5:
                keywords_dict.update({keyword: rating})
        return json.dumps(keywords_dict)
    
    def generate_resume(self, prompt: str, resume_content: str,
                tone: str, language: str, key_words: str = "", 
                additional_info: str = None) -> dict:
        completion = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"""
                    User's Resume:
                    {resume_content}
                    Job Description:
                    {self.job_description}
                    Job Description Keywords:
                    {key_words}
                    Tone to be applied:
                    {tone}
                    Language of the new resume:
                    {language}
                    User's Additional Information:
                    {additional_info}"""}
            ],
            max_tokens=100000,
            presence_penalty=self.presence_penalty,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return self.extract_json(completion.choices[0].message['content'])
    
    def extract_keywords_ai(self, prompt: str) -> str:
        completion = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{self.job_description}"}
            ],
            max_tokens=4000,
            presence_penalty=self.presence_penalty,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return completion.choices[0].message['content']