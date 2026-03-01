# models/constants.py

# Core skills groups - ALWAYS present
CORE_SKILLS_GROUPS = [
    "Programming & Scripting: Python, SQL (expert), PySpark, Scala, Bash, PowerShell",
    "Cloud Platforms: Azure (Data Factory, Databricks, Synapse, Functions), AWS (S3, Lambda, Glue, Kinesis)",
    "Data Engineering: ETL/ELT Pipeline Development, Apache Spark, Apache Airflow, Apache Kafka, Data Warehousing",
    "Databases: SQL Server, PostgreSQL, MySQL, CosmosDB, Oracle, Snowflake",
    "DevOps & Tools: Docker, Kubernetes, Jenkins, Git, CI/CD, Terraform",
    "BI & Visualization: Tableau, Power BI, Looker",
    "Compliance & Security: IAM, RBAC, KMS, HIPAA, GxP, Data Governance"
]

# Fallback bullets for when AI fails
FALLBACK_BULLETS = {
    'optum': [
        "Developed Python-based data validation frameworks ensuring healthcare claims data integrity for 5M+ daily records before production loading",
        "Orchestrated cross-functional migration strategies transitioning legacy SQL Server workloads to cloud-native platforms",
        "Engineered automated reconciliation systems comparing source and target data, reducing manual validation effort by 40% across 10+ datasets",
        "Integrated CI/CD pipelines for data services using GitHub Actions, enabling automated testing and deployment with 99.9% success rate",
        "Translated complex business requirements from healthcare stakeholders into scalable technical data solutions adopted by 50+ users",
        "Optimized ETL performance by refactoring PySpark jobs, reducing processing time from 4 hours to 90 minutes for critical claims data"
    ],
    'state_street': [
        "Designed Python/SQL reconciliation frameworks validating 50M+ daily transactions between source systems and enterprise data warehouse",
        "Spearheaded migration of 500GB on-premise data warehouse to Azure Synapse, achieving zero data loss and 40% cost reduction",
        "Constructed ETL pipelines with comprehensive error handling and real-time monitoring, maintaining 99.9% data delivery reliability",
        "Partnered with finance, risk, and operations leaders to resolve complex data discrepancies and improve regulatory reporting accuracy",
        "Standardized data modeling practices across 15+ teams, creating reusable dimension tables that reduced development time by 30%",
        "Implemented infrastructure as code using Terraform, automating cloud resource provisioning and reducing deployment time by 60%"
    ],
    'tech_mahindra': [
        "Formulated SQL transformation logic supporting data migration from Oracle to SQL Server, improving query performance by 60%",
        "Established data validation frameworks that reduced manual investigation time by 30% and ensured 99.5% data reliability for client reporting",
        "Collaborated with international clients to gather requirements and deliver 10+ custom data solutions meeting strict SLA requirements",
        "Streamlined ETL workflows through strategic indexing and parallel processing, cutting batch runtimes from 4 hours to 45 minutes",
        "Generated reusable data quality monitoring dashboards in Tableau, enabling real-time visibility into pipeline health for operations teams",
        "Developed automated alerting systems for pipeline failures, reducing mean time to recovery by 40% for critical production jobs"
    ]
}

# Company display names
COMPANY_NAMES = {
    'optum': 'Optum',
    'state_street': 'State Street Corporation',
    'tech_mahindra': 'Tech Mahindra'
}

# Company locations
COMPANY_LOCATIONS = {
    'optum': 'Chicago, IL',
    'state_street': '',
    'tech_mahindra': ''
}

# Company dates
COMPANY_DATES = {
    'optum': '01/2025 - Present',
    'state_street': '05/2021 - 12/2023',
    'tech_mahindra': '09/2018 - 04/2021'
}