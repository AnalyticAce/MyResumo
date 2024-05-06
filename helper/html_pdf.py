from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import json
from .tools import read_file

def parse_user_information(data):
    user_information = data["user_information"]
    if user_information["name"] == '':
        return ""
    if user_information["main_job_title"] == '':
        return ""
    if user_information["profile_description"] == '':
        return ""
    if user_information["email"] == '':
        return ""
    if user_information["linkedin"] == '':
        return ""
    if user_information["github"] == []:
        return ""
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

def parse_experiences(data):
    experiences = data["user_information"]["experiences"]
    if experiences == []:
        return ""
    experiences_html = "<section><h2>EXPERIENCE</h2>"
    for experience in experiences:
        experience_html = f"""
        <h3>{experience['job_title']} at {experience['company']} - {experience['start_date']} to {experience['end_date']}</h3>
        <ul>
        """
        for task in experience["four_tasks"]:
            experience_html += f"<li>{task}</li>"
        experience_html += "</ul>"
        experiences_html += experience_html
    experiences_html += "</section>"
    return experiences_html

def parse_education(data):
    education = data["user_information"]["education"]
    if education == []:
        return ""
    education_html = "<section><h2>EDUCATION</h2>"
    for institution in education:
        description = institution.get('description', '')
        institution_html = f"""
        <h3>{institution['degree']} at {institution['institution']} - {institution['start_date']} to {institution['end_date']}</h3>
        <p>{description}</p>
        """
        education_html += institution_html
    education_html += "</section>"
    return education_html


def parse_skills(data):
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

def parse_projects(data):
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

def parse_hobbies(data):
    if data["user_information"]["hobbies"] == []:
        return ""
    hobbies = data["user_information"]["hobbies"]
    hobbies_html = "<section><h2>HOBBIES</h2><ul>"
    for hobby in hobbies:
        hobbies_html += f"<li>{hobby}</li>"
    hobbies_html += "</ul></section>"
    return hobbies_html

def parse_certificate(data):
    certifications = data["certificate"]
    if certifications == []:
        return ""
    certifications_html = "<section><h2>CERTIFICATIONS</h2>"
    for certification in certifications:
        certification_html = f"""
        <h3>{certification['name']} at {certification['institution']} - {certification['date']}</h3>
        <p>{certification['description']}</p>
        """
        certifications_html += certification_html
    certifications_html += "</section>"
    return certifications_html

def parse_extra_curricular_activities(data):
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

def create_resume(data):
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
    
def perfect_css_style(file="style.css"):
    style = read_file(file)
    css = f"""
    {style}
    """
    return css

def create_pdf(data, filename, style="style.css"):
    try:
        font_config = FontConfiguration()
        html = HTML(string=f"""{create_resume(data)}""")
        css = CSS(string=f'''{perfect_css_style(style)}''', font_config=font_config)
        html.write_pdf(filename, stylesheets=[css], font_config=font_config)
        return True
    except Exception as e:
        print(f"Failed to create PDF: {e}")
        return False