# main.py

import sys
import user_session
from services.resume_parser import parse_resume, validate_parsed_data
from utils.resume_reader import read_resume_file
from controllers.resume_controller import run_resume_generator
from utils.color_utils import Colors


def _read_multiline(prompt):
    """Read multi-line input until EOF (Ctrl+Z on Windows, Ctrl+D on Mac/Linux)."""
    print(prompt)
    lines = []
    try:
        while True:
            lines.append(input())
    except EOFError:
        pass
    return "\n".join(lines).strip()


def main():
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}      AI RESUME TAILORING ENGINE{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    # ── Step 1: Load resume from file ────────────────────────
    print(f"{Colors.YELLOW}STEP 1 of 3 — Provide your resume file.{Colors.END}")
    print(f"{Colors.YELLOW}Drag & drop your file here (PDF, DOCX, or TXT) and press Enter:{Colors.END} ", end="")

    file_path = input().strip()

    if not file_path:
        print(f"{Colors.RED}❌ No file provided.{Colors.END}")
        sys.exit(1)

    try:
        resume_text = read_resume_file(file_path)
    except FileNotFoundError as e:
        print(f"{Colors.RED}❌ {e}{Colors.END}")
        sys.exit(1)
    except ValueError as e:
        print(f"{Colors.RED}❌ {e}{Colors.END}")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Resume file loaded ({len(resume_text.split())} words){Colors.END}")

    # AI parses resume into structured profile
    try:
        parsed = parse_resume(resume_text)
    except Exception:
        print(f"{Colors.RED}❌ Could not parse resume. Try saving it as a DOCX or TXT file.{Colors.END}")
        sys.exit(1)

    warnings = validate_parsed_data(parsed)
    for w in warnings:
        print(f"{Colors.YELLOW}⚠️  {w}{Colors.END}")

    print(f"\n{Colors.GREEN}✅ Resume loaded for: {parsed.get('name', 'Unknown')}{Colors.END}")
    if parsed.get("experience"):
        companies = [e["company"] for e in parsed["experience"]]
        print(f"{Colors.BLUE}   Companies: {', '.join(companies)}{Colors.END}")

    user_session.load_from_dict(parsed)

    # ── Step 2: Paste JD ────────────────────────────────────
    print(f"\n{Colors.YELLOW}STEP 2 of 3 — Paste the job description.{Colors.END}")
    print(f"{Colors.YELLOW}Press Ctrl+Z then Enter when done (Ctrl+D on Mac):{Colors.END}\n")

    jd_text = _read_multiline("")

    if not jd_text:
        print(f"{Colors.RED}❌ No job description provided.{Colors.END}")
        sys.exit(1)

    # ── Step 3: Job title ───────────────────────────────────
    print(f"\n{Colors.YELLOW}STEP 3 of 3 — Enter the job title (used as the file name): {Colors.END}", end="")
    job_title = input().strip()
    if not job_title:
        job_title = "Resume"

    # ── Generate ────────────────────────────────────────────
    run_resume_generator(jd_text, job_title)


if __name__ == "__main__":
    main()
