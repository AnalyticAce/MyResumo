from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
from .tools import extract_json

def generate_resume(template, resume_content, job_description, tone, language, API_KEY):
    client = OctoAI(api_key=API_KEY,)
    
    completion = client.text_gen.create_chat_completion(
        max_tokens=10000,
        messages=[
            ChatMessage(
                content=f"{template}",
                role="system"
            ),
            ChatMessage(
                content=f"{resume_content}\n{job_description}\n{tone}\n{language}",
                role="user"
            )
        ],
        model="mixtral-8x22b-instruct",
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9
    )

    return extract_json(completion.choices[0].message.content)

# template = create_prompt()
# resume = pdf_to_text("../../../../Téléchargements/DOSSEH_SHALOM_CV.pdf")
# job_description = """
# """

# API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiJkMmJjNGRlZC0zNmI2LTRiZmQtODBlZi1lNjM0MGE5NGUyZDgiLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiJkYmJmYzE3MS1kNmQ1LTQ4MGItOWIxNC1lNmU3MWRiYzg1MzciLCJ1c2VySWQiOiJmYTBlY2YwZS1mNjIyLTQ0ZTYtYTYzMi1jMTEzNDdiMGRiNTMiLCJyb2xlcyI6WyJGRVRDSC1ST0xFUy1CWS1BUEkiXSwicGVybWlzc2lvbnMiOlsiRkVUQ0gtUEVSTUlTU0lPTlMtQlktQVBJIl0sImF1ZCI6IjNkMjMzOTQ5LWEyZmItNGFiMC1iN2VjLTQ2ZjYyNTVjNTEwZSIsImlzcyI6Imh0dHBzOi8vaWRlbnRpdHkub2N0b21sLmFpIiwiaWF0IjoxNzE0MTE5OTU2fQ.QBQIZosU_6fnUPJKlHHGQiwRsmGEzhmGUmy5X55ttP_cOqMUU-NS_-cl16Lhv_TUL_WkjYpK_JnpSnk0bLCoWtJss5_wsE24BOvJKPWry8Jg70mN1NVNdBGjWPROAsR_RudMXbSYiFpWYxGyMYOPjhsTsKTbuiTW39hhiJLOmujhvcZI9bHc9HSKv2AYm010wfm0J2tler9xK-jAtTfjc9WpQJ5FRytwdFVcHTBFfcmuf0fhOCNXYtPVthxDL15DwWQGIEezaAjPZv4fAp9QAZc1MYxOVdk6IfMqcEpJ9bP8fggIk-TjXC7CtyVt5UqEm-IStuiHi1VByk0bpQBEkg"
# result = generate_resume(template, resume, job_description, "Professional", "English", API_KEY)
# print(result)
# create_pdf(result, "resume.pdf")