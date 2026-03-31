# utils/file_utils.py

import os
import subprocess
import sys
from datetime import datetime


def save_document(doc, job_title, user_name="", auto_open=True, keep_docx=False):
    """Save as docx, optionally convert to PDF, and open the result.

    Files are saved to:  output/<FirstName_LastName>/<JobTitle>_<timestamp>.(docx|pdf)

    keep_docx=True  → skip PDF conversion; return the .docx path (web mode).
    keep_docx=False → convert to PDF, delete docx, return .pdf path (CLI mode).
    """
    # Build output directory
    if user_name:
        safe_name = user_name.strip().replace(" ", "_")
        out_dir = os.path.join("output", safe_name)
    else:
        out_dir = "output"

    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    job_title_clean = job_title.strip().replace(" ", "_").replace("/", "_")

    docx_path = os.path.join(out_dir, f"{job_title_clean}_{timestamp}.docx")
    pdf_path = os.path.join(out_dir, f"{job_title_clean}_{timestamp}.pdf")

    doc.save(docx_path)

    if keep_docx:
        final_path = docx_path
    else:
        final_path = docx_path
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            os.remove(docx_path)
            final_path = pdf_path
        except Exception:
            pass  # Keep the .docx if PDF conversion is unavailable

    if auto_open:
        _open_file(final_path)
    return final_path


def _open_file(path):
    """Open the generated resume in the default viewer."""
    try:
        if sys.platform == "win32":
            os.startfile(os.path.abspath(path))
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception:
        pass  # Opening is best-effort; don't crash if it fails
