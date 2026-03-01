# main.py

import sys
from controllers.resume_controller import run_resume_generator
from utils.color_utils import Colors

def main():
    """Main entry point"""
    
    print(f"{Colors.YELLOW}Paste job description below.{Colors.END}")
    print(f"{Colors.YELLOW}Press Ctrl+Z then Enter when done (Ctrl+D on Mac):{Colors.END}\n")
    
    # Read JD from user input
    jd_lines = []
    try:
        while True:
            line = input()
            jd_lines.append(line)
    except EOFError:
        pass
    
    jd_text = '\n'.join(jd_lines)
    
    if not jd_text.strip():
        print(f"{Colors.RED}❌ No JD provided.{Colors.END}")
        return
    
    job_title = input(f"\n{Colors.YELLOW}Enter job title: {Colors.END}").strip()
    if not job_title:
        job_title = "Resume"
    
    # Run the generator
    run_resume_generator(jd_text, job_title)

if __name__ == "__main__":
    main()