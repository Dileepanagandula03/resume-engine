# templates/experience_template.py

from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from utils.docx_utils import add_horizontal_line
from models.constants import COMPANY_LOCATIONS, COMPANY_DATES

def add_experience_section(doc, bullets, optum_role, ss_role, tm_role):
    """Add experience section with all three companies"""
    
    # Header
    exp_heading = doc.add_paragraph()
    exp_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    exp_heading.paragraph_format.space_before = Pt(4)
    exp_heading.paragraph_format.space_after = Pt(0)
    exp_run = exp_heading.add_run('Experience')
    exp_run.font.size = Pt(11)
    exp_run.bold = True
    exp_run.font.color.rgb = RGBColor(0, 86, 193)
    
    # Line
    line_para = doc.add_paragraph()
    line_para.paragraph_format.space_before = Pt(0)
    line_para.paragraph_format.space_after = Pt(2)
    add_horizontal_line(line_para)
    
    # OPTUM
    _add_company_block(doc, 'optum', optum_role, bullets['optum'][:6])
    
    # Spacer
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(2)
    spacer.paragraph_format.space_after = Pt(0)
    
    # STATE STREET
    _add_company_block(doc, 'state_street', ss_role, bullets['state_street'][:6])
    
    # Spacer
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(2)
    spacer.paragraph_format.space_after = Pt(0)
    
    # TECH MAHINDRA
    _add_company_block(doc, 'tech_mahindra', tm_role, bullets['tech_mahindra'][:6])

def _add_company_block(doc, company, role_name, company_bullets):
    """Add a single company block with title and bullets"""
    
    # Company title row
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    row = table.rows[0]
    left_cell = row.cells[0]
    right_cell = row.cells[1]
    
    # Left cell - Company and role
    left_para = left_cell.paragraphs[0]
    left_para.paragraph_format.space_before = Pt(0)
    left_para.paragraph_format.space_after = Pt(0)
    
    company_display = {
        'optum': 'Optum',
        'state_street': 'State Street Corporation',
        'tech_mahindra': 'Tech Mahindra'
    }.get(company, company)
    
    comp_run = left_para.add_run(f'{role_name}, {company_display}')
    comp_run.bold = True
    comp_run.font.size = Pt(10)
    
    location = COMPANY_LOCATIONS.get(company, '')
    if location:
        left_para.add_run(f' | {location}').font.size = Pt(10)
    
    # Right cell - Date
    right_para = right_cell.paragraphs[0]
    right_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    right_para.paragraph_format.space_before = Pt(0)
    right_para.paragraph_format.space_after = Pt(0)
    date_run = right_para.add_run(COMPANY_DATES.get(company, ''))
    date_run.font.size = Pt(10)
    date_run.bold = True
    
    # Remove table borders
    for row in table.rows:
        for cell in row.cells:
            tc = cell._element
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for border_name in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'none')
                tcBorders.append(border)
            tcPr.append(tcBorders)
    
    # Add bullets
    for bullet in company_bullets:
        p = doc.add_paragraph(bullet, style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.left_indent = Inches(0.25)
        for run in p.runs:
            run.font.size = Pt(10)