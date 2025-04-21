# MyResumo <img src="https://img.shields.io/badge/version-2.0.0-blue" alt="Version 2.0.0"/>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status: Beta](https://img.shields.io/badge/Status-Beta-orange)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4%2B-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-8A2BE2?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTIgMmEyIDIgMCAwIDAgLTIgMnY3YTIgMiAwIDAgMCA0IDB2LTdhMiAyIDAgMCAwIC0yIC0yeiI+PC9wYXRoPjxwYXRoIGQ9Ik0yIDEyYTIgMiAwIDAgMCAtMiAydjdhMiAyIDAgMCAwIDQgMHYtN2EyIDIgMCAwIDAgLTIgLTJ6Ij48L3BhdGg+PHBhdGggZD0iTTIyIDEyYTIgMiAwIDAgMCAtMiAydjdhMiAyIDAgMCAwIDQgMHYtN2EyIDIgMCAwIDAgLTIgLTJ6Ij48L3BhdGg+PHBhdGggZD0iTTEyIDEyYTIgMiAwIDAgMCAtMiAydjdhMiAyIDAgMCAwIDQgMHYtN2EyIDIgMCAwIDAgLTIgLTJ6Ij48L3BhdGg+PHBhdGggZD0iTTYgNmEyIDIgMCAwIDAgLTIgMnYyYTIgMiAwIDAgMCA0IDB2LTJhMiAyIDAgMCAwIC0yIC0yeiI+PC9wYXRoPjxwYXRoIGQ9Ik0xOCA2YTIgMiAwIDAgMCAtMiAydjJhMiAyIDAgMCAwIDQgMHYtMmEyIDIgMCAwIDAgLTIgLTJ6Ij48L3BhdGg+PC9zdmc+)](https://github.com/AnalyticAce/MyResumo)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

</div>

## 📋 Overview

**MyResumo** is an AI-powered resume customization platform that tailors your professional profile to match specific job descriptions. By leveraging advanced natural language processing, it analyzes job requirements and adapts your resume to highlight relevant skills and experiences, significantly improving your chances of passing through Applicant Tracking Systems (ATS) and catching recruiters' attention.

<div align="center">
  <img src="https://github.com/AnalyticAce/MyResumo/blob/develop/.github/assets/demo-screenshot.png" alt="MyResumo Screenshot" width="600"/>
</div>

## ✨ Key Features

- **🤖 AI-Powered Resume Customization**: Automatically tailors your resume content to match job requirements
- **🔍 ATS Optimization**: Enhances keyword matching for better visibility in applicant tracking systems
- **📊 Skills Gap Analysis**: Identifies missing skills based on job descriptions
- **📝 Resume Generation**: Creates formatted, professional resumes in multiple formats
- **💬 Interactive Chat Interface**: Get personalized resume advice through conversational AI
- **🔄 Version Management**: Track different versions of your resume for various applications

## 🚀 Technologies

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), Python 3.8+
- **Database**: MongoDB
- **Frontend**: Jinja2 templates, Alpine.js, HTML/CSS
- **AI Integration**: Deepseek API
- **Deployment**: Docker, Docker Compose
- **Caching**: Redis

> [!CAUTION]
> This application utilizes LLM models which may generate unpredictable responses. Always review and verify AI-generated content before submitting to potential employers. The application is currently in beta, with ongoing improvements to the prompt engineering and output quality.

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- MongoDB instance (local or remote)
- Deepseek API key

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEEPSEEK_API_KEY=your_api_key_here
MONGODB_URI=mongodb://username:password@host:port/
DB_NAME=myresumo
REDIS_URL=redis://localhost:6379
```

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/AnalyticAce/MyResumo.git
cd MyResumo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

5. Access the application at `http://localhost:8080`

### Docker Deployment

1. Build and run the containers:
```bash
docker-compose up -d
```

2. Access the application at `http://localhost:8080`

## 📚 API Documentation

Once the application is running, access the API documentation at:
- Interactive API docs: `http://localhost:8080/docs`
- OpenAPI specification: `http://localhost:8080/openapi.json`

## 🧪 Testing

Run the test suite with:

```bash
pytest tests/
```

## 📖 Usage Guide

1. **Upload Your Resume**: Submit your existing resume in PDF or DOCX format
2. **Add Job Description**: Paste the job description or upload it as a text file
3. **Generate Tailored Resume**: Let AI analyze and customize your resume
4. **Review and Edit**: Make any final adjustments to the generated content
5. **Export**: Download your optimized resume in your preferred format

## 🤝 Contributing

Contributions are welcome! Please check the [contribution guidelines](CONTRIBUTING.md) for more details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Resume analytics dashboard
- [ ] Interview preparation suggestions
- [ ] Cover letter generation
- [ ] Integration with job search platforms
- [ ] Enhanced PDF parsing and extraction

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**DOSSEH Shalom** - [LinkedIn](https://www.linkedin.com/in/shalom-dosseh-4a484a262) - [GitHub](https://github.com/AnalyticAce)

Project Link: [https://github.com/AnalyticAce/MyResumo](https://github.com/AnalyticAce/MyResumo)

