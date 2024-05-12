from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
import json, nltk
from rake_nltk import Rake

class ResumeGenerator:
    def __init__(self, API_KEY, job_description):
        """
        Initialize the ResumeGenerator class.

        Parameters:
        - API_KEY (str): The API key for OctoAI.
        - job_description (str): The job description for generating the resume.
        """
        self.client = OctoAI(api_key=API_KEY,)
        self.job_description = job_description

    def extract_json(self, text):
        """
        Extracts a valid JSON string from the given text.

        Parameters:
        - text (str): The text to extract the JSON string from.

        Returns:
        - str: The extracted JSON string.
        """
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        try:
            json.loads(json_text)
        except json.JSONDecodeError:
            print(f'Invalid JSON string: {json_text}')
            return None
        return json_text

    def extract_keywords(self):
        """
        Extracts keywords from the job description using RAKE algorithm.

        Returns:
        - str: The extracted keywords in JSON format.
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        r = Rake()
        r.extract_keywords_from_text(self.job_description)
        keywords_dict = {}
        for rating, keyword in r.get_ranked_phrases_with_scores():
            if rating > 5:
                keywords_dict.update({keyword: rating})
        return json.dumps(keywords_dict)
    
    def generate_resume(self, template, resume_content, tone, language, key_words):
        """
        Generates a resume using the given template, resume content, tone, language, and keywords.

        Parameters:
        - template (str): The template for the resume.
        - resume_content (str): The content of the resume.
        - tone (str): The tone to be applied to the resume.
        - language (str): The language of the new resume.
        - key_words (str): The keywords and ratings in dictionary format.

        Returns:
        - str: The generated resume.
        """
        completion = self.client.text_gen.create_chat_completion(
            max_tokens=10000,
            messages=[
                ChatMessage(
                    content=f"{template}",
                    role="system"
                ),
                ChatMessage(
                    content=f"""
                    User's Resume:
                    {resume_content}
                    Job Description:
                    {self.job_description}
                    Job Description Keywords:
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

        return self.extract_json(completion.choices[0].message.content)
    
    def extract_keywords_ai(self, prompt):
        """
        Extracts keywords from the job description using the AI model.
        
        Parameters:
        - prompt (str): The prompt for extracting the keywords.
        
        Returns:
        - str: The extracted keywords in text format.
        """
        completion = self.client.text_gen.create_chat_completion(
            max_tokens=4000,
            messages=[
                ChatMessage(
                    content=f"""{prompt}
                    """,
                    role="system"
                ),
                ChatMessage(
                    content=f"{self.job_description}",
                    role="user"
                )
            ],
            model="mixtral-8x22b-instruct",
            presence_penalty=0,
            temperature=0.1,
            top_p=0.9
        )

        return completion.choices[0].message.content