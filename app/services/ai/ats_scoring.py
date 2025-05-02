"""AI-powered ATS Soring module.

This module provides the ATSScorerLLM class that leverages AI language models
to analyze and score resumes based on job descriptions.
"""

import json
import os
import re
from typing import List, Optional

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.token_tracker import TokenTracker


class SkillsExtraction(BaseModel):
    """Model for structured extraction of skills and qualifications from text.

    This Pydantic model defines the structure for extracted information from
    resumes and job descriptions, including technical skills, experience,
    requirements, and industry domains.
    """

    skills: List[str] = Field(
        description="List of technical skills extracted from the text"
    )
    experience_years: Optional[int] = Field(
        description="Years of experience mentioned in the text, if any"
    )
    key_requirements: List[str] = Field(
        description="Key requirements or qualifications extracted from the text"
    )
    domains: List[str] = Field(
        description="Domains or industries mentioned in the text"
    )


class ATSScorerLLM:
    """Class for scoring resumes against job descriptions using AI techniques.

    This class provides methods to extract information from resumes and job descriptions,
    calculate semantic similarity, and perform a comprehensive match analysis using
    LLM-based techniques.
    """

    def __init__(self, model_name="", api_key=None, api_base="", user_id=None):
        """Initialize the ATS scorer with API credentials and model configuration.

        Args:
            model_name (str): Name of the LLM model to use. Falls back to MODEL_NAME env var.
            api_key (str, optional): API key for the LLM service. Falls back to API_KEY env var.
            api_base (str, optional): Base URL for the API service. Falls back to API_BASE env var.
            user_id (str, optional): User ID for token tracking.

        Raises:
            ValueError: If required credentials are missing after falling back to environment variables.
        """
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_base = api_base or os.getenv("API_BASE")
        self.model_name = model_name or os.getenv("MODEL_NAME")
        self.user_id = user_id

        if not self.api_key:
            raise ValueError(
                "An LLM API key is required. Provide it or set API_KEY environment variable."
            )

        if not self.api_base:
            raise ValueError(
                "An LLM API base is required. Provide it or set API_BASE environment variable."
            )

        if not self.model_name:
            raise ValueError(
                "An LLM model name is required. Provide it or set MODEL_NAME environment variable."
            )

        # Use TokenTracker to create a tracked instance of the LLM
        self.llm = TokenTracker.get_tracked_langchain_llm(
            model_name=self.model_name,
            temperature=0.1,
            api_key=self.api_key,
            api_base=self.api_base,
            feature="ats_scoring",
            user_id=self.user_id
        )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )

        self.parser = PydanticOutputParser(pydantic_object=SkillsExtraction)

        self.setup_prompts()

        self.setup_chains()

    def setup_prompts(self):
        """Set up the prompts for various extraction tasks."""
        # Prompt for extracting skills from resume
        self.resume_prompt = PromptTemplate(
            template="""You are an expert ATS (Applicant Tracking System) analyzer.
            Extract ALL skills, experience, and qualifications from the following resume text.
            Be comprehensive and generous in your extraction, including:
            - Technical skills (programming languages, tools, frameworks, etc.)
            - Soft skills (communication, leadership, etc.)
            - Domain knowledge and industry experience
            - Implied skills based on work descriptions
            - Educational qualifications and certifications
            - Transferable skills from different contexts
            
            Be inclusive rather than restrictive - capture everything that could potentially match a job requirement.
            
            RESUME TEXT:
            {resume_text}
            
            {format_instructions}
            """,
            input_variables=["resume_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Prompt for extracting requirements from job description
        self.job_prompt = PromptTemplate(
            template="""You are an expert job analyzer.
            Extract ALL skills, experience requirements, and qualifications from the following job description.
            Be comprehensive, including both required and preferred qualifications.
            
            Include:
            - Technical skills and tools mentioned
            - Experience and education requirements
            - Soft skills and personal qualities
            - Domain knowledge and industry expertise
            - Any other attributes that would make a candidate suitable
            
            JOB DESCRIPTION:
            {job_text}
            
            {format_instructions}
            """,
            input_variables=["job_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Prompt for skill matching and score analysis
        self.matching_prompt = PromptTemplate(
            template="""You are an expert ATS (Applicant Tracking System) analyzer and recruiter.
            Compare the candidate's skills and qualifications with the job requirements and provide an analysis.
            
            CANDIDATE SKILLS AND QUALIFICATIONS:
            {resume_skills}
            
            JOB REQUIREMENTS:
            {job_requirements}
            
            Based on a detailed analysis, provide:
            1. A scoring from 0-100 indicating how well the candidate's skills match the job requirements:
               - Score 70-100 if the candidate meets the core requirements and has most of the desired skills
               - Score 50-69 if the candidate meets most core requirements but is missing some key skills
               - Score 30-49 if the candidate meets some requirements but has significant gaps
               - Score 0-29 if the candidate lacks most of the core requirements
               
               Consider transferable skills and potential ability to learn required skills when scoring.
               If a candidate has 60% or more relevant skills, they deserve serious consideration.
               
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
            input_variables=["resume_skills", "job_requirements"],
        )

    def setup_chains(self):
        """Set up the LangChain runnable chains for each task."""
        self.resume_chain = self.resume_prompt | self.llm 
        
        self.job_chain = self.job_prompt | self.llm
        
        self.matching_chain = self.matching_prompt | self.llm

    def extract_resume_info(self, resume_text):
        """Extract skills and qualifications from resume using LLM."""
        try:
            result = self.resume_chain.invoke({"resume_text": resume_text})
            parsed_result = self.parser.parse(result.content)
            return parsed_result
        except Exception as e:
            print(f"Error extracting resume info: {e}")
            result = self.resume_chain.invoke({"resume_text": resume_text})
            return result

    def extract_job_info(self, job_text):
        """Extract requirements from job description using LLM."""
        try:
            result = self.job_chain.invoke({"job_text": job_text})
            parsed_result = self.parser.parse(result.content)
            return parsed_result
        except Exception as e:
            print(f"Error extracting job info: {e}")
            result = self.job_chain.invoke({"job_text": job_text})
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
            return 0.5

    def calculate_keyword_overlap(self, resume_skills, job_skills):
        """Calculate a sophisticated keyword overlap score between resume and job skills.
        
        This method identifies semantic matches between job skills and resume skills,
        recognizing related concepts and synonyms, not just exact matches.
        
        Args:
            resume_skills: List of skills extracted from the resume
            job_skills: List of skills extracted from the job description
            
        Returns:
            float: Overlap score between 0 and 1
        """
        if not resume_skills or not job_skills:
            return 0.5

        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Define technology and concept synonym groups to enhance matching
        synonyms = {
            "python": ["py", "python programming", "python development"],
            "data science": ["data analytics", "data analysis", "analytics", "data scientist"],
            "machine learning": ["ml", "ai", "artificial intelligence", "predictive modeling"],
            "sql": ["database", "mysql", "postgresql", "tsql", "relational database"],
            "communication": ["presenting", "public speaking", "writing", "interpersonal"],
            "visualization": ["dashboard", "charts", "data viz", "looker", "tableau", "power bi"],
            "analysis": ["analytics", "analyze", "analytical"],
            "programming": ["coding", "development", "software engineering"],
            "statistics": ["statistical analysis", "statistical methods", "data modeling"],
            "cloud": ["aws", "azure", "gcp", "google cloud"],
            "devops": ["ci/cd", "jenkins", "git", "github", "deployment"],
        }
        
        # Create an expanded set of resume skills using synonyms
        extended_resume_skills = set(resume_skills_lower)
        for skill in resume_skills_lower:
            for key, values in synonyms.items():
                # Add related skills and concepts to the extended set
                if skill == key or any(v in skill for v in values):
                    extended_resume_skills.update(values)
                    extended_resume_skills.add(key)
        
        # Count exact and semantic matches with the extended skill set
        matches = sum(
            1
            for skill in job_skills_lower
            if any(
                job_skill in skill or skill in job_skill 
                for job_skill in extended_resume_skills
            )
        )
        
        # Handle composite skills (multi-word concepts)
        for job_skill in job_skills_lower:
            words = job_skill.split()
            if len(words) > 1:
                # Award partial credit for partial matches of multi-word skills
                if sum(1 for word in words if any(word in rs for rs in resume_skills_lower)) >= len(words) / 2:
                    matches += 0.5  # Partial match
        
        # Calculate normalized overlap score
        overlap_score = matches / len(job_skills_lower) if len(job_skills_lower) > 0 else 0.5
        
        # Ensure score is within valid range
        return min(1.0, overlap_score)

    def analyze_match(self, resume_analysis, job_analysis):
        """Have the LLM analyze the match between resume and job requirements."""
        try:
            if not isinstance(resume_analysis, str):
                resume_analysis = str(resume_analysis.model_dump())
            if not isinstance(job_analysis, str):
                job_analysis = str(job_analysis.model_dump())

            result = self.matching_chain.invoke({
                "resume_skills": resume_analysis, 
                "job_requirements": job_analysis
            })

            json_match = re.search(r"\{.*\}", result.content, re.DOTALL)

            if json_match:
                try:
                    json_str = json_match.group(0)
                    parsed_result = json.loads(json_str)
                    return parsed_result
                except json.JSONDecodeError:
                    pass

            # If we can't parse as JSON, extract the fields manually
            score_match = re.search(
                r'["\']?score["\']?\s*:\s*(\d+)', result.content, re.IGNORECASE
            )
            score = (
                int(score_match.group(1)) if score_match else 50
            )

            matching_section = re.search(
                r'["\']?matching_skills["\']?\s*:\s*\[(.*?)\]', result.content, re.DOTALL
            )
            matching_skills = []
            if matching_section:
                skills_text = matching_section.group(1)
                matching_skills = re.findall(r'["\']([^"\']+)["\']', skills_text)

            missing_section = re.search(
                r'["\']?missing_skills["\']?\s*:\s*\[(.*?)\]', result.content, re.DOTALL
            )
            missing_skills = []
            if missing_section:
                skills_text = missing_section.group(1)
                missing_skills = re.findall(r'["\']([^"\']+)["\']', skills_text)

            # Extract recommendation
            rec_match = re.search(
                r'["\']?recommendation["\']?\s*:\s*["\']([^"\']+)["\']', result.content
            )
            recommendation = (
                rec_match.group(1)
                if rec_match
                else "No specific recommendation provided."
            )

            return {
                "score": score,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "recommendation": recommendation,
            }

        except Exception as e:
            print(f"Error analyzing match: {e}")
            return {
                "score": 50,
                "matching_skills": [],
                "missing_skills": [],
                "recommendation": "Error analyzing match. The candidate appears to have relevant skills but a detailed analysis could not be completed.",
            }

    def compute_match_score(self, resume_text, job_text, weights=None):
        """Calculate comprehensive match score between resume and job."""
        if weights is None:
            # Default weights for scoring components
            # These can be adjusted based on the specific use case or user preference
            # Default weights are set to balance the components
            weights = {
                "llm_analysis": 0.4,
                "semantic": 0.3,
                "keyword_overlap": 0.3,
            }

        # Extract information using LLM
        resume_analysis = self.extract_resume_info(resume_text)
        job_analysis = self.extract_job_info(job_text)

        # Calculate semantic similarity with TF-IDF
        semantic_score = self.calculate_semantic_similarity(resume_text, job_text)
        
        # Apply a minimum baseline for semantic similarity to avoid underscoring
        semantic_score = max(semantic_score, 0.4)  # Set a floor of 0.4 (40%) for semantic similarity

        # Calculate keyword overlap score
        resume_skills = (
            resume_analysis.skills if hasattr(resume_analysis, "skills") else []
        )
        job_skills = job_analysis.skills if hasattr(job_analysis, "skills") else []
        keyword_score = self.calculate_keyword_overlap(resume_skills, job_skills)

        # Get LLM analysis of match
        match_analysis = self.analyze_match(resume_analysis, job_analysis)
        llm_score = match_analysis.get("score", 50) / 100  # Convert to 0-1 scale
        
        # Apply a minimum baseline for LLM score to prevent severe underscoring
        llm_score = max(llm_score, 0.45)  # Set a floor of 0.45 (45%) for LLM score
        
        # Calculate final weighted score
        final_score = (
            weights["llm_analysis"] * llm_score
            + weights["semantic"] * semantic_score
            + weights["keyword_overlap"] * keyword_score
        )
        
        # Apply a gentle curve to the final score to avoid excessively low scores
        # This makes scores more realistic for real-world job applications
        if final_score < 0.7:  # If score is below 70%
            # Apply a gentle boost that increases lower scores more than higher ones
            boost_factor = 0.15 * (1 - final_score)  # More boost for lower scores
            final_score = min(final_score + boost_factor, 1.0)  # Cap at 100%

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
            "recommendation": match_analysis.get("recommendation", ""),
        }

        return result


# Example usage
def demo_ats_scorer_llm():
    """Demo function to showcase the ATSScorerLLM functionality."""
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("API_MODEL_NAME", "gpt-4-turbo")
    api_base = os.getenv("API_BASE", "https://api.openai.com/v1")

    scorer = ATSScorerLLM(api_key=api_key, model_name=model_name, api_base=api_base)

    resume = """
    """

    job_desc = """
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
