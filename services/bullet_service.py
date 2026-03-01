# services/bullet_service.py

from openai import OpenAI
import random
import re
from models.constants import FALLBACK_BULLETS
from models.role_detector import detect_role
from services.skills_service import extract_jd_technologies
from config import OPENAI_API_KEY
from utils.color_utils import Colors
from my_info import YOUR_EXPERIENCE, CORE_SKILLS

client = OpenAI(api_key=OPENAI_API_KEY)

# Tool category patterns (NOT hardcoded tools!)
TOOL_CATEGORIES = {
    'programming_languages': {
        'patterns': ['java', 'scala', 'python', 'go', 'rust', 'javascript', 'typescript', 'c#', 'c++', 'django', 'celery'],
        'companies': ['tech_mahindra', 'optum'],
        'context': 'development and automation'
    },
    'orchestration': {
        'patterns': ['airflow', 'dagster', 'prefect', 'luigi', 'azure data factory', 'aws step functions', 'glue workflows'],
        'companies': ['state_street', 'optum'],
        'context': 'pipeline orchestration and scheduling'
    },
    'cloud_platforms': {
        'patterns': ['aws', 'azure', 'gcp', 'cloud', 's3', 'ec2', 'lambda', 'emr', 'databricks'],
        'companies': ['state_street', 'optum'],
        'context': 'cloud infrastructure and data processing'
    },
    'data_warehouse': {
        'patterns': ['snowflake', 'redshift', 'bigquery', 'synapse', 'teradata', 'clickhouse'],
        'companies': ['state_street'],
        'context': 'data warehousing and analytics'
    },
    'streaming': {
        'patterns': ['kafka', 'kinesis', 'pubsub', 'spark streaming', 'flink', 'pulsar'],
        'companies': ['state_street'],
        'context': 'real-time data processing'
    },
    'databases': {
        'patterns': ['postgresql', 'mysql', 'oracle', 'sql server', 'mongodb', 'cassandra', 'dynamodb', 'redis'],
        'companies': ['optum', 'tech_mahindra'],
        'context': 'data storage and query optimization'
    },
    'transformation': {
        'patterns': ['dbt', 'spark', 'pyspark', 'pandas', 'dataflow'],
        'companies': ['optum', 'state_street'],
        'context': 'data transformation and modeling'
    },
    'ci_cd': {
        'patterns': ['jenkins', 'github actions', 'gitlab ci', 'circleci', 'terraform', 'cloudformation'],
        'companies': ['state_street'],
        'context': 'infrastructure as code and deployment'
    },
    'visualization': {
        'patterns': ['tableau', 'power bi', 'looker', 'quickSight', 'superset'],
        'companies': ['optum'],
        'context': 'business intelligence and dashboards'
    },
    'container': {
        'patterns': ['docker', 'kubernetes', 'k8s', 'ecs', 'eks', 'aks'],
        'companies': ['state_street'],
        'context': 'containerization and microservices'
    }
}

def categorize_tool(tool_name):
    """Dynamically categorize ANY tool based on patterns"""
    tool_lower = tool_name.lower()
    
    for category, info in TOOL_CATEGORIES.items():
        for pattern in info['patterns']:
            if pattern in tool_lower or tool_lower in pattern:
                return category, info
    
    # If no match, try to guess from common suffixes/prefixes
    if any(term in tool_lower for term in ['sql', 'db', 'database']):
        return 'databases', TOOL_CATEGORIES['databases']
    elif any(term in tool_lower for term in ['flow', 'pipeline', 'etl', 'orchestr']):
        return 'orchestration', TOOL_CATEGORIES['orchestration']
    elif any(term in tool_lower for term in ['stream', 'queue', 'event', 'kafka']):
        return 'streaming', TOOL_CATEGORIES['streaming']
    elif any(term in tool_lower for term in ['cloud', 'aws', 'azure', 'gcp']):
        return 'cloud_platforms', TOOL_CATEGORIES['cloud_platforms']
    elif any(term in tool_lower for term in ['warehouse', 'lake', 'house', 'clickhouse', 'bigquery']):
        return 'data_warehouse', TOOL_CATEGORIES['data_warehouse']
    elif any(term in tool_lower for term in ['lang', 'script', 'py', 'js', 'django', 'celery']):
        return 'programming_languages', TOOL_CATEGORIES['programming_languages']
    elif any(term in tool_lower for term in ['docker', 'k8s', 'kubernetes', 'container']):
        return 'container', TOOL_CATEGORIES['container']
    elif any(term in tool_lower for term in ['gitlab', 'jenkins', 'ci/cd', 'ci cd']):
        return 'ci_cd', TOOL_CATEGORIES['ci_cd']
    
    # Default to most common category
    return 'cloud_platforms', TOOL_CATEGORIES['cloud_platforms']

