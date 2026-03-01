# Resume Generator

AI-powered tool that customizes resumes to match job descriptions using OpenAI.

## 🚀 Features
- Matches resume to any job description
- Auto-injects missing technical skills
- Generates formatted Word document
- 90%+ ATS match score

## 📋 Prerequisites
- Python 3.8+
- OpenAI API key

## 🔧 Installation

1. Clone the repository
```bash
git clone https://github.com/Dileepanagandula03/resume-engine.git
cd resume-engine


Create config.py file:
OPENAI_API_KEY = "your-api-key-here"


Install dependencies (if any):
pip install openai python-docx


Usage
python main.py


Paste job description when prompted

Resume will be generated in output/ folder


Security
API key stays local in config.py

config.py is ignored by git (see .gitignore)




📁 Project Structure

resume-engine/
├── controllers/     # Main logic
├── models/         # Data models
├── services/       # Core services
├── templates/      # Resume templates
├── utils/          # Helper functions
└── main.py         # Entry point


Author
Dileep Anagandula


---


Done! ✅
