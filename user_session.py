# user_session.py
#
# Runtime user profile. Populated either from my_info.py (if user has configured it)
# or from a parsed resume (if user pastes their resume at runtime).
# All services and templates import from HERE — not directly from my_info.

YOUR_NAME = ""
YOUR_PHONE = ""
YOUR_EMAIL = ""
YOUR_LOCATION = ""
YOUR_LINKEDIN = ""
YOUR_GITHUB = ""
YOUR_PORTFOLIO = ""

YEARS_OF_EXPERIENCE = 0
PROFESSIONAL_SUMMARY = ""

YOUR_EXPERIENCE = []   # list of dicts: key, company, role, location, start_date, end_date, context
CORE_SKILLS = []       # list of "Category: skill1, skill2" strings
YOUR_EDUCATION = []    # list of dicts: school, degree, location, start_date, end_date, gpa
YOUR_PROJECTS = []     # list of dicts: title, url, description, link_text


def load_from_my_info():
    """Populate session from the static my_info.py configuration."""
    import my_info
    _set(
        name=my_info.YOUR_NAME,
        phone=my_info.YOUR_PHONE,
        email=my_info.YOUR_EMAIL,
        location=my_info.YOUR_LOCATION,
        linkedin=my_info.YOUR_LINKEDIN,
        github=my_info.YOUR_GITHUB,
        portfolio=my_info.YOUR_PORTFOLIO,
        years=my_info.YEARS_OF_EXPERIENCE,
        summary=my_info.PROFESSIONAL_SUMMARY,
        experience=my_info.YOUR_EXPERIENCE,
        skills=my_info.CORE_SKILLS,
        education=my_info.YOUR_EDUCATION,
        projects=my_info.YOUR_PROJECTS,
    )


def load_from_dict(data: dict):
    """Populate session from a parsed resume dict (output of resume_parser)."""
    _set(
        name=data.get("name", ""),
        phone=data.get("phone", ""),
        email=data.get("email", ""),
        location=data.get("location", ""),
        linkedin=data.get("linkedin", ""),
        github=data.get("github", ""),
        portfolio=data.get("portfolio", ""),
        years=data.get("years_of_experience", 0),
        summary=data.get("summary", ""),
        experience=data.get("experience", []),
        skills=data.get("skills", []),
        education=data.get("education", []),
        projects=data.get("projects", []),
    )


def _set(name, phone, email, location, linkedin, github, portfolio,
         years, summary, experience, skills, education, projects):
    global YOUR_NAME, YOUR_PHONE, YOUR_EMAIL, YOUR_LOCATION
    global YOUR_LINKEDIN, YOUR_GITHUB, YOUR_PORTFOLIO
    global YEARS_OF_EXPERIENCE, PROFESSIONAL_SUMMARY
    global YOUR_EXPERIENCE, CORE_SKILLS, YOUR_EDUCATION, YOUR_PROJECTS

    YOUR_NAME = name
    YOUR_PHONE = phone
    YOUR_EMAIL = email
    YOUR_LOCATION = location
    YOUR_LINKEDIN = linkedin
    YOUR_GITHUB = github
    YOUR_PORTFOLIO = portfolio
    YEARS_OF_EXPERIENCE = years
    PROFESSIONAL_SUMMARY = summary
    YOUR_EXPERIENCE = experience
    CORE_SKILLS = skills
    YOUR_EDUCATION = education
    YOUR_PROJECTS = projects
