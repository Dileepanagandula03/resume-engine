# services/summary_service.py

from openai import OpenAI
from models.role_detector import detect_role
from config import OPENAI_API_KEY
import user_session
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_matched_summary(jd_text):
    """Generate a JD-tailored, ATS-optimized summary using the candidate's background."""
    print(f"{Colors.BLUE}Generating JD-matched summary...{Colors.END}")

    role = detect_role(jd_text)
    yoe = f"{user_session.YEARS_OF_EXPERIENCE}+" if user_session.YEARS_OF_EXPERIENCE else ""

    prompt = f"""You are an expert ATS-optimized resume writer. Your goal is a summary that scores 90%+ on ATS.

JOB DESCRIPTION:
{jd_text}

CANDIDATE BACKGROUND:
{user_session.PROFESSIONAL_SUMMARY}

DETECTED ROLE: {role}
YEARS OF EXPERIENCE: {yoe}

YOUR TASK:
Write a 3–4 sentence professional summary. Follow this exact structure:

Sentence 1: Start with exactly "{role} with {yoe} years of experience" — then mention 2–3 of the candidate's most relevant technical strengths that directly match the JD.
Sentence 2: Call out specific tools, platforms, or technologies from the JD using the EXACT same wording as the job description (copy terms verbatim — do not paraphrase).
Sentence 3: Mention relevant methodologies, architectures, or practices from the JD (e.g., "object-oriented programming", "REST APIs", "CI/CD", "ERP customization") — again use exact JD phrasing.
Sentence 4: Close with a concise business impact statement that aligns with the JD's stated goals.

CRITICAL RULES:
- Use the EXACT keyword phrases from the JD — ATS systems match exact strings.
- Do NOT mention industry domains (healthcare, finance, etc.) unless the JD explicitly asks.
- Mention the candidate's advanced degree if present in their background.
- Do NOT add markdown, bullet points, or headings — return plain text only.
- Keep the total under 80 words.

Return ONLY the summary paragraph — no labels, no explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=250,
        )
        summary = response.choices[0].message.content.strip()
        return summary.replace("**", "").replace("__", "").replace("*", "")
    except Exception:
        print(f"{Colors.RED}Summary generation failed, using default{Colors.END}")
        return (
            f"{role} with {yoe} years of experience designing and delivering scalable, "
            "production-ready applications using modern technologies and cloud platforms. "
            "Proficient in backend services, REST APIs, CI/CD pipelines, and cross-functional "
            "collaboration to drive business outcomes."
        )
