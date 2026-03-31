# my_info.py
# ============================================================
# USER CONFIGURATION — Edit this file with YOUR information.
# The resume engine uses ONLY what you put here. Nothing else.
# ============================================================


# ── PERSONAL INFORMATION ────────────────────────────────────
YOUR_NAME = "Dileep Anagandula"
YOUR_PHONE = "314-575-7231"
YOUR_EMAIL = "dileepanagandula3@gmail.com"
YOUR_LOCATION = "Austin, TX"

YOUR_LINKEDIN = "https://linkedin.com/in/yourprofile"
YOUR_GITHUB = "https://github.com/Dileepanagandula03"
YOUR_PORTFOLIO = ""  # Leave empty string to hide from resume


# ── SUMMARY (base — AI will tailor it to each JD) ───────────
YEARS_OF_EXPERIENCE = 6

PROFESSIONAL_SUMMARY = """Data Engineer with 6+ years of experience architecting cloud-native data \
platforms. Proven ability to migrate legacy infrastructures and develop scalable solutions that \
enhance data accessibility and performance. Recently completed a Master's degree in Information \
Systems, further enhancing expertise in translating business needs into effective data strategies."""


# ── WORK EXPERIENCE ──────────────────────────────────────────
# List your jobs from MOST RECENT to OLDEST.
# "key"  — short internal ID (letters/underscores only, unique)
# "role" — your actual title at that company
YOUR_EXPERIENCE = [
    {
        "key": "optum",
        "company": "Optum",
        "role": "Data Engineer",
        "location": "Chicago, IL",
        "start_date": "01/2025",
        "end_date": "Present",
        "context": (
            "Current role at a large healthcare company. "
            "Building ETL pipelines using Python, Spark, and Azure. "
            "Implementing data validation frameworks for 5M+ daily records."
        ),
    },
    {
        "key": "state_street",
        "company": "State Street Corporation",
        "role": "Senior Data Engineer",
        "location": "Boston, MA",
        "start_date": "05/2021",
        "end_date": "12/2023",
        "context": (
            "Senior role at a major financial-services firm. "
            "Designed reconciliation frameworks for 50M+ daily transactions. "
            "Led migration of 500 GB data warehouse to Azure cloud."
        ),
    },
    {
        "key": "tech_mahindra",
        "company": "Tech Mahindra",
        "role": "Data Engineer",
        "location": "Hyderabad, India",
        "start_date": "09/2018",
        "end_date": "04/2021",
        "context": (
            "Early-career role building ETL pipelines for telecom clients. "
            "Used SSIS and T-SQL. "
            "Automated data-quality checks for 2M+ daily records."
        ),
    },
]


# ── CORE SKILLS ──────────────────────────────────────────────
# Format: "Category Label: skill1, skill2, skill3"
# These are YOUR actual skills. The engine will NOT invent skills
# you don't have — it only reorders them to match the JD.
CORE_SKILLS = [
    "Programming & Scripting: Python, SQL (expert), PySpark, Scala, Bash, PowerShell",
    "Cloud Platforms: Azure (Data Factory, Databricks, Synapse, Functions), AWS (S3, Lambda, Glue, Kinesis)",
    "Data Engineering: ETL/ELT Pipeline Development, Apache Spark, Apache Airflow, Apache Kafka, Data Warehousing",
    "Databases: SQL Server, PostgreSQL, MySQL, CosmosDB, Oracle, Snowflake",
    "DevOps & Tools: Docker, Kubernetes, Jenkins, Git, CI/CD, Terraform",
    "BI & Visualization: Tableau, Power BI, Looker",
    "Compliance & Security: IAM, RBAC, KMS, HIPAA, GxP, Data Governance",
]


# ── EDUCATION ────────────────────────────────────────────────
YOUR_EDUCATION = [
    {
        "school": "Webster University",
        "degree": "Master of Science in Information Systems",
        "location": "St. Louis, MO",
        "start_date": "Jan 2024",
        "end_date": "Dec 2025",
        "gpa": "3.8/4.0",   # Leave empty string "" to hide GPA
    },
]


# ── PROJECTS ────────────────────────────────────────────────
# Remove entries or add new ones — the resume will adjust.
YOUR_PROJECTS = [
    {
        "title": "Azure Medallion Data Pipeline",
        "url": "https://github.com/Dileepanagandula03/azure-medallion-data-pipeline",
        "description": (
            "Built a Medallion architecture leveraging ADF, ADLS, and Databricks to orchestrate "
            "ETL workflows, apply data quality checks, and deliver curated datasets consumed by "
            "Power BI dashboards."
        ),
        "link_text": "View Project",
    },
    {
        "title": "AI-Powered Resume Tailoring Tool",
        "url": "https://github.com/Dileepanagandula03/resume-engine",
        "description": (
            "Built an AI-powered resume tailoring tool using OpenAI LLM APIs and Python that "
            "automates resume customization in under 2 minutes, improves ATS match scores by "
            "25–40%, and delivers 75% cost savings compared to commercial solutions."
        ),
        "link_text": "View Project",
    },
    {
        "title": "Real-Time and Batch Weather Data Pipeline",
        "url": "https://github.com/Dileepanagandula03/weather-pipeline-project",
        "description": (
            "Built an end-to-end real-time and batch weather data pipeline on Azure, leveraging "
            "serverless ingestion and streaming analytics to process API-based event data, apply "
            "transformations and validations, and deliver analytics-ready datasets with a "
            "cost-optimized architecture."
        ),
        "link_text": "View Project",
    },
    {
        "title": "ETL vs ELT Decision Framework — Capstone",
        "url": "https://github.com/Dileepanagandula03/Capstone-Data-Engineering-Pipelines",
        "description": (
            "Developed a comparative ETL vs ELT decision framework by evaluating performance, "
            "scalability, cost efficiency, and governance trade-offs in cloud-based data pipelines, "
            "providing actionable guidance for architecture selection."
        ),
        "link_text": "View Paper",
    },
]
