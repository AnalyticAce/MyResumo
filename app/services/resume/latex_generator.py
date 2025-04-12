import json
import os
import re
import html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class FlexibleLaTeXGenerator:
    def __init__(self, template_dir=None):
        self.template_dir = template_dir or os.path.join(os.getcwd(), 'templates')
        self.json_data = None
        self.env = None
        self.setup_jinja_environment()

    def setup_jinja_environment(self):
        """Set up the Jinja2 environment with the template directory."""
        os.makedirs(self.template_dir, exist_ok=True)

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=False,
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<<',
            variable_end_string='>>',
            comment_start_string='<#',
            comment_end_string='#>'
        )

        self.env.filters['format_date'] = self.format_date
        self.env.filters['bold_numbers'] = self.bold_numbers
        self.env.filters['latex_escape'] = self.latex_escape

    def load_json(self, json_path):
        """Load and parse the JSON data from a file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return False

    def parse_json_from_string(self, json_string):
        """Parse JSON data from a string."""
        try:
            self.json_data = json.loads(json_string)
            return True
        except Exception as e:
            print(f"Error parsing JSON string: {e}")
            return False

    @staticmethod
    def format_date(date_str):
        """Format date strings from MM/YYYY to Month YYYY format."""
        if not date_str or date_str.lower() == 'present':
            return "Present"

        try:
            date_obj = datetime.strptime(date_str, "%m/%Y")
            return date_obj.strftime("%b. %Y")
        except:
            return date_str

    @staticmethod
    def bold_numbers(text):
        """Make numbers and percentages bold in LaTeX."""
        return re.sub(
            r'(\d+[\d,.]*(?:\+|\%?))', 
            r'\\textbf{\1}', 
            text
        )
    @staticmethod
    def latex_escape(text):
        """Escape LaTeX special characters and decode HTML entities."""
        if not isinstance(text, str):
            return text

        text = html.unescape(text)
        
        text = text.replace('\\', r'\textbackslash{}')

        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text

    def preprocess_json_data(self):
        """Recursively process all string values to decode HTML entities."""
        def process_value(value):
            if isinstance(value, str):
                return html.unescape(value)
            elif isinstance(value, dict):
                return {k: process_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [process_value(item) for item in value]
            else:
                return value

        if self.json_data:
            self.json_data = process_value(self.json_data)

    def generate_from_template(self, template_name, output_path):
        """Generate a LaTeX document from a template and JSON data."""
        if not self.json_data:
            raise ValueError("JSON data not loaded")

        self.preprocess_json_data()

        try:
            template = self.env.get_template(template_name)

            rendered_content = template.render(data=self.json_data)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(rendered_content)

            return True
        except Exception as e:
            print(f"Error generating from template: {e}")
            return False

    def create_sample_template(self, template_name="resume_template.tex"):
        """Create a sample LaTeX resume template with Jinja2 placeholders."""
        sample_template = r"""% Resume Template with Jinja2 Placeholders
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

%----------HEADING----------
\begin{center}
    \textbf{\Huge \scshape <<data.user_information.name|latex_escape>>} \\ \vspace{1pt}
    \href{mailto:<<data.user_information.email|latex_escape>>}{\underline{<<data.user_information.email|latex_escape>>}} $|$
    \href{https://github.com/<<data.user_information.github|latex_escape>>}{\underline{Github: <<data.user_information.github|latex_escape>>}} $|$
    \href{https://www.linkedin.com/in/<<data.user_information.linkedin|latex_escape|lower|replace(" ", "-")>>}{\underline{LinkedIn: <<data.user_information.linkedin|latex_escape>>}}
\end{center}

<% if data.user_information.get('profile_description') %>
%-----------PROFILE-----------
\section{Profile}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     <<data.user_information.profile_description|latex_escape>>
    }}
 \end{itemize}
<% endif %>

<% if data.user_information.get('experiences') %>
%-----------EXPERIENCE-----------
\section{Work Experience}
  \resumeSubHeadingListStart
    <% for exp in data.user_information.experiences %>
    \resumeSubheading
      {<<exp.job_title|latex_escape>>}{<<exp.start_date|format_date>> -- <<exp.end_date|format_date>>}
      {<<exp.company|latex_escape>>}{Cotonou, Benin}
      \resumeItemListStart
        <% for task in exp.four_tasks %>
        \resumeItem{<<task|latex_escape|bold_numbers>>}
        <% endfor %>
      \resumeItemListEnd
    <% endfor %>
  \resumeSubHeadingListEnd
<% endif %>

