# templates/projects_template.py

from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from utils.docx_utils import add_horizontal_line, add_hyperlink

def add_projects_section(doc):
    """Add projects section with 4 projects"""
    
    # Header
    proj_heading = doc.add_paragraph()
    proj_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    proj_heading.paragraph_format.space_before = Pt(4)
    proj_heading.paragraph_format.space_after = Pt(0)
    proj_run = proj_heading.add_run('Projects')
    proj_run.font.size = Pt(11)
    proj_run.bold = True
    proj_run.font.color.rgb = RGBColor(0, 86, 193)
    
    # Line
    line_para = doc.add_paragraph()
    line_para.paragraph_format.space_before = Pt(0)
    line_para.paragraph_format.space_after = Pt(2)
    add_horizontal_line(line_para)
    
    # Project 1
    _add_project(
        doc, 
        'Azure Medallion Data Pipeline',
        'https://github.com/Dileepanagandula03/azure-medallion-data-pipeline',
        'Built a Medallion architecture leveraging ADF, ADLS, and Databricks to orchestrate ETL workflows, apply data quality checks, and deliver curated datasets consumed by Power BI dashboards.'
    )
    
    # Project 2
    _add_project(
        doc,
        'AI-Powered Resume Tailoring Tool | Recently developed',
        'https://github.com/Dileepanagandula03/azure-medallion-data-pipeline',
        'Built an AI-powered resume tailoring tool using OpenAI\'s LLM APIs and Python that automates resume customization in under 2 minutes, improves ATS match scores by 25-40%, and delivers 75% cost savings compared to commercial solutions.'
    )
    
    # Project 3
    _add_project(
        doc,
        'Real-Time and Batch Weather Data Pipeline',
        'https://github.com/Dileepanagandula03/weather-pipeline-project',
        'Built an end-to-end real-time and batch weather data pipeline on Azure, leveraging serverless ingestion and streaming analytics to process API-based event data, apply transformations and validations, and deliver analytics-ready datasets with cost-optimized architecture.'
    )
    
    # Project 4
    _add_project(
        doc,
        'ETL vs ELT Decision Framework Capstone Project',
        'https://github.com/Dileepanagandula03/Capstone-Data-Engineering-Pipelines',
        'Developed a comparative ETL vs ELT decision framework by evaluating performance, scalability, cost efficiency, and governance tradeoffs in cloud-based data pipelines, providing actionable guidance for selecting architectures.',
        link_text='View Paper'
    )

def _add_project(doc, title, url, description, link_text='View Project'):
    """Add a single project with title, link, and description"""
    
    # Title line with hyperlink
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    
    # Clean title (remove any existing link text)
    clean_title = title.replace(' | Recently developed', '').strip()
    
    title_run = p.add_run(clean_title)
    title_run.bold = True
    title_run.font.size = Pt(10)
    p.add_run(' ').font.size = Pt(10)
    add_hyperlink(p, link_text, url)
    
    # Description
    desc = doc.add_paragraph(description)
    desc.paragraph_format.space_before = Pt(0)
    desc.paragraph_format.space_after = Pt(4)  # Space between projects
    desc.paragraph_format.left_indent = Inches(0.25)
    for run in desc.runs:
        run.font.size = Pt(9)