def parse_bullets(text):
    """Parse bullet points from AI response"""
    bullets = {'optum': [], 'state_street': [], 'tech_mahindra': []}
    lines = text.strip().split('\n')
    current_company = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        upper_line = line.upper()
        if 'OPTUM' in upper_line:
            current_company = 'optum'
            continue
        elif 'STATE STREET' in upper_line:
            current_company = 'state_street'
            continue
        elif 'TECH MAHINDRA' in upper_line:
            current_company = 'tech_mahindra'
            continue
        
        if current_company and line and (line[0].isdigit() or line[0] in ['-', '•', '·']):
            bullet = line.lstrip('0123456789.-•·) ').strip()
            if len(bullet) > 15 and 'bullet with' not in bullet.lower():
                bullets[current_company].append(bullet)
    
    return bullets

def get_missing_tools(jd_tech_list, current_skills_text):
    """Find tools that are in JD but not in current skills/bullets"""
    jd_tools = [t.lower().strip() for t in jd_tech_list if len(t.strip()) > 2]
    current_text = current_skills_text.lower()
    
    missing = []
    for tool in jd_tools:
        # Check if tool already exists in skills or common variations
        tool_variations = [tool, tool.replace(' ', ''), tool.replace('-', '')]
        found = False
        for var in tool_variations:
            if var in current_text:
                found = True
                break
        if not found:
            missing.append(tool)
    
    return missing

def generate_dynamic_injection_instructions(missing_tools):
    """DYNAMICALLY generate where to inject ANY tool - NO HARDCODING!"""
    
    if not missing_tools:
        return ""
    
    instructions = "\n\n📌 **CRITICAL INSTRUCTIONS - INJECT THESE TOOLS:**\n"
    instructions += "For each tool below, inject it into the SPECIFIED company bullet:\n\n"
    
    for tool in missing_tools:
        # Dynamically categorize the tool
        category, category_info = categorize_tool(tool)
        
        # Pick appropriate company from category
        companies = category_info['companies']
        context = category_info['context']
        
        # For each company, decide which bullet position based on category
        for company in companies:
            if company == 'state_street':
                if category == 'data_warehouse':
                    bullet_num = 1
                elif category == 'orchestration':
                    bullet_num = 2
                elif category == 'ci_cd':
                    bullet_num = 6
                elif category == 'streaming':
                    bullet_num = 1
                elif category == 'container':
                    bullet_num = 6
                else:
                    bullet_num = random.choice([1, 2, 3, 4])
            elif company == 'optum':
                if category == 'programming_languages':
                    bullet_num = 1
                elif category == 'transformation':
                    bullet_num = 2
                elif category == 'databases':
                    bullet_num = 3
                else:
                    bullet_num = random.choice([1, 2, 4, 5])
            else:  # tech_mahindra
                if category == 'programming_languages':
                    bullet_num = 1
                elif category == 'databases':
                    bullet_num = 2
                else:
                    bullet_num = random.choice([1, 2, 3])
            
            company_display = company.upper().replace('_', ' ')
            instructions += f"• **{tool}** (category: {category}) → Add to **{company_display}** bullet {bullet_num} in {context} context\n"
    
    return instructions