<% if data.get('projects') %>
%-----------PROJECTS-----------
\section{Projects}
    \resumeSubHeadingListStart
      <% for project in data.projects %>
      \resumeProjectHeading
          {\textbf{<<project.project_name|latex_escape>>} $|$ \emph{<% if project.tech_stack is defined %><<project.tech_stack|latex_escape>><% else %>Python<% endif %>}}{}
          \resumeItemListStart
            <% for goal in project.two_goals_of_the_project %>
            \resumeItem{<<goal|latex_escape|bold_numbers>>}
            <% endfor %>
            <% if project.project_end_result %>
            \resumeItem{<<project.project_end_result|latex_escape|bold_numbers>>}
            <% endif %>
          \resumeItemListEnd
      <% endfor %>
    \resumeSubHeadingListEnd
<% endif %>

<% if data.user_information.get('education') %>
%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    <% for edu in data.user_information.education %>
    \resumeSubheading
      {<<edu.institution|latex_escape>>}{<<edu.start_date|format_date>> -- <% if edu.end_date|lower == 'present' %>Present<% else %><<edu.end_date|format_date>><% endif %>}
      {<<edu.degree|latex_escape>>}{Cotonou, Benin}
      <% if edu.description %>
      \resumeItemListStart
        \resumeItem{<<edu.description|latex_escape>>}
      \resumeItemListEnd
      <% endif %>
    <% endfor %>
  \resumeSubHeadingListEnd
<% endif %>

<% if data.user_information.get('skills') %>
%-----------SKILLS-----------
\section{Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: English (Proficient), French (Native)} \\
     <% if data.user_information.skills.hard_skills %>
     \textbf{Programming}{: <<data.user_information.skills.hard_skills|join(', ')|latex_escape>>} \\
     <% endif %>
     <% if data.user_information.skills.soft_skills %>
     \textbf{Soft Skills}{: <<data.user_information.skills.soft_skills|join(', ')|latex_escape>>}
     <% endif %>
    }}
 \end{itemize}
<% endif %>

<% if data.get('extra_curricular_activities') %>
%-----------LEADERSHIP-----------
\section{Leadership \& Community Involvement}
  \resumeSubHeadingListStart
    <% for activity in data.extra_curricular_activities %>
    <% if activity.name and ',' in activity.name %>
    <% set parts = activity.name.split(',', 1) %>
    \resumeSubheading
      {<<parts[0]|latex_escape>>}{March 2024 -- Present}
      {<% if parts|length > 1 %><<parts[1]|latex_escape>><% else %><% endif %>}{}
    <% else %>
    \resumeSubheading
      {<<activity.name|latex_escape>>}{March 2024 -- Present}
      {}{}
    <% endif %>
      <% if activity.description %>
      \resumeItemListStart
        <% for desc in activity.description.split('.') %>
        <% if desc.strip() %>
        \resumeItem{<<desc.strip()|latex_escape>>.<% if not desc.strip().endswith('.') %><% endif %>}
        <% endif %>
        <% endfor %>
      \resumeItemListEnd
      <% endif %>
    <% endfor %>
  \resumeSubHeadingListEnd
<% endif %>

<% if data.get('certificate') %>
%-----------CERTIFICATIONS-----------
\section{Certifications}
  \resumeSubHeadingListStart
    <% for cert in data.certificate %>
    \resumeItem{<<cert.name|latex_escape>> (<<cert.institution|latex_escape>>, <% if '2025' in cert.date %>Expected<% else %>Completed<% endif %> <<cert.date|format_date>>)}
    <% endfor %>
  \resumeSubHeadingListEnd
<% endif %>

%-------------------------------------------
\end{document}
"""

        # Create the template file
        template_path = os.path.join(self.template_dir, template_name)
        try:
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(sample_template)
            return True
        except Exception as e:
            print(f"Error creating sample template: {e}")
            return False

    def create_simple_template(self, template_name="simple_resume.tex"):
        """Create a simpler LaTeX resume template with Jinja2 placeholders."""
        simple_template = r"""% Simple Resume Template with Jinja2 Placeholders
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{\vspace{-4pt}\scshape\raggedright\large}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\begin{document}

% Header
\begin{center}
    {\huge\textbf{<<data.user_information.name|latex_escape>>}} \\
    \vspace{2mm}
    <<data.user_information.email|latex_escape>> $|$
    Github: <<data.user_information.github|latex_escape>> $|$
    LinkedIn: <<data.user_information.linkedin|latex_escape>>
\end{center}

<% if data.user_information.get('profile_description') %>
% Profile
\section*{Profile}
<<data.user_information.profile_description|latex_escape>>
<% endif %>

