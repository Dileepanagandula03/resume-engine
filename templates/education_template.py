# templates/education_template.py

from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from utils.docx_utils import add_horizontal_line

def add_education_section(doc):
    """Add education section"""
    
    # Header
    edu_heading = doc.add_paragraph()
    edu_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    edu_heading.paragraph_format.space_before = Pt(4)
    edu_heading.paragraph_format.space_after = Pt(0)
    edu_run = edu_heading.add_run('Education')
    edu_run.font.size = Pt(11)
    edu_run.bold = True
    edu_run.font.color.rgb = RGBColor(0, 86, 193)
    
    # Line
    line_para = doc.add_paragraph()
    line_para.paragraph_format.space_before = Pt(0)
    line_para.paragraph_format.space_after = Pt(2)
    add_horizontal_line(line_para)
    
    # Education line 1 - University and Degree
    table = doc.add_table(rows=1, cols=2)
    row = table.rows[0]
    left_cell = row.cells[0]
    right_cell = row.cells[1]
    
    left_para = left_cell.paragraphs[0]
    left_para.paragraph_format.space_before = Pt(0)
    left_para.paragraph_format.space_after = Pt(0)
    left_para.add_run('Webster University, Master of Science in Information Systems').font.size = Pt(10)
    
    right_para = right_cell.paragraphs[0]
    right_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    right_para.paragraph_format.space_before = Pt(0)
    right_para.paragraph_format.space_after = Pt(0)
    right_para.add_run('Jan 2024 – Dec 2025').font.size = Pt(10)
    
    # Remove borders
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
    
    # Education line 2 - Location and GPA
    table = doc.add_table(rows=1, cols=2)
    row = table.rows[0]
    left_cell = row.cells[0]
    right_cell = row.cells[1]
    
    left_para = left_cell.paragraphs[0]
    left_para.paragraph_format.space_before = Pt(0)
    left_para.paragraph_format.space_after = Pt(0)
    left_para.add_run('St. Louis, MO').font.size = Pt(10)
    
    right_para = right_cell.paragraphs[0]
    right_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    right_para.paragraph_format.space_before = Pt(0)
    right_para.paragraph_format.space_after = Pt(0)
    right_para.add_run('3.8/4.0').font.size = Pt(10)
    
    # Remove borders
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