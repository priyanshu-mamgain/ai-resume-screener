import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uuid
from flask import Flask, request, jsonify, render_template, session
import pdfplumber
from matcher import calculate_match_score, get_missing_keywords
from database import save_result, get_all_results

app = Flask(__name__)

# Secret key is required for Flask sessions to work securely.
# In production (Render), set SECRET_KEY as an environment variable.
app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-key-change-this")

@app.before_request
def assign_user_id():
    """Give every visitor a unique, anonymous ID stored in their browser session,
    so each person only ever sees their own screening history."""
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

def extract_text_from_pdf(file):
    """Extract text from an uploaded PDF file object"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/screen', methods=['POST'])
def screen_resume():
    job_description = ""
    resume_text = ""

    if 'resume_file' in request.files:
        file = request.files['resume_file']
        job_description = request.form.get('job_description', '')

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400

        try:
            resume_text = extract_text_from_pdf(file)
        except Exception as e:
            return jsonify({"error": f"Could not read PDF: {str(e)}"}), 400

        if not resume_text:
            return jsonify({"error": "Could not extract any text from this PDF"}), 400

    else:
        data = request.get_json(silent=True) or {}
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')

    if not resume_text or not job_description:
        return jsonify({"error": "Both resume and job description are required"}), 400

    score = calculate_match_score(resume_text, job_description)
    missing = get_missing_keywords(resume_text, job_description)

    save_result(resume_text, job_description, score, session["user_id"])

    return jsonify({
        "score": score,
        "missing_keywords": missing
    })

@app.route('/history')
def history():
    results = get_all_results(session["user_id"])
    return render_template('history.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)