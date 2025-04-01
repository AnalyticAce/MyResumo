# MyResumo
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)

## Overview
**MyResumo** is an AI-backed resume generator designed to tailor your resume and skills based on a given job description. This innovative tool leverages the latest advancements in AI technology to provide you with a customized resume that stands out.

## Features
- **AI-Powered Customization**: Utilizes AI to analyze job descriptions and tailor your resume accordingly.
- **Deepseek API**: Incorporates Deepseek API for intelligent interactions and suggestions with the use of the model.

## Technologies Used
- FastAPI
- HTML
- CSS
- Deepseek API
- Docker
- Jinja2

> [!CAUTION]
> This app uses LLM models, which may generate unpredictable responses. Always use caution and common sense when following the generated responses. This
> app is in its beta version, and there is still a lot of room for improvements. Issues will be opened in the following days to solve core bugs and fine-tune the prompt for better outputs.

## Running the Application

To run **MyResumo**, you'll need to set up your environment and install the necessary dependencies.

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Docker (if running with Docker Compose)

### Installation
#### Running Locally
1. Clone the repository:
```bash
git clone https://github.com/AnalyticAce/MyResumo.git
```
2. Navigate to the project directory:
```bash
cd MyResumo
```
3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
5. Start the FastAPI backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

#### Running With Docker Compose
1. Ensure Docker is installed on your system.
2. Navigate to the project directory and build the Docker containers:
```bash
docker-compose up --build
```
3. The application will be available at `http://localhost:8080` for the backend and `http://localhost:8501` for the frontend.

#### Running With Docker
1. Ensure Docker is installed on your system.
2. Navigate to the project directory and pull the Docker image:
```bash
    docker pull ghcr.io/analyticace/myresumo:latest
```
3. Build the docker images:
```bash
    docker run ghcr.io/analyticace/myresumo:latest -p 8080:8080
```
4. The application will be available at `http://localhost:8080` for the backend and `http://localhost:8501` for the frontend.

## Contribution Guidelines

We welcome contributions to **MyResumo**! If you'd like to contribute, please follow these guidelines:

1. **Fork the Repository**: Start by forking the MyResumo repository on GitHub.
2. **Clone the Forked Repository**: Clone your forked repository to your local machine using `git clone`.
3. **Create a New Branch**: Create a new branch for your contribution using `git checkout -b feature/my-contribution`.
4. **Make Changes**: Add new features, fix bugs, or improve existing functionality.
5. **Test Locally**: Ensure everything works as expected by running:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```
6. **Commit and Push**: Commit your changes and push them to your forked repository.
7. **Create a Pull Request**: Open a pull request to the `main` branch of the original repository with a clear description of your changes.
8. **Review and Merge**: The maintainers will review your pull request, and once approved, your changes will be merged.

## Contact
For any inquiries or collaboration requests, please reach out to **DOSSEH Shalom** on [LinkedIn](https://www.linkedin.com/in/shalom-dosseh-4a484a262).

