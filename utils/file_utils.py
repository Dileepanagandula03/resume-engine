# utils/file_utils.py

import os
from datetime import datetime
from docx2pdf import convert

def save_document(doc, job_title):
    """Save docx and convert to PDF"""
    if not os.path.exists('output'):
        os.makedirs('output')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    job_title_clean = job_title.replace(' ', '_').replace('/', '_')
    
    word_filename = f"output/{job_title_clean}_{timestamp}.docx"
    doc.save(word_filename)
    
    pdf_filename = f"output/{job_title_clean}_{timestamp}.pdf"
    try:
        convert(word_filename, pdf_filename)
        os.remove(word_filename)
        return pdf_filename
    except Exception as e:
        return word_filename