from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from typing import Dict, Any
import json
import re
import os

class AtsResumeOptimizer:
    def __init__(self, model_name: str = "gpt-3.5-turbo", resume: str = "", api_key: str = "", api_base = "https://api.openai.com/v1/chat/completions", language: str = "en") -> None:
        self.model_name = model_name
        self.resume = resume
        self.api_key = api_key
        self.api_base = api_base
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
                openai_api_base=self.api_base,
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
        # self.chain = prompt_template | self.llm
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
    job_description_1 = """
    Schedule: Full-Time, Monday - Friday, Eastern Time

    Benefits: Fully remote position, 40 hours Weekly, Paid Time Off, 2 Days Off

    Salary / Rate: $5,000 Annually

    About The Company

    At Nao Medical, we're revolutionizing healthcare by blending cutting-edge technology with heartfelt, personalized care. Over the past 13 years, we've proudly served more than a million New Yorkers at our various locations. Our mission is simple: through our multi-specialty practice, we provide accessible, quality care tailored to each patient's needs. We're breaking down barriers, championing health equity, and delivering value-based care to create healthier communities.

    Job Summary

    As a Junior Engineer - generative AI, you will play a crucial role in supporting our development efforts. You will work closely with cross-functional teams and participate in building applications that utilize generative AI technologies. This is an excellent opportunity for junior developers looking to expand their skills in a fast-paced environment.

    Primary Responsibilities

    Collaborate with global teams to design and develop AI - Driven applications. 
    Write clean and efficient code in Python to implement generative AI solutions. 
    Communicate ideas and projects updates clearly to team members and stake holders. 

    Job Requirements

    Qualifications

    Solid foundation in Python Programming. 
    Excellent English communication skills (both written and verbal) 
    Strong confidence and the ability to articulate ideas clearly. 
    Genuine Interest in generative AI technologies and automation 

    Technical Requirements

    Candidates must provide their equipment and technology meeting these minimum specification 
    Up-to-date desktop or laptop computer with at least 8GB of RAM and a modern processor (Intel i5 or equivalent)
    Windows 10 or macOS 10.15 or later
    High-speed internet connection with a minimum speed of 100 Mbps
    Functional headset with microphone, webcam, and reliable keyboard and mouse
    Quiet workspace devoid of distractions
    A second monitor is preferred but not required
    Emergency backup or contingency plan for technology or connectivity issues.

    What We Offer 

    A Collaborative and innovative work environment. 
    Opportunities for professional growth and development. 
    The chance to work on cutting - edge technologies in the AI Space 

    Equal Employment Opportunity Statement

    Nao Medical is n Equal Opportunity Employer. We are committed to fostering, cultivating, and preserving a culture of diversity, equity, and inclusion. We do not discriminate based on race, color, religion, creed, national origin, ancestry, sex, age, disability, marital status, sexual orientation, gender identity, genetic information, military or veteran status, or any other characteristic protected by applicable federal, state, or local laws. This policy applies to all employment terms and conditions, including recruiting, hiring, placement, promotion, termination, layoff, recall, transfer, leaves of absences, compensation, and training.

    Nao Medical is dedicated to providing a work environment free from discrimination and harassment and treating all individuals with respect and dignity. Combining individuals from diverse backgrounds and experiences creates a more innovative, creative and productive workforce.

    Nao Medical is an equal opportunity employer, celebrates diversity, and is committed to building an inclusive environment for all employees and patients.

    Experience the Nao Medical difference. Join us in transforming healthcare, Nao!
    """

    with open("job_description_1.txt", "w") as f:
        f.write(job_description_1)

    job_description_2 = """
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

    with open("job_description_2.txt", "w") as f:
        f.write(job_description_2)

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

    with open("resume.txt", "w") as f:
        f.write(resume)

    with open("resume.txt", "r") as f:
        resume = f.read()
    
    with open("job_description_1.txt", "r") as f:
        job_description = f.read()

    DEEPSEEK_API_KEY = "sk-********************"
    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
    MODEL_NAME = "deepseek-chat"
    
    model = AtsResumeOptimizer(
        model_name=MODEL_NAME,
        resume=resume,
        api_key=DEEPSEEK_API_KEY,
        api_base=DEEPSEEK_API_BASE,
        language="en"
    )

    result = model.generate_ats_optimized_resume_json(job_description)

    print(json.dumps(result, indent=2))
    
    # delete file
    os.remove("job_description_1.txt")
    os.remove("job_description_2.txt")
    os.remove("resume.txt")