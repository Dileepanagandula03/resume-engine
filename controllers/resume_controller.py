# controllers/resume_controller.py

from services.summary_service import generate_matched_summary
from services.skills_service import generate_matched_skills
from services.bullet_service import generate_matching_bullets
from services.ats_service import calculate_ats_score
from models.role_detector import detect_role, get_company_role_name
from templates.header_template import add_header
from templates.summary_template import add_summary_section
from templates.skills_template import add_skills_section
from templates.experience_template import add_experience_section
from templates.projects_template import add_projects_section
from templates.education_template import add_education_section
from utils.file_utils import save_document
from utils.color_utils import Colors
from my_info import (
    YOUR_NAME, YOUR_PHONE, YOUR_EMAIL, YOUR_LOCATION,
    YOUR_LINKEDIN, YOUR_GITHUB, YOUR_PORTFOLIO
)
from docx import Document
from docx.shared import Inches, Pt

def run_resume_generator(jd_text, job_title):
    """Main orchestration function"""
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}   JD MATCHING RESUME GENERATOR{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    # Detect role
    role = detect_role(jd_text)
    print(f"{Colors.BLUE}📋 Detected Role: {role}{Colors.END}")
    
    # Generate summary
    matched_summary = generate_matched_summary(jd_text)
    print(f"\n{Colors.GREEN}✅ Summary generated{Colors.END}")
    
    # Generate bullets
    bullets = generate_matching_bullets(jd_text)
    
    # Display generated bullets
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}GENERATED BULLETS:{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    for company, company_bullets in bullets.items():
        if company_bullets:
            company_display = {
                'optum': 'OPTUM',
                'state_street': 'STATE STREET',
                'tech_mahindra': 'TECH MAHINDRA'
            }.get(company, company.upper())
            print(f"\n{Colors.BLUE}{company_display}:{Colors.END}")
            for i, bullet in enumerate(company_bullets[:6], 1):
                print(f"{i}. {bullet}")
    
    # Generate document
    doc = generate_document(bullets, job_title, matched_summary, jd_text, role)
    
    # Save file
    filename = save_document(doc, job_title)
    
    # Calculate ATS score
    resume_text = '\n'.join([p.text for p in doc.paragraphs])
    ats_score = calculate_ats_score(resume_text, jd_text)
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}🎉 DONE! Check your output folder!{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    return filename

def generate_document(bullets, job_title, matched_summary, jd_text, role):
    """Generate the Word document"""
    
    doc = Document()
    
    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.3)
        section.bottom_margin = Inches(0.3)
        section.left_margin = Inches(0.4)
        section.right_margin = Inches(0.4)
    
    # Default paragraph spacing
    doc.styles['Normal'].paragraph_format.space_before = Pt(0)
    doc.styles['Normal'].paragraph_format.space_after = Pt(0)
    doc.styles['Normal'].paragraph_format.line_spacing = 1.0
    
    # Add header
    add_header(
        doc, YOUR_NAME, YOUR_PHONE, YOUR_EMAIL, YOUR_LOCATION,
        YOUR_LINKEDIN, YOUR_GITHUB, YOUR_PORTFOLIO
    )
    
    # Add summary
    add_summary_section(doc, matched_summary)
    
    # Generate and add skills
    matched_skills = generate_matched_skills(jd_text)
    add_skills_section(doc, matched_skills)
    
    # Get role names for each company
    optum_role = get_company_role_name('optum', role)
    ss_role = get_company_role_name('state_street', role)
    tm_role = get_company_role_name('tech_mahindra', role)
    
    # Add experience
    add_experience_section(doc, bullets, optum_role, ss_role, tm_role)
    
    # Add projects
    add_projects_section(doc)
    
    # Add education
    add_education_section(doc)
    
    return doc