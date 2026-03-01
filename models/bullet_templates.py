# models/bullet_templates.py

# Template structure for bullets by category
BULLET_TEMPLATES = {
    'optum': {
        1: {"category": "python_validation", "template": "Developed Python scripts to {action} data, achieving {metric} accuracy across {volume} records"},
        2: {"category": "pipeline_tool", "template": "Built {tool} pipelines processing {volume} records daily, improving {metric} by {percentage}%"},
        3: {"category": "sql", "template": "Optimized SQL queries for data validation, reducing {metric} by {percentage}%"},
        4: {"category": "cloud_migration", "template": "Migrated legacy data to {cloud} using {tool}, enhancing {benefit} by {percentage}%"},
        5: {"category": "production_support", "template": "Monitored production systems, ensuring {metric} uptime for critical data pipelines"},
        6: {"category": "queue_tool", "template": "Managed {tool} task queues processing {volume} jobs daily with {percentage}% reliability"}
    },
    'state_street': {
        1: {"category": "big_data", "template": "Architectured large-scale data processing in {tool}, handling {volume} records with {metric} accuracy"},
        2: {"category": "orchestration", "template": "Orchestrated data pipelines using {tool}, reducing {metric} by {percentage}%"},
        3: {"category": "iac", "template": "Implemented Infrastructure as Code with {tool}, reducing costs by {percentage}%"},
        4: {"category": "data_modeling", "template": "Designed dimensional data models in {tool}, improving {metric} by {percentage}%"},
        5: {"category": "stakeholder", "template": "Collaborated with stakeholders to gather requirements, reducing delivery time by {percentage}%"},
        6: {"category": "ci_cd", "template": "Automated CI/CD processes using {tool}, achieving {percentage}% faster deployment"}
    },
    'tech_mahindra': {
        1: {"category": "python_automation", "template": "Automated data quality checks using Python, reducing discrepancies by {percentage}% across {volume} records"},
        2: {"category": "sql_performance", "template": "Enhanced SQL query performance by {percentage}% through strategic indexing"},
        3: {"category": "etl_tool", "template": "Developed ETL pipelines with {tool}, processing {volume} records daily"},
        4: {"category": "client_delivery", "template": "Delivered client-specific solutions by translating requirements, achieving {metric} satisfaction"},
        5: {"category": "bi_tool", "template": "Utilized {tool} for business intelligence, increasing efficiency by {percentage}%"},
        6: {"category": "monitoring", "template": "Established monitoring systems, reducing downtime by {percentage}%"}
    }
}

# Category to technology mapping
TECH_CATEGORIES = {
    "scraping_tools": ["scrapy", "zyte", "selenium", "playwright", "beautifulsoup", "scrapinghub"],
    "queue_tools": ["celery", "redis", "kafka", "rabbitmq", "aws sqs", "azure service bus"],
    "pipeline_tools": ["spark", "airflow", "databricks", "flink", "beam"],
    "cloud_platforms": ["aws", "azure", "gcp", "digitalocean"],
    "iac_tools": ["terraform", "cloudformation", "arm", "bicep", "pulumi"],
    "ci_cd_tools": ["jenkins", "github actions", "gitlab ci", "circleci", "azure devops"],
    "databases": ["postgresql", "mysql", "sql server", "oracle", "snowflake", "mongodb", "cosmosdb"],
    "bi_tools": ["tableau", "power bi", "looker", "quickSight"],
    "web_frameworks": ["django", "flask", "fastapi", "spring", "node.js"],
    "python": ["python"],
    "sql": ["sql"]
}