<% if data.user_information.get('experiences') %>
% Experience
\section*{Work Experience}
<% for exp in data.user_information.experiences %>
\textbf{<<exp.job_title|latex_escape>>} \hfill <<exp.start_date|format_date>> -- <<exp.end_date|format_date>> \\
\textit{<<exp.company|latex_escape>>} \\
\begin{itemize}
    <% for task in exp.four_tasks %>
    \item <<task|latex_escape|bold_numbers>>
    <% endfor %>
\end{itemize}
<% endfor %>
<% endif %>

<% if data.get('projects') %>
% Projects
\section*{Projects}
<% for project in data.projects %>
\textbf{<<project.project_name|latex_escape>>} \\
\begin{itemize}
    <% for goal in project.two_goals_of_the_project %>
    \item <<goal|latex_escape|bold_numbers>>
    <% endfor %>
    <% if project.project_end_result %>
    \item <<project.project_end_result|latex_escape|bold_numbers>>
    <% endif %>
\end{itemize}
<% endfor %>
<% endif %>

<% if data.user_information.get('education') %>
% Education
\section*{Education}
<% for edu in data.user_information.education %>
\textbf{<<edu.institution|latex_escape>>} \hfill <<edu.start_date|format_date>> -- <% if edu.end_date|lower == 'present' %>Present<% else %><<edu.end_date|format_date>><% endif %> \\
\textit{<<edu.degree|latex_escape>>} \\
<% if edu.description %>
<<edu.description|latex_escape>>
<% endif %>
<% endfor %>
<% endif %>

<% if data.user_information.get('skills') %>
% Skills
\section*{Skills}
<% if data.user_information.skills.hard_skills %>
\textbf{Technical Skills:} <<data.user_information.skills.hard_skills|join(', ')|latex_escape>> \\
<% endif %>
<% if data.user_information.skills.soft_skills %>
\textbf{Soft Skills:} <<data.user_information.skills.soft_skills|join(', ')|latex_escape>>
<% endif %>
<% endif %>

<% if data.get('certificate') %>
% Certifications
\section*{Certifications}
\begin{itemize}
    <% for cert in data.certificate %>
    \item <<cert.name|latex_escape>> (<<cert.institution|latex_escape>>, <% if '2025' in cert.date %>Expected<% else %>Completed<% endif %> <<cert.date|format_date>>)
    <% endfor %>
\end{itemize}
<% endif %>