def generate_matching_bullets(jd_text):
    """Generate bullets with DYNAMIC auto-inject logic for ANY tool"""
    print(f"\n{Colors.BLUE}🤖 AI analyzing JD and generating bullets...{Colors.END}")

    # Get JD technologies
    jd_tech = extract_jd_technologies(jd_text)
    jd_tech_list = [t.strip() for t in jd_tech.split(',')]
    role = detect_role(jd_text)
    
    print(f"{Colors.GREEN}✅ Detected Role: {role}{Colors.END}")
    
    # Get current skills text from CORE_SKILLS
    current_skills_text = ' '.join(CORE_SKILLS) if 'CORE_SKILLS' in dir() else ""
    
    # Find missing tools
    missing_tools = get_missing_tools(jd_tech_list, current_skills_text)
    if missing_tools:
        print(f"{Colors.YELLOW}⚠️ Found {len(missing_tools)} tools in JD missing from skills: {', '.join(missing_tools[:10])}{Colors.END}")
        
        # Show categorization for each missing tool
        for tool in missing_tools[:5]:
            category, _ = categorize_tool(tool)
            print(f"{Colors.BLUE}  • {tool} → categorized as: {category}{Colors.END}")
        
        print(f"{Colors.BLUE}📝 Will DYNAMICALLY inject these into appropriate bullets{Colors.END}")
    
    # Generate dynamic injection instructions
    injection_instructions = generate_dynamic_injection_instructions(missing_tools)
    
    # Build base prompt with dynamic role and NO domain focus
    base_prompt = f"""You are an expert resume writer. Your job is to create bullets that SHOW real experience with EVERY technology from the JD.

JOB DESCRIPTION TECHNOLOGIES (must include these in bullets):
{jd_tech}

DETECTED ROLE: {role}

CANDIDATE BACKGROUND:
{YOUR_EXPERIENCE}

CRITICAL RULE: ONLY use technologies that appear in the JOB DESCRIPTION TECHNOLOGIES list above.
DO NOT invent or add any tools not in that list.

{injection_instructions}

YOUR TASK:
Create 6 bullets for EACH company below.
Each bullet MUST:
1. ONLY include technologies from the JOB DESCRIPTION TECHNOLOGIES list
2. Use metrics SPARINGLY - maximum 2-3 metrics across all 6 bullets for this company
3. Focus on HOW you built systems, solved problems, and worked with stakeholders
4. Sound like actual work done at that specific company
5. Be 20-30 words
6. Start with strong action verb
7. All 18 bullets must have UNIQUE action verbs (no repeats)

WRITE BULLETS FOR:

OPTUM (Current Role - {role}):
- Focus on Python, data validation, production pipelines
- Bullet positions: 1=Development, 2=Pipelines, 3=SQL/Data Modeling, 4=Migration, 5=Support, 6=DevOps

STATE STREET (Senior {role}):
- Focus on large-scale data, migrations, data modeling
- Bullet positions: 1=Large-scale processing, 2=Orchestration, 3=Migration/IaC, 4=Data Modeling, 5=Collaboration, 6=CI-CD/DevOps

TECH MAHINDRA ({role}):
- Focus on automation, data quality, SQL, client delivery
- Bullet positions: 1=Automation, 2=SQL/Data Modeling, 3=ETL/Pipelines, 4=Client Delivery, 5=BI/Analytics, 6=Monitoring

OUTPUT FORMAT - Write complete sentences, not placeholders:

OPTUM:
1. [bullet with Python/validation]
2. [bullet with pipeline tools]
3. [bullet with SQL/data modeling]
4. [bullet with cloud migration]
5. [bullet with production support]
6. [bullet with DevOps/queues]

STATE STREET:
1. [bullet with large-scale processing]
2. [bullet with pipeline orchestration]
3. [bullet with cloud migration/IaC]
4. [bullet with data modeling]
5. [bullet with stakeholder collaboration]
6. [bullet with CI-CD/DevOps]

TECH MAHINDRA:
1. [bullet with Python automation + data quality]
2. [bullet with SQL optimization + data modeling]
3. [bullet with ETL tools + pipelines]
4. [bullet with client delivery + requirements]
5. [bullet with BI tools + efficiency]
6. [bullet with monitoring/alerting + troubleshooting]

Remember: ONLY use technologies from the JOB DESCRIPTION TECHNOLOGIES list. Use the detected role '{role}' naturally in context where relevant. Focus on scalable systems, data modeling, and working with stakeholders."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a senior {role} writing real resume bullets.
                    CRITICAL RULE #1: Only use technologies that appear in the JOB DESCRIPTION TECHNOLOGIES list.
                    CRITICAL RULE #2: Every bullet must start with a DIFFERENT action verb (18 unique verbs).
                    CRITICAL RULE #3: Follow the injection instructions EXACTLY - add each specified tool to its designated bullet.
                    CRITICAL RULE #4: Use metrics SPARINGLY - only 2-3 metrics across all 6 bullets per company.
                    Match technologies to appropriate companies based on seniority.
                    Focus on HOW you built systems, not just listing tools.
                    Make it sound like real work done."""
                },
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.4,
            max_tokens=3500
        )

        bullets_text = response.choices[0].message.content
        bullets = parse_bullets(bullets_text)

        # Ensure we have 6 bullets per company
        for company in bullets:
            while len(bullets[company]) < 6:
                bullets[company].append(random.choice(FALLBACK_BULLETS.get(company, FALLBACK_BULLETS['tech_mahindra'])))
            bullets[company] = bullets[company][:6]

        print(f"{Colors.GREEN}✅ Generated bullets with JD technologies{Colors.END}")
        if missing_tools:
            print(f"{Colors.GREEN}✅ DYNAMICALLY injected missing tools: {', '.join(missing_tools)}{Colors.END}")
        
        return bullets

    except Exception as e:
        print(f"{Colors.RED}Error generating bullets, using fallback: {str(e)}{Colors.END}")
        return {
            'optum': random.sample(FALLBACK_BULLETS['optum'], 6),
            'state_street': random.sample(FALLBACK_BULLETS['state_street'], 6),
            'tech_mahindra': random.sample(FALLBACK_BULLETS['tech_mahindra'], 6)
        }