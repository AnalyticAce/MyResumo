from langchain.prompts import PromptTemplate
from langchain.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from typing import Dict, Any
import json
import re

class AtsResumeOptimizer:
    def __init__(self, model_name: str = "gpt-3.5-turbo", resume: str = "", api_key: str = "", language: str = "en") -> None:
        self.model_name = model_name
        self.resume = resume
        self.api_key = api_key
        self.language = language
        self.llm = self._get_openai_model()
        self.output_parser = JsonOutputParser()
        self._setup_chain()

    def _get_openai_model(self):
        """Initialize the OpenAI model with appropriate settings"""
        if self.model_name:
            return ChatOpenAI(
                model_name=self.model_name,
                temperature=0,
                openai_api_key=self.api_key,
                openai_api_base="https://api.openai.com/v1/chat/completions",
            )
        else:
            return ChatOpenAI(temperature=0)

    def _get_prompt_template(self):
        """Create the PromptTemplate for ATS resume optimization"""
        template = """
        # ROLE: Expert ATS Resume Optimization Specialist

        You are an expert ATS (Applicant Tracking System) Resume Optimizer with specialized knowledge in resume writing, keyword optimization, and applicant tracking systems. Your task is to transform the candidate's existing resume into a highly optimized version tailored specifically to the provided job description, maximizing the candidate's chances of passing through ATS filters while maintaining honesty and accuracy.

        ## INPUT DATA:
        
        ### JOB DESCRIPTION:
        {job_description}
        
        ### CANDIDATE'S CURRENT RESUME:
        {resume}
        
        ## OPTIMIZATION INSTRUCTIONS:

        1. **ANALYZE THE JOB DESCRIPTION**
            - Extract key requirements, skills, qualifications, and responsibilities
            - Identify primary keywords, secondary keywords, and industry-specific terminology
            - Note the exact phrasing and terminology used by the employer
        
        2. **EVALUATE THE CURRENT RESUME**
            - Compare existing content against job requirements
            - Identify skills and experiences that align with the job
            - Identify gaps or areas where alignment could be improved
            
        3. **CREATE AN ATS-OPTIMIZED RESUME**
            - Use a clean, ATS-friendly format with standard section headings
            - Include the candidate's name, contact information, and LinkedIn profile (if available)
            - Create a targeted professional summary highlighting relevant qualifications
            - Incorporate exact keywords and phrases from the job description throughout the resume
            - Prioritize and emphasize experiences most relevant to the target position
            - Use industry-standard terminology that ATS systems recognize
            - Quantify achievements with metrics where possible
            - Remove irrelevant information that doesn't support this application
            - Use a chronological format unless a functional format is clearly better for this candidate
            - Include a skills section with bullet points of relevant hard and soft skills
            
        4. **ATS OPTIMIZATION TECHNIQUES**
            - Use standard section headings (e.g., "Work Experience" not "Career Adventures")
            - Avoid tables, columns, headers, footers, images, and special characters
            - Use standard bullet points (• or - only)
            - Use common file formats and fonts (Arial, Calibri, Times New Roman)
            - Include keywords in context rather than keyword stuffing
            - Use both spelled-out terms and acronyms where applicable (e.g., "Search Engine Optimization (SEO)")
            - Ensure job titles, company names, dates, and locations are clearly formatted
            - Keep formatting consistent throughout the document
            
        5. **ETHICAL GUIDELINES**
            - Only include truthful information from the original resume
            - Do not fabricate experience, skills, or qualifications
            - Focus on highlighting relevant actual experience, not inventing new experience
            - Optimize language and presentation while maintaining accuracy
            
        ## OUTPUT FORMAT:

        You MUST return ONLY a valid JSON object with NO additional text, explanation, or commentary.
        The JSON must follow this EXACT structure:

        {{
            "user_information": {{
                "name": "",
                "main_job_title": "",
                "profile_description": "",
                "email": "",
                "linkedin": "",
                "github": "",
                "experiences": [
                    {{
                        "job_title": "",
                        "company": "",
                        "start_date": "",
                        "end_date": "",
                        "four_tasks": []
                    }}
                ],
                "education": [
                    {{
                        "institution": "",
                        "degree": "",
                        "description": "",
                        "start_date": "",
                        "end_date": ""
                    }}
                ],
                "skills": {{
                    "hard_skills": [],
                    "soft_skills": []
                }},
                "hobbies": []
            }},
            "projects": [
                {{
                    "project_name": "",
                    "two_goals_of_the_project": [],
                    "project_end_result": ""
                }}
            ],
            "certificate": [
                {{
                    "name": "",
                    "institution": "",
                    "description": "",
                    "date": ""
                }}
            ],
            "extra_curricular_activities": [
                {{
                    "name": "",
                    "description": ""
                }}
            ]
        }}

        IMPORTANT REQUIREMENTS:
        1. The "four_tasks" array must contain EXACTLY 4 items for each experience
        2. The "two_goals_of_the_project" array must contain EXACTLY 2 items for each project
        3. Make sure all dates follow a consistent format (YYYY-MM or MM/YYYY)
        4. Ensure all fields are filled with appropriate data extracted from the resume
        5. Return ONLY the JSON object with no other text
        """
        return PromptTemplate.from_template(template=template)

    def _setup_chain(self):
        """Set up the LLMChain for processing job descriptions and resumes"""
        prompt_template = self._get_prompt_template()
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt_template,
            output_key="ats_resume"
        )

    def generate_ats_optimized_resume_json(self, job_description: str) -> Dict[str, Any]:
        """
        Generate an ATS-optimized resume in JSON format
        
        Args:
            job_description (str): The target job description
            
        Returns:
            dict: The optimized resume in JSON format
        """
        if not self.resume:
            return {"error": "Resume not provided"}

        try:
            result = self.chain.invoke({
                "job_description": job_description,
                "resume": self.resume
            })
            try:
                json_result = json.loads(result["ats_resume"])
                return json_result
            except json.JSONDecodeError:
                try:
                    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', result["ats_resume"])
                    if json_match:
                        json_str = json_match.group(1)
                        return json.loads(json_str)
                    
                    json_str = re.search(r'(\{[\s\S]*\})', result["ats_resume"])
                    if json_str:
                        return json.loads(json_str.group(1))
                    
                    return {"error": "Could not extract valid JSON from response"}
                except Exception as e:
                    return {"error": f"JSON parsing error: {str(e)}", "raw_response": result["ats_resume"]}
                
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}

if __name__ == "__main__":
    model = AtsResumeOptimizer(
        model_name="gpt-3.5-turbo",
        resume="Your resume text here...",
        api_key="your-api-key-here"
    )

    job_description = "Your job description here..."
    result = model.generate_ats_optimized_resume_json(job_description)

    print(json.dumps(result, indent=2))