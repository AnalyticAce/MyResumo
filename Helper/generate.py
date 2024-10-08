from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
import json, nltk
from rake_nltk import Rake

class ResumeGenerator:
    def __init__(self, API_KEY: str, job_description: str, model_name: str = "mixtral-8x7b-instruct",
        presence_penalty=0, temperature=0.1, top_p=0.9) -> None:
        """
        Initialize the ResumeGenerator class.

        Parameters:
        ----------
        - API_KEY (str): The API key for OctoAI.
        - job_description (str): The job description for generating the resume.
        - model_name (str): The name of the model to use for generating the resume.
        """
        self.client = OctoAI(api_key=API_KEY,)
        self.job_description = job_description
        self.model_name = model_name
        self.presence_penalty = presence_penalty
        self.temperature = temperature
        self.top_p = top_p

    def extract_json(self, text: str) -> dict:
        """
        Extracts a valid JSON string from the given text.

        Parameters:
        -----------
        - text (str): The text to extract the JSON string from.

        Returns:
        -------
        - str: The extracted JSON string.
        """
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        try:
            json.loads(json_text)
        except json.JSONDecodeError:
            # print(f'Invalid JSON string: {json_text}')
            return None
        return json_text

    def extract_keywords(self) -> str:
        """
        Extracts keywords from the job description using RAKE algorithm.

        Returns:
        -------
        - str: The extracted keywords in JSON format.
        """
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
        """
        Generates a resume using the given prompt, resume content, tone, language, and keywords.

        Parameters:
        ----------
        - template (str): The template for the resume.
        - resume_content (str): The content of the resume.
        - tone (str): The tone to be applied to the resume.
        - language (str): The language of the new resume.
        - key_words (str): The keywords and ratings in dictionary format.

        Returns:
        -------
        - str: The generated resume.
        """
        completion = self.client.text_gen.create_chat_completion(
            max_tokens=100000,
            messages=[
                ChatMessage(
                    content=f"{prompt}",
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
                    {language}
                    User's Additional Information:
                    {additional_info}""",
                    role="user"
                )
            ],
            model=self.model_name,
            presence_penalty=self.presence_penalty,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return self.extract_json(completion.choices[0].message.content)
    
    def extract_keywords_ai(self, prompt: str) -> str:
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
            model=self.model_name,
            presence_penalty=self.presence_penalty,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return completion.choices[0].message.content
