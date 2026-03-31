# services/bullet_service.py

import random
from openai import OpenAI
from config import OPENAI_API_KEY
from models.constants import FALLBACK_BULLETS
from models.role_detector import detect_role
from services.skills_service import extract_jd_technologies
from utils.color_utils import Colors
import user_session

client = OpenAI(api_key=OPENAI_API_KEY)


# ── Seniority helper ──────────────────────────────────────────────────────────

def _seniority_label(idx, total):
    if idx == 0:
        return "Current / most recent role"
    if idx == total - 1:
        return "Earliest / entry-level role"
    return "Mid-career role"


# ── AI prompt builder ─────────────────────────────────────────────────────────

def _build_prompt(jd_text, jd_tech, role, companies):
    """Build an ATS-optimized bullet-generation prompt."""

    total = len(companies)

    company_sections = []
    for idx, exp in enumerate(companies):
        label = _seniority_label(idx, total)
        company_sections.append(
            f"{exp['company'].upper()} ({label} — {exp['role']}):\n"
            f"  Context: {exp['context']}\n"
            f"  Dates: {exp['start_date']} – {exp['end_date']}"
        )

    output_format_sections = []
    for exp in companies:
        output_format_sections.append(
            f"{exp['company'].upper()}:\n"
            + "\n".join(f"{i+1}. [bullet]" for i in range(6))
        )

    return f"""You are a senior technical resume writer who specializes in ATS optimization.

JOB DESCRIPTION (read carefully — use the EXACT terminology and keywords from here):
{jd_text[:3000]}

KEY TECHNOLOGIES & SKILLS EXTRACTED FROM JD:
{jd_tech}

DETECTED ROLE: {role}

CANDIDATE EXPERIENCE:
{chr(10).join(company_sections)}

RULES — follow every rule exactly:
1. EVERY bullet must contain at least one keyword from KEY TECHNOLOGIES & SKILLS above — use the exact JD phrasing.
2. Write 6 bullets per company, each 20–28 words.
3. Every bullet across ALL {total} companies must start with a DIFFERENT action verb — no repeats at all.
4. Distribute these themes across the 6 bullets per company:
   - Bullet 1: Core implementation / development (primary technical work)
   - Bullet 2: Integration / APIs / data flow
   - Bullet 3: Performance optimization / scalability
   - Bullet 4: Architecture / design decisions
   - Bullet 5: Cross-functional collaboration / delivery impact
   - Bullet 6: CI/CD / automation / DevOps / quality
5. Include 2–3 quantified metrics per company (%, numbers, scale, time saved, improvement).
6. Match seniority to each company label — earlier roles should sound less senior.
7. Do NOT repeat the same metric pattern (e.g., don't use "30%" in every company).
8. Sound like real work — specific and technical, not vague filler.
9. Naturally weave in JD keywords so bullets read fluently, not like keyword lists.

OUTPUT FORMAT — complete sentences only, no placeholders:

{chr(10).join(output_format_sections)}"""


# ── Response parser ───────────────────────────────────────────────────────────

def _parse_bullets(text, companies):
    """Parse AI response into a dict keyed by company key."""
    name_to_key = {exp["company"].upper(): exp["key"] for exp in companies}
    for exp in companies:
        words = exp["company"].upper().split()
        for word in words:
            if len(word) > 3 and word not in name_to_key:
                name_to_key[word] = exp["key"]

    bullets = {exp["key"]: [] for exp in companies}
    current_key = None

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        upper = line.upper()
        matched_key = None
        for name_fragment, key in name_to_key.items():
            if name_fragment in upper:
                matched_key = key
                break

        if matched_key:
            current_key = matched_key
            continue

        if current_key and line and (line[0].isdigit() or line[0] in "-•·"):
            bullet = line.lstrip("0123456789.-•·) ").strip()
            if len(bullet) > 15 and "bullet" not in bullet.lower()[:10]:
                bullets[current_key].append(bullet)

    return bullets


# ── Public API ────────────────────────────────────────────────────────────────

def generate_matching_bullets(jd_text):
    """Generate 6 ATS-optimized bullets for each company."""
    print(f"\n{Colors.BLUE}Generating JD-matched bullets...{Colors.END}")

    jd_tech = extract_jd_technologies(jd_text)
    role = detect_role(jd_text)
    companies = user_session.YOUR_EXPERIENCE

    print(f"{Colors.GREEN}Detected Role: {role}{Colors.END}")

    prompt = _build_prompt(jd_text, jd_tech, role, companies)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an expert resume writer specializing in ATS-optimized {role} resumes. "
                        "Your goal is to write bullets that score 90%+ on ATS systems by naturally embedding "
                        "exact JD keywords into every single bullet point. "
                        f"Write exactly {len(companies) * 6} bullets total. "
                        "Every bullet must start with a unique action verb — zero repeats. "
                        "Make every bullet sound like real, specific engineering work."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.35,
            max_tokens=4500,
        )

        bullets = _parse_bullets(response.choices[0].message.content, companies)

        # Fill any gaps with generic fallbacks
        for exp in companies:
            key = exp["key"]
            while len(bullets[key]) < 6:
                bullets[key].append(random.choice(FALLBACK_BULLETS))
            bullets[key] = bullets[key][:6]

        print(f"{Colors.GREEN}Bullets generated for {len(companies)} companies{Colors.END}")
        return bullets

    except Exception as e:
        print(f"{Colors.RED}Bullet generation failed ({e}), using fallbacks{Colors.END}")
        return {
            exp["key"]: random.sample(FALLBACK_BULLETS, min(6, len(FALLBACK_BULLETS)))
            + [FALLBACK_BULLETS[i % len(FALLBACK_BULLETS)] for i in range(max(0, 6 - len(FALLBACK_BULLETS)))]
            for exp in companies
        }
