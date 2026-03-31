# services/ats_service.py

import re
from openai import OpenAI
from config import OPENAI_API_KEY
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)

# Common abbreviation aliases — both directions are checked
_ALIASES = {
    # Languages
    "javascript":           ["js", "es6", "es2015", "ecmascript"],
    "typescript":           ["ts"],
    "python":               ["py"],
    "c#":                   ["csharp", "c sharp", ".net language"],
    # Frameworks / libraries
    "react":                ["reactjs", "react.js", "react js"],
    "node":                 ["nodejs", "node.js", "node js"],
    "vue":                  ["vuejs", "vue.js"],
    "angular":              ["angularjs", "angular js"],
    "express":              ["expressjs", "express.js"],
    "next.js":              ["nextjs", "next js"],
    "spring boot":          ["spring", "springboot"],
    "asp.net":              ["aspnet", "asp net"],
    # Cloud
    "amazon web services":  ["aws"],
    "google cloud platform":["gcp", "google cloud"],
    "microsoft azure":      ["azure"],
    # Databases
    "postgresql":           ["postgres", "psql"],
    "mongodb":              ["mongo"],
    "microsoft sql server": ["mssql", "sql server", "ms sql"],
    "elasticsearch":        ["elastic", "es"],
    "dynamodb":             ["dynamo db", "amazon dynamodb"],
    # DevOps / infra
    "kubernetes":           ["k8s"],
    "continuous integration":["ci"],
    "continuous deployment": ["cd"],
    "ci/cd":                ["ci cd", "cicd", "continuous integration", "continuous deployment"],
    "terraform":            ["infrastructure as code", "iac"],
    "github actions":       ["gh actions"],
    # APIs / protocols
    "restful":              ["rest", "rest api", "restful api", "rest apis"],
    "graphql":              ["graph ql"],
    "soap":                 ["web services"],
    "oauth 2.0":            ["oauth", "oauth2"],
    "jwt":                  ["json web token"],
    # AI / ML
    "machine learning":     ["ml"],
    "artificial intelligence": ["ai"],
    "natural language processing": ["nlp"],
    "large language model": ["llm", "llms"],
    "retrieval augmented generation": ["rag"],
    # NetSuite / ERP
    "netsuite":             ["net suite"],
    "suitescript":          ["suitescript 2.0", "suite script"],
    "suiteflow":            ["suite flow", "workflow automation"],
    "suitecloud":           ["suite cloud"],
    "suitecommerce":        ["suite commerce"],
    # Salesforce
    "salesforce":           ["sfdc"],
    "apex":                 ["salesforce apex"],
    # Misc tech
    "object-oriented":      ["oop", "object oriented", "object-oriented programming"],
    "html":                 ["html5"],
    "css":                  ["css3"],
    "sql":                  ["mysql", "postgresql", "sqlite", "mssql", "t-sql", "pl/sql"],
    "nosql":                ["mongodb", "dynamodb", "cassandra", "couchdb"],
    "websockets":           ["websocket", "web sockets", "real-time"],
    "apache kafka":         ["kafka"],
    "redis":                ["redis cache"],
    "docker":               ["containerization", "containers"],
    "power bi":             ["powerbi"],
    "tableau":              ["tableau desktop"],
    "xml":                  ["extensible markup language"],
    "json":                 ["javascript object notation"],
    "celigo":               ["celigo integration"],
}


def _normalize(text: str) -> str:
    """Lowercase and strip punctuation for flexible matching."""
    return re.sub(r'[^a-z0-9 ]', ' ', text.lower()).strip()


def _keyword_in_resume(keyword: str, resume_lower: str) -> bool:
    """
    Returns True if keyword (or any known alias) appears in the resume.
    Uses word-boundary-aware substring matching to avoid false positives.
    """
    norm_kw = _normalize(keyword)

    # Direct substring match
    if norm_kw in resume_lower:
        return True

    # Multi-word: all significant words must appear
    words = norm_kw.split()
    if len(words) >= 2:
        if all(w in resume_lower for w in words if len(w) > 2):
            return True

    # Alias lookup — check canonical and all aliases
    for canonical, aliases in _ALIASES.items():
        if norm_kw == canonical or norm_kw in aliases:
            targets = [canonical] + aliases
            if any(t in resume_lower for t in targets):
                return True

    return False


def calculate_ats_score(resume_text, jd_text):
    print(f"\n{Colors.BLUE}Calculating ATS score...{Colors.END}")

    prompt = f"""Extract the core technical skills and keywords from this job description.

{jd_text}

Rules:
- Return ONLY short, atomic terms (1-3 words max per item)
- Use the simplest common form: "React" not "ReactJS framework", "Python" not "Python programming language"
- Include: programming languages, frameworks, tools, platforms, databases, cloud services, methodologies
- Exclude: soft skills, years of experience, education requirements, generic terms like "software development"
- Deduplicate: don't list the same skill in multiple forms

Return as a comma-separated list only. No numbering, no explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=400
        )

        raw_keywords = [k.strip() for k in response.choices[0].message.content.split(',')]
        jd_keywords = [k for k in raw_keywords if len(k) > 1]

        resume_lower = _normalize(resume_text)

        matched = [kw for kw in jd_keywords if _keyword_in_resume(kw, resume_lower)]
        missing = [kw for kw in jd_keywords if kw not in matched]
        score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0

        print(f"\n{Colors.GREEN}{Colors.BOLD}ATS SCORE: {score:.1f}%{Colors.END}")
        print(f"\n{Colors.GREEN}Matched ({len(matched)}): {', '.join(matched[:15])}{Colors.END}")
        if missing:
            print(f"\n{Colors.YELLOW}Missing ({len(missing)}): {', '.join(missing[:10])}{Colors.END}")

        return {"score": round(score, 1), "matched": matched, "missing": missing}

    except Exception as e:
        print(f"{Colors.RED}ATS scoring failed: {e}{Colors.END}")
        return {"score": 0, "matched": [], "missing": []}
