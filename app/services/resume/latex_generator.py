import json
import os
import re
import html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class LaTeXGenerator:
    def __init__(self, template_dir=None):
        self.template_dir = template_dir
        self.json_data = None
        self.env = None
        self.setup_jinja_environment()

    def setup_jinja_environment(self):
        """Set up the Jinja2 environment with the template directory."""
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

    def generate_from_template(self, template_name):
        """Generate a LaTeX document from a template and JSON data."""
        if not self.json_data:
            raise ValueError("JSON data not loaded")

        self.preprocess_json_data()

        try:
            template = self.env.get_template(template_name)

            rendered_content = template.render(data=self.json_data)
            return rendered_content
        except Exception as e:
            print(f"Error generating from template: {e}")
            return False

    def create_simple_template(self, template_name="simple_resume_template.tex"):
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
    generator = LaTeXGenerator("../../../data/sample_latex_templates")

    print("Creating sample templates...")
    generator.create_simple_template()

    with open("../../../data/sample_responses/example.json", "r", encoding="utf-8") as file:
        json_data = file.read()
    print("Parsing JSON data...")
    generator.json_data = json.loads(json_data)
    result = generator.generate_from_template("resume_template.tex")
    print("Generated LaTeX content successfully.")
    print(result)

if __name__ == "__main__":
    main()