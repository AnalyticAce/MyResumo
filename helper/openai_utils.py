import json
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

def generate_resume_prompt(resume_content, job_description, tone, OPENAI_API_KEY):
    template = f"""
    You are an advanced and sophisticated AI model trained to optimize resumes based on a specific job description. 
    Your task is to enhance the user's existing resume by incorporating relevant keywords from the job description, valuing their past jobs or projects, and ensuring it aligns with the job requirements. 
    However, it's crucial not to over-qualify the user.
    The user's existing resume is as follows:
    {resume_content}

    The job description the user is applying to the job description as follows:
    {job_description}

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
    
    NB: You are to only reply the output (structured result) nothing else, Not even an inductory sentence to the output.    """
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY),
            prompt=chat_prompt,
        )
        
        # Run the LangChain model with resume_content as the input data
        generated_resume = chain.run(resume_content)

        # Convert the generated resume to a Python dictionary
        generated_resume_dict = json.loads(generated_resume)

        # Save the dictionary as a JSON file
        with open('generated_resume.json', 'w') as json_file:
            json.dump(generated_resume_dict, json_file, indent=4)

        return 'generated_resume.json'
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()