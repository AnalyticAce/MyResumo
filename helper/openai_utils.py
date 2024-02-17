# import json
# import streamlit as st
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain.chains import LLMChain

import openai
import json

def generate_resume_prompt(resume_content, job_description, tone, OPENAI_API_KEY):
    openai.api_key = OPENAI_API_KEY
    template = f"""
    You are an advanced and sophisticated Interviewer and Recruiter powered with an AI model trained to optimize resumes based on a specific job description. 
    Your task is to enhance the user's existing resume by incorporating relevant keywords from the job description, valuing their past jobs or projects, and ensuring it aligns with the job requirements. 
    However, it's crucial not to over-qualify the user.
    The user's existing resume is as follows:
    {resume_content}

    The job description the user is applying to the job description as follows:
    {job_description}

    Below are some tips to follow:
    Tip: Match the skills in your resume to the exact spelling in the job description. Prioritize skills that appear most frequently in the job description.
    Tip: Prioritize hard skills in your resume to get interviews, and then showcase your soft skills in the interview to get jobs.
    Tip: Other keywords are words included in the job description more than 3 times and not hard skills or soft skills. These words are typically buzzwords, industry lingo, or company specific jargon that may be unique to the specific company and help your resume get noticed. 
    Other keywords have a low impact on your match score. Spend less time including these in your resume on a case-by-case basis.
    Tip:  Consider adding at least 5 specific achievements or impact you had in your job (e.g. time saved, increase in sales, etc).
    Tip: Avoid negative phrase or cliche in the resume.
    Tip: Position yourself as an expert in your field. This can help to set you apart from other candidates who may not be as confident in their abilities.
    Tip: Use attention-grabbing action verbs. The example above uses the verb “leading,” which quickly tells employers what the applicant has accomplished.
    Tip: Be specific. Generic phrases such as “hard worker” or “team player” are nice, but they don’t really tell employers anything. If you can, include a specific accomplishment or skill that makes you stand out from the rest.
    Tip: Keep it brief – no more than a few sentences or bullet points.
    Tip: Look for patterns in your work history – anything that you can point to and say “this is what I do, and I’m good at it.”
    Tip: Focus only on your most relevant skills and experience.
    Tip: Use numbers and specifics to show that you are a results-oriented individual who is able to produce tangible outcomes.
    Tip: Incorporate keywords from the job description whenever possible.
    Tip: Tailor your summary statement to each job you apply for.
    Tip: Identify important keywords and skills. 
    Tip: Highlight achievements as well as responsibilities Instead of saying, “Managed a team of 12 people.” You could say, “Managed a team of 12 people, consistently meeting or exceeding quarterly targets.”
    Tip: Use action verbs, Use active voice, not passive eg: Active voice, “The chef prepared the meal.” Passive voice, “The meal was prepared by the chef.”
    Tip: Use numbers eg, Instead of saying, “Created marketing campaigns.” You could say, “Created 10 successful marketing campaigns that generated a 20% increase in leads.”
    Here are some more examples of using numbers (with action verbs underlined)
    Saved $7 million while introducing nationwide transport service for medical patients.
    Successfully increased sales by 20% within the first quarter of implementing a new marketing strategy.
    Streamlined project management process, reducing overall project completion time by 15% and improving team efficiency.
    
    Your Role as a Job Scanner
    Your task is to generate a revised resume that is tailored to the job description. 
    The output should be a well-structured JSON object containing the following sections: user name, profile description, email, LinkedIn, experiences (with details about the tasks completed and the period), education (in a structured way with the name of the college or university, diploma, and year), hard and soft skills, and hobbies.
    
    The structure of the JSON object should be as follows:

    {{
    "user_information": {{
        "name": "",
        "main_job_title": "",
        "profile_description": "",
        "email": "",
        "linkedin": "",
        "experiences": [
        {{
            "job_title": "",
            "company": "",
            "start_date": "",
            "end_date": "",
            "tasks": []
        }},
        ...
        ],
        "education": [
        {{
            "institution": "",
            "degree": "",
            "start_date": "",
            "end_date": ""
        }},
        ...
        ],
        "skills": {{
            "hard_skills": [],
            "soft_skills": []
        }},
        "hobbies": []
    }},
    "projects": [{{
        "project_name": "",
        "two_goals_of_the_project": [],
        "project_end_result": ""
    }}
    ...
    ],
    }}
    
    Generate a tailored resume that emphasizes relevant experiences, skills, and qualifications for the mentioned job. Ensure the output is in a well-structured JSON format.
    
    Please ensure that the tone of the resume matches the provided tone parameter: {tone}.
    
    NB: You are to only reply the output (structured result) nothing else, Not even an inductory sentence to the output."""

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=template,
        temperature=0.7
        ,max_tokens=1000
    )

    response_text = response.choices[0].text.strip()
    #print("Response text:", response_text)
    try:
        result_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        result_json = None

    return result_json