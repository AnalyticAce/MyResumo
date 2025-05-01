"""AI-powered resume optimization module.

This module provides the AtsResumeOptimizer class that leverages AI language models
to analyze and optimize resumes based on job descriptions, improving compatibility
with Applicant Tracking Systems (ATS).
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from app.services.ai.ats_scoring import ATSScorerLLM


class AtsResumeOptimizer:
    """ATS Resume Optimizer.

    A class that uses AI language models to optimize resumes for Applicant Tracking
    Systems (ATS) based on specific job descriptions.

    This class leverages OpenAI's language models to analyze a job description and a
    provided resume, then generates an ATS-optimized version of the resume in JSON format.
    The optimization focuses on incorporating relevant keywords, formatting for ATS
    readability, and highlighting the most relevant experience for the target position.

    Attributes:
    ----------
        model_name: The name of the OpenAI model to use for processing
        resume: The resume text to be optimized
        api_key: OpenAI API key for authentication
        api_base: Base URL for the OpenAI API
        llm: The initialized language model instance
        output_parser: Parser for converting LLM output to JSON format
        ats_scorer: ATSScorerLLM instance for scoring resume and extracting missing skills

    Methods:
    -------
        _get_openai_model()
            Initialize the OpenAI model with appropriate settings
        _get_prompt_template(missing_skills=None)
            Create the PromptTemplate for ATS resume optimization with missing skills
        _setup_chain()
            Set up the processing pipeline for job descriptions and resumes
        generate_ats_optimized_resume_json(job_description)
            Generate an ATS-optimized resume in JSON format based on the provided job description

    Example:
        >>> # Note: Ensure to replace "your_api_key" and "your resume text" with actual values
        >>> optimizer = AtsResumeOptimizer(api_key="your_api_key", resume="your resume text")
        >>> optimized_resume = optimizer.generate_ats_optimized_resume_json("job description text")
        >>> print(optimized_resume)
        >>> # Output: JSON object with optimized resume
    """

    def __init__(
        self,
        model_name: str = None,
        resume: str = None,
        api_key: str = None,
        api_base: str = None,
    ) -> None:
        """Initialize the AI model for resume processing.

        Args:
            model_name: The name of the OpenAI model to use.
            resume: The resume text to be optimized.
            api_key: OpenAI API key for authentication.
            api_base: Base URL for the OpenAI API.
            language: Language for processing the resume.
        """
        self.model_name = model_name or os.getenv("MODEL_NAME")
        self.resume = resume
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_base = api_base or os.getenv("API_BASE")

        # Initialize LLM component and output parser
        self.llm = self._get_openai_model()
        self.output_parser = JsonOutputParser()
        self.chain = None
        
        # Initialize ATS scorer for skill extraction and analysis
        self.ats_scorer = None
        if self.api_key and self.api_base and self.model_name:
            self.ats_scorer = ATSScorerLLM(
                model_name=self.model_name,
                api_key=self.api_key,
                api_base=self.api_base,
            )

        self._setup_chain()

    def _get_openai_model(self) -> ChatOpenAI:
        """Initialize the OpenAI model with appropriate settings."""
        if self.model_name:
            return ChatOpenAI(
                model_name=self.model_name,
                temperature=0,
                openai_api_key=self.api_key,
                openai_api_base=self.api_base,
            )
        else:
            return ChatOpenAI(temperature=0)

    def _get_prompt_template(self, missing_skills: Optional[List[str]] = None) -> PromptTemplate:
        """Create the PromptTemplate for ATS resume optimization.
        
        Args:
            missing_skills: A list of skills identified as missing from the resume
                        that should be incorporated if the candidate has them.

        Returns:
            PromptTemplate: A prompt template with instructions for resume optimization.
        """
        recommended_skills_section = ""
        if missing_skills and len(missing_skills) > 0:
            skills_list = ", ".join([f"'{skill}'" for skill in missing_skills])
            recommended_skills_section = f"""
        ## RECOMMENDED SKILLS TO ADD
        
        The following skills were identified as potentially valuable for this position but may be missing or not prominently featured in the resume:
        
        {skills_list}
        
        If the candidate has any experience with these skills, even minor exposure:
        - Highlight them prominently in the skills section
        - Look for ways to showcase these skills in past experience descriptions
        - Ensure you're using the exact terminology as listed
        - Do NOT fabricate experience with these skills, only highlight them if they exist
        """
        
        template = f"""
        # ROLE: Expert ATS Resume Optimization Specialist
        You are an expert ATS (Applicant Tracking System) Resume Optimizer with specialized knowledge in resume writing, keyword optimization, and applicant tracking systems. Your task is to transform the candidate's existing resume into a highly optimized version tailored specifically to the provided job description, maximizing the candidate's chances of passing through ATS filters while maintaining honesty and accuracy.
        
        ## INPUT DATA:

        ### JOB DESCRIPTION:
        {{job_description}}

        ### CANDIDATE'S CURRENT RESUME:
        {{resume}}
        
        {recommended_skills_section}

        ## OPTIMIZATION PROCESS:

        1. **ANALYZE THE JOB DESCRIPTION**
            - Extract key requirements, skills, qualifications, and responsibilities
            - Identify primary keywords, secondary keywords, and industry-specific terminology
            - Note the exact phrasing and terminology used by the employer
            - Identify technical requirements (software, tools, frameworks, etc.)
            - Detect company values and culture indicators
            - Determine desired experience level and specific metrics/achievements valued

        2. **EVALUATE THE CURRENT RESUME**
            - Compare existing content against job requirements
            - Identify skills and experiences that align with the job
            - Detect terminology mismatches and missing keywords
            - Assess the presentation of achievements and results
            - Calculate an initial "match score" to identify improvement areas
            - Note transferable skills that could be reframed for the target position

        3. **CREATE AN ATS-OPTIMIZED RESUME**
            - Use a clean, ATS-friendly format with standard section headings
            - Include the candidate's name, contact information, and professional profiles
            - Create a targeted professional summary highlighting relevant qualifications
            - Incorporate exact keywords and phrases from the job description throughout the resume
            - Prioritize and emphasize experiences most relevant to the target position
            - Reorder content to place most relevant experiences and skills first
            - Use industry-standard terminology that ATS systems recognize
            - Quantify achievements with metrics where possible (numbers, percentages, dollar amounts)
            - Remove irrelevant information that doesn't support this application
            - Ensure job titles, company names, dates, and locations are clearly formatted
            - Include a skills section with relevant hard and soft skills using job description terminology

        4. **ATS OPTIMIZATION TECHNIQUES**
            - Use standard section headings (e.g., "Work Experience" not "Career Adventures")
            - Avoid tables, columns, headers, footers, images, and special characters
            - Use standard bullet points (• or - only)
            - Use common file formats and fonts (Arial, Calibri, Times New Roman)
            - Include keywords in context rather than keyword stuffing
            - Use both spelled-out terms and acronyms where applicable (e.g., "Search Engine Optimization (SEO)")
            - Keep formatting consistent throughout the document
            - For technical positions, include relevant projects with clear descriptions
            - Limit project listings to 3-4 most relevant examples

        5. **ETHICAL GUIDELINES**
            - Only include truthful information from the original resume
            - Do not fabricate experience, skills, or qualifications
            - Focus on highlighting relevant actual experience, not inventing new experience
            - Reframe existing experience to highlight relevant skills
            - Optimize language and presentation while maintaining accuracy

        ## OUTPUT FORMAT:

        You MUST return ONLY a valid JSON object with NO additional text, explanation, or commentary.
        The JSON must follow this EXACT structure:

        {{{{
            "user_information": {{{{
                "name": "",
                "main_job_title": "",
                "profile_description": "",
                "email": "",
                "linkedin": "",
                "github": "",
                "experiences": [
                    {{{{
                        "job_title": "",
                        "company": "",
                        "start_date": "",
                        "end_date": "",
                        "location": "",
                        "four_tasks": []
                    }}}}
                ],
                "education": [
                    {{{{
                        "institution": "",
                        "degree": "",
                        "location": "",
                        "description": "",
                        "start_date": "",
                        "end_date": ""
                    }}}}
                ],
                "skills": {{{{
                    "hard_skills": [],
                    "soft_skills": []
                }}}},
                "hobbies": []
            }}}},
            "projects": [
                {{{{
                    "project_name": "",
                    "project_link": "",
                    "two_goals_of_the_project": [],
                    "project_end_result": "",
                    "tech_stack": []
                }}}}
            ],
            "certificate": [
                {{{{
                    "name": "",
                    "link" : "",
                    "institution": "",
                    "description": "",
                    "date": ""
                }}}}
            ],
            "extra_curricular_activities": [
                {{{{
                    "name": "",
                    "description": "",
                    "start_date": "",
                    "end_date": ""
                }}}}
            ]
        }}}}

        IMPORTANT REQUIREMENTS:
        1. The "four_tasks" array must contain EXACTLY 4 items for each experience
        2. The "two_goals_of_the_project" array must contain EXACTLY 2 items for each project
        3. Make sure all dates follow a consistent format (YYYY-MM or MM/YYYY)
        4. Ensure all fields are filled with appropriate data extracted from the resume
        5. Return ONLY the JSON object with no other text
        """
        return PromptTemplate.from_template(template=template)

    def _setup_chain(self, missing_skills: Optional[List[str]] = None) -> None:
        """Set up the processing pipeline for job descriptions and resumes.

        This method configures the functional composition approach with the pipe operator
        to create a processing chain from prompt template to language model.
        
        Args:
            missing_skills: List of skills identified as missing that should be incorporated
                        into the optimization prompt.
        """
        prompt_template = self._get_prompt_template(missing_skills)
        self.chain = prompt_template | self.llm

    def generate_ats_optimized_resume_json(
        self, job_description: str
    ) -> Dict[str, Any]:
        """Generate an ATS-optimized resume in JSON format.

        Args:
            job_description: The target job description.

        Returns:
        -------
            dict: The optimized resume in JSON format.
        """
        if not self.resume:
            return {"error": "Resume not provided"}

        try:
            missing_skills = []
            if self.ats_scorer:
                try:
                    score_result = self.ats_scorer.compute_match_score(
                        self.resume, job_description
                    )
                    missing_skills = score_result.get("missing_skills", [])
                    self._setup_chain(missing_skills)
                except Exception as e:
                    print(f"Warning: ATS scoring failed, proceeding without skill recommendations: {str(e)}")
                    pass

            result = self.chain.invoke(
                {"job_description": job_description, "resume": self.resume}
            )

            try:
                if hasattr(result, "content"):
                    content = result.content
                else:
                    content = result

                try:
                    json_result = json.loads(content)
                    return json_result
                except json.JSONDecodeError:
                    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
                    if json_match:
                        json_str = json_match.group(1)
                        return json.loads(json_str)

                    json_str = re.search(r"(\{[\s\S]*\})", content)
                    if json_str:
                        return json.loads(json_str.group(1))

                    return {
                        "error": f"Could not extract valid JSON from response: {content[:100]}..."
                    }
            except Exception as e:
                return {
                    "error": f"JSON parsing error: {str(e)}",
                    "raw_response": str(result)[:500],
                }

        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}


if __name__ == "__main__":
    with open("../../../data/sample_resumes/resume.txt", "r") as f:
        resume = f.read()

    with open("../../../data/sample_descriptions/job_description_1.txt", "r") as f:
        job_description = f.read()

    API_KEY = "sk-********************"
    API_BASE = "https://api.deepseek.com/v1"
    MODEL_NAME = "deepseek-chat"

    model = AtsResumeOptimizer(
        model_name=MODEL_NAME,
        resume=resume,
        api_key=API_KEY,
        api_base=API_BASE,
    )

    result = model.generate_ats_optimized_resume_json(job_description)

    print(json.dumps(result, indent=2))
