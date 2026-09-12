# AI Resume Screener

A full-stack web app that scores how well a resume matches a job description, built with Flask, MongoDB, and vanilla JS — styled around a "case file" metaphor, with results delivered as a hand-stamped verdict.

**Live demo:** [ai-resume-screener-n2wf.onrender.com](https://ai-resume-screener-n2wf.onrender.com/)
*(hosted on Render's free tier — the first load may take 30-60 seconds if the server has gone to sleep)*

[Screening page](screenshots\screen-main.png)
[Result stamp](screenshots/screen-result.png)
[History page](screenshots/screen-history.png)

## What it does

- Upload a resume (PDF) or paste its text, along with a job description
- Get a match score (0-100%) based on how closely the two align
- See which important terms from the job description are missing from the resume
- Every screening is saved, viewable later in a "filing cabinet" history page

## Tech stack

| Layer          | Technology |
|----------------|------------|
| Backend        | Flask (Python), REST API |
| Matching logic | scikit-learn (TF-IDF + cosine similarity) |
| Database       | MongoDB Atlas  |
| PDF parsing    | pdfplumber |
| Frontend       | HTML, CSS, vanilla JavaScript |
| Deployment     | Render (gunicorn) |

## Why TF-IDF, not embeddings?

I initially built this with `sentence-transformers` for semantic similarity, since it understands meaning rather than just exact word overlap. I ended up reverting to TF-IDF + cosine similarity after running into Windows environment constraints (PyTorch's compiled dependencies didn't play well with my setup). TF-IDF is lighter, has zero native-dependency headaches, and is easier to deploy reliably — a reasonable tradeoff for a project at this scale. Text is cleaned first (removing emails, links, dates, and resume "noise" words like section headers) before scoring, which noticeably improves match quality.

## Running it locally

1. Clone the repo:
   ```
   git clone https://github.com/priyanshu-mamgain/ai-resume-screener.git
   cd ai-resume-screener
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   MONGO_URI=your_mongodb_connection_string_here
   ```

4. Run the app:
   ```
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Project structure

```
├── app.py # Flask routes and API
├── matcher.py # TF-IDF matching logic
├── database.py # MongoDB connection and queries
├── templates/
│ ├── index.html # Main screening page
│ └── history.html # Past screenings
├── static/
│ ├── style.css
│ └── script.js
├── screenshots/ # Images used in this README
└── requirements.txt
```

## Possible improvements

- Swap TF-IDF for semantic embeddings (sentence-transformers) given a more flexible deployment environment
- Section-aware parsing (weight "Skills" and "Experience" sections higher than education/contact info)
- Support for `.docx` resumes, not just PDF