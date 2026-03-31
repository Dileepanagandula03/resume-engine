# services/skills_service.py

from openai import OpenAI
from config import OPENAI_API_KEY
from utils.color_utils import Colors
import user_session

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_jd_technologies(jd_text):
    """Extract technical skills mentioned in the JD."""
    prompt = f"""Extract every technical skill, tool, technology, and platform from this job description.

JOB DESCRIPTION:
{jd_text}

Return as a comma-separated list. Include: programming languages, frameworks, platforms, databases,
DevOps tools, security/compliance terms, methodologies. Use the EXACT phrasing from the JD.
ONLY technical items — no soft skills, no years of experience."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Python, SQL, JavaScript, REST APIs, AWS, Docker, CI/CD, Git"


def _extract_top_jd_skills(jd_text, candidate_skills_flat, n=12):
    """
    Ask GPT: given the JD and the candidate's actual skills, return the top N
    skills from the candidate that best match the JD — in JD keyword order.
    Returns a comma-separated string.
    """
    prompt = f"""Job description (extract key required skills from this):
{jd_text[:2000]}

Candidate's actual skills (ONLY pick from this list):
{candidate_skills_flat}

Task: Return the top {n} skills from the candidate's list that best match the job description requirements.
Use the EXACT phrasing from the JD where possible (e.g. if JD says "SuiteScript 2.0" and candidate has "JavaScript", use "JavaScript").
Order them by relevance to the JD (most important first).
Return as a comma-separated list only. No explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ""


def generate_matched_skills(jd_text):
    """Return the candidate's skills reordered for ATS, with a Core Competencies
    row prepended that lists the top JD-matched skills for maximum keyword visibility.

    We NEVER add skills the candidate doesn't have — only reorder and surface them.
    """
    print(f"{Colors.BLUE}Matching skills to JD...{Colors.END}")

    jd_tech_raw = extract_jd_technologies(jd_text)
    jd_keywords = {t.strip().lower() for t in jd_tech_raw.split(",") if t.strip()}

    # ── Step 1: Reorder existing skill groups ─────────────────────────────────
    reordered = []
    all_candidate_skills = []

    for group_line in user_session.CORE_SKILLS:
        if ":" not in group_line:
            reordered.append(group_line)
            continue

        category, skills_str = group_line.split(":", 1)
        skills = [s.strip() for s in skills_str.split(",") if s.strip()]
        all_candidate_skills.extend(skills)

        # Split into JD-matched and the rest (preserve original order within each bucket)
        matched = [s for s in skills if any(kw in s.lower() or s.lower() in kw for kw in jd_keywords)]
        rest = [s for s in skills if s not in matched]

        reordered.append(f"{category}: {', '.join(matched + rest)}")

    # ── Step 2: Build a Core Competencies row from top JD-matched skills ──────
    # This puts the most ATS-critical keywords at the very top of the skills section.
    candidate_skills_flat = ", ".join(all_candidate_skills)
    top_skills_str = _extract_top_jd_skills(jd_text, candidate_skills_flat, n=12)

    if top_skills_str:
        core_competencies = f"Core Competencies: {top_skills_str}"
        final_skills = [core_competencies] + reordered
    else:
        final_skills = reordered

    print(f"{Colors.GREEN}Skills matched and reordered for ATS{Colors.END}")
    return final_skills
