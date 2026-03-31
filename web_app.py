# web_app.py

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import uuid
import tempfile
import threading
from flask import Flask, render_template, request, send_file, jsonify

import user_session
from services.resume_parser import parse_resume, validate_parsed_data
from utils.resume_reader import read_resume_file
from controllers.resume_controller import run_resume_generator

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB max upload

# One job at a time (personal tool — no queue needed)
_lock = threading.Lock()

# Token → absolute file path (in-memory; cleared on restart)
_generated_files: dict[str, str] = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not _lock.acquire(blocking=False):
        return jsonify({"error": "Another resume is being generated. Please wait a moment."}), 429

    tmp_path = None
    try:
        # ── Validate inputs ──────────────────────────────────
        if "resume" not in request.files or request.files["resume"].filename == "":
            return jsonify({"error": "No resume file provided."}), 400

        jd_text = request.form.get("jd", "").strip()
        if not jd_text:
            return jsonify({"error": "No job description provided."}), 400

        job_title = request.form.get("job_title", "Resume").strip() or "Resume"

        # ── Save uploaded file to temp location ──────────────
        resume_file = request.files["resume"]
        ext = os.path.splitext(resume_file.filename)[1].lower()
        if ext not in (".pdf", ".docx", ".doc", ".txt"):
            return jsonify({"error": f"Unsupported file type '{ext}'. Use PDF, DOCX, or TXT."}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            resume_file.save(tmp.name)
            tmp_path = tmp.name

        # ── Parse resume ─────────────────────────────────────
        resume_text = read_resume_file(tmp_path)
        parsed = parse_resume(resume_text)

        # Override parsed URLs with manually entered ones (PDFs lose hyperlinks)
        linkedin_url  = request.form.get("linkedin_url",  "").strip()
        github_url    = request.form.get("github_url",    "").strip()
        portfolio_url = request.form.get("portfolio_url", "").strip()
        if linkedin_url:
            parsed["linkedin"]  = linkedin_url
        if github_url:
            parsed["github"]    = github_url
        if portfolio_url:
            parsed["portfolio"] = portfolio_url

        user_session.load_from_dict(parsed)
        validate_parsed_data(parsed)

        # ── Generate tailored resume (DOCX for web — user can edit) ──
        result = run_resume_generator(jd_text, job_title, auto_open=False, keep_docx=True)

        abs_path = os.path.abspath(result["filename"])
        token = str(uuid.uuid4())
        _generated_files[token] = abs_path

        ats = result["ats"]
        return jsonify({
            "ats_score":      ats["score"],
            "matched":        ats["matched"],
            "missing":        ats["missing"],
            "download_token": token,
            "filename":       os.path.basename(abs_path),
        })

    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        _lock.release()


@app.route("/download/<token>")
def download(token):
    path = _generated_files.get(token)
    if not path or not os.path.exists(path):
        return jsonify({"error": "File not found or expired. Please regenerate."}), 404
    return send_file(path, as_attachment=True, download_name=os.path.basename(path))


if __name__ == "__main__":
    print("\nResume Engine running at http://localhost:5000\n")
    app.run(debug=False, port=5000)
