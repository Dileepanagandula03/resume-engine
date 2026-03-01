# services/summary_service.py

from openai import OpenAI
from models.role_detector import detect_role
from config import OPENAI_API_KEY
from my_info import PROFESSIONAL_SUMMARY
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_matched_summary(jd_text):
    """Generate summary with role detection"""
    print(f"{Colors.BLUE}✍️  Generating JD-matched summary...{Colors.END}")
    
    role = detect_role(jd_text)

    prompt = f"""You are an expert resume writer.

JOB DESCRIPTION:
{jd_text}

CANDIDATE BACKGROUND:
{PROFESSIONAL_SUMMARY}

ROLE DETECTED: {role}

YOUR TASK:
Write a 3-4 sentence summary that:
1. Starts with exactly "{role} with 6+ years of experience"
2. Focus on BUILDING SCALABLE SYSTEMS and DATA INFRASTRUCTURE (NOT domains like healthcare/finance)
3. Do NOT mention healthcare or financial services unless the JD specifically asks for them
4. Include key technical strengths relevant to the JD (Python, SQL, cloud, data modeling)
5. Mention Master's degree in Information Systems
6. End with impact statement about treating data as strategic asset

Return ONLY the summary text, no explanations."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        summary = response.choices[0].message.content.strip()
        summary = summary.replace('**', '').replace('__', '').replace('*', '')
        return summary
    except Exception as e:
        print(f"{Colors.RED}Summary generation failed, using default{Colors.END}")
        return f"{role} with 6+ years of experience designing and maintaining scalable data infrastructure that powers analytics and decision-making. Expert in Python, SQL, and cloud platforms with strong focus on building reliable data pipelines and data models. Recently completed a Master's degree in Information Systems, enhancing ability to translate business needs into effective data strategies. Passionate about treating data as a strategic asset to enable business growth."