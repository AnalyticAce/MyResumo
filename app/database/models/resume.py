"""Resume data models module.

This module defines the Pydantic data models for resumes, including their structure,
validation rules, and relationships. These models define the core domain entities
for the resume optimization system and are used for data validation, serialization,
and API documentation.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr, Field, validator

from app.database.models.base import BaseSchema


class Experience(BaseSchema):
    """Model representing a work experience entry in a resume.

    Attributes:
    ----------
        job_title (str): The job title/position held
        company (str): The company or organization name
        location (Optional[str]): The location/city of the job
        start_date (str): When the job started (stored as string for flexibility)
        end_date (str): When the job ended (or "Present" for current positions)
        four_tasks (List[str]): List of four key responsibilities or achievements
    """

    job_title: str
    company: str
    location: Optional[str] = None
    start_date: str
    end_date: str
    four_tasks: List[str] = Field(..., min_items=4, max_items=4)


class Education(BaseSchema):
    """Model representing an education entry in a resume.

    Attributes:
    ----------
        institution (str): Name of the educational institution
        degree (str): The degree or qualification obtained
        description (Optional[str]): Additional details about the education
        start_date (str): When education began
        end_date (str): When education completed (or "Present")
    """

    institution: str
    degree: str
    description: Optional[str] = None
    start_date: str
    end_date: str


class Skills(BaseSchema):
    """Model representing skills in a resume.

    Attributes:
    ----------
        hard_skills (List[str]): List of technical/professional skills
        soft_skills (List[str]): List of interpersonal/soft skills
    """

    hard_skills: List[str]
    soft_skills: List[str]


class UserInformation(BaseSchema):
    """Model representing basic user information in a resume.

    Attributes:
    ----------
        name (str): The full name of the resume owner
        main_job_title (str): Primary professional title
        profile_description (str): Professional summary or objective
        email (EmailStr): Contact email address
        linkedin (Optional[str]): LinkedIn profile URL or username
        github (Optional[str]): GitHub profile URL or username
        experiences (List[Experience]): List of work experiences
        education (List[Education]): List of education entries
        skills (Skills): Technical and soft skills
        hobbies (Optional[List[str]]): List of hobbies/interests
    """

    name: str
    main_job_title: str
    profile_description: str
    email: EmailStr
    linkedin: Optional[str] = None
    github: Optional[str] = None
    experiences: List[Experience]
    education: List[Education]
    skills: Skills
    hobbies: Optional[List[str]] = None


class Project(BaseSchema):
    """Model representing a project in a resume.

    Attributes:
    ----------
        project_name (str): Name of the project
        two_goals_of_the_project (List[str]): Two main goals or objectives
        project_end_result (str): The outcome or result of the project
        tech_stack (Optional[List[str]]): Technologies used in the project
    """

    project_name: str
    two_goals_of_the_project: List[str] = Field(..., min_items=2, max_items=2)
    project_end_result: str
    tech_stack: Optional[List[str]] = None


class Certificate(BaseSchema):
    """Model representing a professional certificate in a resume.

    Attributes:
    ----------
        name (str): Name of the certification
        institution (str): Organization that issued the certificate
        description (Optional[str]): Details about the certification
        date (str): When the certification was obtained
    """

    name: str
    institution: str
    description: Optional[str] = None
    date: str


class ExtraCurricularActivity(BaseSchema):
    """Model representing an extracurricular activity in a resume.

    Attributes:
    ----------
        name (str): Name of the activity
        description (str): Details about the activity
        start_date (Optional[str]): When the activity began
        end_date (Optional[str]): When the activity ended (or "Present")
    """

    name: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ResumeData(BaseSchema):
    """Complete model for resume data that will be used for AI optimization and LaTeX generation.

    Attributes:
    ----------
        user_information (UserInformation): Basic personal and professional info
        projects (Optional[List[Project]]): List of projects
        certificate (Optional[List[Certificate]]): List of certificates
        extra_curricular_activities (Optional[List[ExtraCurricularActivity]]): List of activities
    """

    user_information: UserInformation
    projects: Optional[List[Project]] = None
    certificate: Optional[List[Certificate]] = None
    extra_curricular_activities: Optional[List[ExtraCurricularActivity]] = None


class Resume(BaseSchema):
    """Model representing a resume in the database.

    Attributes:
    ----------
        user_id (str): ID of the user who owns this resume
        title (str): Title/name of this resume version
        original_content (str): The original uploaded resume content as text
        job_description (str): The job description used for optimization
        optimized_data (Optional[ResumeData]): AI-optimized resume data
        ats_score (Optional[int]): ATS compatibility score (0-100)
        created_at (datetime): When the resume was created
        updated_at (datetime): When the resume was last updated
        latex_template (str): Name of LaTeX template to use for PDF generation
    """

    user_id: str
    title: str
    original_content: str
    job_description: str
    optimized_data: Optional[ResumeData] = None
    ats_score: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    latex_template: str = "resume_template.tex"

    @validator("ats_score")
    def validate_ats_score(self, v):
        """Validate that ATS score is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("ATS score must be between 0 and 100")
        return v
