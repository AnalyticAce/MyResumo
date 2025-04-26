import json
import os
import re
from typing import List, Optional

# Replace SentenceTransformer with sklearn's TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class SkillsExtraction(BaseModel):
    """Model for structured extraction of skills and qualifications from text.
    
    This Pydantic model defines the structure for extracted information from 
    resumes and job descriptions, including technical skills, experience, 
    requirements, and industry domains.
    """
    skills: List[str] = Field(description="List of technical skills extracted from the text")
    experience_years: Optional[int] = Field(description="Years of experience mentioned in the text, if any")
    key_requirements: List[str] = Field(description="Key requirements or qualifications extracted from the text")
    domains: List[str] = Field(description="Domains or industries mentioned in the text")


class ATSScorerLLM:
    """Class for scoring resumes against job descriptions using AI techniques.
    
    This class provides methods to extract information from resumes and job descriptions,
    calculate semantic similarity, and perform a comprehensive match analysis using
    LLM-based techniques.
    """
    def __init__(self, model_name="", api_key=None, api_base=""):
        """Initialize the ATS scorer with API credentials and model configuration.
        
        Args:
            model_name (str): Name of the LLM model to use. Falls back to MODEL_NAME env var.
            api_key (str, optional): API key for the LLM service. Falls back to API_KEY env var.
            api_base (str, optional): Base URL for the API service. Falls back to API_BASE env var.
            
        Raises:
            ValueError: If required credentials are missing after falling back to environment variables.
        """
        self.api_key = api_key or os.environ.get("API_KEY")
        self.api_base = api_base or os.environ.get("API_BASE")
        self.model_name = model_name or os.environ.get("MODEL_NAME")
        if not self.api_key:
            raise ValueError("An LLM API key is required. Provide it or set API_KEY environment variable.")

        if not self.api_base:
            raise ValueError("An LLM API base is required. Provide it or set API_BASE environment variable.")
        
        if not self.model_name:
            raise ValueError("An LLM model name is required. Provide it or set MODEL_NAME environment variable.")

        self.llm = ChatOpenAI(
            model_name=self.model_name, 
            temperature=0.1,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base
        )

        # Replace SentenceTransformer with TfidfVectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),  # Use both unigrams and bigrams
            max_features=5000
        )
        
        self.parser = PydanticOutputParser(pydantic_object=SkillsExtraction)

        self.setup_prompts()
        
        self.setup_chains()
        
    def setup_prompts(self):
        """Set up the prompts for various extraction tasks."""
        # Prompt for extracting skills from resume
        self.resume_prompt = PromptTemplate(
            template="""You are an expert ATS (Applicant Tracking System) analyzer.
            Extract all technical skills, experience, and qualifications from the following resume text.
            Be thorough but precise - only extract actual skills (like programming languages, tools, frameworks)
            and professionally relevant qualifications.
            
            RESUME TEXT:
            {resume_text}
            
            {format_instructions}
            """,
            input_variables=["resume_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        # Prompt for extracting requirements from job description
        self.job_prompt = PromptTemplate(
            template="""You are an expert job analyzer.
            Extract all required technical skills, experience requirements, and key qualifications
            from the following job description. Focus on must-have requirements, not nice-to-have ones.
            
            JOB DESCRIPTION:
            {job_text}
            
            {format_instructions}
            """,
            input_variables=["job_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        # Prompt for skill matching and score analysis
        self.matching_prompt = PromptTemplate(
            template="""You are an expert ATS (Applicant Tracking System) analyzer.
            Compare the candidate's skills and qualifications with the job requirements and provide an analysis.
            
            CANDIDATE SKILLS AND QUALIFICATIONS:
            {resume_skills}
            
            JOB REQUIREMENTS:
            {job_requirements}
            
            Based on a detailed analysis, provide:
            1. A scoring from 0-100 indicating how well the candidate's skills match the job requirements
            2. A list of matching skills between the candidate and job requirements
            3. A list of important missing skills the candidate should highlight or develop
            4. A brief recommendation about the candidate's fit for this role
            
            Format your response as a JSON object with the following structure:
            {{
                "score": number,
                "matching_skills": [list of strings],
                "missing_skills": [list of strings],
                "recommendation": string
            }}
            """,
            input_variables=["resume_skills", "job_requirements"]
        )
        
    def setup_chains(self):
        """Set up the LLM chains for each task."""
        self.resume_chain = LLMChain(
            llm=self.llm,
            prompt=self.resume_prompt,
            output_key="resume_analysis"
        )
        
        self.job_chain = LLMChain(
            llm=self.llm,
            prompt=self.job_prompt,
            output_key="job_analysis"
        )
        
        self.matching_chain = LLMChain(
            llm=self.llm,
            prompt=self.matching_prompt,
            output_key="matching_analysis"
        )
    
    def extract_resume_info(self, resume_text):
        """Extract skills and qualifications from resume using LLM."""
        try:
            result = self.resume_chain.run(resume_text=resume_text)
            # Parse the result into our schema
            parsed_result = self.parser.parse(result)
            return parsed_result
        except Exception as e:
            print(f"Error extracting resume info: {e}")
            # Fallback to simpler extraction if parsing fails
            result = self.resume_chain.run(resume_text=resume_text)
            return result
    
    def extract_job_info(self, job_text):
        """Extract requirements from job description using LLM."""
        try:
            result = self.job_chain.run(job_text=job_text)
            # Parse the result into our schema
            parsed_result = self.parser.parse(result)
            return parsed_result
        except Exception as e:
            print(f"Error extracting job info: {e}")
            # Fallback
            result = self.job_chain.run(job_text=job_text)
            return result
    
    def calculate_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity between two texts using TF-IDF and cosine similarity."""
        try:
            # Fit and transform the texts
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.5  # Default to middle value
    
    def calculate_keyword_overlap(self, resume_skills, job_skills):
        """Calculate a simple keyword overlap score as an additional signal."""
        if not resume_skills or not job_skills:
            return 0.5
            
        # Convert all skills to lowercase for better matching
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Count matches
        matches = sum(1 for skill in job_skills_lower if any(
            job_skill in skill or skill in job_skill for job_skill in resume_skills_lower
        ))
        
        # Calculate overlap score
        if len(job_skills_lower) > 0:
            return matches / len(job_skills_lower)
        return 0.5
    
    def analyze_match(self, resume_analysis, job_analysis):
        """Have the LLM analyze the match between resume and job requirements."""
        try:
            # Convert analyses to strings if they're not already
            if not isinstance(resume_analysis, str):
                resume_analysis = str(resume_analysis.model_dump())
            if not isinstance(job_analysis, str):
                job_analysis = str(job_analysis.model_dump())
                
            # Add explicit instruction for JSON format
            result = self.matching_chain.run(
                resume_skills=resume_analysis,
                job_requirements=job_analysis
            )
            
            # Try to find a JSON object in the response
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if json_match:
                try:
                    # Extract and parse the JSON
                    json_str = json_match.group(0)
                    parsed_result = json.loads(json_str)
                    return parsed_result
                except json.JSONDecodeError:
                    pass
            
            # If we can't parse as JSON, extract the fields manually
            score_match = re.search(r'["\']?score["\']?\s*:\s*(\d+)', result, re.IGNORECASE)
            score = int(score_match.group(1)) if score_match else 50  # Default to 50 if not found
            
            # Extract matching skills
            matching_section = re.search(r'["\']?matching_skills["\']?\s*:\s*\[(.*?)\]', result, re.DOTALL)
            matching_skills = []
            if matching_section:
                skills_text = matching_section.group(1)
                matching_skills = re.findall(r'["\']([^"\']+)["\']', skills_text)
            
            # Extract missing skills
            missing_section = re.search(r'["\']?missing_skills["\']?\s*:\s*\[(.*?)\]', result, re.DOTALL)
            missing_skills = []
            if missing_section:
                skills_text = missing_section.group(1)
                missing_skills = re.findall(r'["\']([^"\']+)["\']', skills_text)
            
            # Extract recommendation
            rec_match = re.search(r'["\']?recommendation["\']?\s*:\s*["\']([^"\']+)["\']', result)
            recommendation = rec_match.group(1) if rec_match else "No specific recommendation provided."
                
            return {
                "score": score,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "recommendation": recommendation
            }
        
        except Exception as e:
            print(f"Error analyzing match: {e}")
            return {
                "score": 50,
                "matching_skills": [],
                "missing_skills": [],
                "recommendation": "Error analyzing match. The candidate appears to have relevant skills but a detailed analysis could not be completed."
            }
    
    def compute_match_score(self, resume_text, job_text, weights=None):
        """Calculate comprehensive match score between resume and job."""
        if weights is None:
            weights = {
                'llm_analysis': 0.5,
                'semantic': 0.3,
                'keyword_overlap': 0.2  # Added keyword overlap as a lightweight signal
            }
        
        # Extract information using LLM
        resume_analysis = self.extract_resume_info(resume_text)
        job_analysis = self.extract_job_info(job_text)
        
        # Calculate semantic similarity with TF-IDF
        semantic_score = self.calculate_semantic_similarity(resume_text, job_text)
        
        # Calculate keyword overlap score
        resume_skills = resume_analysis.skills if hasattr(resume_analysis, 'skills') else []
        job_skills = job_analysis.skills if hasattr(job_analysis, 'skills') else []
        keyword_score = self.calculate_keyword_overlap(resume_skills, job_skills)
        
        # Get LLM analysis of match
        match_analysis = self.analyze_match(resume_analysis, job_analysis)
        llm_score = match_analysis.get("score", 50) / 100  # Convert to 0-1 scale
        
        # Calculate final weighted score
        final_score = (
            weights['llm_analysis'] * llm_score +
            weights['semantic'] * semantic_score +
            weights['keyword_overlap'] * keyword_score
        )
        
        # Format the result
        result = {
            "llm_score": round(llm_score * 100, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "keyword_overlap_score": round(keyword_score * 100, 2),
            "final_score": round(final_score * 100, 2),
            "resume_skills": resume_skills,
            "job_requirements": job_skills,
            "matching_skills": match_analysis.get("matching_skills", []),
            "missing_skills": match_analysis.get("missing_skills", []),
            "recommendation": match_analysis.get("recommendation", "")
        }
        
        return result


# Example usage
def demo_ats_scorer_llm():
    """Demo function to showcase the ATSScorerLLM functionality."""
    api_key = "sk-**************************" 
    model_name = "deepseek-chat"
    api_base = "https://api.deepseek.com/v1" 
    
    scorer = ATSScorerLLM(
        api_key=api_key,
        model_name=model_name,
        api_base=api_base
    )
    
    resume = """
    John Smith
    Data Scientist & Machine Learning Engineer
    
    EXPERIENCE
    Senior Machine Learning Engineer, TechCorp (2019-Present)
    - Developed production-ready ML pipelines using Python, TensorFlow and Kubernetes
    - Optimized recommendation algorithms resulting in 20% uplift in user engagement
    - Collaborated with cross-functional teams to deploy cloud-based data solutions
    
    Data Scientist, DataCompany (2016-2019)
    - Built predictive models using scikit-learn, XGBoost and SQL
    - Created dashboards and visualizations with Tableau
    
    SKILLS
    Programming: Python, R, SQL, Java
    ML Frameworks: TensorFlow, PyTorch, Keras
    Tools: Git, Docker, Kubernetes, AWS, GCP
    Data: Pandas, NumPy, Spark, Hadoop
    """

    job_desc = """
    Machine Learning Engineer
    
    We are seeking an experienced Machine Learning Engineer to join our AI team.
    
    REQUIREMENTS:
    - 3+ years experience in ML/AI engineering
    - Strong programming skills in Python
    - Experience with TensorFlow or PyTorch
    - Familiarity with ML pipelines and deployments
    - Knowledge of cloud platforms (AWS, GCP, or Azure)
    - Understanding of data structures and algorithms
    
    RESPONSIBILITIES:
    - Design and implement machine learning models
    - Optimize existing algorithms for production
    - Collaborate with data scientists and engineers
    - Deploy and monitor ML systems in cloud environments
    """
    
    result = scorer.compute_match_score(resume, job_desc)
    
    print("Resume Skills:", result["resume_skills"])
    print("Job Requirements:", result["job_requirements"])
    print("Matching Skills:", result["matching_skills"])
    print("Missing Skills:", result["missing_skills"])
    print(f"Final Score: {result['final_score']}%")
    print("Recommendation:", result["recommendation"])


if __name__ == "__main__":
    demo_ats_scorer_llm()