from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from .tools import ToolKit
import json

def parse_user_information(data: dict) -> str:
    user_information = data["user_information"]
    user_information_html = f"""
    <header>
        <h1 style="text-align: center;">{user_information['name']}</h1>
        <p style="text-align: center;">{user_information['main_job_title']}</p>
        <p style="text-align: center;">{user_information['email']} - 
            {user_information['linkedin']} - {user_information["github"]}</p>
        <h2>SUMMARY</h2>
        <p>{user_information['profile_description']}</p>
    </header>
    """
    return user_information_html

def parse_experiences(data: dict) -> str:
    experiences = data["user_information"]["experiences"]
    if experiences == []:
        return ""
    experiences_html = "<section><h2>EXPERIENCE</h2>"
    for experience in experiences:
        experience_html = f"""
        <div style="display: flex; justify-content: space-between; margin-top: 0;">
            <p><strong>{experience['job_title']} - <i>{experience['company']}</i></strong></p>
            <p>{experience['start_date']} to {experience['end_date']}</p>
        </div>
        """
        for task in experience["four_tasks"]:
            experience_html += f"<li>{task}</li>"
        experience_html += "</ul>"
        experiences_html += experience_html
    experiences_html += "</section>"
    return experiences_html

def parse_education(data: dict) -> str:
    education = data["user_information"]["education"]
    if education == []:
        return ""
    education_html = "<section><h2>EDUCATION</h2>"
    for institution in education:
        institution_html = f"""
        <div style="display: flex; justify-content: space-between; margin-top: 0;">
            <p><strong>{institution['degree']} - <i>{institution['institution']}</i></strong></p>
            <p>{institution['start_date']} to {institution['end_date']}</p>
        </div>
        <p style="margin-top: 0;">{institution['description']}</p>
        """
        education_html += institution_html
    education_html += "</section>"
    return education_html

def parse_skills(data: dict) -> str:
    skills = data["user_information"]["skills"]
    if skills["hard_skills"] == [] and skills["soft_skills"] == []:
        return ""
    skills_html = "<section><h2>SKILLS</h2>"
    skills_html += "<h3>Hard Skills</h3><ul>"
    hard_skills = ", ".join(skills["hard_skills"])
    skills_html += f"<li>{hard_skills}</li>"
    skills_html += "</ul>"
    skills_html += "<h3>Soft Skills</h3><ul>"
    soft_skills = ", ".join(skills["soft_skills"])
    skills_html += f"<li>{soft_skills}</li>"
    skills_html += "</ul></section>"
    return skills_html

def parse_projects(data: dict) -> str:
    projects = data["projects"]
    if projects == []:
        return ""
    projects_html = "<section><h2>PROJECTS</h2>"
    for project in projects:
        project_html = f"""
        <h3>{project['project_name']}</h3>
        <ul>
            <li>{project['two_goals_of_the_project'][0]}</li>
            <li>{project['two_goals_of_the_project'][1]}</li>
            <li>{project['project_end_result']}</li>
        </ul>
        """
        projects_html += project_html
    projects_html += "</section>"
    return projects_html

def parse_hobbies(data: dict) -> str:
    if data["user_information"]["hobbies"] == []:
        return ""
    hobbies = data["user_information"]["hobbies"]
    hobbies_html = "<section><h2>HOBBIES</h2><ul>"
    for hobby in hobbies:
        hobbies_html += f"<li>{hobby}</li>"
    hobbies_html += "</ul></section>"
    return hobbies_html

def parse_certificate(data: dict) -> str:
    certifications = data["certificate"]
    if certifications == []:
        return ""
    certifications_html = "<section><h2>CERTIFICATES</h2>"
    for certification in certifications:
        certification_html = f"""
        <h3 style="margin-top: 0; margin-bottom: 0;"><i>{certification['institution']}</i></h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0;">
            <h3>{certification['name']}</h3>
            <p>{certification['date']}</p>
        </div>
        <p style="margin-top: 0;">{certification['description']}</p>
        """
        certifications_html += certification_html
    certifications_html += "</section>"
    return certifications_html

def parse_extra_curricular_activities(data: dict) -> str:
    extra_curricular_activities = data["extra_curricular_activities"]
    if extra_curricular_activities == []:
        return ""
    extra_curricular_activities_html = "<section><h2>EXTRA-CURRICULAR ACTIVITIES</h2>"
    for activity in extra_curricular_activities:
        activity_html = f"""
        <h3>{activity['name']}</h3>
        <p>{activity['description']}</p>
        """
        extra_curricular_activities_html += activity_html
    extra_curricular_activities_html += "</section>"
    return extra_curricular_activities_html

def create_resume(data : str) -> str:
    data = json.loads(data)
    user_information_html = parse_user_information(data)
    experiences_html = parse_experiences(data)
    education_html = parse_education(data)
    skills_html = parse_skills(data)
    projects_html = parse_projects(data)
    hobbies_html = parse_hobbies(data)
    certificates_html = parse_certificate(data)
    extra_curricular_activities_html = parse_extra_curricular_activities(data)
    resume_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="index.css">
    </head>
    <body>
        {user_information_html}
        {experiences_html}
        {education_html}
        {certificates_html}
        {projects_html}
        {extra_curricular_activities_html}
        {skills_html}
        {hobbies_html}
    </body>
    </html>
    """
    return resume_html

def perfect_css_style(color_code : str) -> str:
    css = f"""
    body {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 14px;
        line-height: 1.5;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}

    header, section {{
        padding: 10px 20px;
    }}

    header h1 {{
        font-size: 36px;
        color: {color_code};
    }}

    header p, header a, section a {{
        font-size: 14px;
        color: #333333;
        text-decoration: none;
    }}

    h2 {{
        font-size: 9px;
        color: #333333;
        border-bottom: 1px solid #dddddd;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 10px;
    }}

    h3 {{
        font-size: 12px;
        color: #333333;
    }}

    ul {{
        padding: 0;
    }}

    ul li {{
        list-style: inside;
        margin-bottom: 2px;
    }}

    a:hover {{
        text-decoration: underline;
    }}

    @media print {{
        body {{
            background-color: #ffffff;
        }}

        header, section {{
            padding: 0;
            border: none;
        }}

        h2 {{
            font-size: 20px;
            color: {color_code};
            border-bottom: 2px solid {color_code};
        }}
    }}
    """
    return css

def create_pdf(data: str, filename: str, color_code="#000000") -> bool:
    try:
        font_config = FontConfiguration()
        html = HTML(string=f"""{create_resume(data)}""")
        css = CSS(string=f'''{perfect_css_style(color_code)}''', font_config=font_config)
        html.write_pdf(filename, stylesheets=[css], font_config=font_config)
        return True
    except Exception as e:
        print(f"Failed to create PDF: {e}")
        return False