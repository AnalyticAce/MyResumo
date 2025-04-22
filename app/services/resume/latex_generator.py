import json
import os
import re
import html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class LaTeXGenerator:
    """
    A class to generate LaTeX files from given templates and data.
    The LaTeXGenerator handles the creation of LaTeX documents using Jinja2 templates
    and input data in JSON format. It provides methods for loading and parsing JSON data,
    processing the data to be compatible with LaTeX, and generating output documents
    by rendering templates with the processed data.
    Attributes:
        template_dir (str): Directory path containing LaTeX templates.
        json_data (dict): Parsed JSON data to be used in template rendering.
        env (jinja2.Environment): Configured Jinja2 environment for template processing.
    Methods:
        setup_jinja_environment: Configures the Jinja2 environment with LaTeX-friendly delimiters.
        load_json: Loads JSON data from a file.
        parse_json_from_string: Parses JSON data from a string.
        format_date: Converts date strings from MM/YYYY to Month YYYY format.
        bold_numbers: Makes numbers and percentages bold in LaTeX.
        latex_escape: Escapes LaTeX special characters and decodes HTML entities.
        preprocess_json_data: Recursively processes all string values to decode HTML entities.
        generate_from_template: Generates a LaTeX document from a template and the loaded JSON data.
        create_simple_template: Creates a simple LaTeX resume template with Jinja2 placeholders.
    """
    def __init__(self, template_dir=None):
        """
        Initialize the LaTeX generator.

        This constructor sets up the LaTeX generator with a template directory and initializes
        the Jinja2 environment for template rendering.

        Parameters
        ----------
        template_dir : str, optional
            The directory path where LaTeX templates are stored. If None, a default directory
            will be used.

        Attributes
        ----------
        template_dir : str
            Directory containing LaTeX templates
        json_data : dict
            Resume data in JSON format, initially None until loaded
        env : jinja2.Environment
            The Jinja2 environment for template rendering
        """
        self.template_dir = template_dir
        self.json_data = None
        self.env = None
        self.setup_jinja_environment()

    def setup_jinja_environment(self) -> None:
        """
        Set up the Jinja2 environment with the template directory and custom delimiters.

        This method initializes the Jinja2 Environment object with:
        - A FileSystemLoader using the template_dir attribute to locate templates
        - Custom delimiters to avoid conflicts with LaTeX syntax:
            - Block delimiters: <% %>
            - Variable delimiters: << >>
            - Comment delimiters: <# #>
        - Autoescaping disabled (False) since we're generating LaTeX content

        Additionally, registers custom filters for LaTeX content processing:
        - format_date: Formats date strings according to specified format
        - bold_numbers: Adds LaTeX bold formatting to numeric values
        - latex_escape: Escapes special LaTeX characters to prevent rendering issues

        Returns:
                None
        """
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
        """
        Load and parse the JSON data from a file.
        
        Args:
            json_path (str): Path to the JSON file to be loaded.
            
        Returns:
            bool: True if JSON was successfully loaded, False otherwise.
            
        Side effects:
            Sets self.json_data with the parsed JSON content when successful.
            Prints error message to console when loading fails.
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return False

    def parse_json_from_string(self, json_string) -> bool:
        """
        Parse a JSON string into a Python object.
        
        Args:
            json_string (str): A string containing valid JSON data.
            
        Returns:
            bool: True if parsing was successful, False otherwise.
            
        Side effects:
            If successful, sets self.json_data to the parsed JSON object.
            If unsuccessful, prints an error message.
        """
        try:
            self.json_data = json.loads(json_string)
            return True
        except Exception as e:
            print(f"Error parsing JSON string: {e}")
            return False

    @staticmethod
    def format_date(date_str) -> str:
        """
        Convert a date string to a formatted date.

        Takes a date string in format 'mm/yyyy' and converts it to 'Mon. YYYY' format.

        Args:
            date_str (str): The date string to format, typically in 'mm/yyyy' format.
                        Can also be 'present' (case insensitive) or empty.

        Returns:
            str: The formatted date string. Returns 'Present' if input is empty or 
                'present' (case insensitive). Returns the original string if parsing fails.
        """
        if not date_str or date_str.lower() == 'present':
            return "Present"

        try:
            date_obj = datetime.strptime(date_str, "%m/%Y")
            return date_obj.strftime("%b. %Y")
        except Exception as e:
            print(f"Error formatting date: {e}")
            return date_str

    @staticmethod
    def bold_numbers(text) -> str:
        """
        Makes all numbers in text bold by wrapping them with LaTeX \textbf command.
        
        Args:
            text (str): The input text containing numbers to be made bold.
        
        Returns:
            str: The text with all numbers wrapped in \textbf{} LaTeX command.
            
        Example:
            >>> bold_numbers("I have 42 apples and a 99.5% success rate")
            "I have \\textbf{42} apples and a \\textbf{99.5\\%} success rate"
        
        Notes:
            - Matches integers, decimals, numbers with commas, and numbers with % or + suffix
            - Doesn't affect numbers that are already part of a LaTeX command
        """
        return re.sub(
            r'(\d+[\d,.]*(?:\+|\%?))', 
            r'\\textbf{\1}', 
            text
        )

    @staticmethod
    def latex_escape(text) -> str:
        """
        Escape special LaTeX characters in a string to make it safe for LaTeX documents.
        This function replaces special LaTeX characters with their escaped equivalents.
        It first unescapes any HTML entities using html.unescape, then performs LaTeX-specific escaping.
        Args:
            text: The text to escape. If not a string, it will be returned unchanged.
        Returns:
            str: The input text with LaTeX special characters properly escaped.
        Example:
            >>> latex_escape("100% of $10 is $10")
            "100\\% of \\$10 is \\$10"
        """
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

    def preprocess_json_data(self) -> None:
        """
        Preprocesses the JSON data stored in the instance by recursively unescaping HTML entities.
        
        This method traverses through the entire JSON data structure (dictionaries, lists, and strings)
        and converts any HTML escaped characters (like &amp;, &lt;, etc.) back to their original form.
        The processed data replaces the original json_data attribute.
        
        Returns:
            None: The method modifies the self.json_data attribute in place.
        """
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

    def generate_from_template(self, template_name) -> str | bool:
        """
        Generates LaTeX content from a template using the loaded JSON data.

        This method renders the specified Jinja2 template with the preprocessed JSON data,
        producing LaTeX code that can be compiled into a PDF document.

        Args:
            template_name (str): The filename of the template to use (must be available
                                in the Jinja2 environment).

        Returns:
            str or bool: The rendered LaTeX content as a string if successful, False if an error occurs.

        Raises:
            ValueError: If JSON data has not been loaded before calling this method.

        Example:
            latex_content = generator.generate_from_template("modern_template.tex")
        """
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