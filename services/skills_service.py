# services/skills_service.py

from openai import OpenAI
from models.constants import CORE_SKILLS_GROUPS
from config import OPENAI_API_KEY
from utils.color_utils import Colors

client = OpenAI(api_key=OPENAI_API_KEY)

# Skill group mapping for dynamic insertion
SKILL_GROUP_KEYWORDS = {
    'Programming & Scripting': ['python', 'sql', 'pyspark', 'scala', 'bash', 'powershell', 'java', 'django', 'celery'],
    'Cloud Platforms': ['aws', 'azure', 'gcp', 'cloud', 's3', 'lambda', 'glue', 'kinesis', 'data factory', 'databricks', 'synapse'],
    'Data Engineering': ['etl', 'elt', 'spark', 'airflow', 'kafka', 'warehousing', 'pipeline'],
    'Databases': ['sql server', 'postgresql', 'mysql', 'cosmosdb', 'oracle', 'snowflake', 'clickhouse', 'bigquery', 'redis'],
    'DevOps & Tools': ['docker', 'kubernetes', 'jenkins', 'git', 'ci/cd', 'terraform', 'gitlab'],
    'BI & Visualization': ['tableau', 'power bi', 'looker'],
    'Compliance & Security': ['iam', 'rbac', 'kms', 'hipaa', 'gxp', 'governance']
}

def extract_jd_technologies(jd_text):
    """Extract ALL technical skills from JD"""
    prompt = f"""Extract EVERY technical skill, tool, technology, and platform from this job description.

JOB DESCRIPTION:
{jd_text}

Return as a comma-separated list. Include:
- Programming languages (Python, SQL, Scala, Java, etc.)
- Tools (Airflow, Spark, Kafka, Tableau, etc.)
- Platforms (Azure, AWS, Snowflake, Databricks, etc.)
- Databases (SQL Server, PostgreSQL, MySQL, Oracle, etc.)
- DevOps tools (Docker, Kubernetes, Terraform, Jenkins, etc.)
- Compliance/security terms (IAM, KMS, HIPAA, GxP, etc.)

ONLY technical items. NO soft skills."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except:
        return "Python, SQL, Azure, AWS, Spark, Airflow, Databricks, Snowflake, Terraform, Docker, Kubernetes, Tableau"

def find_skill_group(skill_name):
    """Find which group a skill belongs to"""
    skill_lower = skill_name.lower()
    
    for group, keywords in SKILL_GROUP_KEYWORDS.items():
        for keyword in keywords:
            if keyword in skill_lower or skill_lower in keyword:
                return group
    
    # Default to 'Data Engineering' if no match
    return 'Data Engineering'

def generate_matched_skills(jd_text):
    """Generate skills section - Insert JD skills into existing groups, NO additional section"""
    print(f"{Colors.BLUE}🔧 Generating JD-matched skills...{Colors.END}")
    
    # Extract all tech from JD
    jd_tech_skills = extract_jd_technologies(jd_text)
    jd_tech_list = [t.strip() for t in jd_tech_skills.split(',')]
    
    # Convert core skills groups to a dictionary for easier manipulation
    core_skills_dict = {}
    for group_line in CORE_SKILLS_GROUPS:
        if ':' in group_line:
            group_name, skills = group_line.split(':', 1)
            core_skills_dict[group_name.strip()] = [s.strip() for s in skills.split(',')]
    
    # Add JD skills to appropriate groups
    for tech in jd_tech_list:
        tech = tech.strip()
        if not tech or len(tech) < 2:
            continue
            
        # Find which group this tech belongs to
        target_group = find_skill_group(tech)
        
        # Check if already in the group
        already_exists = False
        if target_group in core_skills_dict:
            for existing in core_skills_dict[target_group]:
                if tech.lower() in existing.lower() or existing.lower() in tech.lower():
                    already_exists = True
                    break
        
        # Add if not exists
        if not already_exists and target_group in core_skills_dict:
            core_skills_dict[target_group].append(tech)
    
    # Convert back to list format
    updated_skills = []
    for group_name, skills in core_skills_dict.items():
        # Remove duplicates while preserving order
        unique_skills = []
        for skill in skills:
            if skill not in unique_skills:
                unique_skills.append(skill)
        
        updated_skills.append(f"{group_name}: {', '.join(unique_skills)}")
    
    print(f"{Colors.GREEN}✅ Skills updated - JD tools added to existing groups{Colors.END}")
    return updated_skills