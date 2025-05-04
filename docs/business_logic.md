# Core Business Logic

This document explains the core business logic implemented in the MyResumo project. It provides insights into the key functionalities and their underlying principles.

## Resume Optimization
The primary feature of MyResumo is to optimize resumes for better alignment with job descriptions. This involves:

1. **Keyword Matching**:
   - Extracts keywords from job descriptions using natural language processing (NLP).
   - Matches these keywords with the content of the resume to identify gaps.

2. **ATS Scoring**:
   - Simulates Applicant Tracking System (ATS) scoring by analyzing formatting, keyword density, and section organization.
   - Provides actionable feedback to improve the resume's ATS compatibility.

3. **AI-Powered Suggestions**:
   - Leverages AI models to suggest improvements in phrasing, structure, and content.
   - Ensures the resume highlights relevant skills and experiences.

## PDF and LaTeX Resume Generation
- Converts optimized resumes into professional PDF formats using LaTeX templates.
- Supports multiple templates to cater to different industries and preferences.

## Token Usage Tracking
- Monitors the usage of AI tokens to ensure fair and efficient resource allocation.
- Implements limits and notifications to prevent overuse.

## Job Description Analysis
- Analyzes job descriptions to extract key requirements and skills.
- Provides insights into the most critical aspects of the job for better resume alignment.

## Error Handling and Edge Cases
- Handles scenarios like empty inputs, invalid file formats, and unsupported languages gracefully.
- Ensures robust error messages and fallback mechanisms.

For detailed implementation, refer to the respective modules in the `app/` directory.