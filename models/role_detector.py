# models/role_detector.py

import re


def detect_role(jd_text):
    """Detect the primary role from job description.

    Priority order:
    1. ERP / platform-specific roles (most specific — must come first)
    2. ML / Data / Cloud specialist roles
    3. Full-stack (before frontend/backend to avoid false splits)
    4. Frontend / Backend (only when clearly the PRIMARY focus, not just listed as a sub-skill)
    5. DevOps / SRE
    6. Generic software engineer/developer
    7. Title extraction fallback
    """
    jd_lower = jd_text.lower()

    # ── 1. ERP / Platform-specific ────────────────────────────────────────────
    if re.search(r'netsuite|suitescript|suiteflow|suitecloud|suitecommerce', jd_lower):
        return 'NetSuite Developer'
    if re.search(r'\bsalesforce\b|apex developer|visualforce|\bsoql\b|\bsosl\b', jd_lower):
        return 'Salesforce Developer'
    if re.search(r'\bsap\b|s/4hana|sap hana|sap abap|sap fiori', jd_lower):
        return 'SAP Developer'
    if re.search(r'servicenow|snow developer|snow platform', jd_lower):
        return 'ServiceNow Developer'
    if re.search(r'\bdynamics 365\b|\bpower platform\b|power apps|power automate', jd_lower):
        return 'Microsoft Dynamics Developer'

    # ── 2. Specialist roles ────────────────────────────────────────────────────
    if re.search(r'machine learning engineer|ml engineer|ai/ml engineer', jd_lower):
        return 'ML Engineer'
    if re.search(r'data engineer|data engineering|data infrastructure engineer', jd_lower):
        return 'Data Engineer'
    if re.search(r'database engineer|\bdba\b|sql developer|database developer', jd_lower):
        return 'Database Engineer'
    if re.search(r'cloud engineer|aws engineer|azure engineer|cloud architect|gcp engineer', jd_lower):
        return 'Cloud Engineer'
    if re.search(r'data analyst|business analyst|\bbi engineer\b', jd_lower):
        return 'Data Analyst'
    if re.search(r'security engineer|cybersecurity|penetration tester|infosec', jd_lower):
        return 'Security Engineer'
    if re.search(r'mobile developer|ios developer|android developer|react native|flutter developer', jd_lower):
        return 'Mobile Developer'

    # ── 3. Full-stack (before frontend/backend) ────────────────────────────────
    if re.search(r'full.?stack|fullstack', jd_lower):
        return 'Full Stack Developer'

    # ── 4. Frontend / Backend — only when clearly the PRIMARY role ─────────────
    # Check the first 10 lines (title area) first for a definitive match.
    first_lines = '\n'.join(jd_text.splitlines()[:10]).lower()

    if re.search(r'frontend developer|front.end developer|frontend engineer|front.end engineer', first_lines):
        return 'Frontend Developer'
    if re.search(r'backend developer|back.end developer|backend engineer|back.end engineer', first_lines):
        return 'Backend Developer'

    # Body-level check — only fire if NOT countered by "full-stack" or opposite side
    has_frontend_body = bool(re.search(r'frontend engineer|front.end engineer|frontend developer', jd_lower))
    has_backend_body = bool(re.search(r'backend engineer|back.end engineer|backend developer', jd_lower))
    mentions_both = has_frontend_body and has_backend_body

    if has_frontend_body and not mentions_both and not re.search(r'full.?stack', jd_lower):
        return 'Frontend Developer'
    if has_backend_body and not mentions_both and not re.search(r'full.?stack', jd_lower):
        return 'Backend Developer'

    # ── 5. DevOps / SRE ────────────────────────────────────────────────────────
    if re.search(r'devops engineer|site reliability|sre |platform engineer', jd_lower):
        return 'DevOps Engineer'

    # ── 6. Generic software roles ──────────────────────────────────────────────
    if re.search(r'software engineer|software developer|application developer', jd_lower):
        return 'Software Developer'

    # ── 7. Fallback: extract from "seeking a <Title>" pattern ──────────────────
    title_match = re.search(
        r'seeking\s+(?:a\s+|an\s+)?([A-Z][a-zA-Z\s/]+?)(?:\s+to\b|\s+who\b|\s+with\b|\s+responsible)',
        jd_text,
    )
    if title_match:
        return title_match.group(1).strip()

    return 'Software Developer'
