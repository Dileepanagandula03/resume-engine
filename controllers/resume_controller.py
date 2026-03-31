# controllers/resume_controller.py

from services.summary_service import generate_matched_summary
from services.skills_service import generate_matched_skills
from services.bullet_service import generate_matching_bullets
from services.ats_service import calculate_ats_score
from models.role_detector import detect_role
from templates.header_template import add_header
from templates.summary_template import add_summary_section
from templates.skills_template import add_skills_section
from templates.experience_template import add_experience_section
from templates.projects_template import add_projects_section
from templates.education_template import add_education_section
from utils.file_utils import save_document
from utils.color_utils import Colors
import user_session
from docx import Document
from docx.shared import Inches, Pt


def run_resume_generator(jd_text, job_title, auto_open=True, keep_docx=False):
    """Main orchestration function. Requires user_session to be populated first.

    Returns dict: {filename, ats: {score, matched, missing}}
    """

    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}   JD MATCHING RESUME GENERATOR{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    role = detect_role(jd_text)
    print(f"{Colors.BLUE}📋 Detected Role: {role}{Colors.END}")

    matched_summary = generate_matched_summary(jd_text)
    print(f"{Colors.GREEN}✅ Summary generated{Colors.END}")

    bullets = generate_matching_bullets(jd_text)
    matched_skills = generate_matched_skills(jd_text)

    doc = _build_document(bullets, matched_summary, matched_skills, role)

    filename = save_document(
        doc, job_title, user_name=user_session.YOUR_NAME,
        auto_open=auto_open, keep_docx=keep_docx
    )
    print(f"\n{Colors.GREEN}✅ Resume saved: {filename}{Colors.END}")

    resume_text = "\n".join(p.text for p in doc.paragraphs)
    ats = calculate_ats_score(resume_text, jd_text)

    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}🎉 Done! Resume opened automatically.{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    return {"filename": filename, "ats": ats}


def _build_document(bullets, matched_summary, matched_skills, role):
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.3)
        section.bottom_margin = Inches(0.3)
        section.left_margin = Inches(0.4)
        section.right_margin = Inches(0.4)

    doc.styles["Normal"].paragraph_format.space_before = Pt(0)
    doc.styles["Normal"].paragraph_format.space_after = Pt(0)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.0

    add_header(
        doc,
        user_session.YOUR_NAME,
        user_session.YOUR_PHONE,
        user_session.YOUR_EMAIL,
        user_session.YOUR_LOCATION,
        user_session.YOUR_LINKEDIN,
        user_session.YOUR_GITHUB,
        user_session.YOUR_PORTFOLIO,
    )
    add_summary_section(doc, matched_summary)
    add_skills_section(doc, matched_skills)
    add_experience_section(doc, bullets, role)
    add_projects_section(doc)
    add_education_section(doc)

    return doc
