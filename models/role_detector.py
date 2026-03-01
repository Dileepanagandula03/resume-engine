# models/role_detector.py

import re

def detect_role(jd_text):
    """Detect role from job description"""
    jd_lower = jd_text.lower()
    
    # Check for exact role matches (prioritize Data Engineer)
    if re.search(r'data engineer|data engineering|data infrastructure engineer', jd_lower):
        return 'Data Engineer'
    elif re.search(r'database engineer|dba|sql developer|database developer', jd_lower):
        return 'Database Engineer'
    elif re.search(r'cloud engineer|aws engineer|azure engineer|cloud architect|gcp engineer', jd_lower):
        return 'Cloud Engineer'
    elif re.search(r'data analyst|business analyst|analyst|bi engineer', jd_lower):
        return 'Data Analyst'
    elif re.search(r'machine learning|ml engineer|ai engineer|ai/ml', jd_lower):
        return 'ML Engineer'
    elif re.search(r'backend.*engineer|backend.*developer', jd_lower):
        return 'Backend Engineer'
    else:
        return 'Data Engineer'  # Default to Data Engineer

def get_company_role_name(company, base_role):
    """Get appropriate role name based on company and JD role"""
    role_mapping = {
        'optum': {
            'Database Engineer': 'Database Engineer',
            'Cloud Engineer': 'Cloud Engineer',
            'Data Analyst': 'Data Analyst',
            'ML Engineer': 'ML Engineer',
            'Backend Engineer': 'Backend Engineer',
            'Data Engineer': 'Data Engineer'
        },
        'state_street': {
            'Database Engineer': 'Senior Database Engineer',
            'Cloud Engineer': 'Senior Cloud Engineer',
            'Data Analyst': 'Senior Data Analyst',
            'ML Engineer': 'Senior ML Engineer',
            'Backend Engineer': 'Senior Backend Engineer',
            'Data Engineer': 'Senior Data Engineer'
        },
        'tech_mahindra': {
            'Database Engineer': 'Database Engineer',
            'Cloud Engineer': 'Cloud Engineer',
            'Data Analyst': 'Data Analyst',
            'ML Engineer': 'ML Engineer',
            'Backend Engineer': 'Backend Engineer',
            'Data Engineer': 'Data Engineer'
        }
    }
    
    # If base_role not in mapping, create appropriate title
    if base_role not in role_mapping['optum']:
        if company == 'state_street':
            return f'Senior {base_role}'
        else:
            return base_role
    
    return role_mapping.get(company, {}).get(base_role, f"{'Senior ' if company == 'state_street' else ''}{base_role}")