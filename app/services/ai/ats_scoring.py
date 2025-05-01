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
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

    def __init__(self, model_name="", api_key=None, api_base=""):
        """Initialize the ATS scorer with API credentials and model configuration.

        Args:
            model_name (str): Name of the LLM model to use. Falls back to MODEL_NAME env var.
            api_key (str, optional): API key for the LLM service. Falls back to API_KEY env var.
            api_base (str, optional): Base URL for the API service. Falls back to API_BASE env var.

        Raises:
            ValueError: If required credentials are missing after falling back to environment variables.
        """
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_base = api_base or os.getenv("API_BASE")
        self.model_name = model_name or os.getenv("MODEL_NAME")
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

        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.1,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base,
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
            Extract all technical skills, experience, and qualifications from the following resume text.
            Be thorough but precise - only extract actual skills (like programming languages, tools, frameworks)
            and professionally relevant qualifications.
            
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
            Extract all required technical skills, experience requirements, and key qualifications
            from the following job description. Focus on must-have requirements, not nice-to-have ones.
            
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
        """Calculate a simple keyword overlap score as an additional signal."""
        if not resume_skills or not job_skills:
            return 0.5

        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]

        matches = sum(
            1
            for skill in job_skills_lower
            if any(
                job_skill in skill or skill in job_skill
                for job_skill in resume_skills_lower
            )
        )

        if len(job_skills_lower) > 0:
            return matches / len(job_skills_lower)
        return 0.5

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
            weights = {
                "llm_analysis": 0.5,
                "semantic": 0.3,
                "keyword_overlap": 0.2,
            }

        # Extract information using LLM
        resume_analysis = self.extract_resume_info(resume_text)
        job_analysis = self.extract_job_info(job_text)

        # Calculate semantic similarity with TF-IDF
        semantic_score = self.calculate_semantic_similarity(resume_text, job_text)

        # Calculate keyword overlap score
        resume_skills = (
            resume_analysis.skills if hasattr(resume_analysis, "skills") else []
        )
        job_skills = job_analysis.skills if hasattr(job_analysis, "skills") else []
        keyword_score = self.calculate_keyword_overlap(resume_skills, job_skills)

        # Get LLM analysis of match
        match_analysis = self.analyze_match(resume_analysis, job_analysis)
        llm_score = match_analysis.get("score", 50) / 100  # Convert to 0-1 scale

        # Calculate final weighted score
        final_score = (
            weights["llm_analysis"] * llm_score
            + weights["semantic"] * semantic_score
            + weights["keyword_overlap"] * keyword_score
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
            "recommendation": match_analysis.get("recommendation", ""),
        }

        return result


