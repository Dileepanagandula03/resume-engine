# services/ats_service.py

from openai import OpenAI
from config import OPENAI_API_KEY
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)

def calculate_ats_score(resume_text, jd_text):
    print(f"\n{Colors.BLUE}📊 Calculating ATS score...{Colors.END}")
    
    prompt = f"""Extract ALL technical skills and keywords from this JD.

{jd_text}

Return comma-separated list. Include ONLY technical items:
- Programming languages
- Tools and technologies
- Platforms
- Databases
- Technical methodologies
- Compliance/security terms

NO soft skills."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )
        
        jd_keywords = [k.strip() for k in response.choices[0].message.content.split(',')]
        resume_lower = resume_text.lower()
        matched = [kw for kw in jd_keywords if kw.lower() in resume_lower]
        
        score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ATS SCORE: {score:.1f}%{Colors.END}")
        print(f"\n{Colors.GREEN}✅ Matched ({len(matched)}): {', '.join(matched[:15])}...{Colors.END}")
        
        missing = [kw for kw in jd_keywords if kw not in matched]
        if missing:
            print(f"\n{Colors.YELLOW}⚠️ Missing ({len(missing)}): {', '.join(missing[:10])}...{Colors.END}")
        
        return score
    except Exception as e:
        print(f"{Colors.RED}ATS scoring failed: {e}{Colors.END}")
        return 0