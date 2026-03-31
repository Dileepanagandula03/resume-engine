# services/resume_parser.py
#
# Parses a raw resume (plain text paste) into a structured dict
# that matches the user_session schema.

import json
import re
from openai import OpenAI
from config import OPENAI_API_KEY
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)

PARSE_PROMPT = """You are a resume parser. Extract ALL information from the resume below into this exact JSON structure.

RULES:
- "key" for each experience entry = company name lowercased, spaces replaced with underscores (e.g. "google_inc")
- "context" = 3–5 sentences capturing: (1) the primary technologies and tools used, (2) the type of systems/applications built, (3) the scale or impact, (4) the team/domain context. Be specific — include actual tech names (e.g. "Python, React, AWS Lambda, PostgreSQL"). This field is used by an AI to write ATS-optimized resume bullets, so the richer and more technical, the better.

- "skills" = list of strings in the format "ActualCategoryName: skill1, skill2, skill3"
    CRITICAL RULES FOR SKILLS:
    1. Use the EXACT category name from the resume (e.g. "Programming & Databases", "Tools & Frameworks", "Cloud Platforms").
    2. NEVER use the word "Category" as a category name. The word "Category" is just a placeholder in the schema — replace it with the real name.
    3. Each string must have exactly ONE colon. The text before the colon is the category name; after is the comma-separated skills.
    4. Example correct output: ["Programming & Databases: Python, SQL, JavaScript", "Cloud Platforms: AWS, Azure, GCP"]
    5. Example WRONG output: ["Category: Python, Programming & Databases: JavaScript"] ← this is wrong, do not do this.

- "years_of_experience" = total years inferred from dates (integer)
- "gpa" = empty string if not mentioned
- "linkedin" = full URL only (must start with https://). If the resume has "linkedin.com/in/username" without https://, prepend https://. If only the word "LinkedIn" appears with no URL, use "".
- "github"  = full URL only (must start with https://). If the resume has "github.com/username" without https://, prepend https://. If only the word "GitHub" appears with no URL, use "".
- "portfolio" = full URL only (must start with https://). If the resume has any personal website URL, prepend https:// if missing. If nothing found, use "".
- "projects" = extract ALL projects listed under any section named "Projects", "Personal Projects", "Side Projects", "Academic Projects", etc.
    For each project: "title" = project name, "description" = what the project does (1-2 sentences), "url" = project URL if mentioned else "", "link_text" = "View Project"
    If genuinely no projects section exists, use [].
- For start_date / end_date: convert any date format to MM/YYYY (e.g. "Aug '22" → "08/2022", "Oct '24" → "10/2024"). Use "Present" for current roles.
- "location" = extract city/state from resume header if present, otherwise "".
- Return ONLY the JSON object — no markdown fences, no explanations.

JSON SCHEMA:
{
  "name": "",
  "phone": "",
  "email": "",
  "location": "",
  "linkedin": "",
  "github": "",
  "portfolio": "",
  "years_of_experience": 0,
  "summary": "",
  "experience": [
    {
      "key": "",
      "company": "",
      "role": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "context": ""
    }
  ],
  "skills": [
    "Category: skill1, skill2"
  ],
  "education": [
    {
      "school": "",
      "degree": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "gpa": ""
    }
  ],
  "projects": [
    {
      "title": "",
      "url": "",
      "description": "",
      "link_text": "View Project"
    }
  ]
}

RESUME:
{resume_text}"""


def parse_resume(resume_text: str) -> dict:
    """Use GPT to extract structured profile data from raw resume text."""
    print(f"{Colors.BLUE}Parsing your resume...{Colors.END}")

    prompt = PARSE_PROMPT.replace("{resume_text}", resume_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise resume parser. Extract information exactly as it appears. "
                        "For the 'context' field per job, be thorough and technical — list the actual "
                        "technologies, frameworks, and systems used so that an AI can later write "
                        "accurate, specific resume bullets. "
                        "Return ONLY valid JSON — no markdown, no extra text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=4500,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if model adds them anyway
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        data = json.loads(raw)

        # Post-process: clean malformed skill strings where the AI used "Category" literally
        if "skills" in data and isinstance(data["skills"], list):
            cleaned_skills = []
            for entry in data["skills"]:
                if isinstance(entry, str) and ":" in entry:
                    category, rest = entry.split(":", 1)
                    if category.strip().lower() == "category" and ":" in rest:
                        continue
                    cleaned_skills.append(entry)
                elif isinstance(entry, str):
                    cleaned_skills.append(entry)
            data["skills"] = cleaned_skills

        print(f"{Colors.GREEN}Resume parsed: {data.get('name', 'Unknown')}{Colors.END}")
        return data

    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Failed to parse resume JSON: {e}{Colors.END}")
        raise
    except Exception as e:
        print(f"{Colors.RED}Resume parsing failed: {e}{Colors.END}")
        raise


def validate_parsed_data(data: dict) -> list[str]:
    """Return list of warnings for missing critical fields."""
    warnings = []
    if not data.get("name"):
        warnings.append("Name not found")
    if not data.get("email"):
        warnings.append("Email not found")
    if not data.get("experience"):
        warnings.append("No work experience found")
    if not data.get("skills"):
        warnings.append("No skills found")
    return warnings
