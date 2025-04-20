# Project Requirements Document
**Name:**  
**MyResumo**

**Primary Purpose:**  
MyResumo is an AI-powered resume generator that intelligently tailors a user’s resume to align with a specific job description. It ensures resumes are optimized to pass ATS (Applicant Tracking Systems) while offering personalized suggestions based on modern hiring standards.

---

### 👥 **Target Users and Stakeholders**

**Key Users:**
- Job seekers wanting to stand out in competitive job markets.
- Users who struggle with formatting, keyword optimization, or tailoring resumes manually.
- Those aiming to pass ATS screenings effectively.

**Pain Points Addressed:**
- Generic or poorly tailored resumes.
- Resumes that fail to pass ATS filters.
- Lack of resume feedback and scoring tools.
- Time-consuming manual editing and formatting.

---

### 🚀 **Core Features**

1. **Resume Upload:**
   - Upload resume in PDF format.

2. **AI Resume Scoring:**
   - Analyze the resume against a job description.
   - Assign a score based on ATS compatibility and content relevance.

3. **AI Suggestions:**
   - Provide targeted improvement suggestions (content, keywords, formatting).
   - User can select preferred suggestions.

4. **Resume Regeneration:**
   - Apply chosen changes to generate a new, ATS-friendly resume.
   - Generate in PDF format with LaTeX templating.

5. **Download & Use:**
   - Users can download the new version and begin applying to jobs instantly.

6. **LLM Integration:**
   - Built-in support for Large Language Models with API key management.

7. **Templating & Frontend:**
   - HTML, CSS, Jinja2 templates for rendering pages.
   - Clean, modern UI/UX with the possibility to scale to React.js if needed.

8. **Contribution Page:**
   - Community contribution guidelines and developer onboarding.

9. **API Access:**
   - Allow for integration into job platforms or external tools.

---

### 📋 **Non-Functional Requirements**

- **AI Reliability:**  
  Minimal or no hallucinations in AI-generated text.
  
- **Scalability & Modularity:**  
  Components must be modular and easy to scale individually (e.g., LLM services, PDF generation).

- **Security:**  
  Secure handling of uploaded documents and user data.

- **Performance:**  
  Lightweight footprint—able to run efficiently with minimal resources.

- **Maintainability:**  
  Reusable components and modules for faster development and easier updates.

---

### 🛠 **Tech Stack & Constraints**

**Backend:**  
- FastAPI (core backend framework)
- Modular architecture for services (e.g., scoring, suggestions, PDF generator)

**Frontend:**  
- HTML, CSS, Jinja2 (initially)
- Optional upgrade path to ReactJS if necessary for advanced UX

**Other Technologies:**
- LaTeX for high-quality resume PDFs
- OpenAI models (configurable via API key setting)
- Docker for deployment
- GitHub (with contribution guidelines)

**Constraints:**  
- Must perform well with minimal server resources.  
- No vendor lock-in or reliance on high-cost services.
