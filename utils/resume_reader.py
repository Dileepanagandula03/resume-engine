# utils/resume_reader.py
#
# Reads a resume file (PDF, DOCX, or TXT) and returns the plain text content.

import os


def read_resume_file(file_path: str) -> str:
    """Extract plain text from a PDF, DOCX, or TXT resume file."""
    path = file_path.strip().strip('"').strip("'")  # handle drag-and-drop quotes

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return _read_pdf(path)
    elif ext in (".docx", ".doc"):
        return _read_docx(path)
    elif ext == ".txt":
        return _read_txt(path)
    else:
        raise ValueError(f"Unsupported file type '{ext}'. Use PDF, DOCX, or TXT.")


def _read_pdf(path: str) -> str:
    import pdfplumber
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    result = "\n".join(text_parts).strip()
    if not result:
        raise ValueError("Could not extract text from PDF. Try saving it as DOCX or TXT.")
    return result


def _read_docx(path: str) -> str:
    from docx import Document
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    result = "\n".join(paragraphs).strip()
    if not result:
        raise ValueError("DOCX file appears to be empty.")
    return result


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()