\end{document}
"""

        template_path = os.path.join(self.template_dir, template_name)
        try:
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(simple_template)
            return True
        except Exception as e:
            print(f"Error creating simple template: {e}")
            return False


def main():
    os.makedirs("output", exist_ok=True)

    generator = FlexibleLaTeXGenerator()

    print("Creating sample templates...")
    generator.create_sample_template()
    generator.create_simple_template()

    json_data = {
        "user_information": {
          "name": "Shalom DOSSEH",
          "main_job_title": "Junior Engineer - Generative AI",
          "profile_description": "Data Professional with a strong foundation in Python programming and a genuine interest in generative AI technologies. Experienced in developing AI-driven applications and collaborating with cross-functional teams to deliver innovative solutions.",
          "email": "dosseh.contact@gmail.com",
          "linkedin": "DOSSEH Shalom",
          "github": "AnalyticAce",
          "experiences": [
            {
              "job_title": "Data Science & Analytics - Internship",
              "company": "Gozem - Africa's Super App",
              "start_date": "07/2024",
              "end_date": "04/2025",
              "four_tasks": [
                "Partnered with Gozem Money leadership to understand data requirements for the pre-launch phase of a new fintech vertical, including data extraction and analysis across large-scale financial datasets for financial forecasting and transaction analytics.",
                "Utilized Python (Pandas, Scikit-learn), SQL, and Looker Studio to generate actionable insights and align business needs with technical solutions.",
                "Leveraged SQL and Astro Airflow to design and implement real-time transaction monitoring for 8,000,000+ monthly transactions to detect and prevent fraud, money laundering, and terrorist financing activities.",
                "Collaborated with the data engineering team to gather, structure, and integrate data from multiple sources into a centralized analytics repository, enabling a unified view of key product insights."
              ]
            },
            {
              "job_title": "Data Analyst (Ride-hailing) - Internship",
              "company": "Gozem - Africa's Super App",
              "start_date": "09/2023",
              "end_date": "01/2024",
              "four_tasks": [
                "Executed 65%+ of the squad\u2019s quarterly tasks, completing 92% of high-priority deliverables efficiently.",
                "Investigated transaction data, detecting and dismantling fraudulent schemes, leading to millions in recovered revenue.",
                "Performed data integrity checks, identifying and resolving anomalies to maintain accurate reporting.",
                "Automated routine reporting and analytics tasks, improving efficiency and precision in data insights."
              ]
            }
          ],
          "education": [
            {
              "institution": "EPITECH - European Institute of Technology",
              "degree": "Bachelor's degree, Innovation and Information Technology",
              "description": "Cultivated robust skills across various domains of computer science, completing nearly 130 projects and mini-projects. Relevant Courses: Computer Numerical Analysis, Artificial Intelligence, Advanced DevOps, Advanced C++.",
              "start_date": "10/2022",
              "end_date": "Present"
            }
          ],
          "skills": {
            "hard_skills": [
              "Python",
              "SQL",
              "Pandas",
              "NumPy",
              "Scikit-Learn",
              "Looker Studio",
              "Excel",
              "GCP",
              "Azure",
              "MongoDB",
              "Docker",
              "Jenkins",
              "Ansible",
              "Apache Airflow",
              "Git Source Control",
              "Github action",
              "Linux"
            ],
            "soft_skills": [
              "Adaptability",
              "Coachable",
              "Problem-Solving",
              "Decision-Making",
              "Effective communication",
              "Active listening"
            ]
          },
          "hobbies": []
        },
        "projects": [
          {
            "project_name": "MyResumo",
            "two_goals_of_the_project": [
              "Built an AI-backed resume generator designed to tailor your resume and skills based on a given job description.",
              "Leveraged the latest advancements in AI to provide an ATS-friendly resume."
            ],
            "project_end_result": "Innovative tool that helps users create optimized resumes for job applications."
          },
          {
            "project_name": "MyTorch",
            "two_goals_of_the_project": [
              "Developed a neural network-based chessboard analyzer from scratch without deep learning libraries.",
              "Trained models on FEN notation to classify six game states."
            ],
            "project_end_result": "Achieved 90% accuracy in binary classification and 60-70% in multi-class tasks."
          },
          {
            "project_name": "Gomoku AI",
            "two_goals_of_the_project": [
              "Developed a high-performance Gomoku AI bot using Min-Max with Alpha-Beta pruning and heuristic scoring.",
              "Designed to compete with GomokuCup AI bots, ensuring efficiency under computational constraints."
            ],
            "project_end_result": "Optimized decision-making for the Gomoku game."
          },
          {
            "project_name": "PyDepViz",
            "two_goals_of_the_project": [
              "A Python-native dependency graph visualizer designed to simplify dependency management in Python projects.",
              "Helps developers visualize and resolve dependency deadlocks efficiently."
            ],
            "project_end_result": "Tool that aids in managing Python project dependencies."
          }
        ],
        "certificate": [
          {
            "name": "Career Essentials in GitHub Professional Certificate",
            "institution": "Github",
            "description": "Professional certification in GitHub essentials.",
            "date": "02/2025"
          },
          {
            "name": "Data Scientist Certification",
            "institution": "Datacamp",
            "description": "Certification in data science.",
            "date": "07/2025"
          },
          {
            "name": "AI Engineer for Data Scientists Associate Certification",
            "institution": "Datacamp",
            "description": "Certification in AI engineering for data scientists.",
            "date": "09/2025"
          },
          {
            "name": "Certified Associate in Project Management (CAPM)",
            "institution": "PMI",
            "description": "Certification in project management.",
            "date": "09/2025"
          }
        ],
        "extra_curricular_activities": [
          {
            "name": "Technical Workshop Facilitator, Innovation Hub at Epitech",
            "description": "Hosted Python, DevOps, and AI workshops, mentoring students in technical fields. Partnered with industry professionals to deliver hands-on training sessions."
          },
          {
            "name": "Lead Project Manager, Epitech\u2019s Student Bureau",
            "description": "Led a team of 3 project managers, overseeing 30+ initiatives within time and budget constraints. Developed planning & tracking tools to optimize project execution."
          },
          {
            "name": "Event Manager & Core Member, Google Developer Students Club",
            "description": "Organized tech events, hackathons, and networking sessions to engage student developers. Drove community initiatives to enhance learning in AI & Google Cloud Technologies."
          },
          {
            "name": "Social Data Analyst, AFRIK EDUTECH - EPITECH X IMPACT",
            "description": "Conducted impact analysis & forecasting, guiding leadership decisions on program effectiveness. Collected & cleaned large-scale datasets for resource optimization."
          }
        ]
    }
    generator.json_data = json_data
    generator.generate_from_template("resume_template.tex", "output/my_resume.tex")
    generator.generate_from_template("simple_resume.tex", "output/my_simple_resume.tex")

if __name__ == "__main__":
  main()