# Example usage
def demo_ats_scorer_llm():
    """Demo function to showcase the ATSScorerLLM functionality."""
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("API_MODEL_NAME", "gpt-3.5-turbo")
    api_base = os.getenv("API_BASE", "https://api.openai.com/v1")

    scorer = ATSScorerLLM(api_key=api_key, model_name=model_name, api_base=api_base)

    resume = """
    Shalom
    DOSSEH
    Data Professional

    Number: (+229) 01-57-94-88-04
    Email: dosseh.contact@gmail.com

    Github: AnalyticAce
    LinkedIn: DOSSEH Shalom

    Portfolio: analyticace.github.io

    WORK EXPERIENCE

    Gozem - Africa's Super App,                                                                                                                                                     Cotonou, Benin
    Data Science & Analytics - Internship                                                                                                                            July. 2024 - April 2025
    Partnered with Gozem Money leadership to understand data requirements for the pre-launch phase of a new fintech vertical, including data extraction, and analysis across large-scale financial datasets for financial forecasting, and transaction analytics.
    Utilized Python (Pandas, Scikit-learn), SQL, and Looker Studio to generate actionable insights and align business needs with technical solutions.
    Leveraged SQL and Astro Airflow to design and implement real-time transaction monitoring 8,000,000+ monthly transactions, to detect and prevent fraud, money laundering, and terrorist financing activities, leveraging rule-based and anomaly detection models.
    Collaborated with the data engineering team to gather, structure, and integrate data from multiple sources (App Stores, Firebase, Data Warehouse) into a centralized analytics repository, enabling a unified view of key product insights.
    Worked closely with the Head of Data to define core KPIs for tracking app performance across digital storefronts, in-app engagement, and crash analytics, equipping product managers with data-driven insights to optimize user experience, and app store rankings.
    Gozem - Africa's Super App,                                                                                                                                                      Cotonou, Benin
    Data Analyst (Ride-hailing) - Internship                                                                                                                        Sept. 2023 - Jan. 2024
    Executed 65%+ of the squad’s quarterly tasks, completing 92% of high-priority deliverables  efficiently.
    Investigated transaction data, detecting and dismantling fraudulent schemes, leading to millions in recovered revenue.
    Performed data integrity checks, identifying and resolving anomalies to maintain accurate reporting.
    Automated routine reporting and analytics tasks, improving efficiency and precision in data insights.

    PROJECT

    MyResumo | Python, Streamlit, Natural Language Processing, Prompt Engineering
    Built an AI-backed resume generator designed to tailor your resume and skills based on a given job description. This innovative tool leverages the latest advancements in AI to provide you with an ATS friendly resume.
    MyTorch  | Python, Computational Analysis, Azure
    Developed a neural network-based chessboard analyzer from scratch without deep learning libraries. Trained models on FEN notation to classify six game states, achieving 90% accuracy in binary classification and 60-70% in multi-class tasks.
    Gomoku AI  | Python, Genetic Algorithm
    Developed a high-performance Gomoku AI bot using Min-Max with Alpha-Beta pruning and heuristic scoring to optimize decision-making. Designed to compete with GomokuCup AI bots, ensuring efficiency under computational constraints.
    PyDepViz | Python,  Package, Git Action
    A Python-native dependency graph visualizer designed to simplify dependency management in Python projects. It helps developers visualize and resolve dependency deadlocks efficiently.

    EDUCATION

    EPITECH - European Institute of Technology,                                                                                                                        Cotonou, Benin
    Bachelor's degree, Innovation and Information Technology                                                                                                  Oct. 2022 - Present
    I have cultivated robust skills across various domains of computer science, completing nearly 130 projects and mini-projects.
    Relevant Courses: Computer Numerical Analysis, Artificial Intelligence, Advanced DevOps, Advanced C++

    SKILLS

    Languages: English (Proficient),  French (Native)
    Programming: Python, SQL, Bash
    Soft Skills: Adaptability, Coachable, Problem-Solving, Decision-Making, Effective communication, Active listening
    Data Tools: Pandas, NumPy, Scikit-Learn, Looker Studio, Excel
    Cloud & DevOps: GCP, Azure, MongoDB, Docker, Jenkins, Ansible, Apache Airflow, Git Source Control, Github action, Linux.

    LEADERSHIP & COMMUNITY INVOLVEMENT

    Technical Workshop Facilitator, Innovation Hub at Epitech (March 2025 - Present)
    Hosted Python, DevOps, and AI workshops, mentoring students in technical fields.
    Partnered with industry professionals to deliver hands-on training sessions.
    Lead Project Manager, Epitech’s Student Bureau (March 2024 - Present)
    Led a team of 3 project managers, overseeing 30+ initiatives within time and budget constraints.
    Developed planning & tracking tools to optimize project execution.

    Event Manager & Core Member, Google Developer Students Club (June 2023 - July 2024)
    Organized tech events, hackathons, and networking sessions to engage student developers.
    Drove community initiatives to enhance learning in AI & Google Cloud Technologies.

    Social Data Analyst, AFRIK EDUTECH - EPITECH X IMPACT (Dec 2023 - Dec 2024)

    Conducted impact analysis & forecasting, guiding leadership decisions on program effectiveness.
    Collected & cleaned large-scale datasets for resource optimization.

    CERTIFICATIONS

    Career Essentials in GitHub Professional Certificate (Github, Completed February 2025)
    Data Scientist Certification (Datacamp, Expected July 2025) 
    AI Engineer for Data Scientists Associate Certification (Datacamp, Expected Sept 2025)                                                                                                        
    Certified Associate in Project Management (CAPM) (PMI, Expected Sept 2025)
    """

    job_desc = """
    Deel is the all-in-one payroll and HR platform for global teams. Our vision is to unlock global opportunity for every person, team, and business. Built for the way the world works today, Deel combines HRIS, payroll, compliance, benefits, performance, and equipment management into one seamless platform. With AI-powered tools and a fully owned payroll infrastructure, Deel supports every worker type in 100+ countries—helping businesses scale smarter, faster, and more compliantly.

    Among the largest globally distributed companies in the world, our team of 5,000 spans more than 100 countries, speaks 74 languages, and brings a connected and dynamic culture that drives continuous learning and innovation for our customers.

    Why should you be part of our success story?

    As the fastest-growing Software as a Service (SaaS) company in history, Deel is transforming how global talent connects with world-class companies – breaking down borders that have traditionally limited both hiring and career opportunities. We're not just building software; we're creating the infrastructure for the future of work, enabling a more diverse and inclusive global economy. In 2024 alone, we paid $11.2 billion to workers in nearly 100 currencies and provided healthcare and benefits to workers in 109 countries—ensuring people get paid and protected, no matter where they are.

    Our momentum is reflected in our achievements and customer satisfaction: CNBC Disruptor 50, Forbes Cloud 100, Deloitte Fast 500, and repeated recognition on Y Combinator’s top companies list – all while maintaining a 4.83 average rating from 15,000 reviews across G2, Trustpilot, Captera, Apple and Google.

    Your experience at Deel will be a career accelerator. At the forefront of the global work revolution, you'll tackle complex challenges that impact millions of people's working lives. With our momentum—backed by a $12 billion valuation and $800 million in Annual Recurring Revenue (ARR) in just over five years—you'll drive meaningful impact while building expertise that makes you a sought-after leader in the transformation of global work.

    Why join our Data team?

    Deel is a fast-growing company with a developing Data Science team, which gives the opportunity to contribute to our practices, direction, and tooling selection
    The nature of the role will be mostly project focused, so a lot of opportunity to dive deep into a single problem and solve it properly
    This role in particular aims to develop data insights from a large salary grouping. There’s scope to define how the data pipelines will work, and what statistical techniques and ML approaches to use
    Over 90% of the team’s work makes it to production which is rare for Data science/AI teams, we aim to deliver value each quarter


    Responsibilities

    Solve real world problems using Data Science and statistical techniques
    Implement functionality which can be served in production for internal customers as well as external customers
    Designing, building and maintaining data sets
    Data cleaning & modelling
    Feature engineering
    Feature extraction
    Building end-to-end data & machine learning pipelines
    Conduct reproducible research
    Collaborate with Engineering, Operations, Product Management and other functions in the company to deliver algorithmic solutions
    Apply software engineering practices in our code that implements our research and its infrastructure
    Produce high quality, clean, maintainable reproducible research and code


    Requirements

    High proficiency in Python and its data science stack.
    Background and experience in data/backend engineering, ideally in production environments (3+ years) (Mid/Senior Level role)
    Background and hands-on experience (2+ years) in implementing research and algorithms in Python, specifically in information retrieval, text processing, NLP, and machine learning
    Experience with developing AI solutions across a variety of domains
    Track record of good written and verbal communication of complex things in a simple way as well as ability to collaborate well with people from different backgrounds and professions
    A Bachelor’s degree or higher
    Must have hands on experience working with SQL
    Must have hands on experience working with Python (Preferably with Pandas)
    Must be strong at applying statistical methods to data
    Must be strong with data pipelining
    Must be an independent thinker and have the ability to work independently to solve problems


    Total Rewards

    Our workforce deserves fair and competitive pay that meets them where they are. With scalable benefits, rewards, and perks, our total rewards programs reflect our commitment to inclusivity and access for all.

    Some things you’ll enjoy

    Stock grant opportunities dependent on your role, employment status and location
    Additional perks and benefits based on your employment status and country
    The flexibility of remote work, including optional WeWork access


    At Deel, we’re an equal-opportunity employer that values diversity and positively encourage applications from suitably qualified and eligible candidates regardless of race, religion, sex, national origin, gender, sexual orientation, age, marital status, veteran status, disability status, pregnancy or maternity or other applicable legally protected characteristics.

    Unless otherwise agreed, we will communicate with job applicants using Deel-specific emails, which include @deel.com and other acquired company emails like @payspace.com and @paygroup.com. You can view the most up-to-date job listings at Deel by visitingour careers page.

    Deel is an equal-opportunity employer and is committed to cultivating a diverse and inclusive workplace that reflects different abilities, backgrounds, beliefs, experiences, identities and perspectives.

    Deel will provide accommodation on request throughout the recruitment, selection and assessment process for applicants with disabilities. If you require accommodation, please inform our Talent Acquisition Team at recruiting@deel.com of the nature of the accommodation that you may require, to ensure your equal participation.

    We use Covey as part of our hiring and/or promotional processes. As part of the evaluation process, we provide Covey with job requirements and candidate-submitted applications.Certain features of the platform may qualify it as an Automated Employment Decision Tool (AEDT) under applicable regulations. For positions in New York City, our use of Covey complies with NYC Local Law 144.

    We began using Covey Scout for Inbound on March 30, 2025.

    For more information about our data protection practices, please visit our Privacy Policy. You can review the independent bias audit report covering our use of Covey here: https://getcovey.com/nyc-local-law-144-independent-bias-audit-report/
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
